import pandas as pd
from app.models.data_model import read_data


def get_number_of_orders(order_df):
    number_of_orders = len(order_df)
    return number_of_orders


def get_number_of_items_sold(order_lines_df):
    number_of_items_sold = sum(order_lines_df['quantity'])
    return number_of_items_sold


def get_number_of_customers(order_df):
    number_of_customers = len(pd.unique(order_df['customer_id']))
    return number_of_customers


def get_total_discount(order_lines_df):
    total_discount = sum(order_lines_df['full_price_amount'] - order_lines_df['discounted_amount'])
    return total_discount


def get_ave_discount_rate(number_of_items_sold, order_lines_df):
    total_discount_rate = sum(order_lines_df['discount_rate'] * order_lines_df['quantity'])
    ave_discount_rate = total_discount_rate / number_of_items_sold

    return ave_discount_rate


def get_ave_order_total(number_of_orders, order_lines_df):
    total_order = sum(order_lines_df['total_amount'])
    ave_order_total = total_order / number_of_orders

    return ave_order_total


def get_commission_total_and_ave(number_of_orders, order_lines_df, order_df, commission_df):

    order_id_and_total = order_lines_df[['order_id', 'total_amount']].groupby('order_id').sum()
    merge_vendor_id = order_id_and_total.merge(order_df, left_on='order_id', right_on='id')
    vendor_id_and_total = merge_vendor_id[['vendor_id', 'total_amount']].groupby('vendor_id').sum()
    merge_commission_rate = vendor_id_and_total.merge(commission_df, on='vendor_id', how='left')

    # compute commissions
    total_commission = sum(merge_commission_rate['total_amount'] * merge_commission_rate['rate'])
    ave_commission = total_commission / number_of_orders

    return total_commission, ave_commission


def get_commission_total_per_promotion(order_lines_df, products_df, product_promotions_df, orders_df,
                                       commissions_df):
    report_data = {}

    # order_lines_with_products_df = pd.merge(order_lines_df, products_df, left_on='product_id', right_on='id',
    #                                         how='inner')
    # order_lines_with_promotions_df = pd.merge(order_lines_with_products_df, product_promotions_df,
    #                                           on='product_id', how='inner')
    # commissions_with_promotions_df = pd.merge(order_lines_with_promotions_df, promotions_df,
    #                                           left_on='promotion_id', right_on='id', how='inner')
    # commissions_with_promotions_df = pd.merge(commissions_with_promotions_df, commissions_df,
    #                                           left_on='date', right_on='date')
    #
    # commissions_with_promotions_df['commission'] = (commissions_with_promotions_df['rate'] *
    #                                                 commissions_with_promotions_df['discounted_amount'])
    #
    # total_commissions_per_promotion = commissions_with_promotions_df.groupby('promotion_id')
    #
    #

    orders_df["created_at"] = pd.to_datetime(orders_df["created_at"])
    product_promotions_df["date"] = pd.to_datetime(product_promotions_df["date"])
    commissions_df["date"] = pd.to_datetime(commissions_df["date"])

    # Step 3: Filter data based on the given date
    given_date = "2019-08-01"  # Replace with the desired date
    filtered_orders = orders_df[orders_df["created_at"].dt.date == pd.to_datetime(given_date).date()]

    # Step 4: Merge dataframes to get relevant information for each order
    merged_data = filtered_orders.merge(order_lines_df, left_on="id", right_on="order_id")
    merged_data = merged_data.merge(products_df, left_on="product_id", right_on="id")
    merged_data["date"] = pd.to_datetime(merged_data["date"])
    merged_data = merged_data.merge(product_promotions_df, on=["product_id", "date"])
    merged_data = merged_data.merge(commissions_df, on=["vendor_id", "date"])

    merged_data["commission"] = merged_data["discounted_amount"] * merged_data["rate"]

    commissions_by_promotion = merged_data.groupby("promotion_id")

    for name, group_indices in commissions_by_promotion.groups.items():
        report_data[name] = (merged_data.iloc[group_indices])['commission'].sum()

    return report_data


def clean_order_csv_dates(orders_df):

    orders_df['date'] = orders_df['created_at'].str.split(' ', n=1).str[0]
    return orders_df


def filter_for_date(date_string, orders_df, commissions_df, order_lines_df):

    orders_df = clean_order_csv_dates(orders_df)
    commissions_df = commissions_df[commissions_df['date'] == date_string]
    orders_df = orders_df[orders_df['date'] == date_string]
    order_ids_for_date = orders_df['id']
    order_lines_df = order_lines_df[order_lines_df['order_id'].isin(order_ids_for_date)]
    return order_lines_df, orders_df, commissions_df


def create_report(order_lines_df, orders_df, commissions_df, products_df, product_promotions_df, promotions_df):
    report_data = {}

    number_of_orders = get_number_of_orders(orders_df)
    report_data['orders'] = number_of_orders
    report_data['items'] = get_number_of_items_sold(order_lines_df)
    report_data['customers'] = get_number_of_customers(orders_df)
    report_data['total_discount_amount'] = get_total_discount(order_lines_df)
    report_data['discount_rate_avg'] = get_ave_discount_rate(report_data['items'], order_lines_df)

    # total_avg = get_ave_order_total(number_of_orders, order_lines_df)
    total, total_avg = get_commission_total_and_ave(number_of_orders, order_lines_df, orders_df, commissions_df)
    promotions = get_commission_total_per_promotion(order_lines_df, products_df, product_promotions_df, orders_df,
                                                    commissions_df)

    report_data['commissions'] = {
        'order_avg': total_avg,
        'total': total,
        'promotions': promotions
    }

    return report_data


def generate_report(date):

    commissions_df, order_lines_df, orders_df, product_promotions_df, promotions_df, products_df = read_data()
    order_lines_df, orders_df, commissions_df = filter_for_date(date, orders_df, commissions_df, order_lines_df)
    report_data = create_report(order_lines_df, orders_df, commissions_df, products_df, product_promotions_df,
                                promotions_df)
    return report_data
