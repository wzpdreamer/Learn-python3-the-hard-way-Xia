import matplotlib.pyplot as plt
import numpy as np

x = np.array([2010,2011,2012,2013,2014,2015,2016])
y = np.array([70,122,144,152,174,196,202])
z1 = np.polyfit(x, y, 1) # 用1次多项式拟合
p1 = np.poly1d(z1)
print("曹宇 1707004223")
print("拟合多项式为：",p1) #输出拟合多项式
print("预测2017年的利润为:",z1[0]*2017+z1[1])
print("预测2018年的利润为:",z1[0]*2018+z1[1])
yvals=p1(x) # 也可以使用yvals=np.polyval(z1,x)
plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4) # 指定legend的位置,读者可以自己help它的用法
plt.title("1707004223")
plt.show()

