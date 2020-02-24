import matplotlib.pyplot as plt

from parse import parse_china, parse_china_wo_hubei, daily_cases_by_admin1


def plot_case_histograms(df, top_n_provinces=6, suptitle=''):

    resampled = df.T.iloc[:, :top_n_provinces].resample('d').sum()
    print(resampled.tail())

    # df.columns = [dt.strftime('%m/%d') for dt in df.columns]

    axes = resampled.plot.bar(
        rot=90, subplots=True, sharey=True, figsize=(6, 8))

    for ax in axes:
        ax.legend(loc=2)
        ax.set(title='')

    ax.xaxis.set_major_formatter(plt.FixedFormatter(resampled.index.to_series().dt.strftime("%d %b")))

    fig = plt.gcf()

    fig.suptitle(suptitle, y=1)
    # fig.autofmt_xdate()
    fig.set_tight_layout(True)


if __name__ == '__main__':

    cases_df = parse_china()
    # cases_df = parse_china_wo_hubei()
    province_incidence = daily_cases_by_admin1(cases_df)

    plot_case_histograms(province_incidence, top_n_provinces=6, suptitle='China')

    plt.show()
