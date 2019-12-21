import numpy as np
import pandas as pd
import re
from numpy import log, min

def generate():
    for m in range(2, max_sep+1):
        print(u'正在生成%s字詞...'%m)
        t.append([])
        for i in range(m): #生成所有可能的m字詞
            t[m-1] = t[m-1] + re.findall(myre[m], s[i:])
        
        t[m-1] = pd.Series(t[m-1]).value_counts() #逐詞統計
        t[m-1] = t[m-1][t[m-1] > min_count] #最小次數篩選
        tt = t[m-1][:]
        for k in range(m-1):
            qq = np.array(list(map(lambda ms: tsum*t[m-1][ms]/t[m-2-k][ms[:m-1-k]]/t[k][ms[m-1-k:]], tt.index))) > min_support #最小支持度篩選。
            tt = tt[qq]
        rt.append(tt.index)


def cal_S(sl):  # 信息熵計算函數
    return -((sl/sl.sum()).apply(log)*sl/sl.sum()).sum()


def entropy_filter():
    for i in range(2, max_sep+1):
        print(u'正在進行%s字詞的最大熵篩選(%s)...' % (i, len(rt[i-2])))
        pp = []  # 保存所有的左右鄰結果
        for j in range(i+2):
            pp = pp + re.findall('(.)%s(.)' % myre[i], s[j:])
        pp = pd.DataFrame(pp).set_index(1).sort_index()  # 先排序加快檢索速度
        index = np.sort(np.intersect1d(rt[i-2], pp.index))  # 作交集
        # 下面兩句分別是左鄰和右鄰信息熵篩選
        index = index[np.array(
            list(map(lambda s: cal_S(pd.Series(pp[0][s]).value_counts()), index))) > min_s]
        rt[i-2] = index[np.array(
            list(map(lambda s: cal_S(pd.Series(pp[2][s]).value_counts()), index))) > min_s]

def output_process():
    # 下面都是輸出前處理
    for i in range(len(rt)):
        t[i+1] = t[i+1][rt[i]]
        t[i+1].sort_index(ascending=False)

def save_result():
    # 保存結果並輸出
    print('save result')
    pd.DataFrame(pd.concat(t[1:])).to_csv('output.txt', header=False)

def write_dict():
    with open('new_dict.txt', 'r') as f:
        oridict = f.readlines()
        oridict = list(map(lambda x: x.strip('\n'), oridict))
    with open('output.txt', 'r') as f:
        readyToWrite = f.readlines()
        readyToWrite = list(map(lambda x: x.strip('\n'), readyToWrite))  
        readyToWrite = list(map(lambda x: x.split(',')[0], readyToWrite))
    print('all new words: ', len(readyToWrite))
    with open('new_dict.txt', 'a+') as f:
        for word in readyToWrite:
            if word not in oridict:
                f.write(word+'\n')

    # print(oridict)


# main
if __name__=='__main__':
    f = open('input.txt', 'r')  # 讀取文章
    s = f.read()  # 讀取為一個字符串

    # 定義要去掉的標點字
    drop_dict = [u'，', u'\n', u'。', u'、', u'：',
                 u'(', u')', u'[', u']', u'.', u',', u' ', u'\u3000', u'」', u'「', u'？', u'?', u'！', u'‘', u'’', u'…']
    for i in drop_dict:  # 去掉標點字
        s = s.replace(i, '')

    # 為了方便調用，自定義了一個正則表達式的詞典
    myre = {2: '(..)', 3: '(...)', 4: '(....)',
            5: '(.....)', 6: '(......)', 7: '(.......)'}

    min_count = 10  # 錄取詞語最小出現次數
    min_support = 30  # 錄取詞語最低支持度，1代表著隨機組合
    min_s = 3  # 錄取詞語最低信息熵，越大說明越有可能獨立成詞
    max_sep = 4  # 候選詞語的最大字數
    t = []  # 保存結果用。

    t.append(pd.Series(list(s)).value_counts())  # 逐字統計
    tsum = t[0].sum()  # 統計總字數
    rt = []  # 保存結果用

    generate()
    entropy_filter()
    output_process()
    save_result()
    write_dict()
