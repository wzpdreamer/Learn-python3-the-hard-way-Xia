# 将字符转换为对应的Unicode码，中文用2个字节表示
def char2unicode_ascii(intext, length):
    outtext = []
    for i in range(length):
        outtext.append(ord(intext[i]))
    return outtext  # 将Unicode码转为bit


def unicode2bit(intext, length):
    outbit = []
    for i in range(length * 16):
        outbit.append((intext[int(i / 16)] >> (i % 16)) & 1)  # 一次左移一bit
    return outbit  # 将8位ASCII码转为bit


def byte2bit(inchar, length):
    outbit = []
    for i in range(length * 8):
        outbit.append((inchar[int(i / 8)] >> (i % 8)) & 1)  # 一次左移一bit
    return outbit  # 将bit转为Unicode码


def bit2unicode(inbit, length):
    out = []
    temp = 0
    for i in range(length):
        temp = temp | (inbit[i] << (i % 16))
        if i % 16 == 15:
            out.append(temp)
            temp = 0
    return out  # 将bit转为ascii 码


def bit2byte(inbit, length):
    out = []
    temp = 0
    for i in range(length):
        temp = temp | (inbit[i] << (i % 8))
        if i % 8 == 7:
            out.append(temp)
            temp = 0
    return out  # 将unicode码转为字符（中文或英文）


def unicode2char(inbyte, length):
    out = ""
    for i in range(length):
        out = out + chr(inbyte[i])
    return out  # 生成每一轮的key


def createKeys(inkeys):
    keyResult = []
    asciikey = char2unicode_ascii(inkeys, len(inkeys))
    keyinit = byte2bit(asciikey, len(asciikey))
    #    print("keyinit=",end='')
    #    print(keyinit)    #初始化列表key0,key1
    key0 = [0 for i in range(56)]
    key1 = [0 for i in range(48)]  # 进行密码压缩置换1，将64位密码压缩为56位
    for i in range(56):
        key0[i] = keyinit[yasuo1_table[i] - 1]  # 进行16轮的密码生成
    for i in range(16):  # 确定左移的次数
        if (i == 0 or i == 1 or i == 8 or i == 15):
            moveStep = 1
        else:
            moveStep = 2

        # 分两部分，每28bit位一部分，进行循环左移

        for j in range(moveStep):
            for k in range(8):
                temp = key0[k * 7]
                for m in range(7 * k, 7 * k + 6):
                    key0[m] = key0[m + 1]
                key0[k * 7 + 6] = temp
            temp = key0[0]
            for k in range(27):
                key0[k] = key0[k + 1]
            key0[27] = temp
            temp = key0[28]
            for k in range(28, 55):
                key0[k] = key0[k + 1]
            key0[55] = temp

        # 对56位密钥进行压缩置换，压缩为48位
        for k in range(48):
            key1[k] = key0[yasuo2_table[k] - 1]
        keyResult.extend(key1)

    return keyResult


def DES(text, key, optionType):
    keyResult = createKeys(key)
    finalTextOfBit = [0 for i in range(64)]
    finalTextOfUnicode = [0 for i in range(4)]
    #    print(keyResult)

    if optionType == 0:  # 选择的操作类型为加密

        tempText = [0 for i in range(64)]  # 用于临时盛放IP逆置换之前，将L部分和R部分合并成64位的结果
        extendR = [0 for i in range(48)]  # 用于盛放R部分的扩展结果
        unicodeText = char2unicode_ascii(text, len(text))
        #        print('unicodeText: ')
        #       print(unicodeText)
        bitText = unicode2bit(unicodeText, len(unicodeText))
        #        print('bitText: ')
        #       print(bitText)

        initTrans = [0 for i in range(64)]  # 初始化，用于存放IP置换后的结果

        # 进行初始IP置换
        for i in range(64):
            initTrans[i] = bitText[IP_table[i] - 1]
        # 将64位明文分为左右两部分
        L = [initTrans[i] for i in range(32)]
        R = [initTrans[i] for i in range(32, 64)]

        # 开始进行16轮运算
        for i in range(16):
            tempR = R  # 用于临时盛放R

            # 进行扩展，将32位扩展为48位
            for j in range(48):
                extendR[j] = R[extend_table[j] - 1]
            #           print(len(keyResult))
            keyi = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # 与key值进行异或运算
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if keyi[j] != extendR[j]:
                    XORResult[j] = 1

            SResult = [0 for k in range(32)]
            # 开始进行S盒替换

            for k in range(8):
                row = XORResult[k * 6] * 2 + XORResult[k * 6 + 5]
                column = XORResult[k * 6 + 1] * 8 + XORResult[k * 6 + 2] * 4 + XORResult[k * 6 + 3] * 2 + XORResult[
                    k * 6 + 4]
                temp = S[k][row * 16 + column]
                for m in range(4):
                    SResult[k * 4 + m] = (temp >> m) & 1

            PResult = [0 for k in range(32)]
            # 开始进行P盒置换
            for k in range(32):
                PResult[k] = SResult[P_table[k] - 1]

            # 与L部分的数据进行异或
            XORWithL = [0 for k in range(32)]
            for k in range(32):
                if L[k] != PResult[k]:
                    XORWithL[k] = 1

            # 将临时保存的R部分值，即tempR复制给L
            L = tempR
            R = XORWithL

        # 交换左右两部分
        L, R = R, L

        # -合并为一部分
        tempText = L
        tempText.extend(R)
        # IP逆置换
        for k in range(64):
            finalTextOfBit[k] = tempText[_IP_table[k] - 1]
        finalTextOfUnicode = bit2byte(finalTextOfBit, len(finalTextOfBit))
        #        print(finalTextOfUnicode)
        finalTextOfChar = unicode2char(finalTextOfUnicode, len(finalTextOfUnicode))
        #        print(finalTextOfChar)
        return finalTextOfChar
    else:  # 选择的操作类型为解密
        tempText = [0 for i in range(64)]  # 用于临时盛放IP逆置换之前，将L部分和R部分合并成64位的结果
        extendR = [0 for i in range(48)]  # 用于盛放R部分的扩展结果
        unicodeText = char2unicode_ascii(text, len(text))
        #        print(unicodeText)
        bitText = byte2bit(unicodeText, len(unicodeText))
        #        print(bitText)

        initTrans = [0 for i in range(64)]  # 初始化，用于存放IP置换后的结果

        # 进行初始IP置换
        for i in range(64):
            initTrans[i] = bitText[IP_table[i] - 1]
        # 将64位明文分为左右两部分
        L = [initTrans[i] for i in range(32)]
        R = [initTrans[i] for i in range(32, 64)]

        # 开始16轮的循环
        for i in range(15, -1, -1):
            tempR = R  # 用于临时盛放R

            # 进行扩展，将32位扩展为48位
            for j in range(48):
                extendR[j] = R[extend_table[j] - 1]

            keyi = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # 与key值进行异或运算
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if keyi[j] != extendR[j]:
                    XORResult[j] = 1

            SResult = [0 for k in range(32)]
            # 开始进行S盒替换
            for k in range(8):
                row = XORResult[k * 6] * 2 + XORResult[k * 6 + 5]
                column = XORResult[k * 6 + 1] * 8 + XORResult[k * 6 + 2] * 4 + XORResult[k * 6 + 3] * 2 + XORResult[
                    k * 6 + 4]
                temp = S[k][row * 16 + column]
                for m in range(4):
                    SResult[k * 4 + m] = (temp >> m) & 1
            PResult = [0 for k in range(32)]
            # 开始进行P盒置换
            for k in range(32):
                PResult[k] = SResult[P_table[k] - 1]
            # 与L部分的数据进行异或
            XORWithL = [0 for k in range(32)]
            for k in range(32):
                if L[k] != PResult[k]:
                    XORWithL[k] = 1
            # 将临时保存的R部分值，即tempR复制给L
            L = tempR
            R = XORWithL

        # 交换左右两部分
        L, R = R, L

        # 合并为一部分
        tempText = L
        tempText.extend(R)
        # IP逆置换
        for k in range(64):
            finalTextOfBit[k] = tempText[_IP_table[k] - 1]
        finalTextOfUnicode = bit2unicode(finalTextOfBit, len(finalTextOfBit))
        finalTextOfChar = unicode2char(finalTextOfUnicode, len(finalTextOfUnicode))
        return finalTextOfChar


def main():
    text = ''
    optionType = input("加密：0  解密：1  ")
    while (not (optionType == '0' or optionType == '1')):
        print("错误！")
        optionType = input("加密：0  解密：1:  ")
    if optionType == '0':
        print("即将打开待加密文件：1.txt")
        f1 = open('1.txt', encoding='utf-8')
        text = f1.read()
        f1.close()

    else:
        print("即将打开待解密文件：2.txt")
        f2 = open('2.txt', encoding='utf-8')
        text = f2.read()
        f2.close()
    print("内容为: ")
    print(text)
    length = len(text)
    Result = ""
    if optionType == '0':
        f2 = open('2.txt', 'w', encoding='utf-8')
        # ----------若输入文本的长度不是4的整数倍，即不是64字节的整数倍，用空格补全（此处为了加密中文，用的是unicode编码，即用16字节表示一个字符）-------
        text = text + (length % 4) * " "
        length = len(text)
        key = input("输入8位秘钥:\n")

        while (len(key) != 8):
            # print("wrong!! Enter the key(8 bits)")
            key = input("请确定8位秘钥： \n")

        print("加密后密文为：", end=" ")
        for i in range(int(length / 4)):
            tempText = [text[j] for j in range(i * 4, i * 4 + 4)]
            Result = "".join([Result, DES(tempText, key, int(optionType))])
        f2.write(Result)
        f2.close()
        print(Result)
        print("并将其写入 2.txt")
    if optionType == '1':  # ----------若输入文本的长度不是8的整数倍，即不是64字节的整数倍，用空格补全（此处解密出来的密文用的是每8bit转换为一个ascii码，所以生成的八位表示的字符）-------
        f3 = open('3.txt', 'w', encoding='utf-8')
        length = len(text)
        key = input("输入8位秘钥: \n")
        while (len(key) != 8):
            #  print("wrong!! Enter the key(8 bits)")
            key = input("请确定8位秘钥: \n")

        print("解密后明文为：", end=" ")
        for i in range(int(length / 8)):
            tempText = [text[j] for j in range(i * 8, i * 8 + 8)]
            Result = "".join([Result, DES(tempText, key, int(optionType))])
        f3.write(Result)
        f3.close()
        print(Result)
        print("并将其写入 3.txt")


# IP置换表
IP_table = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40,
    32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55,
    47, 39, 31, 23, 15, 7, ]

# 逆IP_table
_IP_table = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13,
    53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1,
    41, 9, 49, 17, 57, 25, ]

# 用于对数据进行扩展置换，将32位数据扩展为48bit
extend_table = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20,
    21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1, ]

# P盒
P_table = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22,
    11, 4, 25, ]

# S盒
S = [[0xe, 0x4, 0xd, 0x1, 0x2, 0xf, 0xb, 0x8, 0x3, 0xa, 0x6, 0xc, 0x5, 0x9, 0x0, 0x7, 0x0, 0xf, 0x7, 0x4, 0xe, 0x2, 0xd,
    0x1, 0xa, 0x6, 0xc, 0xb, 0x9, 0x5, 0x3, 0x8, 0x4, 0x1, 0xe, 0x8, 0xd, 0x6, 0x2, 0xb, 0xf, 0xc, 0x9, 0x7, 0x3, 0xa,
    0x5, 0x0, 0xf, 0xc, 0x8, 0x2, 0x4, 0x9, 0x1, 0x7, 0x5, 0xb, 0x3, 0xe, 0xa, 0x0, 0x6, 0xd, ],
    [0xf, 0x1, 0x8, 0xe, 0x6, 0xb, 0x3, 0x4, 0x9, 0x7, 0x2, 0xd, 0xc, 0x0, 0x5, 0xa, 0x3, 0xd, 0x4, 0x7, 0xf, 0x2, 0x8,
        0xe, 0xc, 0x0, 0x1, 0xa, 0x6, 0x9, 0xb, 0x5, 0x0, 0xe, 0x7, 0xb, 0xa, 0x4, 0xd, 0x1, 0x5, 0x8, 0xc, 0x6, 0x9,
        0x3, 0x2, 0xf, 0xd, 0x8, 0xa, 0x1, 0x3, 0xf, 0x4, 0x2, 0xb, 0x6, 0x7, 0xc, 0x0, 0x5, 0xe, 0x9, ],
    [0xa, 0x0, 0x9, 0xe, 0x6, 0x3, 0xf, 0x5, 0x1, 0xd, 0xc, 0x7, 0xb, 0x4, 0x2, 0x8, 0xd, 0x7, 0x0, 0x9, 0x3, 0x4, 0x6,
        0xa, 0x2, 0x8, 0x5, 0xe, 0xc, 0xb, 0xf, 0x1, 0xd, 0x6, 0x4, 0x9, 0x8, 0xf, 0x3, 0x0, 0xb, 0x1, 0x2, 0xc, 0x5,
        0xa, 0xe, 0x7, 0x1, 0xa, 0xd, 0x0, 0x6, 0x9, 0x8, 0x7, 0x4, 0xf, 0xe, 0x3, 0xb, 0x5, 0x2, 0xc, ],
    [0x7, 0xd, 0xe, 0x3, 0x0, 0x6, 0x9, 0xa, 0x1, 0x2, 0x8, 0x5, 0xb, 0xc, 0x4, 0xf, 0xd, 0x8, 0xb, 0x5, 0x6, 0xf, 0x0,
        0x3, 0x4, 0x7, 0x2, 0xc, 0x1, 0xa, 0xe, 0x9, 0xa, 0x6, 0x9, 0x0, 0xc, 0xb, 0x7, 0xd, 0xf, 0x1, 0x3, 0xe, 0x5,
        0x2, 0x8, 0x4, 0x3, 0xf, 0x0, 0x6, 0xa, 0x1, 0xd, 0x8, 0x9, 0x4, 0x5, 0xb, 0xc, 0x7, 0x2, 0xe, ],
    [0x2, 0xc, 0x4, 0x1, 0x7, 0xa, 0xb, 0x6, 0x8, 0x5, 0x3, 0xf, 0xd, 0x0, 0xe, 0x9, 0xe, 0xb, 0x2, 0xc, 0x4, 0x7, 0xd,
        0x1, 0x5, 0x0, 0xf, 0xa, 0x3, 0x9, 0x8, 0x6, 0x4, 0x2, 0x1, 0xb, 0xa, 0xd, 0x7, 0x8, 0xf, 0x9, 0xc, 0x5, 0x6,
        0x3, 0x0, 0xe, 0xb, 0x8, 0xc, 0x7, 0x1, 0xe, 0x2, 0xd, 0x6, 0xf, 0x0, 0x9, 0xa, 0x4, 0x5, 0x3, ],
    [0xc, 0x1, 0xa, 0xf, 0x9, 0x2, 0x6, 0x8, 0x0, 0xd, 0x3, 0x4, 0xe, 0x7, 0x5, 0xb, 0xa, 0xf, 0x4, 0x2, 0x7, 0xc, 0x9,
        0x5, 0x6, 0x1, 0xd, 0xe, 0x0, 0xb, 0x3, 0x8, 0x9, 0xe, 0xf, 0x5, 0x2, 0x8, 0xc, 0x3, 0x7, 0x0, 0x4, 0xa, 0x1,
        0xd, 0xb, 0x6, 0x4, 0x3, 0x2, 0xc, 0x9, 0x5, 0xf, 0xa, 0xb, 0xe, 0x1, 0x7, 0x6, 0x0, 0x8, 0xd, ],
    [0x4, 0xb, 0x2, 0xe, 0xf, 0x0, 0x8, 0xd, 0x3, 0xc, 0x9, 0x7, 0x5, 0xa, 0x6, 0x1, 0xd, 0x0, 0xb, 0x7, 0x4, 0x9, 0x1,
        0xa, 0xe, 0x3, 0x5, 0xc, 0x2, 0xf, 0x8, 0x6, 0x1, 0x4, 0xb, 0xd, 0xc, 0x3, 0x7, 0xe, 0xa, 0xf, 0x6, 0x8, 0x0,
        0x5, 0x9, 0x2, 0x6, 0xb, 0xd, 0x8, 0x1, 0x4, 0xa, 0x7, 0x9, 0x5, 0x0, 0xf, 0xe, 0x2, 0x3, 0xc, ],
    [0xd, 0x2, 0x8, 0x4, 0x6, 0xf, 0xb, 0x1, 0xa, 0x9, 0x3, 0xe, 0x5, 0x0, 0xc, 0x7, 0x1, 0xf, 0xd, 0x8, 0xa, 0x3, 0x7,
        0x4, 0xc, 0x5, 0x6, 0xb, 0x0, 0xe, 0x9, 0x2, 0x7, 0xb, 0x4, 0x1, 0x9, 0xc, 0xe, 0x2, 0x0, 0x6, 0xa, 0xd, 0xf,
        0x3, 0x5, 0x8, 0x2, 0x1, 0xe, 0x7, 0x4, 0xa, 0x8, 0xd, 0xf, 0xc, 0x9, 0x0, 0x3, 0x5, 0x6, 0xb, ], ]

# 压缩置换表1，不考虑初始秘钥中的奇偶校验位（每个字节的第八位），将64位秘钥压缩至56位
yasuo1_table = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44,
    36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4, ]

# 压缩置换表2，将循环左移和右移的56bit秘钥压缩为48位
yasuo2_table = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37,
    47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32, ]

if __name__ == '__main__':
    main()