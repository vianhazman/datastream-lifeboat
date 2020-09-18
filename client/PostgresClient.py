import sqlalchemy
import pandas as pd


class PostgresClient:
    def __init__(self, username, password, host, port, dbname):
        urlDb = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, dbname)
        self.engine = sqlalchemy.create_engine(urlDb, client_encoding='utf8')

    def queryTimeRange(self, table, dstart, dend):
        query_template = sqlalchemy.text(""" 
                    SELECT *
                    FROM {}
                    WHERE to_timestamp(timecreated) >= '{}'::timestamp  and to_timestamp(timecreated) < '{}'::timestamp ; 
        """.format(table, dstart, dend))

        query = query_template
        temp, result_list = {}, []
        for row in self.engine.execute(query):
            for column, value in row.items():
                temp = {**temp, **{column: value}}
            result_list.append(temp)
        return result_list

    def queryMissingData(self, table, filter_field, filter_list):
        query_template = sqlalchemy.text(""" 
                    SELECT *
                    FROM {}
                    WHERE {} IN :values; 
        """.format(table, filter_field))

        query = query_template.bindparams(values=tuple(filter_list))

        temp, result_list = {}, []
        for row in self.engine.execute(query):
            for column, value in row.items():
                temp = {**temp, **{column: value}}
            result_list.append(temp)
        return result_list
