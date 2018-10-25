#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demographics Devices Analysis
Saving the data into a database MySQL
"""

import pandas as pd
# code block deprecated
# import json
# from shapely.geometry import Point, shape


def load_data(path):
    try:
        gen_age_tr = pd.read_csv(path + 'gender_age_train.csv')
        ev = pd.read_csv(path + 'events.csv')
        ph_br_dev_model = pd.read_csv(path + 'phone_brand_device_model.csv')

        return gen_age_tr, ev, ph_br_dev_model

    except Exception as err:
        print("\n>> Process did not finish with success!")
        print("-" * 50)
        print(err.message)


def merge_data(gen_age_tr, ev, ph_br_dev_model):
    df = gen_age_tr.merge(ev, how='left', on='device_id')
    df = df.merge(ph_br_dev_model, how='left', on='device_id')

    print(df.shape)

    return df


def get_phone_brand(df):
    top_10_brands_en = {'华为': 'Huawei', '小米': 'Xiaomi', '三星': 'Samsung', 'vivo': 'vivo', 'OPPO': 'OPPO',
                        '魅族': 'Meizu', '酷派': 'Coolpad', '乐视': 'LeEco', '联想': 'Lenovo', 'HTC': 'HTC'}

    df['phone_brand_en'] = df['phone_brand'].apply(
        lambda phone_brand: top_10_brands_en[phone_brand] if (phone_brand in top_10_brands_en) else 'Other')

    print(df.shape)

    return df


def get_age_segment(age):
    if age <= 22:
        return '< 22'
    elif age <= 26:
        return '23-26'
    elif age <= 28:
        return '27-28'
    elif age <= 32:
        return '29-32'
    elif age <= 38:
        return '33-38'
    else:
        return '> 39'


def apply_age_segment(df):
    df['age_segment'] = df['age'].apply(lambda age: get_age_segment(age))

    print(df.shape)

    return df

# code block deprecated
# path = '/home/lserra/dashio/static/geojson/'
#
# with open(path + 'china_provinces_en.json') as data_file:
#     provinces_json = json.load(data_file)

# code block deprecated
# def get_location(longitude, latitude, provinces_json):
#     point = Point(longitude, latitude)
#     for record in provinces_json['features']:
#         polygon = shape(record['geometry'])
#         if polygon.contains(point):
#             return record['properties']['name']
#
#     return 'other'

# code block deprecated
# df['location'] = df.apply(lambda row: get_location(row['longitude'], row['latitude'], provinces_json), axis=1)

# cols_to_keep = ['timestamp', 'longitude', 'latitude', 'phone_brand_en', 'gender', 'age_segment', 'location']


def clean_up(df):
    cols_to_keep = ['timestamp', 'longitude', 'latitude', 'phone_brand_en', 'gender', 'age_segment']

    df_clean = df[cols_to_keep].dropna()  # delete all values NaN (null)
    df_clean = df_clean[df_clean['longitude'] > 0.0]
    df_clean = df_clean[df_clean['latitude'] > 0.0]

    print(df_clean.shape)

    return df_clean


def save_to_csv(path, df_clean):
    try:
        df_clean.to_csv(path + "demographics.csv")  # export the result to a file (CSV)

        print("\n>> Process finished with success!")

    except Exception as err:
        print("\n>> Process did not finish with success!")
        print("-" * 50)
        print(err.message)


if __name__ == "__main__":
    # path = '/home/df/dashio/data/demographics/'
    path = '/home/lserra/dashio/data/demographics/'
    gen_age_tr, ev, ph_br_dev_model = load_data(path)
    df = merge_data(gen_age_tr, ev, ph_br_dev_model)
    df = get_phone_brand(df)
    df = apply_age_segment(df)
    df = clean_up(df)
    save_to_csv(df)
