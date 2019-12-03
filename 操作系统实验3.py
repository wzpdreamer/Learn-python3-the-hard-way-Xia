# 实验3：模拟分页式存储管理中硬件的地址转换和产生缺页中断，然后分别用
# LRU、FIFO、改进型的CLOCK算法实现分页管理的缺页中断。
# 要求：显示每个页面在内存中的绝对地址，页表信息、列出缺页情况等。
import random
import copy
PAGE_MEMORY = 4
INTERVAL = 1
def time_up(page_list):
    for p in page_list:
        p['time'] += INTERVAL
def print_list(page_list):
    page_num = []
    for p in page_list:
        page_num.append(int(p['No']))
    print('序列为：', end='')
    print(page_num)
#################### FIFO置换算法 #############################
def FIFO(pages_):
    pages = copy.deepcopy(pages_)
    print('')
    print('页面请求序列为 8 9 10 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1')
    print('### FIFO ###')
    page_list = []
    for p in pages:
        page_list_data = []
        if len(page_list) < PAGE_MEMORY:
            page_list.append(p)
        else:
            # s = [page_['No'] for page_ in page_list]
            for page_ in page_list:
                page_list_data.append(page_['No'])

            if p['No'] in page_list_data:
                print('----Remind-----: 新页表%d已经在队列中,绝对地址为%d' % (p['No'], 1024 * page_list_data.index(p['No'])))
            else:
                print('----Remind-----: 新页面%d将替换旧页面%d' % (p['No'], page_list[0]['No']))
                page_list.remove(page_list[0])
                page_list.append(p)
        # print("目前的队列为[{0[0]},{0[1]},{0[2]}]".format(page_list))
        print_list(page_list)
#################### LRU置换算法 #############################
def LRU(page_):
    print('')
    print('页面请求序列为 8 9 10 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1')
    print('### LRU ###')
    pages = copy.deepcopy(page_)
    page_list = []
    for p in pages:
        page_list_data = []
        if len(page_list) < PAGE_MEMORY:
            page_list.append(p)
        else:
            for page_ in page_list:
                page_list_data.append(page_['No'])
            time_up(page_list)
            if p['No'] in page_list_data:
                page_list[page_list_data.index(p['No'])]['time'] = 0
                print('----Remind-----: 页表%d已经在队列中,绝对地址为%d' % (p['No'], 1024 * page_list_data.index(p['No'])))
            else:
                tran = max(page_list, key=lambda t: t['time'])  # 原本是应该位置上的元素替换，但是需要占位，于是直接采取了append的方法
                page_list.remove(tran)
                page_list.append(p)
                print('----Remind-----: 新页表%d将替换%d' % (p['No'], tran['No']))
        print_list(page_list)
####################改进型Clock置换算法#############################
def obsolete_page(page_list):
    while True:
        for page in page_list:
            if page['visited'] == False and page['modified'] == False:
                return page
        for page_ in page_list:
            if page_['visited'] == False and page_['modified'] == True:
                return page_
        for _page in page_list:
            _page['visited'] = False

def getIndex(p, page_list):
    i = 0
    for pages_ in page_list:
        if p['No'] == pages_['No']:
            return i
        i += 1
    return 0

"""def Improved_Clock(pages_):
    pages = copy.deepcopy(pages_)
    print('')
    print('页面请求序列为 8 9 10 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1')
    print('############ Improved_Clock ################')
    page_list = []
    for p in pages:
        page_list_data = []
        if len(page_list) < PAGE_MEMORY:
            page_list.append(p)
        else:
            for page_ in page_list:
                page_list_data.append(page_['No'])
            if p['No'] not in page_list_data:
                _page = obsolete_page(page_list)
                print('----Remind-----: 新页表%d将会替换页表%d' % (_page['No'], p['No']))
                page_list.remove(_page)
                page_list.append(p)
            else:
                print('----Remind-----: 页表%d已存在，绝对地址为%d' % (
                page_list[getIndex(p, page_list)]['No'], 1024 * getIndex(p, page_list)))
                page_list[getIndex(p, page_list)]['visited'] = True
        print_list(page_list)"""

def init(pages):
    for p in pages:
        p['time'] = 0
        p['visited'] = False
        a = random.random()
        if a < 0.5:
            p['modified'] = False
        else:
            p['modified'] = True  # 被访问过

if __name__ == '__main__':
    pages = [{'No': 8}, {'No': 9}, {'No': 10}, {'No': 7}, {'No': 0}, {'No': 1}, {'No': 2}, {'No': 0}, {'No': 3},
        {'No': 0}, {'No': 4}, {'No': 2}, {'No': 3}, {'No': 0}, {'No': 3}, {'No': 2}, {'No': 1}, {'No': 2}, {'No': 0},
        {'No': 1}, {'No': 7}, {'No': 0}, {'No': 1}]
    init(pages)
    FIFO(pages)
    LRU(pages)
    ##Improved_Clock(pages)