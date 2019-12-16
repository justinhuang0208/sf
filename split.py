def read_dict(path):
    words_dict = []
    with open(path, 'r') as r:
        line = r.readlines()
        for i in line:
            word = i.split(' ')
            words_dict.append(word[0])
    return words_dict
def fmm(source, words_dict):
    len_source = len(source)
    index = 0
    words = [] # 分詞後每個詞的列表

    while index < len_source:
        match = False
        for i in range(window_size, 0, -1):
            sub_str = source[index: index+i]
            if sub_str in words_dict:
                match = True
                words.append(sub_str)
                index += i
                break
        if not match:
            words.append(source[index])
            index += 1
    return words

def bmm(source, word_dict):
    len_source = len(source)
    index = len_source
    words = [] # 分詞後每個詞的列表

    while index > 0:
        match = False
        for i in range(window_size, 0, -1):
            sub_str = source[index-i: index]
            if sub_str in words_dict:
                match = True
                words.append(sub_str)
                index -= i
                break
        if not match:
            words.append(source[index-1])
            index -= 1
    words.reverse()
    return words

def bi_mm(source, word_dict):
    forward = fmm(source, words_dict)
    backward = bmm(source, words_dict)
    # print("FMM: ", forward)
    # print("BMM: ", backward)
    f_single_word = 0
    b_single_word = 0
    # 總詞數
    tot_fmm = len(forward)
    tot_bmm = len(backward)
    # 非辭典詞數
    oov_fmm = 0
    oov_bmm = 0
    # 扣分，越低越好
    score_fmm = 0
    score_bmm = 0
    if forward == backward:
        return backward
    else:
        for each in forward:
            if len(each) == 1:
                f_single_word += 1
        for each in backward:
            if len(each) == 1:
                b_single_word += 1
        for each in forward:
            if each not in words_dict:
                oov_fmm += 1
        for each in backward:
            if each not in backward:
                oov_bmm += 1
        # 非辭典詞越少越好
        if oov_fmm > oov_bmm:
            score_bmm += 1
        elif oov_fmm < oov_bmm:
            score_fmm += 1
        # 總詞數越少越好
        if tot_fmm > tot_bmm:
            score_bmm += 1
        elif tot_fmm < tot_bmm:
            score_fmm += 1
        # 單一個字越少越好
        if f_single_word > b_single_word:
            score_bmm += 1
        elif f_single_word < b_single_word:
            score_fmm += 1
        # 回傳分數最少的那個
        if score_fmm < score_bmm:
            return forward
        else:
            return backward
if __name__ == '__main__':
    words_dict = read_dict('dict.txt')
    window_size = 4
    Input = input('input: ')
    result = bi_mm(Input, words_dict)
    for word in result:
        print(word, end=' ')
