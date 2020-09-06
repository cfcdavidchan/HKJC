import csv, sys
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.dates as dates
from datetime import datetime
race_number = sys.argv[1]
today = datetime.now().strftime("%d-%m-%Y")
csv_file = "./RealTime_data/{}/RealTime_Race{}.csv".format(today, race_number)
def read_csv(csv_file):
    odd_list = []
    with open(csv_file, newline='') as data:
        rows = csv.reader(data)
        all_odd = [row for row in rows]
    for i in range(0, len(all_odd)):
        if "Race" in all_odd[i][0]:
            ood_start = i
            crawl_time = all_odd[ood_start][1].split(' ')[1]
            time_odd = all_odd[ood_start + 2 : ood_start + 16]
            odd_list.append([crawl_time, time_odd])
    return odd_list

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    odd_list = read_csv(csv_file)
    xs = []
    ys1 = []
    all_ys = dict()
    for i in range(1,15):
        all_ys["ys_{}".format(i)] = []
    for data in odd_list:
        crawl_time = data[0]
        crawl_time = datetime.strptime(crawl_time, '%H:%M:%S')
        for k in range(1, 15):
            odd = float(data[1][k-1][1])
            if odd == float(0):
                all_ys["ys_{}".format(k)] = None
            else:
                all_ys["ys_{}".format(k)].append((odd))
        xs.append(crawl_time)
    ax1.clear()
    for horse in range(1,15):
        if all_ys["ys_{}".format(horse)] == None:
            pass
        else:
            ax1.plot(xs, all_ys['ys_{}'.format(horse)], label='{}'.format(horse))

    ax1.xaxis.set_major_locator(dates.MinuteLocator(interval=5))  # every 4 hours
    ax1.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))  # hours and minutes
    plt.xticks(rotation=45, ha='right')
    ax1.legend(bbox_to_anchor=(1.0, 1.00))
    ax1.set_ylim((0, 50))

if __name__ == '__main__':
    anim = animation.FuncAnimation(fig, animate, interval=25)
    plt.show()