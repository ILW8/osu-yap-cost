from yap_cost import the_yap
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime


if __name__ == '__main__':
    xs, ys = the_yap("data/owc_gf_yap_transcript.json", "data/owc_gf_diarization.txt")
    print(xs)
    print(ys)

    xs = [datetime.datetime.fromtimestamp(x) for x in xs]

    n_count = 200000

    xs = xs[:n_count]

    # set plot to be 16 by 9
    plt.figure(figsize=(16, 9))

    names = ["t1g", "shiba", "miles"]

    for name in names:
        plt.plot(xs, ys[name])

    # add grid
    plt.grid()
    plt.title("yapped words over time")

    # set x axis label
    plt.xlabel("time (s)")

    # Format the x-axis to show time elapsed
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # add legend
    plt.legend(names)

    plt.show()
