import math
from sys import exit

#二分法
class Dichotomy:

    def __init__(self, start: float, end: float, allow_error: float, function: str):

        self.start = start
        self.end = end
        self.allow_error = allow_error
        self.function = function

    def f(self, x: float) -> float:

        try:
            result = eval(self.function)
            return result
        except NameError:
            print("函数表达式有误")
            exit()

    def judge(self):

        midpoint = (self.start + self.end) / 2
        a = self.f(self.start)
        if a * self.f(midpoint) > 0:
            self.start = (self.start + self.end) / 2
        else:
            self.end = (self.start + self.end) / 2

#牛顿迭代法迭代公式
def compute_newton_iteration_value(x):
    return x-(x**3-2*x-5)/(3*(x**2)-2)


def main():
    print("1707004718 武智鹏")
    function = str(input("请输入函数表达式："))
    start = float(input("请输入区间起点："))
    end = float(input("请输入区间终点："))
    error = float(input("请输入允许误差："))
    count = 0
    d = Dichotomy(start, end, error, function)
    fa = d.f(d.start)
    fb = d.f(d.end)
    if fa * fb < 0:
        print(f"该函数在[{d.start},{d.end}]有零点。")
    else:
        print(f"该函数在[{d.start},{d.end}]无零点，请重新输入区间起点和终点。")
    while True:
        count += 1
        d.judge()
        cha = d.end - d.start
        if cha < d.allow_error:
            result = (d.start + d.end) / 2
            print(f"二分迭代{count}次，结果为{result}")
            break
    print("使用牛顿迭代法：")
    count=0
    x0 = float(input("请输入迭代初值："))
    x1 = compute_newton_iteration_value(x0)  # 计算牛顿迭代式的值并赋给x1
    while (abs(x1 - x0) > d.allow_error):
        count+=1
        x0 = x1
        x1 = compute_newton_iteration_value(x0)
    print(f"使用牛顿迭代法迭代{count}次，结果为{x1}")

if __name__=='__main__':
    main()