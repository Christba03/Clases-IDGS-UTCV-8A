CREATE LOGIN dbc WITH PASSWORD = 'StrongPasswordHere';
USE TiendaPracticas;
CREATE USER dbc FOR LOGIN dbc;


USE TiendaPracticas;

SELECT name FROM sys.database_principals WHERE name = 'dbc';
CREATE SCHEMA Clientes AUTHORIZATION dbo;

CREATE TABLE  Clientes.Clientes (
ClienteID INT PRIMARY KEY,
Nombre VARCHAR(50),
Apellido VARCHAR(50),
Email VARCHAR(100),
FechaRegistro DATETIME

);

EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;

exec XP_CMDSHELL 'bcp"SELECT * FROM TiendasPracticas.dbo.CLientes" queryout "C:\Export\Ventas.csv" -c -t, -T -S localhost -u';


USE TiendaPracticas;
GO

BULK INSERT dbo.Ventas
FROM '/var/opt/mssql/Ventas.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n'
);

SELECT @@VERSION;
SELECT DB_NAME();

SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'Ventas';


SELECT COUNT(*) AS total_tables
FROM INFORMATION_SCHEMA.TABLES;


SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_SCHEMA, TABLE_NAME;






