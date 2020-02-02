""" Inspect city-level cases within a province """

import matplotlib.pyplot as plt

from parse import parse_china_wo_hubei, sum_cases
from histogram import plot_case_histograms


def daily_cases_by_city(df, sort_by_totals=True):

    df['city'] = df.city.str.strip()  # avoid duplication from whitespace

    daily_cases = df.groupby(['city', 'date_confirmation']).country.count().unstack().fillna(0)

    if sort_by_totals:
        total_cases = sum_cases(daily_cases)
        daily_cases = daily_cases.ix[total_cases.index]

        daily_cases = daily_cases.reindex(sorted(daily_cases.columns), axis=1)

    return daily_cases.astype(int)


if __name__ == '__main__':
    cases_df = parse_china_wo_hubei()
    print(cases_df.province.value_counts(dropna=False).head())

    provinces = ['Zhejiang', 'Guangdong', 'Henan', 'Hunan', 'Anhui']

    for province in provinces:
        province_df = cases_df[cases_df.province == province].copy()
        # print(province_df.city.value_counts(dropna=False).head())

        city_incidence = daily_cases_by_city(province_df)
        # print(city_incidence)

        plot_case_histograms(city_incidence, suptitle=province)

    plt.show()
