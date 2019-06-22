import json
import random

MIN_NUMBER = 1
PURCHASE_NUMBER = 1000
USER_NUMBER = 10
PRODUCT_NUMBER = 10
MAX_QUANTIRY = 100


def make_product_sales_history_file():
    file = open('product_sales_history.txt', 'w')

    for i in range(PURCHASE_NUMBER):
        random_user_id = 'uid_{}'.format(random.randint(MIN_NUMBER, USER_NUMBER))
        random_product_id = 'pid_{}'.format(random.randint(MIN_NUMBER, PRODUCT_NUMBER))
        random_quantity = random.randint(MIN_NUMBER, MAX_QUANTIRY)
        purchase = {
            "user_id": random_user_id,
            "product_id": random_product_id,
            "quantity": random_quantity
        }
        file.write(json.dumps(purchase)+'\n')

    file.close()


if __name__ == '__main__':
    make_product_sales_history_file()
