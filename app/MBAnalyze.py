import pandas as pd
from pandas import DataFrame
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
import numpy as np


class MBAnalyze():
    # preprocess_data_path = '../data/preprocessed_data'
    # data_transformation_path = '../data/preprocessed_data'
    metrics = ['support', 'confidence', 'lift']

    def __init__(self, file_id: int, file_path: str, support: float = 0.5, lift: float = 1, confidence: float = 2, rules_length: int = 2, metric: str = 'support') -> None:
        self.support = support
        self.lift = lift
        self.confidence = confidence
        self.rules_length = rules_length
        self.metric = metric if metric in self.metrics else 'support'
        self.min_threshold = self.get_min_threshold()
        self.file_id = file_id
        self.file_path = file_path

    def analyze(self):
        read_df = pd.read_csv(self.file_path)
        df = read_df.copy()

        preprocessed_df = self.preprocess(df)
        print('DF INFO: ', preprocessed_df.info())
        # print(preprocessed_df.head(10))
        # preprocessed_df = preprocessed_df[:1000]
        df_set = self.transform(df)
        print('DF SET TYPE: ', type(df_set))
        frequent_itemsets = self.create_frequent_itemsets(df_set)
        association_rules = self.create_association_rules(frequent_itemsets)

        # preprocess_analyzes = self.analyze_preprocess_data(preprocessed_df)
        # top_items = frequent_itemsets.sort_values(
        #     self.metric, ascending=False)[:10]
        # for i in range(len(top_items.itemsets)):
        #     top_items.itemsets.iloc[i] = str(
        #         list(top_items.itemsets.iloc[i]))
        # top_rules = asoc_rules.sort_values(
        #     self.metric, ascending=False)[:10]

        return association_rules

    def preprocess(self, df: DataFrame, save_csv: bool = False):
        df = df[df.UserId > 0]
        df = df[df.ItemCode > 0]
        df = df[df.NumberOfItemsPurchased > 0]
        df = df[df.CostPerItem > 0]
        df = df[df.ItemDescription.notna()]
        df = df[df.TransactionTime.str[-4:] != '2028']
        df.TransactionTime = pd.to_datetime(df.TransactionTime)
        df['month_year'] = pd.to_datetime(df.TransactionTime).dt.to_period('M')
        df['total_cost_item'] = df.NumberOfItemsPurchased * df.CostPerItem

        if save_csv:
            df.to_csv(
                f'{self.preprocess_data_path}/pd_{self.file_id}.csv', index=False)

        return df

    def transform(self, df: DataFrame, save_csv: bool = False):
        df_set = df.groupby(['TransactionId', 'ItemDescription']).NumberOfItemsPurchased.sum(
        ).unstack().reset_index().fillna(0).set_index('TransactionId')
        df_set = (df_set > 0).astype(np.int8)

        if save_csv:
            df_set.to_csv(f'{self.data_transformation_path}/td_{self.file_id}.csv',
                          index=False)

        return df_set

    def analyze_preprocess_data(self, df: DataFrame):
        df.sort_values(by=['month_year'], inplace=True)
        transactions_month_ser: pd.Series = df.groupby(
            'month_year').TransactionId.nunique()
        transactions_cost_item: pd.Series = df.groupby('ItemDescription').total_cost_item.sum(
        ).sort_values(ascending=False)[:10]

        return [transactions_month_ser.to_frame(), transactions_cost_item.to_frame()]

    def analyze_frequent_itemsets(self, frequent_itemsets: DataFrame):
        top_items = frequent_itemsets.sort_values(
            self.metric, ascending=False)[:10]
        for i in range(len(top_items.itemsets)):
            top_items.itemsets.iloc[i] = str(
                list(top_items.itemsets.iloc[i]))
        return top_items

    def analyze_association_rules(self, association_rules: DataFrame):
        top_rules = association_rules.sort_values(
            self.metric, ascending=False)[:10]
        return top_rules

    def create_association_rules(self, frequent_itemsets: DataFrame, save_csv: bool = False):
        asoc_rules: DataFrame = association_rules(
            frequent_itemsets, metric=self.metric, min_threshold=self.min_threshold)

        if save_csv:
            asoc_rules.to_csv(
                f'{self.preprocess_data_path}/pd_{self.file_id}.csv', index=False)

        return asoc_rules

    def create_frequent_itemsets(self, df_set, save_csv: bool = False):
        frequent_itemsets = fpgrowth(
            df_set, min_support=self.support, use_colnames=True)
        # frequent_itemsets = apriori(df_set, min_support=0.015, use_colnames=True)

        if save_csv:
            frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(
                lambda x: tuple(x))
            frequent_itemsets.to_csv(
                './data/frequent_itemsets.csv', index=False)

        return frequent_itemsets

    def get_min_threshold(self):
        options = {
            'support': self.support,
            'confidence': self.support,
            'lift': self.support,
        }

        for option in options:
            if self.metric == option:
                return options[option]

        return self.support
