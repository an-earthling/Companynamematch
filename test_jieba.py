# 基于jieba分词的文本切分及词性分析, 生成匹配分值(score2)

import jieba.posseg as pseg

from codecs import xmlcharrefreplace_errors
from os import linesep

from pandas.core.frame import DataFrame
from subject_match import*
import sas7bdat as sas
import pandas as pd
import numpy as np
import itertools
'''
itertools模块用于操作迭代对象
SAS7BDAT模块reader.readlines()会创建一个序列包含irm_all.sas7bdat的全部行列表
读取全部行列表程序运行过慢，
因此，import itertools用于将数据切片，指定行数读取数据
'''
path = 'data\irm_all.sas7bdat'

with sas.SAS7BDAT(path, skip_header=False) as reader:
    #islice(iterable, start, stop, step)
    column_heading = itertools.islice(reader.readlines(), 0, 1) # 读取列标题
    for i in column_heading:
        df = pd.DataFrame(columns=i) # 创建包含列标题的dataframe
    
    start_n = 18000 # 从第start_n行开始读取数据
    stop_n = 20000 # 读到第stop_n行(包含第stop_n行)
    lines = itertools.islice(reader.readlines(), start_n, stop_n, 1) 
    for j in lines:
        df.loc[len(df)] = j

# 逐行判断InstitutionName是否包含在S0301a内，留下未包含在内的
# df = df[df.apply(lambda x: x['InstitutionName'] not in x['S0301a'], axis=1)]

# 预备存储原始信息的空列表
list_RID = []
list_Symbol = []
list_IN = []
list_Rer = []
list_S0301a = []

# score
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []

for i in range(0,len(df)): 
    row = df.iloc[i]
    list_RID.append(row['ReportID'])
    list_Symbol.append(row['Symbol'])
    list_IN.append(row['InstitutionName'])
    list_Rer.append(row['Researcher'])
    list_S0301a.append(row['S0301a'])

# method1
    seq1 = row['InstitutionName']
    seq2 = row['S0301a']
    method1 = StringMatcher(seq1, seq2)
    method1.set_seqs(seq1, seq2)
    method1.get_opcodes()
    method1.get_editops()
    method1.get_matching_blocks()
    method1.ratio()
    s_1 = method1.partial_ratio()
    s1.append(s_1)

# method2：基于jieba分词的文本切分及词性分析，生成匹配分值(score2)
    seq2_1 = row['InstitutionName']
    sent = row['S0301a']
    # 清洗标点符号
    score = re.sub(r"[%s]+" % '-', '', sent)
    # jieba_采用n-gram模型(HMM=False，不采用HMM模型，即不认识的词统一切分为单字)最大概率分词
    seq2_2 = pseg.cut(sent, HMM=False) 
    # 将seq2_2m1从generator转为list
    lines2_2 = itertools.islice(seq2_2 , 0, 100, 1) 
    seq2_2m1 = []
    for x,n in lines2_2:
        seq2_2m1.append(x)
    # 将seq2_2m1从list转为array
    words_array2_2 = np.asarray(seq2_2m1)
    seq2_2m1 = join_char(words_array2_2)
    # 基于编辑距离的文本相似度
    temp2 = []
    for i in range(len(seq2_2m1)):
        seq2_2 = str(seq2_2m1[i])
        method2 = StringMatcher(seq2_1, seq2_2)
        method2.set_seqs(seq2_1, seq2_2)
        method2.get_opcodes()
        method2.get_editops()
        method2.get_matching_blocks()
        method2.ratio()
        temp2_s = method2.partial_ratio()
        temp2.append(temp2_s)
    if len(temp2) == 0:
        temp2.append(0)
    s_2 = max(temp2)
    s2.append(s_2)

d = {'ReportID':  list_RID, 'Symbol':  list_Symbol,  'InstitutionName': list_IN, 'Researcher': list_Rer, 'S0301a': list_S0301a, 'score1': s1, 'score2': s2, 'score3': s3, 'score4': s4, 'score5': s5}
dataframe = pd.DataFrame.from_dict(d, orient='index')
print(d)
print(dataframe)
dataframe.to_csv("test18_20k.csv", index=True, sep=',', encoding="utf_8_sig")
