# merge_res.py
# 将多个已生成的csv文件进行合并
import pandas as pd

ls = ['./result/test{}_{}k.csv'.format(2*i, 2*(i+1)) for i in range(10)] # 首先生成表格数据名构成的列表
# 如：ls为['test0_2k.csv', 'test2_4k.csv', ..., 'test16_18k.csv', 'test18_20k.csv']

for i in range(len(ls)):
    if i == 0:
        data = pd.read_csv(ls[i])
        data = data.T # 等价于data.transpose()，对数据做转置
    else:
        temp = pd.read_csv(ls[i])
        temp = temp.T
        # 读取表格，并将其表头去掉（即去掉第一行
        temp = temp.iloc[1:, :] # 对于pandas.DataFrame数据类型而言，需要通过.iloc[]的方式进行数值索引
        data = pd.concat([data, temp]) # pd.concat()函数默认竖直拼接，即axis=1

data.to_csv('./result/data.csv', index=True, header=False, encoding="utf_8_sig")