""" Inspect city-level cases within a province """

import matplotlib.pyplot as plt

from parse import parse_china, parse_china_wo_hubei, sum_cases, parse_shapes
from histogram import plot_case_histograms


def daily_cases_by_city(df, sort_by_totals=True):

    df['city'] = df.city.str.strip()  # avoid duplication from whitespace

    daily_cases = df.groupby(['city', 'date_confirmation']).country.count().unstack().fillna(0)

    if sort_by_totals:
        total_cases = sum_cases(daily_cases)
        daily_cases = daily_cases.ix[total_cases.index]

        daily_cases = daily_cases.reindex(sorted(daily_cases.columns), axis=1)

    return daily_cases.astype(int)


def lat_lon_by_city(df):

    df['city'] = df.city.str.strip()  # avoid duplication from whitespace

    return df.groupby('city')[['latitude', 'longitude', 'geo_resolution']].first()


def plot_city_incidence(df, locations, shapes, title=''):

    shapes.plot(color='none', edgecolor='darkgray', linewidth=0.5)

    city_totals = sum_cases(df)
    city_recent = df.iloc[:, -3:].sum(axis=1).rename('recent')  # last 3 days
    locations = locations.join(city_totals).join(city_recent)
    plt.scatter(locations.longitude, locations.latitude,
                s=locations.total, c='goldenrod')
    plt.scatter(locations.longitude, locations.latitude,
                s=locations.recent, c='yellow')
    ax = plt.gca()
    ax.axis('off')
    ax.set(aspect='equal', title=title)
    plt.gcf().set_tight_layout(True)


if __name__ == '__main__':

    cases_df = parse_china()
    # cases_df = parse_china_wo_hubei()
    print(cases_df.province.value_counts(dropna=False).head())

    provinces = ['Zhejiang', 'Guangdong', 'Henan', 'Hunan', 'Anhui']

    admin2_shapes = parse_shapes(level=2)

    for province in provinces:
        province_df = cases_df[cases_df.province == province].copy()
        # print(province_df.city.value_counts(dropna=False).head())

        city_incidence = daily_cases_by_city(province_df)
        # print(city_incidence)

        city_locations = lat_lon_by_city(province_df)
        # print(city_locations)

        districts = admin2_shapes[admin2_shapes.NAME_1 == province]
        # print(districts.NAME_2.head(10))
        # print(districts.iloc[0])

        plot_city_incidence(city_incidence, city_locations, districts, title=province)

        # plot_case_histograms(city_incidence, suptitle=province)

        break

    plt.show()
