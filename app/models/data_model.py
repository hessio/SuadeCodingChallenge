import os
import pandas as pd


def read_data():
    # Read the CSV files and store the data in DataFrames
    absolute_path = os.path.dirname(__file__)

    commissions_df = pd.read_csv(os.path.join(absolute_path, "../data/commissions.csv"))
    order_lines_df = pd.read_csv(os.path.join(absolute_path, "../data/order_lines.csv"))
    orders_df = pd.read_csv(os.path.join(absolute_path, "../data/orders.csv"))
    product_promotions_df = pd.read_csv(os.path.join(absolute_path, "../data/product_promotions.csv"))
    promotions_df = pd.read_csv(os.path.join(absolute_path, "../data/promotions.csv"))
    products_df = pd.read_csv(os.path.join(absolute_path, "../data/products.csv"))

    return commissions_df, order_lines_df, orders_df, product_promotions_df, promotions_df, products_df
