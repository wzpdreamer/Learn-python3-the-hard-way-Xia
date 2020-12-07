from matplotlib import pyplot as plt

def calF(data):
    #差商计算  n个数据 1--(n-1)阶个差商
    data_x=[data[i][0] for i in range(len(data))]
    data_y=[data[i][1] for i in range(len(data))]
    F= [1 for i in range(len(data))]
    FM=[]
    for i in range(len(data)):
        FME=[]
        if i==0:
            FME=data_y
        else:
            for j in range(len(FM[len(FM)-1])-1):
                delta=data_x[i+j]-data_x[j]
                value=1.0*(FM[len(FM)-1][j+1]-FM[len(FM)-1][j])/delta
                value = round(value, 10)
                FME.append(value)
        FM.append(FME)
    print("1707004718武智鹏")
    print('Xn :')
    print(data_x)
    print('f(n) :')
    for i in range(len(FM)):
        print(FM[i])
        if(i == 9):
            break
        print('第'+str(i+1)+'阶差商 :')
    F=[fme[0] for fme in FM]
    return F

def NT(data,testdata,F):
    predict=0
    data_x=[data[i][0] for i in range(len(data))]
    data_y=[data[i][1] for i in range(len(data))]
    if testdata in data_x:
        return data_y[data_x.index(testdata)]
    else:
        for i in range(len(data_x)):
            Eq=1
            if i!=0:
                for j in range(i):
                    Eq=Eq*(testdata-data_x[j])
            predict+=(F[i]*Eq)
        return predict

def plot(data,nums):
    data_x=[data[i][0] for i in range(len(data))]
    data_y=[data[i][1] for i in range(len(data))]
    Area=[min(data_x),max(data_x)]
    X=[Area[0]+1.0*i*(Area[1]-Area[0])/nums for i in range(nums)]
    X[len(X)-1]=Area[1]
    F=calF(data)
    Y=[NT(data,x,F) for x in X]
    plt.plot(X,Y,label='result')
    for i in range(len(data_x)):
        plt.plot(data_x[i],data_y[i],'ro',label="point")
    plt.savefig('Newton.jpg')
    plt.show()

data=[[0,0],[3,1.2],[5,1.7],[7,2.0],[9,2.1],[11,2.0],
      [12,1.8],[13,1.2],[14,1.0],[15,1.6]]

plot(data,100)

