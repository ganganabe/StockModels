from GetDataAndClean import *
from sklearn.externals.six.moves import zip
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

GetData = GetDataAndClean(30, 30)
data = GetData.GetMatrixData()

a = list(data[data.y > 0.15].index)
b = list(data[(data.y <= 0.15) & (data.y > -0.05)].index)
c = list(data[data.y <= -0.05].index)
data.ix[a, 'y'] = 'A'
data.ix[b, 'y'] = 'B'
data.ix[c, 'y'] = 'C'

x = data.ix[:, 0:60].as_matrix()
y = list(data.ix[:, 60])
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=1234)

bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=3), n_estimators=100, learning_rate=0.8)
bdt.fit(x_train, y_train)

y_pred = bdt.predict(x_test)

k = confusion_matrix(y_test, y_pred)
print(k)
print(classification_report(y_test, y_pred))
