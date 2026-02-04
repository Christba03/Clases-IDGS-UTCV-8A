$ServerInstance = "FERDEV\SQLEXPRESS"
$Database = "TiendaPracticas"
$ExportPath = "D:\Documentos\UTCV\Documentos"

$FechaCorte = (Get-Date).Date.ToString("yyyy-MM-dd")

$Query = @"
    SELECT
    O.OrdenID
    O.FechaOrden
    O.Total
    O.Estado
    C.Nombre
    C.Apellido
    FROM
        Ordenes AS O
    INNER JOIN
        Clientes AS C ON O.ClienteID = C.ClienteID
"@

$ConnectionString = "Server=$ServerInstance;Database=$Database;Integrated Security=True;"

try {
    $Connection = New-Object System.Data.SqlClient.SqlConnection
    $Connection.ConnectionString = $ConnectionString
    $Connection.Open()

    $Command = $Connection.CreateCommand()
    $Command.CommandText = $Query

    $Adapter = New-Object System.Data.SqlClient.SqlDataAdapter $Command
    $DataSet = New-Object System.Data.DataSet
    $rowCount =Adapter.Fill($DataSet)

    $Connection.close()
    
    if ($rowCount -gt 0){
        $Timestap = Get-Date -Format "yyyyMMdd_HHmmss"
        $FileName = "Export_Ventas_$TImestamp.csv"
        $FullPath = Join-Path -Path $ExportPath -ChildPath $FileName

        $DataSet.Tables[0] | Export-Csv - Path $FullPath - NoTypeInformation -Encoding UTF8

        Write-Host "Exito: Se exportaron $rowCount registro al archivo: $FileName" - ForegroundColor Green
    }
    else {
        Write-Host "Info: NO se encontraron registros nuevos para la fecha $FechaCorte. No se genero archivo" -ForegroundColor Yellow
    }

}
catch{
    Write-Host "Error:Ocurrio un problema al ejecutar el proceso" -ForegroundColor Red
    Write-Host $_.Exception.Message
}



