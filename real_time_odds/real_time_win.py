# https://www.youtube.com/watch?v=Ercd-Ip5PfQ

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json

# with open('odds.json', 'r') as json_file:
#     data = json.load(json_file)

for var in range(1,4):
    exec(f'horse_{var} = []')

# print (horse_1)
# print (horse_2)
# print (horse_3)



plt.style.use('fivethirtyeight')
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    with open('odds.json', 'r') as json_file:
        data = json.load(json_file)

    new_data = data[-1]
    new_x = new_data[0]

    for var in range(1, 4):
        new_data_dict =
        exec(f'horse_{var}.append()')


    # Add x and y to lists
    xs.append(new_x)
    ys.append(new_y)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.subplots_adjust(bottom=0.30)

# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000) #per second
# plt.show()
import json
with open('odds.json', 'r') as json_file:
    data = json.load(json_file)
    print (data)
    print (data[0][0])
    print (data[-1])

