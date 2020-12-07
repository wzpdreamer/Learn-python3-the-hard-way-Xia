import matplotlib.pyplot as plt
import numpy as np
x = [2010,2011,2012,2013,2014,2015,2016]
y = [70,122,144,152,174,196,202]
poly = np.polyfit(x, y, 1)
poly1 = np.polyfit(x, y, 2)

def f1(x):
    return poly[0]*x + poly[1]
def f2(x):
    return poly1[0]*x*x + poly1[1]*x + poly1[2]
print("1707004718武智鹏")
print("拟合出的一次函数为:",poly[0],"*x",poly[1])
print("由拟合的一次函数得2017年的利润为:",f1(2017))
print("由拟合的一次函数得2018年的利润为:",f1(2018))
print("拟合出的二次函数为:",poly1[0],"*x*x",
      poly1[1],"*x",poly1[2])
print("由拟合的二次函数得2017年的利润为:",f2(2017))
print("由拟合的二次函数得2018年的利润为:",f2(2018))
z = np.polyval(poly, x)
u = np.polyval(poly1, x)
plt.plot(x, y, 'o')
plt.plot(x, z)
plt.plot(x, u)
plt.show()
plt.savefig('nh.jpg')

