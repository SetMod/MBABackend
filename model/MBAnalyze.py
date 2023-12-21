import mlxtend.frequent_patterns as fp
import mlxtend.frequent_patterns as fp
from pandas import DataFrame
from enum import Enum
import pandas as pd
import functools
import logging
import time
import os


class Metric(Enum):
    SUPPORT = "support"
    CONFIDENCE = "confidence"
    LIFT = "lift"
    LEVERAGE = "leverage"
    CONVICTION = "conviction"
    ZHANGS_METRIC = "zhangs_metric"


class Algorithm(Enum):
    APRIORI = "Apriori"
    FPGROWTH = "FP-growth"
    ECLAT = "ECLAT"
    FPMAX = "FP-Max"
    HMINE = "H-mine"


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        logging.info(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


@timer
def preprocess(df: DataFrame) -> DataFrame:
    logging.info("Preprocessing data")

    df = df[df.UserId > 0]
    df = df[df.ItemCode > 0]
    df = df[df.NumberOfItemsPurchased > 0]
    df = df[df.CostPerItem > 0]
    df = df[df.ItemDescription.notna()]
    df = df[df.TransactionTime.str[-4:] != "2028"]

    df.TransactionTime = df.TransactionTime.str.replace(" IST", "")
    df["month_year"] = pd.to_datetime(df.TransactionTime).dt.to_period("M")
    df.sort_values(by=["month_year"], inplace=True)
    df["total_cost_item"] = df.NumberOfItemsPurchased * df.CostPerItem

    return df


@timer
def transform(df: DataFrame) -> DataFrame:
    logging.info("Transforming data")

    transformed_df = (
        df.groupby(["TransactionId", "ItemDescription"])
        .NumberOfItemsPurchased.sum()
        .unstack()
        .reset_index()
        .fillna(0)
        .set_index("TransactionId")
    )
    transformed_df = (transformed_df > 0).astype("bool")

    return transformed_df


@timer
def get_frequent_itemsets(
    df: DataFrame,
    min_support: float = 0.005,
    rules_max_length: int = 2,
    algorithm: Algorithm = Algorithm.FPGROWTH,
) -> DataFrame:
    logging.info(f"Getting frequent item sets with {algorithm.value} algorithm")

    if algorithm == Algorithm.FPGROWTH:
        frequent_itemsets = fp.fpgrowth(
            df,
            min_support=min_support,
            use_colnames=True,
            max_len=rules_max_length,
        )
    elif algorithm == Algorithm.APRIORI:
        frequent_itemsets = fp.apriori(
            df,
            min_support=min_support,
            use_colnames=True,
            max_len=rules_max_length,
        )
    elif algorithm == Algorithm.FPMAX:
        frequent_itemsets = fp.fpmax(
            df,
            min_support=min_support,
            use_colnames=True,
            max_len=rules_max_length,
        )
    elif algorithm == Algorithm.HMINE:
        frequent_itemsets = fp.hmine(
            df,
            min_support=min_support,
            use_colnames=True,
            max_len=rules_max_length,
        )
    # elif algorithm == Algorithm.ECLAT:
    #     frequent_itemsets = eclat(
    #         df,
    #         min_support=min_support,
    #         use_colnames=True,
    #         max_len=rules_max_length,
    #     )
    else:
        frequent_itemsets = fp.fpgrowth(
            df,
            min_support=min_support,
            use_colnames=True,
            max_len=rules_max_length,
        )
    return frequent_itemsets


@timer
def get_association_rules(
    frequent_itemsets: DataFrame,
    metric: Metric = Metric.SUPPORT,
    metric_min_threshold: float = 0.005,
) -> DataFrame:
    logging.info("Getting association rules")

    association_rules = fp.association_rules(
        df=frequent_itemsets,
        metric=metric.value,
        min_threshold=metric_min_threshold,
    )

    return association_rules


def get_top_frequent_itemsets(
    frequent_itemsets: DataFrame,
    metric: Metric = Metric.SUPPORT,
    top: int = 10,
):
    top_items = frequent_itemsets.sort_values(by=metric.value, ascending=False)

    top_items.astype(str)
    ## Convert frozen set to string list
    # for i in range(len(top_items.itemsets)):
    #     top_items.itemsets.iloc[i] = str(list(top_items.itemsets.iloc[i]))

    return top_items[:top]


def get_top_association_rules(
    association_rules: DataFrame,
    metric: Metric = Metric.SUPPORT,
    top: int = 10,
):
    top_rules = association_rules.sort_values(by=metric.value, ascending=False)

    return top_rules[:top]


def get_transactions_number_per_month(df: DataFrame):
    number_of_transactions_per_month = df.groupby("month_year").TransactionId.nunique()

    return number_of_transactions_per_month.to_frame()


def get_top_highest_cost_items(df: DataFrame, top: int = 10):
    top_highest_cost_items = (
        df.groupby("ItemDescription").total_cost_item.sum().sort_values(ascending=False)
    )

    return top_highest_cost_items.to_frame()[:top]


def save_df(
    df: DataFrame,
    file_name: str,
    save_dir: str = "data",
    override: bool = False,
):
    """Save pandas DataFrame to CSV file

    Args:
        df (DataFrame): Pandas DataFrame object
        file_name (str): File name.
        save_dir (str, optional): Directory to create and save file to. Defaults to "data".
        override (bool, optional): Override existing file. Defaults to False.
    """
    if not file_name.endswith(".csv"):
        file_name = file_name + ".csv"

    if not os.path.exists(save_dir):
        logging.info(f"Creating save dir(s): {save_dir}")
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, file_name)

    logging.info(f"Saving file '{file_name}' at: {file_path}")
    if os.path.exists(file_path):
        logging.warning(f"File '{file_name}' exists at: {file_path}")
        if override:
            logging.warning(f"Overwriting existing file at: {file_path}")
            df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, index=False)


# class MBAnalyze:
#     def __init__(
#         self,
#         support: float = 0.005,
#         lift: float = 1,
#         confidence: float = 1,
#         rules_length: int = 2,
#         metric: Metric = Metric.SUPPORT,
#         metric_min_threshold: float = 0.005,
#     ) -> None:
#         self.support = support
#         self.lift = lift
#         self.confidence = confidence
#         self.rules_length = rules_length
#         self.metric = metric
#         self.metric_min_threshold = metric_min_threshold

#     def analyze(self, file_path: str):
#         read_df = pd.read_csv(file_path)
#         df = read_df.copy()

#         preprocessed_df = preprocess(df)
#         transformed_df = transform(preprocessed_df)

#         frequent_itemsets = self.get_frequent_itemsets(transformed_df)
#         association_rules = self.get_association_rules(frequent_itemsets)

#         # preprocess_analyzes = self.analyze_preprocess_data(preprocessed_df)
#         # top_items = frequent_itemsets.sort_values(
#         #     self.metric, ascending=False)[:10]
#         # for i in range(len(top_items.itemsets)):
#         #     top_items.itemsets.iloc[i] = str(
#         #         list(top_items.itemsets.iloc[i]))
#         # top_rules = asoc_rules.sort_values(
#         #     self.metric, ascending=False)[:10]

#         return association_rules, frequent_itemsets

#     def analyze_preprocess_data(self, df: DataFrame):
#         df.sort_values(by=["month_year"], inplace=True)

#         transactions_month_ser = df.groupby("month_year").TransactionId.nunique()
#         transactions_cost_item = (
#             df.groupby("ItemDescription")
#             .total_cost_item.sum()
#             .sort_values(ascending=False)[:10]
#         )

#         return [transactions_month_ser.to_frame(), transactions_cost_item.to_frame()]

#     def analyze_frequent_itemsets(self, frequent_itemsets: DataFrame):
#         top_items = frequent_itemsets.sort_values(self.metric, ascending=False)[:10]
#         for i in range(len(top_items.itemsets)):
#             top_items.itemsets.iloc[i] = str(list(top_items.itemsets.iloc[i]))
#         return top_items

#     def analyze_association_rules(self, association_rules: DataFrame):
#         top_rules = association_rules.sort_values(self.metric, ascending=False)[:10]
#         return top_rules
