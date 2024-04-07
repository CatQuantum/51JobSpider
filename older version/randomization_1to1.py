# Although I would like to put everything into a Class, as I am not good at Class at the moment

import pandas as pd
pd.options.mode.chained_assignment = None
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta

data = open(
    '/Users/lunzhengli/OneDrive/Scrapy/gender51job/rearrange_data/result_AC.json').read()

############################################################
## now the data is json, let's make the thing a dataframe ##
############################################################
data_str = data[:-3] + data[-1]
data_json = json.loads(data_str)
df = pd.read_json(data_str, orient='records')
print (df.shape[0])
############################
## constants in the study ##
############################
delta_time = 30
now = datetime(2021, 5, 14)  # it should be the time when I crawled the data
start = now - timedelta(days=delta_time)
exclude_lst = ['初中及以下', '中专', '中技', '大专', '在校生/应届生', '高中', '硕士', '博士', ]
####################################################################
## There are a few functions that we need when rearrange the data ##
####################################################################


def f(x):
    '''
    The function gets the description of the salary in 51job and return to an average monthly salary.
    '''
    try:
        if x[-1] == '年':
            if x[-3] == '万':
                rate = x.split('万')[0]
                ave_rate = (
                    float(rate.split('-')[0]) + float(rate.split('-')[1])) / 2 * 10000 / 12
            elif x[-3] == '下':
                rate = x.split('万')[0]
                ave_rate = float(rate) * (1 - 20 / 100) * 10000 / 12
            elif x[-3] == '上':
                rate = x.split('万')[0]
                ave_rate = float(rate) * (1 + 20 / 100) * 10000 / 12
        elif x[-1] == '月':
            if x[-3] == '千':
                rate = x.split('千')[0]
                ave_rate = (
                    float(rate.split('-')[0]) + float(rate.split('-')[1])) / 2 * 1000
            elif x[-3] == '万':
                rate = x.split('万')[0]
                ave_rate = (
                    float(rate.split('-')[0]) + float(rate.split('-')[1])) / 2 * 10000
            elif x[-3] == '上':
                rate = x.split('万')[0]
                ave_rate = float(rate) * (1 + 20 / 100) * 10000
            elif x[-3] == '下':
                if x[-5] == '千':
                    rate = x.split('千')[0]
                    ave_rate = float(rate) * (1 - 20 / 100) * 1000
                elif x[-5] == '万':
                    rate = x.split('万')[0]
                    ave_rate = float(rate) * (1 - 20 / 100) * 10000
    except:
        ave_rate = -1
    return ave_rate


def salary_level(x):
    if x < 0:
        level = 'na'
    elif 0 < x <= 10000:
        level = 'medium rare'
    elif 10000 < x <= 20000:
        level = 'medium'
    elif 20000 < x <= 30000:
        level = 'medium well'
    elif x > 30000:
        level = 'well done'
    return level

# ['' '2年经验' '5-7年经验' '1年经验' '无需经验' '3-4年经验' '10年以上经验' '8-9年经验']
# ['招1人' '招若干人' '招3人' '招5人' '招4人' '招2人' '招6人' '招10人' '招20人' '招55人' '招25人'
#  '招9人' '招8人' '招16人' '招100人' '招50人' '招150人' '招500人' '招300人' '招30人' '招7人'
#  '招15人' '招13人' '招12人' '招99人' '招11人']
# {0, 4, 6, 7}
# {3, 4, 5}


def recruit_level(x):
    if len(x) == 0:
        level = 'na'
    elif len(x) == 3:
        level = 'miser'
    elif len(x) == 4:
        level = 'economist'
    elif len(x) == 5:
        level = 'prodigal'
    return level


def exp_level(x):
    if len(x) == 0:
        level = 'na'
    elif len(x) == 4:
        level = 'settler'
    elif len(x) == 6:
        level = 'warload'
    elif len(x) == 7:
        level = 'emperor'
    return level


def size_level(x):
    if len(x) == 0:
        level = 'na'
    elif x in ['150-500人', '500-1000人', '50-150人', '少于50人']:
        level = 'small'
    else:
        level = 'big'
    return level


######################################
## let's only keep the data we need ##
######################################
# we make issue_date to datetime vars
df['issue_date'] = [datetime.strptime(
    dt, "%Y-%m-%d %H:%M:%S") for dt in df['issue_date']]
# we only need the city without the district
df['work_city'] = df['work_area'].map(lambda x: x.split('-')[0])
df['company_type'] = (df['company_type'].map(lambda x: 'na' if x == '' else x)
                                        .map(lambda x: '外资' if str(x)[0] == '外' else x)
                                        .map(lambda x: '外资' if str(x)[0] == '合' else x)
                                        .map(lambda x: '国有' if str(x)[0] == '国' else x)
                                        .map(lambda x: '国有' if str(x)[0] == '事' else x)
                                        .map(lambda x: '国有' if str(x)[0] == '政' else x)
                                        .map(lambda x: '非上市' if str(x)[0] == '创' else x)
                                        .map(lambda x: '非上市' if str(x)[0] == '非' else x))
df = df.loc[lambda df: (df['work_city'] != '异地招聘') & (
    df['is_intern'] != 1) & (df['issue_date'] > start)]
for i in exclude_lst:
    df = df[np.array([i not in item for item in df['requirement']])]

lst_time = []
for i in df.salary.values:
    try:
        lst_time.append(
            ((str(i).split('/')[1] == '年') | (str(i).split('/')[1] == '月')))
    except:
        lst_time.append(True)

df = df[lst_time]
df['salary'] = df['salary'].map(f)
df = df[df.salary < 40001]
df['salary_level'] = df['salary'].map(salary_level)

df['plus'] = '+'
df['company+postion'] = df['company_name'] + df['plus'] + df['job_title']
df = df.drop(columns=['is_intern', 'work_area', 'plus'])

# print (df.head())
# print (df.shape)
############################################
## break the requirement list into pieces ##
############################################
df['len_requirement'] = df['requirement'].map(lambda x: len(x))
# print (df['len_requirement'].unique())
# when there are len_requirement = 0, we need the following.
df0 = df[df['len_requirement'] == 0]
df0['experience'] = ''
df0['recruit_num'] = ''
# when len_requirement = 1
df1 = df[df['len_requirement'] == 1]
df1['experience'] = df1['requirement'].map(
    lambda x: x[0] if str(x)[-1] == '验' else '')
df1['recruit_num'] = df1['requirement'].map(
    lambda x: x[0] if str(x[0])[0] == '招' else '')
# when len_requirement = 2
df2 = df[df['len_requirement'] == 2]
df2['experience'] = df2['requirement'].map(lambda x: x[0]).map(
    lambda x: x if str(x)[-1] == '验' else '')
df2['recruit_num'] = df2['requirement'].map(lambda x: x[1]).map(
    lambda x: x if str(x[0])[0] == '招' else '')
# when len_requirement = 3
df3 = df[df['len_requirement'] == 3]
df3['experience'] = df3['requirement'].map(lambda x: x[0])
df3['recruit_num'] = df3['requirement'].map(lambda x: x[2])

df = pd.concat([df0, df1, df2, df3])

df['exp_level'] = df['experience'].map(exp_level)
df['recruit_level'] = df['recruit_num'].map(recruit_level)
df['size_level'] = df['company_size'].map(size_level)

df = df.groupby('company_name', as_index=False).apply(
    lambda x: x.sample(n=1))  # we only pick a position in one company

# # print (df.head())
print (df.shape[0])
# print (df.size_level.unique())
# print (df.company_type.unique())
# # print (df.experience.unique())
# # print (df.recruit_num.unique())
# # print (set([len(df.recruit_num.unique()[i]) for i in range(len(df.recruit_num.unique()))]))
# # print (set([len(df.experience.unique()[i]) for i in range(len(df.experience.unique()))]))
# ###################################################
# ## We randomly put firms into 6 different groups ##
# ###################################################
# df['id'] = df.index
# # print (set(df.company_type.values))
# df_lst = []

# for n in range(6, 0, -1):
#     df_sixth = df.groupby(['work_city', 'company_type', 'size_level', 'salary_level', 'exp_level'], as_index=False).apply(lambda x: x.sample(frac=1/n))
#     df = df[np.array([i not in df_sixth['id'].tolist() for i in df['id'].tolist()])]
#     df_lst.append(df_sixth)
# print ([df_lst[i].shape[0] for i in range(6)])

os.chdir('/Users/lunzhengli/OneDrive/Scrapy/gender51job/rearrange_data/AC')
print ("Current working directory is:", os.getcwd())
# labeling = 1
# for i in df_lst:
#     i = i.drop(columns=['len_requirement', 'id']).reset_index().drop(columns=['level_0', 'level_1', 'level_2'])
#     i.to_excel("output"+str(labeling)+'.xlsx')
#     labeling += 1
df = df.drop(columns=['len_requirement']).reset_index().drop(
    columns=['level_0', 'level_1'])
# print (df.columns.values)
df.to_excel('output.xlsx')
