from influxdb import InfluxDBClient
class CustomInfluxDBCLient(InfluxDBClient):
    def __init__(self, ip, port, username, password, database):
        super().__init__(ip, port, username, password, database)
    def query(self, incremental_field, measurement_name, tstart, tend):
        statement = 'SELECT "{}" FROM "{}" where time > {} - {}'.format(incremental_field, measurement_name, tstart, tend)
        return super().query(statement)