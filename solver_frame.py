#!/usr/bin/env python3

import sys
import math
from itertools import permutations, combinations
import random

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def swap_link(tour, left, right):
    swaped_tour = tour[left:right+1]
    swaped_tour.reverse()
    return tour[:left] + swaped_tour + tour[right+1:]


def resolve_cross(tour, dist, c):
    N = len(tour)
    difference = 0
    for left, right in c:
        assert left < right
        left_link = left - 1
        right_link = right + 1
        diff = dist[tour[left]][tour[left_link]] + dist[tour[right]][tour[right_link]] - dist[tour[left]][tour[right_link]] - dist[tour[right]][tour[left_link]]
        if diff > 0:
            tour = swap_link(tour, left, right)
            difference += diff
    return tour, difference


def cal_tour_dist(dist, ids):
    sum = 0
    for i in range(len(ids)):
        sum += dist[ids[i-1]][ids[i]]
    return sum

def solve_all_tour(tour, dist):
    p = list(map(lambda x: [tour[0]] + list(x), list(permutations(tour[1:]))))
    index = 0
    min = cal_tour_dist(dist, p[0])
    for i in range(1, len(p)):
        distance = cal_tour_dist(dist, p[i])
        if min > distance:
            index = i
            min = distance
    tour = p[index]
    return tour


def solve(cities, dist):
    N = len(cities)
    max_h = max(cities, key=lambda x: x[1])[1]
    min_h = min(cities, key=lambda x: x[1])[1]
    # make frame
    limit = 11
    divide = int(math.sqrt((N - 1) / limit + 1))
    length = (max_h - min_h) / divide
    sorted_tour = sorted(range(N), key=lambda id: cities[id][1])
    divided_tour = [[] for _ in range(divide)]
    index = 0
    hight = min_h + length
    for i in range(divide):
        count = 0
        for id in sorted_tour[index:]:
            if cities[id][1] > hight: break
            count += 1
        row = sorted_tour[index:index+count]
        num = int((len(row) - 1) / limit + 1)
        if i % 2 == 0:
            for j in range(num):
                divided_tour[i].append(row[limit*j:limit*(j+1)])
        else:
            for j in range(num-1, -1, -1):
                divided_tour[i].append(row[limit*j:limit*(j+1)])
        index += count
        hight += length

    # all tour search
    tour = []
    for i in range(divide):
        for frame in divided_tour[i]:
            t = solve_all_tour(frame, dist)
            tour += t

    # resolve cross
    i = 20
    distance = 1
    c = list(combinations(range(N-1), 2))
    while i > 0 and distance:
        #random.shuffle(c)
        tour, distance = resolve_cross(tour, dist, c)
        #print(distance)
        i -= 1
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    tour = solve(cities, dist)
    #print(tour)
    path_length = sum(distance(cities[tour[i-1]], cities[tour[i]])
                                for i in range(N))
    #print(path_length)
    print_tour(tour)

    #12個→42s challenge7は２時間
