
    # 根据'requirement'列的前两项分别拆分为'exp'和'edu'，然后删除原来的'requirement'列
    #df[['exp', 'edu']] = pd.DataFrame(df['requirement'].tolist(), index=df.index)[[0, 1]]
    #df.drop(columns=['requirement'], inplace=True)

    # 将修改后的DataFrame保存为Excel文件