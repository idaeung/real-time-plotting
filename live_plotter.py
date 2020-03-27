import argparse

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pylab import rcParams

from datetime import datetime as dt

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')
# set figure size
rcParams['figure.figsize'] = 13, 6

HOUR = 60

def _check_time(start, end, interval):
    try:
        assert abs(int(start[3:]) - int(end[3:])) % interval
        assert start[2] == ':' and end[2] == ':'
    except Exception:
        print('check parser options')

def parse_arguments():
    parser = argparse.ArgumentParser(description='plotting live')
    parser.add_argument("-s", "--start", required=True, help="set 'x-axis' start time (time range 00:00 ~ 24:00)")
    parser.add_argument("-e", "--end", required=True, help="set 'x-axis' end time (time range 00:00 ~ 24:00)")
    parser.add_argument("-d", "--dir", required=True, help="path to read file")

    parser.add_argument("-t", "--type", help="type of plot {0: line, 1: bar, 2: stacked bar}", default=1)
    parser.add_argument("-f", "--font", help="set font (malgun is korean font)", default="malgun.ttf")
    parser.add_argument("-i", "--interval", help="set the 'x axis' time interval to one of 15, 30, 60", default=30)
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
    y2_data = [N - data if data else 0 for data in y_data]
    x_bar_vec = [i for i in range(len(y_data))]

    p1 = plt.bar(x_bar_vec, y_data, width=0.7, alpha=0.5)
    if stacked:
        p2 = plt.bar(x_bar_vec, y2_data, width=0.7, alpha=0.5, bottom=y_data)
        plt.legend((p1, p2), ('없다', '있다'), fontsize=15, prop=font_prop)
    else:
        plt.legend(p1, ('없다',), fontsize=15, prop=font_prop)

    # set x-axis int to string (1000 -> 10:00)
    plt.xticks(x_bar_vec, x_vec)
    draw_plot(N, font_prop)

def line_plotter(x_vec, y_data, N, font_prop):
    plt.ion()
    p1 = plt.plot(x_vec, y_data, '-o', alpha=0.5)
    plt.legend(p1, ('없다',), fontsize=15, prop=font_prop)
    draw_plot(N, font_prop)

def get_diff_h_m(start, end):
    # str to datetime
    start_dt = dt.strptime(start, '%H:%M')
    end_dt = dt.strptime(end, '%H:%M')
    # set 'end time-start time' in the x-axis.
    diff = end_dt - start_dt

    # get diff hour, minutes
    seconds = diff.total_seconds()
    hour = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    return hour, minutes

def get_xy_vec(start, end, interval):

    diff_hour, diff_minutes = get_diff_h_m(start, end)

    # set x-axis label
    time_unit = start[3:] if interval==60 else '00'
    x_list = [str(i*interval) if i else time_unit for i in range(HOUR // interval)]
    if not diff_minutes and not interval == 15 and not start[3:] == '00':
        x_list = x_list[::-1]
    # if interval==30 and start[3:] == '30':
    #     x_list = x_list[::-1]

    # set x-axis range
    x_range = diff_hour * len(x_list) + (diff_minutes // interval) + 1
    print('diffH: {0}, diffM: {1}, x_range: {2}'.format(diff_hour, diff_minutes, x_range))

    # get a minimum index of 'start-interval' from the x-axis
    x_diff = [abs(int(x_time) - int(start.split(':')[-1])) for x_time in x_list]
    print('x_list: {0}, x_diff: {1}'.format(x_list, x_diff))
    x_index = x_diff.index(min(x_diff))
    print('start: {0}, end: {1}, x_index: {2}, interval: {3}'.format(start, end, x_index, interval))

    # x-axis start time (hour)
    x_hour = int(start[:2]) + (0 if x_index else -1)

    x_vec = list()
    for i in range(x_range):
        # dequeue x_list value
        front = (i + x_index) % len(x_list)
        if front % len(x_list) == 0:
            x_hour += 1
        time = ':'.join((str(x_hour), x_list[front]))
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

    x_vec, y_vec = get_xy_vec(x_start, x_end, int(x_interval))
    real_data = load_data(args.dir)
    step = len(real_data) // len(x_vec)
    real_data = [data for i, data in enumerate(real_data) if i % step==0]

    # args.type {0: line, 1: bar, 2: stacked bar}
    stacked = True if int(args.type) == 2 else False
    plotter, *params = [bar_plotter, x_vec, y_vec, args.number, font_prop, stacked] if int(args.type) \
                        else [line_plotter, x_vec, y_vec, args.number, font_prop]

    for i, num in enumerate(real_data):
        if i >= len(x_vec): break
        y_vec[i] = num
        plotter(*params)

if __name__ == '__main__':
    main()