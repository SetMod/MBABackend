import pandas as pd
from pandas import DataFrame
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np


def preprocess_data(df: DataFrame):
    # Exploratory data analysis(EDA) and data cleaning is done as follows:
    df = df[df.UserId > 0]  # userId <= 0 : 25%
    df = df[df.ItemCode > 0]
    df = df[df.NumberOfItemsPurchased > 0]
    df = df[df.CostPerItem > 0]
    df = df[df.ItemDescription.notna()]
    df = df[df.TransactionTime.str[-4:] != '2028']
    # print(df.info())
    # print(df.head(10))
    df = df[:1000]
    return df


def analyze_data(df: DataFrame):
    # Lets do some exploratory data analysis now. Lets see the no. of transactions
    # being done in each part of the year.
    analyze = {'transactions_month': {'analyze': True, 'plot': True},
               'transactions_unique': {'analyze': True, 'plot': True},
               'transactions_cost_item': {'analyze': True, 'plot': True}}

    df.TransactionTime = pd.to_datetime(df.TransactionTime)
    df['month_year'] = pd.to_datetime(df.TransactionTime).dt.to_period('M')
    df['total_cost_item'] = df.NumberOfItemsPurchased * df.CostPerItem

    if analyze['transactions_month']['analyze'] is True:
        df.sort_values(by=['month_year'], inplace=True)
        Ser = df.groupby('month_year').TransactionId.nunique()

        if analyze['transactions_month']['plot'] is True:
            x = np.arange(0, len(Ser), 1)
            style.use('ggplot')
            fig = plt.figure(figsize=(10, 10))
            ax1 = fig.add_subplot(111)
            ax1.plot(x, Ser, color='k')
            ax1.fill_between(x, Ser, color='r', alpha=0.5)
            ax1.set_xticks(x)
            ax1.set_xticklabels(Ser.index)
            plt.xlabel('Time period')
            plt.ylabel('No. of transactions')

    if analyze['transactions_unique']['analyze'] is True:
        Ser = df.groupby('TransactionId').ItemDescription.nunique()
        # Ser.describe()
        if analyze['transactions_unique']['plot'] is True:
            bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
            fig = plt.figure(figsize=(10, 10))
            plt.hist(Ser, bins, histtype='bar', rwidth=0.5)
            plt.xlabel('No. of items')
            plt.ylabel('No. of transactions')
            plt.show()

            # bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
            # 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
            # fig = plt.figure(figsize=(10, 10))
            # ax1 = fig.add_subplot(111)
            # ax1.hist(Ser, bins, histtype='bar', rwidth=0.5)
            # ax1.set_xticks(bins)
            # plt.xlabel('No. of items')
            # plt.ylabel('No. of transactions')
            # plt.show()

    if analyze['transactions_cost_item']['analyze'] is True:
        Ser = df.groupby('ItemDescription').total_cost_item.sum()
        Ser.sort_values(ascending=False, inplace=True)

        if analyze['transactions_cost_item']['plot'] is True:
            Ser = Ser[:10]
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
            ax.barh(Ser.index, Ser, height=0.5)

    return df


def analyze(file_path):
    read_df = pd.read_csv(file_path)
    df = read_df.copy()
    # print(df.info())
    # print(df.head(10))

    df = preprocess_data(df)
    df = analyze_data(df)

    df_set = df.groupby(['TransactionId', 'ItemDescription']).NumberOfItemsPurchased.sum(
    ).unstack().reset_index().fillna(0).set_index('TransactionId')
    df_set.head()

    def encode(x):
        return 0 if x <= 0 else 1

    df_set = df_set.applymap(encode)

    frequent_itemsets = fpgrowth(df_set, min_support=0.015, use_colnames=True)
    # frequent_itemsets = apriori(df_set, min_support=0.015, use_colnames=True)

    if analyze['top_frequent_items']['analyze'] is True:
        top_items = frequent_itemsets.sort_values(
            'support', ascending=False)[:20]
        for i in range(len(top_items.itemsets)):
            top_items.itemsets.iloc[i] = str(list(top_items.itemsets.iloc[i]))
        if analyze['top_frequent_items']['plot'] is True:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
            ax.bar(top_items.itemsets, top_items.support)
            for label in ax.xaxis.get_ticklabels():
                label.set_rotation(90)
            plt.xlabel('Item')
            plt.ylabel('Support')

    # apply the association rules to these item-sets formed by FPGrowth algorithm
    rules = association_rules(
        frequent_itemsets, metric='confidence', min_threshold=0.2)

    if analyze['top_association_rules']['analyze'] is True:
        top_rules = rules.sort_values('confidence', ascending=False)[:10]
        if analyze['association_rules']['plot'] is True:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
            ax.scatter(top_rules.support, top_rules.confidence, top_rules.lift)
