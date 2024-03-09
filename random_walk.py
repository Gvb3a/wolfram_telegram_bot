import matplotlib.pyplot as plt
import random
import re


def random_walk_main(query, id):
    dimension_match = re.search(r'(\d)\s*d', query)
    dimension = int(dimension_match.group(1)) if dimension_match else random.randint(1, 3)

    steps_match = re.search(r'(\d+)\s*steps', query)
    steps = int(steps_match.group(1)) if steps_match else 1000

    increment_match = re.search(r'increment\s*(\d+)', query)
    increment = int(increment_match.group(1)) if increment_match else 1

    start_pos_match = re.search(r'start\s*pos\s*(\d+)', query)
    start_pos = int(start_pos_match.group(1)) if start_pos_match else 0

    final_pos_match = re.search(r'final\s*pos\s*(\d+)', query)
    final_pos = int(final_pos_match.group(1)) if final_pos_match else 0

    intersection_match = re.search(r'intersection\s*(\d+)', query)
    intersection = int(intersection_match.group(1)) if intersection_match else False

    number_of_graphics_match = re.search(r'num\s*(\d+)', query)
    number_of_graphics = int(number_of_graphics_match.group(1)) if number_of_graphics_match else random.randint(1, 5)

    if dimension == 1:
        line = []
        len_line = []
        for i in range(number_of_graphics):
            x, len_x = one_dimension(start_pos, final_pos, steps, increment, intersection)
            plt.plot(x)
            len_line.append(len_x)
            print(f'{i+1}/{number_of_graphics}')
        line_value = 0 if type(final_pos) == int else final_pos
        for _ in range(max(len_line)):
            line.append(line_value)
        plt.plot(line, color='k')
        plt.savefig(f"{id}.png")

    elif dimension == 2:
        plt.scatter(0, 0, color='green')
        for i in range(number_of_graphics):
            x, y = two_dimensional(start_pos, final_pos, steps, increment, intersection)
            plt.plot(x, y)
            plt.scatter(x[-1], y[-1], color='r')
            print(f'{i+1}/{number_of_graphics}')
        plt.savefig(f"{id}.png")

    elif dimension == 3:
        ax = plt.figure().add_subplot(projection='3d')
        ax.scatter(0, 0, 0, color='g')
        for i in range(number_of_graphics):
            x, y, z = three_dimensionality(start_pos, steps, increment)
            ax.plot(x, y, z)
            ax.scatter(x[-1], y[-1], z[-1], color='r')
            print(f'{i + 1}/{number_of_graphics}')
        plt.savefig(f"{id}.png")

    else:
        print('Incorrect dimensioning')

    plt.clf()


def one_dimension(start_pos, final_pos, steps, increment, intersection):
    x = [start_pos]
    while steps > 0:
        x.append(x[-1] + random.choice([-increment, increment]))
        steps -= 1
    if type(final_pos) == int:
        while intersection > 0:
            x.append(x[-1] + random.choice([-increment, increment]))
            if x[-1] == final_pos:
                intersection -= 1
    return x, len(x)


def two_dimensional(start_pos, final_pos, steps, increment, intersection):
    x = [start_pos]
    y = [start_pos]
    while steps > 0:
        random_choice = random.choice([True, False])
        if random_choice:
            x.append(x[-1] + random.choice([-increment, increment]))
            y.append(y[-1])
        else:
            y.append(y[-1] + random.choice([-increment, increment]))
            x.append(x[-1])
        steps -= 1
    if type(final_pos) == int:
        while intersection > 0:
            random_choice = random.choice([True, False])
            if random_choice:
                x.append(x[-1] + random.choice([-increment, increment]))
                y.append(y[-1])
            else:
                y.append(y[-1] + random.choice([-increment, increment]))
                x.append(x[-1])
            if x[-1] == 0 and y[-1] == 0:
                intersection -= 1
    return x, y


def three_dimensionality(start_pos, steps, increment):
    x = [start_pos]
    y = [start_pos]
    z = [start_pos]
    while steps > 0:
        random_choice = random.randint(1, 3)
        if random_choice == 1:
            x.append(x[-1] + random.choice([-increment, increment]))
            y.append(y[-1])
            z.append(z[-1])
        elif random_choice == 2:
            x.append(x[-1])
            y.append(y[-1] + random.choice([-increment, increment]))
            z.append(z[-1])
        else:
            x.append(x[-1])
            y.append(y[-1])
            z.append(z[-1] + random.choice([-increment, increment]))
        steps -= 1
    if z[-1] == y[-1] == z[-1] == 0:
        print(1)
    return x, y, z
