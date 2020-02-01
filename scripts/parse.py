""" Parse the line list data and do some cleaning and joining with administrative shapes """

import os

import pandas as pd
import geopandas


def parse_hubei():
    return parse_sheet(sheetname='Hubei')


def parse_outside_hubei():
    return parse_sheet(sheetname='outside_Hubei')


def parse_sheet(sheetname):

    linelist_path = os.path.join('..', 'data', 'cases', 'nCoV2019_2020_line_list_open.xlsx')

    df = pd.read_excel(
        linelist_path,
        sheet_name=sheetname,
        index_col='ID',
        parse_dates=['date_confirmation'])

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

    daily_cases = df.groupby(['province', 'date_confirmation']).country.count().unstack().fillna(0)

    if sort_by_totals:
        total_cases = sum_cases(daily_cases)
        daily_cases = daily_cases.ix[total_cases.index]

    return daily_cases


if __name__ == '__main__':
    outside_hubei_df = parse_outside_hubei()
    print(outside_hubei_df.province.value_counts(dropna=False).head())

    province_incidence = daily_cases_by_admin1(outside_hubei_df)
    print(province_incidence)

