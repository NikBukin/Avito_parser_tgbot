import json


def save_param(user_id, user_firstname, user_lastname, city, interval, price, item):
    with open("users_par_dir/user_{}.json".format(user_id), "w", encoding='utf8') as fh:
        json.dump({'user_id': user_id, 'user_firstname': user_firstname, 'user_lastname': user_lastname,
        'city': city, 'interval': interval, 'price': price, 'item': item}, fh)
