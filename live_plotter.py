import argparse
import os

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pylab import rcParams

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')
# set figure size
rcParams['figure.figsize'] = 13, 6

def parse_arguments():
    parser = argparse.ArgumentParser(description='plotting live')
    parser.add_argument("-s", "--start", required=True, help="set 'x-axis' start time (time unit is 00:00 ~ 24:00)")
    parser.add_argument("-e", "--end", required=True, help="set 'x-axis' end time (time unit is 00:00 ~ 24:00)")
    parser.add_argument("-d", "--dir", help="path to read file")

    parser.add_argument("-t", "--type", help="type of plot {0: line, 1: bar, 2: stacked bar}", default=0)
    parser.add_argument("-f", "--font", help="set font (malgun is korean font)", default="malgun.ttf")
    parser.add_argument("-i", "--interval", help="set 'x-axis' time interval", default=30)
    parser.add_argument("-n", "--number", help="set y-axis max range", default=100)
    parser.add_argument('-p', "--pause_time", help="set plt pause time", default=0.5)

    return parser.parse_args()

def draw_plot(N, font_prop, pause_time=0.5):
    plt.ylim(0, N)
    plt.xlabel('시간', fontproperties=font_prop)
    plt.ylabel('예측량', fontproperties=font_prop)
    plt.title('차트', fontproperties=font_prop)

    plt.draw()
    plt.pause(pause_time)
    plt.clf()

def bar_plotter(x_vec, y_data, N, font_prop, stacked):
    plt.ion()
    y2_data = [N-data if data else 0 for data in y_data]
    x_bar_vec = [i for i in range(len(y_data))]

    p1 = plt.bar(x_bar_vec, y_data, width=0.7, alpha=0.5)
    if stacked:
        p2 = plt.bar(x_bar_vec, y2_data, width=0.7, alpha=0.5, bottom=y_data)
        plt.legend((p1, p2), ('없다', '있다'), fontsize=15, prop=font_prop)

    # set x-axis int to string
    plt.xticks(x_bar_vec, x_vec)
    draw_plot(N, font_prop)

def line_plotter(x_vec, y_data, N, font_prop):
    plt.ion()
    plt.plot(x_vec, y_data, '-o', alpha=0.5)
    draw_plot(N, font_prop)

def get_x_y_vec(start, end, interval):
    hour = 60
    # set x-axis
    # Ex. [00, 30] or [45, 30, 15, 00] ...
    x_list = [str(i*interval) if i else '00' for i in range(hour // interval)]
    if interval == 5:
        x_list[1] = '05'
    x_list = x_list if start.endswith('00') else x_list[::-1]

    # hour, h_plus, h_minus = (int(start[:2])-1, 1, 0) if start.endswith('00') else (int(start[:2]), 0, 1)
    hour, h_plus, h_minus = (int(start[:2]) - 1, 1, 0)

    diff = abs(int(''.join((start.split(':')))) - int(''.join((end.split(':')))))
    alpha = 2 if diff % 100 else 1
    x_range = diff // 100 * len(x_list) + alpha

    x_vec = list()
    for i in range(x_range):
        index = i % len(x_list)
        print('i: {2}, index: {0}, x_list: {1}'.format(index, x_list[index], i))
        hour += h_plus if index == 0 else h_minus
        time = ':'.join((str(hour), x_list[index]))
        x_vec.append(time)

    y_vec = [0 for _ in range(len(x_vec))]
    return x_vec, y_vec

def load_data(path):
    with open(path, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]

def main():
    args = parse_arguments()
    font_prop = fm.FontProperties(fname=args.font, size=12)

    x_start = args.start
    x_end = args.end
    x_interval = args.interval

    x_vec, y_vec = get_x_y_vec(x_start, x_end, int(x_interval))
    real_data = load_data(args.dir)
    interval = int(len(real_data) / len(x_vec))
    real_data = [data for i, data in enumerate(real_data) if i % interval==0]

    # args.type {0: line, 1: bar, 2: stacked bar}
    stacked = True if int(args.type) == 2 else False
    plotter, *params = [bar_plotter, x_vec, y_vec, args.number, font_prop, stacked] if int(args.type) \
                        else [line_plotter, x_vec, y_vec, args.number, font_prop]

    for i, num in enumerate(real_data):
        if i >= len(x_vec): break
        y_vec[i] = num
        plotter(*params)

    while True:
        plt.show()

if __name__ == '__main__':
    main()