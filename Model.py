from GetDataAndClean import *

GetData = GetDataAndClean(30, 30)
data = GetData.GetMatrixData()

a = list(data[data.y > 0.15].index)
b = list(data[(data.y <= 0.15) & (data.y > -0.05)].index)
c = list(data[data.y <= -0.05].index)
data.ix[a, 'y'] = 'A'
data.ix[b, 'y'] = 'B'
data.ix[c, 'y'] = 'C'
print('B')