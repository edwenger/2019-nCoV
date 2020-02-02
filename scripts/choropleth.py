import matplotlib.pyplot as plt

from parse import parse_china, parse_china_wo_hubei, daily_cases_by_admin1, parse_shapes, sum_cases


def plot_case_map(df, shapes):
    merged = shapes.join(df, on='NAME_1').fillna(0)
    merged.plot(column='total', cmap='Reds')
    ax = plt.gca()
    ax.axis('off')
    ax.set(aspect='equal')
    merged.plot(color='none', edgecolor='darkgray', linewidth=0.5, ax=ax)
    plt.gcf().set_tight_layout(True)


if __name__ == '__main__':

    cases_df = parse_china()
    # cases_df = parse_china_wo_hubei()
    province_incidence = daily_cases_by_admin1(cases_df)
    print(province_incidence)

    total_incidence = sum_cases(province_incidence)
    admin1_shapes = parse_shapes(level=1)

    plot_case_map(total_incidence, admin1_shapes)

    plt.show()
