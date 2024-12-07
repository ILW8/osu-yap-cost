from yap_cost import the_yap
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime


if __name__ == '__main__':
    xs, ys = the_yap()
    print(xs)
    print(ys)

    xs = [datetime.datetime.fromtimestamp(x) for x in xs]

    plt.plot(xs, ys["ChillierPear"])
    plt.plot(xs, ys["Azer"])
    plt.plot(xs, ys["D I O"])

    # add grid
    plt.grid()
    plt.title("yapped words over time")

    # set x axis label
    plt.xlabel("time (s)")

    # Format the x-axis to show time elapsed
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    plt.show()
