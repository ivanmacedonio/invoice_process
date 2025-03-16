# Asociate-procesos-facturacion-payclub

### Estrategias de procesamiento.

1. Si se desea facturar un rango de fechas personalizado, se debera indicar como `query_param` en la URL de la ruta inicial, siguiendo el siguiente formato:

`{HOST}}/credits_billing?dateFrom=YYmmdd HH:MM:SS&dateTo=YYmmdd HH:MM:SS`

Por ejemplo, `{HOST}/credits_billing?dateFrom=20250310 00:00:00&dateTo=20250311 23:59:59` ejecutaria en el rango de fechas de 10/03/2025 al 11/03/2025

2. Si se desea facturar las transacciones registradas en las ultimas 24 horas (proceso recurrente), no debe indicarse ningun `query_param`