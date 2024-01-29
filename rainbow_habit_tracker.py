# create rainbow

from create_svg import *
import math
import os 

inch = 96

SVG_WIDTH = int(8.26 * inch)
SVG_HEIGHT = int(5.5 * inch)



x_buffer = int(inch/4)
min_x_radius = int(inch/3*2)
x_center = SVG_WIDTH / 2

def get_y_arc_coordinates(x,a,b):
    y = - (b * math.sqrt(a*a - x*x)/ a)

def draw_numbers(chart, count, days):
    start_r = min_x_radius + (count) * x_buffer
    end_r = start_r + x_buffer
    buffer = 180 / days
    index = 1
    for x in range(0, days):
        degree = (buffer * x) - 90 + (buffer/2)
        c = chart.get_int_coordinates(degree, x_center, start_r, end_r)
        chart.add_text(index, "Janda", (c[0]), (c[1]), 15)
        index = index + 1

def draw_arcs( list, chart):

    for i in range(0,len(list)):
        start_r = min_x_radius + (i) * x_buffer
        end_r = start_r + x_buffer
        buffer = 180 / list[i]
        for x in range(0, list[i]):
            degree = (buffer * x) - 90
            c = chart.get_coordinates(degree, x_center, start_r, end_r)
            chart.draw_line(c[0], c[1], c[2], c[3])
      
def draw_words(chart, tasks):
    for index in range(len(tasks)):
        x = x_center - min_x_radius - x_buffer/2 - (x_buffer*index)
        y = SVG_HEIGHT*3/4
        print(tasks[index])
        chart.add_sideways_text(tasks[index][0], "Janda", -y-5, x, 15)


def sort_tasks(tasks):
    sorted_list = []

    for task in tasks:
        if len(sorted_list) == 0:
            sorted_list.append(task)
        else:
            added = False
            for index in range(len(sorted_list)):
                if sorted_list[index][1] > task[1]:
                    sorted_list.insert(index, task)
                    added = True
                    break
            if not added:
                sorted_list.append(task)

    return sorted_list


def main():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    chart = svg(dir_path + '/rainbow')
    print('hi')
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = open(dir_path + "/Database/kitchen.txt", "r")

    lines = file.readlines()

    other_chores_count = read_entries(lines)

    other_chores_count.reverse()
    print(other_chores_count)

    just_ints = []
    for task in other_chores_count:
        just_ints.append(task[1])
    print('hello')
    days = 30

    number_of_arcs = 1  + len(other_chores_count)


    
    x_center = SVG_WIDTH / 2

    
    max_x_radius = min_x_radius+int(x_buffer * number_of_arcs)

    y_center = SVG_HEIGHT / 2

    #chart.add_font("Janda", "/Users/alexiskubica/Library/Fonts/JandaEverydayCasual.ttf")
    chart.start_svg(SVG_WIDTH,SVG_HEIGHT)

    for x in range(min_x_radius, max_x_radius, x_buffer):
        chart.write('<path d="M {0} {1} A 50 50 0 0 1 {2} {1}\n" stroke="blue" stroke-width="1" fill="none" />\n'.format(x_center - x, SVG_HEIGHT*3/4, x_center + x))

    chart.write('<path d="M {0} {1} A 50 50 0 0 1 {2} {1} H {3} A 50 50 0 0 0 {4} {1} Z" fill="none" />\n'.format(x_center - max_x_radius, SVG_HEIGHT*3/4, x_center + max_x_radius, x_center + min_x_radius, x_center - min_x_radius))



    start_degree = -90
    c = chart.get_coordinates(start_degree, x_center, max_x_radius - x_buffer, min_x_radius)
    chart.draw_line(c[0], c[1], c[2], c[3])

    end_degree = 90
    c = chart.get_coordinates(end_degree, x_center, max_x_radius - x_buffer, min_x_radius)
    chart.draw_line(c[0], c[1], c[2], c[3])
    
    

    draw_numbers(chart, len(other_chores_count) - 1, days)
    draw_arcs(just_ints, chart)
    draw_words(chart, other_chores_count)


    

    chart.end_svg()

    chart.file.close()

main()

