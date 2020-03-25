import argparse

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pylab import rcParams

import datetime

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')
# set figure size
rcParams['figure.figsize'] = 13, 6

def parse_arguments():
    parser = argparse.ArgumentParser(description='plotting live')
    # parser.add_argument("-s", "--start", required=True, help="set 'x-axis' start time (time unit is 00:00 ~ 24:00)")
    # parser.add_argument("-e", "--end", required=True, help="set 'x-axis' end time (time unit is 00:00 ~ 24:00)")
    # parser.add_argument("-d", "--dir", required=True, help="path to read file")

    parser.add_argument("-s", "--start", default='10:00', help="set 'x-axis' start time (time unit is 00:00 ~ 24:00)")
    parser.add_argument("-e", "--end", default='14:00', help="set 'x-axis' end time (time unit is 00:00 ~ 24:00)")
    parser.add_argument("-d", "--dir", default='data.txt', help="path to read file")

    parser.add_argument("-t", "--type", help="type of plot {0: line, 1: bar, 2: stacked bar}", default=0)
    parser.add_argument("-f", "--font", help="set font (malgun is korean font)", default="malgun.ttf")
    parser.add_argument("-i", "--interval", help="set the 'x axis' time interval to one of 15, 30, 60", default=15)
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

    # set x-axis int to string (1000 -> 10:00)
    plt.xticks(x_bar_vec, x_vec)
    draw_plot(N, font_prop)

def line_plotter(x_vec, y_data, N, font_prop):
    plt.ion()
    plt.plot(x_vec, y_data, '-o', alpha=0.5)
    draw_plot(N, font_prop)

def get_x_y_vec(start, end, interval):
    '''
    HOUR = 60
    # set x-axis label
    x_list = [str(i*interval) if i else '00' for i in range(HOUR // interval)]

    s_time = datetime.strptime(start, '%H:%M')
    e_time = datetime.strptime(end, '%H:%M')
    print('s_time: {0}, e_time: {1}'.format(s_time, e_time))
    print(e_time - s_time)

    # get a minimum index of 'start-interval' from the x-axis
    x_diff = [abs(int(x_time) - int(start.split(':')[-1])) for x_time in x_list]
    print('x_list: {0}, x_diff: {1}'.format(x_list, x_diff))
    # x_index = 1 if int(start[3:]) <= interval//2 else x_diff.index(min(x_diff))
    x_index = x_diff.index(min(x_diff))
    print('start: {0}, end: {1}, x_index: {2}, interval: {3}'.format(start, end, x_index, interval))

    # 'start time-end time' in the x-axis.
    time_diff = abs(int(''.join((end.split(':')))) - int(''.join((start.split(':')))))
    q, r = time_diff // 100, time_diff % 100
    print('q: {0}, r: {1}'.format(q, r))
    # alpha = time_diff % 10

    # alpha = 2 if time_diff % 100 else 1
    # alpha += 1 if time_diff % 100 and interval == 15 else 0

    # alpha = 2 if int(start[3:]) < interval else 1
    # alpha = 1

    # loop value
    # x_range = time_diff // 100 * len(x_list) + alpha
    x_range = q * len(x_list) + (r // interval) + 1
    alpha = r//interval

    # x-axis start time (hour)
    # x_hour = int(start[:2]) + -1
    # x_hour = int(start[:2])
    x_hour = int(start[:2]) + (0 if x_index else -1)
    # x_hour = int(start[:2]) + (-1 if interval == 60 else 0)
    print('alpha: {0}, x_range: {1}, x_hour: {2}, time_diff: {3}'.format(alpha, x_range, x_hour, time_diff))

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
    '''
    HOUR = 60

    # str to datetime
    s_time = datetime.datetime.strptime(start, '%H:%M')
    e_time = datetime.datetime.strptime(end, '%H:%M')
    # set 'end time-start time' in the x-axis.
    time_diff = e_time - s_time
    print('time_diff: {0}'.format(time_diff))

    # get hour, minutes
    time_total = time_diff.total_seconds()
    x_hour = int(time_total // 3600)
    time_total -= x_hour * 3600
    x_minutes = int(time_total / 60)
    print('h: {0}, m: {1}'.format(x_hour, x_minutes))

    # set x-axis label
    time_unit = start[3:] if interval==60 else '00'
    x_list = [str(i*interval) if i else time_unit for i in range(HOUR // interval)]
    if not x_minutes and not interval == 15:
        x_list = x_list[::-1]

    # get a minimum index of 'start-interval' from the x-axis
    x_diff = [abs(int(x_time) - int(start.split(':')[-1])) for x_time in x_list]
    print('x_list: {0}, x_diff: {1}'.format(x_list, x_diff))
    x_index = x_diff.index(min(x_diff))
    print('start: {0}, end: {1}, x_index: {2}, interval: {3}'.format(start, end, x_index, interval))

    # loop value
    x_range = x_hour * len(x_list) + (x_minutes // interval) + 1

    # x-axis start time (hour)
    x_hour = int(start[:2]) + (0 if x_index else -1)
    print('x_range: {0}, x_hour: {1}, time_diff: {2}'.format(x_range, x_hour, time_diff))

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

    x_vec, y_vec = get_x_y_vec(x_start, x_end, int(x_interval))
    real_data = load_data(args.dir)
    interval = len(real_data) // len(x_vec)
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
        plt.show

if __name__ == '__main__':
    main()