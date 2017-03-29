# -*- coding:utf-8 -*-
# test
import pandas as pd
import numpy as np
import pymysql


class GetDataAndClean(object):
    def __init__(self, date_interval_forward, date_interval_backward):
        self.date_interval_forward = date_interval_forward
        self.date_interval_backward = date_interval_backward

    def GetRowData(self):
        conn = pymysql.connect(host='172.29.112.122', port=3306, user='root', passwd='root', db='quant')
        cursor = conn.cursor()
        cursor.execute("select date,close,volume,code from t_md_hs_code_k WHERE date >= '2012-01-01'")  # code in('603588','603999')
        row_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return row_data

    def GetMatrixData(self):
        row_data = self.GetRowData()
        row_data_list = []
        for i in range(len(row_data)):
            row_data_list.extend(list(row_data[i]))
            print("row data: %s" % i)

        row_data_arr = np.array(row_data_list).reshape((len(row_data), 4))
        row_data_d = {'date': row_data_arr[:, 0],
                      'close': row_data_arr[:, 1],
                      'volume': row_data_arr[:, 2],
                      'code': row_data_arr[:, 3]}
        data_all = pd.DataFrame(row_data_d, columns=['code', 'date', 'close', 'volume'])
        code_list = list(set(data_all['code']))
        X_close = ["close_day" + str(i) for i in range(1, self.date_interval_forward+1)]
        X_volume = ["volume_day" + str(i) for i in range(1, self.date_interval_forward+1)]

        data_close = pd.DataFrame([range(self.date_interval_forward)], columns=X_close).drop(0, axis=0)
        data_volume = pd.DataFrame([range(self.date_interval_forward)], columns=X_volume).drop(0, axis=0)
        data_y = pd.DataFrame([range(1)], columns=["y"]).drop(0, axis=0)
        for i in code_list:
            data_stock = data_all[data_all['code'] == i]
            data_stock.sort_values(by='date')
            date_list = list(set(data_stock['date']))
            if len(date_list) < self.date_interval_forward+self.date_interval_backward+1:
                continue
            date_list.sort()
            date_code_index = [str(c) + "_" + i for c in date_list]

            for x in range(self.date_interval_forward, len(date_list)-self.date_interval_backward):
                data_close = data_close.append(
                    pd.Series(list(data_stock.iloc[x-self.date_interval_forward:x, 2]), index=X_close, name=date_code_index[x]))
                print("data_close code: %s ,day: %s" % (i, x))
                data_volume = data_volume.append(
                    pd.Series(list(data_stock.iloc[x-self.date_interval_forward:x, 3]), index=X_volume, name=date_code_index[x]))
                print("data_volume code: %s , day: %s" % (i, x))
                y_judge = (data_stock.iloc[x+self.date_interval_backward, 2]-data_stock.iloc[x, 2])/data_stock.iloc[x, 2]
                print("y_judge: %s" % y_judge)
                data_y = data_y.append(pd.Series(y_judge, index=['y'], name=date_code_index[x]))
        data_matrix = pd.concat([data_close, data_volume, data_y], axis=1)
        return data_matrix


if __name__ == '__main__':
    date_interval_forward = 30
    date_interval_backward = 30
    TestData = GetDataAndClean(date_interval_forward, date_interval_backward)
    rowdata = TestData.GetRowData()
    data = TestData.GetMatrixData()
    print(data)
