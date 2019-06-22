import json


def most_popular_products_by_unique_num_of_users():
    file = open('product_sales_history.txt', 'r')
    purchased_products = {}
    most_popular_products = []
    for line in file:
        purchase = json.loads(line)
        if purchase['product_id'] not in purchased_products.keys():
            purchased_products[purchase['product_id']] = []

        purchased_products[purchase['product_id']].append(purchase['user_id'])
        purchased_products[purchase['product_id']] = list(set(purchased_products[purchase['product_id']]))
        if not most_popular_products:
            most_popular_products.append(purchase['product_id'])
        else:
            if len(purchased_products[purchase['product_id']]) > len(purchased_products[most_popular_products[0]]):
                most_popular_products.clear()
                most_popular_products.append(purchase['product_id'])
            elif len(purchased_products[purchase['product_id']]) == len(purchased_products[most_popular_products[0]]):
                if purchase['product_id'] not in most_popular_products:
                    most_popular_products.append(purchase['product_id'])
    file.close()
    return most_popular_products


def most_popular_products_by_total_sales_quantity():
    file = open('product_sales_history.txt', 'r')
    sale_quantity_by_product_id = {}
    most_popular_products = []
    for line in file:
        purchase = json.loads(line)
        if purchase['product_id'] not in sale_quantity_by_product_id.keys():
            sale_quantity_by_product_id[purchase['product_id']] = 0

        sale_quantity_by_product_id[purchase['product_id']] = sale_quantity_by_product_id[purchase['product_id']] + purchase['quantity']

        if not most_popular_products:
            most_popular_products.append(purchase['product_id'])
        else:
            if sale_quantity_by_product_id[purchase['product_id']] > sale_quantity_by_product_id[most_popular_products[0]]:
                most_popular_products.clear()
                most_popular_products.append(purchase['product_id'])
            elif sale_quantity_by_product_id[purchase['product_id']] == sale_quantity_by_product_id[most_popular_products[0]]:
                if purchase['product_id'] not in most_popular_products:
                    most_popular_products.append(purchase['product_id'])

    file.close()
    return most_popular_products


if __name__ == '__main__':
    # test
    # case 1
    print('Most popular product(s) based on the number of purchasers:')
    print(most_popular_products_by_unique_num_of_users())

    # test
    # case 2
    print('Most popular product(s) based on the quantity of goods sold:')
    print(most_popular_products_by_total_sales_quantity())

