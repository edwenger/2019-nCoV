import matplotlib.pyplot as plt

from parse import parse_outside_hubei, daily_cases_by_admin1


def plot_case_histograms(df, top_n_provinces=6):

    province_incidence.columns = [dt.strftime('%b-%d') for dt in province_incidence.columns]

    axes = province_incidence.T.iloc[:, :top_n_provinces].sort_index().plot.bar(
        rot=90, subplots=True, sharey=True, figsize=(6, 8))

    for ax in axes:
        ax.legend(loc=2)
        ax.set(title='')

    plt.gcf().set_tight_layout(True)


if __name__ == '__main__':

    outside_hubei_df = parse_outside_hubei()
    province_incidence = daily_cases_by_admin1(outside_hubei_df)

    plot_case_histograms(province_incidence, top_n_provinces=10)

    plt.show()
