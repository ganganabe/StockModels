import seaborn as sns

from GetDataAndClean import *

GetData = GetDataAndClean(30, 30)
data = GetData.GetMatrixData()
y = data['y'].values

ax = sns.distplot(y)
