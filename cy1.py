import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from sympy.physics.quantum.tests.test_circuitplot import mpl

x = [0, 3, 5, 7, 9, 11, 12, 13, 14, 15]
y = [0, 1.2, 1.7, 2.0, 2.1, 2.0, 1.8, 1.2, 1.0, 1.6]

# 进行样条插值
# t = np.arange(0, 15.1, .10)  # 0到15之间生成一个一维数组，差值0.10
tck = interpolate.splrep(x, y)
xx = np.linspace(min(x), max(x), 150)
yy = interpolate.splev(xx, tck)


def draw(data_x, data_y, data_x_new, data_y_new):  # 画图
    plt.plot(data_x_new, data_y_new, label="三次样条插值拟合曲线", color="black")
    plt.scatter(data_x, data_y, label="离散数据")  # 散点图
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.title("曹宇 1707004223")
    plt.show()


if __name__ == "__main__":
    print("曹宇 1707004223")
    for i in range(yy.__len__()):
        print(round(yy[i], 3), end="  ")
        if i != 0:
            j = i+1
            if j % 10 == 0:
                print('\n')
    draw(x, y, xx, yy)
