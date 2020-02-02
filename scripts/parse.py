""" Parse the line list data and do some cleaning and joining with administrative shapes """

import os
import json

import pandas as pd
import geopandas


def parse_hubei():
    return parse_sheet(sheetname='Hubei')


def parse_china_wo_hubei():
    df = parse_sheet(sheetname='outside_Hubei')
    return df[df.country == 'China']


def parse_international():
    df = parse_sheet(sheetname='outside_Hubei')
    return df[df.country != 'China']


def parse_china():
    h = parse_hubei()
    c = parse_china_wo_hubei()
    return pd.concat([h, c], ignore_index=True, sort=False)


def parse_sheet(sheetname):

    linelist_path = os.path.join('..', 'data', 'cases', 'nCoV2019_2020_line_list_open.xlsx')

    df = pd.read_excel(
        linelist_path,
        sheet_name=sheetname,
        index_col='ID',
        na_values=['not sure'],  # NaT for confirmation date
        parse_dates=['date_confirmation'])

    df['date_confirmation'] = pd.to_datetime(df.date_confirmation)

    return df


def parse_shapes(level):

    # shapefile_path = os.path.join('..', 'data', 'shapes',
    #                               'admin%d' % level, 'chn_admbnda_adm%d_ocha.shp' % level)

    shapefile_path = os.path.join('..', 'data', 'shapes',
                                  'gadm', 'gadm36_CHN_%d.shp' % level)

    shapes = geopandas.read_file(shapefile_path)

    return shapes


def sum_cases(df):
    return df.sum(axis=1).sort_values(ascending=False).rename('total')


def daily_cases_by_admin1(df, sort_by_totals=True):

    df['province'] = df.province.str.strip()  # avoid duplication from whitespace

    daily_cases = df.groupby(['province', 'date_confirmation']).country.count().unstack().fillna(0)

    if sort_by_totals:
        total_cases = sum_cases(daily_cases)
        daily_cases = daily_cases.ix[total_cases.index]

        daily_cases = daily_cases.reindex(sorted(daily_cases.columns), axis=1)

    return daily_cases.astype(int)


def format_json(df):

    all_case_data = {idx: row.tolist() for idx, row in df.iterrows()}
    all_case_data['Cumulative'] = sum_cases(df).to_dict()
    all_case_data['Recent'] = df.iloc[:, -7:].sum(axis=1).to_dict()  # last week

    output = {'CHN': all_case_data}

    tmp_path = os.path.join('..', 'data', 'tmp')
    os.makedirs(tmp_path, exist_ok=True)

    with open(os.path.join(tmp_path, 'tmp.json'), 'w') as fp:
        json.dump(output, fp)


if __name__ == '__main__':
    outside_hubei_df = parse_china_wo_hubei()
    print(outside_hubei_df.province.value_counts(dropna=False).head())

    province_incidence = daily_cases_by_admin1(outside_hubei_df)
    print(province_incidence)

    format_json(province_incidence)  # dumps tmp.json to be copied into all_case_data.js
