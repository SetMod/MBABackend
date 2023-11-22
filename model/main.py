import MBAnalyze as mba
import pandas as pd
import logging
import sys
import os

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s",
)

file_path = "data/transaction_data.csv"


def log_df_info(df: pd.DataFrame):
    logging.info("DataFrame head:")
    logging.info(f"\n{df.head()}")
    logging.info("DataFrame info:")
    logging.info(f"\n{df.info()}")
    logging.info("DataFrame types:")
    logging.info(f"\n{df.dtypes}")


logging.info(f"Reading file: {file_path}")
df = pd.read_csv(file_path)
# log_df_info(df=df)

preprocessed_df = mba.preprocess(df[:1000])
# log_df_info(df=preprocessed_df)
mba.save_df(
    df=preprocessed_df,
    file_name="pd_1",
    save_dir="preprocessed_data",
    override=True,
)

transformed_df = mba.transform(preprocessed_df)
# log_df_info(df=transformed_df)
mba.save_df(
    df=transformed_df,
    file_name="td_1",
    save_dir="transformed_data",
    override=True,
)

frequent_itemsets = mba.get_frequent_itemsets(
    df=transformed_df,
    min_support=0.0005,
    rules_max_length=3,
    algorithm=mba.Algorithm.FPGROWTH,
)
frequent_itemsets = mba.get_frequent_itemsets(
    df=transformed_df,
    min_support=0.0005,
    rules_max_length=3,
    algorithm=mba.Algorithm.APRIORI,
)
frequent_itemsets = mba.get_frequent_itemsets(
    df=transformed_df,
    min_support=0.0005,
    rules_max_length=3,
    algorithm=mba.Algorithm.FPMAX,
)
frequent_itemsets = mba.get_frequent_itemsets(
    df=transformed_df,
    min_support=0.0005,
    rules_max_length=3,
    algorithm=mba.Algorithm.HMINE,
)

# log_df_info(df=frequent_itemsets)
mba.save_df(
    df=frequent_itemsets,
    file_name="fi_1",
    save_dir="final_data",
    override=True,
)

if frequent_itemsets.empty:
    logging.warning(
        "Frequent itemsets are empty. No data to form association rules, exiting"
    )
    exit()

association_rules = mba.get_association_rules(
    frequent_itemsets, mba.Metric.SUPPORT, metric_min_threshold=0.0005
)
mba.save_df(
    df=frequent_itemsets,
    file_name="ar_1",
    save_dir="final_data",
    override=True,
)
# log_df_info(df=association_rules)

if association_rules.empty:
    logging.warning(
        "Association rules are empty. Please, specify different thresholds for metrics, exiting"
    )
    exit()

#################
# visualization #
#################

top_highest_cost_items = mba.get_top_highest_cost_items(df=preprocessed_df)
# log_df_info(df=top_highest_cost_items)
transactions_number_per_month = mba.get_transactions_number_per_month(
    df=preprocessed_df
)
# log_df_info(df=transactions_number_per_month)

top_items = mba.get_top_frequent_itemsets(frequent_itemsets)
top_rules = mba.get_top_association_rules(association_rules)
visualizations_data = [
    top_items,
    top_rules,
    transactions_number_per_month,
    top_highest_cost_items,
]

# print(transactions_number_per_month.to_json(orient='split'))
# print(transactions_number_per_month.to_json(orient='split'))
# print(top_items.to_json(orient='split'))
# print(top_rules.to_json(orient='split'))

# for i, visualization_data in enumerate(visualizations_data):
#     visualization_file_path = os.path.join("visualization_data", f"vd_{i}csv")

#     visualization_data.to_csv(visualization_file_path, index=False)


# file_path = os.path.join(APP_ANALYZES_FOLDER, f"ar_{mba.id}.csv")

# association_rules.to_csv(file_path, index=False)
# print(json.dumps(association_rules))
