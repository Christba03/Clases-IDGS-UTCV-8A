#!/usr/bin/env python3
"""Tkinter GUI for pg_tools.py"""

import threading
import io
import sys
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from types import SimpleNamespace

import pg_tools

BASE_DIR = "/home/christba/Documents/Git/Clases-IDGS-UTCV-8A/base de datos/Backup-test"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PostgreSQL Tools")
        self.minsize(620, 520)
        self._build_connection_frame()
        self._build_notebook()
        self._build_log()

    # ---- connection fields ----

    def _build_connection_frame(self):
        fr = ttk.LabelFrame(self, text="Connection", padding=6)
        fr.pack(fill="x", padx=8, pady=(8, 0))

        labels = ("Host", "Port", "User", "Password", "Database")
        defaults = ("localhost", "5432", "postgres", "postgres", "tienda")
        self.conn = {}
        for col, (label, default) in enumerate(zip(labels, defaults)):
            ttk.Label(fr, text=label).grid(row=0, column=col, sticky="w", padx=2)
            var = tk.StringVar(value=default)
            show = "*" if label == "Password" else ""
            entry = ttk.Entry(fr, textvariable=var, width=14, show=show)
            entry.grid(row=1, column=col, sticky="ew", padx=2)
            fr.columnconfigure(col, weight=1)
            self.conn[label.lower()] = var

    # ---- tabs ----

    def _build_notebook(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        nb.add(self._tab_backup(), text="Backup")
        nb.add(self._tab_restore(), text="Restore")
        nb.add(self._tab_export(), text="Export")
        nb.add(self._tab_import(), text="Import")
        nb.add(self._tab_init(), text="Init")

    def _tab_backup(self):
        fr = ttk.Frame(padding=8)

        ttk.Label(fr, text="Output file:").grid(row=0, column=0, sticky="w")
        self.bk_output = tk.StringVar(value=f"{BASE_DIR}/tienda_backup.dump")
        ttk.Entry(fr, textvariable=self.bk_output, width=40).grid(row=0, column=1, sticky="ew")
        ttk.Button(fr, text="Browse…", command=lambda: self._save_file(self.bk_output)).grid(row=0, column=2)

        ttk.Label(fr, text="Format:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.bk_format = tk.StringVar(value="custom")
        ttk.Combobox(fr, textvariable=self.bk_format, values=["custom", "plain"], state="readonly", width=12).grid(row=1, column=1, sticky="w", pady=(6, 0))

        self.bk_schema = tk.BooleanVar()
        ttk.Checkbutton(fr, text="Schema only", variable=self.bk_schema).grid(row=2, column=1, sticky="w", pady=(4, 0))

        ttk.Button(fr, text="Run Backup", command=self._run_backup).grid(row=3, column=0, columnspan=3, pady=(10, 0))
        fr.columnconfigure(1, weight=1)
        return fr

    def _tab_restore(self):
        fr = ttk.Frame(padding=8)

        ttk.Label(fr, text="Backup file:").grid(row=0, column=0, sticky="w")
        self.rs_backup = tk.StringVar(value=f"{BASE_DIR}/tienda_backup.dump")
        ttk.Entry(fr, textvariable=self.rs_backup, width=40).grid(row=0, column=1, sticky="ew")
        ttk.Button(fr, text="Browse…", command=lambda: self._open_file(self.rs_backup)).grid(row=0, column=2)

        ttk.Label(fr, text="Target DB:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.rs_target = tk.StringVar(value="tienda_copia")
        ttk.Entry(fr, textvariable=self.rs_target, width=20).grid(row=1, column=1, sticky="w", pady=(6, 0))

        self.rs_clean = tk.BooleanVar(value=True)
        ttk.Checkbutton(fr, text="Clean (drop objects before restore)", variable=self.rs_clean).grid(row=2, column=1, sticky="w", pady=(4, 0))

        ttk.Button(fr, text="Run Restore", command=self._run_restore).grid(row=3, column=0, columnspan=3, pady=(10, 0))
        fr.columnconfigure(1, weight=1)
        return fr

    def _tab_export(self):
        fr = ttk.Frame(padding=8)

        ttk.Label(fr, text="Table:").grid(row=0, column=0, sticky="w")
        self.ex_table = tk.StringVar(value="clientes")
        ttk.Entry(fr, textvariable=self.ex_table, width=30).grid(row=0, column=1, sticky="w")

        ttk.Label(fr, text="Output CSV:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.ex_output = tk.StringVar(value=f"{BASE_DIR}/clientes.csv")
        ttk.Entry(fr, textvariable=self.ex_output, width=40).grid(row=1, column=1, sticky="ew", pady=(6, 0))
        ttk.Button(fr, text="Browse…", command=lambda: self._save_file(self.ex_output)).grid(row=1, column=2, pady=(6, 0))

        ttk.Label(fr, text="Custom query:").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.ex_query = tk.StringVar()
        ttk.Entry(fr, textvariable=self.ex_query, width=40).grid(row=2, column=1, sticky="ew", pady=(6, 0))

        ttk.Button(fr, text="Run Export", command=self._run_export).grid(row=3, column=0, columnspan=3, pady=(10, 0))
        fr.columnconfigure(1, weight=1)
        return fr

    def _tab_import(self):
        fr = ttk.Frame(padding=8)

        ttk.Label(fr, text="Table:").grid(row=0, column=0, sticky="w")
        self.im_table = tk.StringVar(value="clientes")
        ttk.Entry(fr, textvariable=self.im_table, width=30).grid(row=0, column=1, sticky="w")

        ttk.Label(fr, text="Input CSV:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.im_input = tk.StringVar(value=f"{BASE_DIR}/clientes.csv")
        ttk.Entry(fr, textvariable=self.im_input, width=40).grid(row=1, column=1, sticky="ew", pady=(6, 0))
        ttk.Button(fr, text="Browse…", command=lambda: self._open_file(self.im_input)).grid(row=1, column=2, pady=(6, 0))

        self.im_truncate = tk.BooleanVar()
        ttk.Checkbutton(fr, text="Truncate table first", variable=self.im_truncate).grid(row=2, column=1, sticky="w", pady=(4, 0))

        ttk.Button(fr, text="Run Import", command=self._run_import).grid(row=3, column=0, columnspan=3, pady=(10, 0))
        fr.columnconfigure(1, weight=1)
        return fr

    def _tab_init(self):
        fr = ttk.Frame(padding=8)

        ttk.Label(fr, text="SQL file:").grid(row=0, column=0, sticky="w")
        self.in_sql = tk.StringVar(value=f"{BASE_DIR}/init.sql")
        ttk.Entry(fr, textvariable=self.in_sql, width=40).grid(row=0, column=1, sticky="ew")
        ttk.Button(fr, text="Browse…", command=lambda: self._open_file(self.in_sql, filetypes=[("SQL", "*.sql"), ("All", "*")])).grid(row=0, column=2)

        ttk.Button(fr, text="Run Init", command=self._run_init).grid(row=1, column=0, columnspan=3, pady=(10, 0))
        fr.columnconfigure(1, weight=1)
        return fr

    # ---- log area ----

    def _build_log(self):
        self.log = scrolledtext.ScrolledText(self, height=8, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---- file dialogs ----

    def _save_file(self, var):
        path = filedialog.asksaveasfilename()
        if path:
            var.set(path)

    def _open_file(self, var, filetypes=None):
        filetypes = filetypes or [("All files", "*")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            var.set(path)

    # ---- build args namespace ----

    def _base_args(self):
        return {
            "host": self.conn["host"].get(),
            "port": self.conn["port"].get(),
            "user": self.conn["user"].get(),
            "password": self.conn["password"].get(),
            "database": self.conn["database"].get(),
            "maintenance_db": "postgres",
            "pg_dump": "pg_dump",
            "pg_restore": "pg_restore",
            "psql": "psql",
        }

    # ---- run in thread ----

    def _run_in_thread(self, label, func, args_dict):
        args = SimpleNamespace(**{**self._base_args(), **args_dict})

        def worker():
            buf = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buf
            try:
                func(args)
                sys.stdout = old_stdout
                output = buf.getvalue().strip()
                if output:
                    self.after(0, self._log, output)
                self.after(0, self._log, f"[OK] {label} completed successfully.")
            except Exception as e:
                sys.stdout = old_stdout
                self.after(0, self._log, f"[FAILED] {label}: {e}")

        threading.Thread(target=worker, daemon=True).start()

    # ---- command handlers ----

    def _run_backup(self):
        self._log("Starting backup…")
        self._run_in_thread("Backup", pg_tools.backup_database, {
            "output": self.bk_output.get(),
            "format": self.bk_format.get(),
            "schema_only": self.bk_schema.get(),
        })

    def _run_restore(self):
        self._log("Starting restore…")
        self._run_in_thread("Restore", pg_tools.restore_backup, {
            "backup": self.rs_backup.get(),
            "target_database": self.rs_target.get() or None,
            "clean": self.rs_clean.get(),
        })

    def _run_export(self):
        self._log("Starting export…")
        self._run_in_thread("Export", pg_tools.export_table, {
            "table": self.ex_table.get(),
            "output": self.ex_output.get(),
            "query": self.ex_query.get() or None,
        })

    def _run_import(self):
        self._log("Starting import…")
        self._run_in_thread("Import", pg_tools.import_table, {
            "table": self.im_table.get(),
            "input": self.im_input.get(),
            "truncate": self.im_truncate.get(),
        })

    def _run_init(self):
        self._log("Starting init…")
        self._run_in_thread("Init", pg_tools.init_database, {
            "sql": self.in_sql.get(),
        })


if __name__ == "__main__":
    App().mainloop()
