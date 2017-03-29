# -*- coding:utf-8 -*-
# test
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class GetDataAndClean(object):
    def __init__(self, date_interval_forward, date_interval_backward):
        self.date_interval_forward = date_interval_forward
        self.date_interval_backward = date_interval_backward
        self.engine = create_engine("mysql+pymysql://root:root@172.29.112.122:3306/quant", echo=False)

    def GetCodeList(self):
        engine = self.engine
        code_list = pd.read_sql_query("SELECT DISTINCT code FROM t_md_hs_code_k WHERE date >= '2012-01-01'", engine)
        return code_list

    def GetDataMatrix(self, code):
        date_interval_forward = self.date_interval_forward
        date_interval_backward = self.date_interval_backward
        engine = self.engine
        raw_data = pd.read_sql_query(
            "SELECT date,close,volume,code FROM t_md_hs_code_k WHERE code = %s AND date>='2012-01-01'" % code, engine)
        raw_data.sort_values(by="date")
        date_list = raw_data.ix[:, 'date']
        X_close = ["close_day" + str(i) for i in range(1, date_interval_forward+1)]
        X_volume = ["close_day" + str(i) for i in range(1, date_interval_forward+1)]
        date_code = [str(d) + "_" + str(code) for d in date_list]
        data_close = pd.DataFrame([range(date_interval_forward)], columns=X_close).drop(0, axis=0)
        data_volume = pd.DataFrame([range(date_interval_forward)], columns=X_volume).drop(0, axis=0)
        data_y = pd.DataFrame([range(1)], columns=["y"]).drop(0, axis=0)
        for x in range(date_interval_forward, len(raw_data)-date_interval_backward):
            data_close = data_close.append(
                pd.Series(list(raw_data.ix[x-date_interval_forward:x-1, 'close']), index=X_close, name=date_code[x]))
            data_volume = data_volume.append(
                pd.Series(list(raw_data.ix[x-date_interval_forward:x-1, 'volume']), index=X_volume, name=date_code[x]))
            y_judge = (raw_data.ix[x+date_interval_backward, 'close']/raw_data.ix[x, 'close'])/raw_data.ix[x, 'close']
            data_y = data_y.append(pd.Series(y_judge, index=['y'], name=date_code[x]))
        data_matrix = pd.concat([data_close, data_volume, data_y], axis=1)
        return data_matrix

    def WtoMysql(self):
        code_list = self.GetCodeList()
        engine = self.engine
        for c in code_list:
            data_matrix = self.GetDataMatrix(c)
            data_matrix.to_sql('data20160101_3030', engine, index_label=['datecode'], index=True, if_exists='append')
            print("stock: %s has been writen to Mysql" % c)

if __name__ == '__main__':
    date_interval_forward = 30
    date_interval_backward = 30
    TestData = GetDataAndClean(date_interval_forward, date_interval_backward)
    WtoS = TestData.WtoMysql()