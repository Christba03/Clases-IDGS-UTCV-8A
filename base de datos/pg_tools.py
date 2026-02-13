#!/usr/bin/env python3
"""PostgreSQL backup/restore/export/import helper"""

import argparse
import os
import sys
import logging
import subprocess
import pathlib
import shutil
import urllib.parse

import psycopg2


# ---------- Helpers ----------

def build_conn_uri(args, database=None):
    user = args.user or os.getenv("PGUSER", "postgres")
    password = args.password or os.getenv("PGPASSWORD")
    host = args.host or os.getenv("PGHOST", "localhost")
    port = str(args.port or os.getenv("PGPORT", "5432"))
    db = database or args.database or os.getenv("PGDATABASE", "postgres")

    if password:
        password = urllib.parse.quote_plus(password)
        auth = f"{user}:{password}"
    else:
        auth = user

    return f"postgresql://{auth}@{host}:{port}/{db}"


def base_env(args):
    env = os.environ.copy()
    if args.password:
        env["PGPASSWORD"] = args.password
    return env


def ensure_binary(path_hint, fallback):
    if path_hint and shutil.which(path_hint):
        return path_hint
    located = shutil.which(fallback)
    if not located:
        raise FileNotFoundError(f"Binary not found: {fallback}")
    return located


def is_custom_format_dump(file_path):
    """Check if a file is a PostgreSQL custom format dump by reading the header."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(5)
            return header == b'PGDMP'
    except (IOError, OSError):
        return False


def run_command(cmd, env):
    result = subprocess.run(cmd, env=env, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        error_msg = f"Command failed: {' '.join(cmd)}"
        if result.stderr:
            error_msg += f"\n{result.stderr.strip()}"
        raise RuntimeError(error_msg)


# ---------- Commands ----------

def backup_database(args):
    pg_dump = ensure_binary(args.pg_dump, "pg_dump")
    out = pathlib.Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        pg_dump,
        f"--format={args.format}",
        "--file", str(out),
        build_conn_uri(args),
    ]

    if args.schema_only:
        cmd.append("--schema-only")

    run_command(cmd, base_env(args))
    print(f"Backup created: {out}")


def ensure_database_exists(args, db):
    """Create the target database if it does not exist."""
    conn = psycopg2.connect(build_conn_uri(args, "postgres"))
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db,))
            if not cur.fetchone():
                cur.execute(f'CREATE DATABASE "{db}"')
                print(f"Created database: {db}")
    finally:
        conn.close()


def restore_backup(args):
    backup = pathlib.Path(args.backup).expanduser().resolve()
    if not backup.exists():
        raise FileNotFoundError(backup)

    db = args.target_database or args.database
    ensure_database_exists(args, db)
    env = base_env(args)

    # Check if it's a custom format dump by extension or file content
    is_custom = (backup.suffix in {".dump", ".backup", ".custom"} or 
                 is_custom_format_dump(backup))

    if is_custom:
        pg_restore = ensure_binary(args.pg_restore, "pg_restore")
        cmd = [
            pg_restore,
            "--dbname", build_conn_uri(args, db),
            str(backup),
        ]
        if args.clean:
            cmd.insert(1, "--clean")

        result = subprocess.run(cmd, env=env, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            warnings = result.stderr.strip()
            if warnings:
                print(f"pg_restore warnings:\n{warnings}")
    else:
        psql = ensure_binary(args.psql, "psql")
        cmd = [
            psql,
            "--dbname", build_conn_uri(args, db),
            "--file", str(backup),
        ]
        run_command(cmd, env)

    print(f"Restore completed into database: {db}")


def export_table(args):
    out = pathlib.Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    query = args.query or f"SELECT * FROM {args.table}"

    conn = psycopg2.connect(build_conn_uri(args))
    conn.autocommit = True
    try:
        with conn.cursor() as cur, out.open("w", encoding="utf-8", newline="") as f:
            cur.copy_expert(f"COPY ({query}) TO STDOUT WITH CSV HEADER", f)
    finally:
        conn.close()

    print(f"Exported to {out}")


def import_table(args):
    inp = pathlib.Path(args.input).expanduser().resolve()
    if not inp.exists():
        raise FileNotFoundError(inp)

    conn = psycopg2.connect(build_conn_uri(args))
    conn.autocommit = True
    try:
        with conn.cursor() as cur, inp.open("r", encoding="utf-8") as f:
            if args.truncate:
                cur.execute(f"TRUNCATE TABLE {args.table}")
            cur.copy_expert(
                f"COPY {args.table} FROM STDIN WITH CSV HEADER",
                f,
            )
    finally:
        conn.close()

    print(f"Imported data into {args.table}")


def init_database(args):
    sql = pathlib.Path(args.sql).expanduser().resolve()
    if not sql.exists():
        raise FileNotFoundError(sql)

    psql = ensure_binary(args.psql, "psql")
    cmd = [
        psql,
        "--dbname", build_conn_uri(args, args.maintenance_db),
        "--file", str(sql),
    ]

    run_command(cmd, base_env(args))
    print(f"Database initialized using {sql}")


# ---------- CLI ----------

def parser_builder():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", default="5432")
    p.add_argument("--user", default="postgres")
    p.add_argument("--password", default="")
    p.add_argument("--database", default="postgres")
    p.add_argument("--maintenance-db", default="postgres")
    p.add_argument("--pg-dump", default="pg_dump")
    p.add_argument("--pg-restore", default="pg_restore")
    p.add_argument("--psql", default="psql")

    subs = p.add_subparsers(dest="command", required=True)

    b = subs.add_parser("backup")
    b.add_argument("--output", required=True)
    b.add_argument("--format", choices=["custom", "plain"], default="custom")
    b.add_argument("--schema-only", action="store_true")
    b.set_defaults(func=backup_database)

    r = subs.add_parser("restore")
    r.add_argument("--backup", required=True)
    r.add_argument("--target-database")
    r.add_argument("--clean", action="store_true")
    r.set_defaults(func=restore_backup)

    e = subs.add_parser("export")
    e.add_argument("--table", required=True)
    e.add_argument("--output", required=True)
    e.add_argument("--query")
    e.set_defaults(func=export_table)

    i = subs.add_parser("import")
    i.add_argument("--table", required=True)
    i.add_argument("--input", required=True)
    i.add_argument("--truncate", action="store_true")
    i.set_defaults(func=import_table)

    d = subs.add_parser("init")
    d.add_argument("--sql", required=True)
    d.set_defaults(func=init_database)

    return p


def main():
    parser = parser_builder()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
