"""IBBC_rooms.py

This script allows you to generate new rooms (of 2 and 3 participants)
given a file database.txt where previous rooms were written.
It requires as an input the new participants, where each name can be followed by strings
which can mean research groups (the code will penalize rooms with people belonging
to the same group). You need to save today's data as YY_MM_DD.txt and in the same folder as this file and the script will find it.

usage: python3.8 IBCC_rooms.py
"""

import numpy as np
import itertools
from more_itertools import set_partitions
from collections import defaultdict
from sys import stdin
from datetime import date


def calculate_cost_match(name1, name2):
    same_group_cost = 0
    for entry in res_group_log[name1]:
        if entry in res_group_log[name2]:
            same_group_cost += 0.5
    return log_past_matches[name1].count(name2)+same_group_cost

def calculate_cost_room(list_of_names):
    cost = 0.
    combinations = list(itertools.combinations(list_of_names, 2))
    for pair in combinations:
        cost+= calculate_cost_match(pair[0], pair[1])
    return cost

def calculate_total_cost(matches):
    all_costs = []
    tot_cost = 0.
    for room in matches:
        cost = calculate_cost_room(room)
        tot_cost+= cost
        all_costs.append(cost)
    return tot_cost, all_costs


filename = "database.txt"
with open(filename, "r") as f:
    data = f.readlines()

log_past_matches = defaultdict(list)
for line in data:
    names = [x.replace('\n', "") for x in line.split(", ")]
    for name in names:
        for name2 in names:
            log_past_matches[name].append(name2)

res_group_log = defaultdict(list)


filename_today = str(date.today()).replace("-", "_")[2:] + ".txt"

try:
    with open(filename_today, "r") as f:
        data_today = f.readlines()
    print("Extracted data from the file {}\n".format(filename_today))
except:
    print("File {} not found.".format(filename_today))
    filename_today = input("Please type the filename with the names for today:\n")
    print(filename_today)
    with open(filename_today, "r") as f:
        data_today = f.readlines()


todays_people = []

for line in data_today:
    l = line.replace('\n', "").split(", ")
    person, res_group = l[0], l[1:]
    todays_people.append(person)
    for r in res_group:
        res_group_log[person].append(r)

N_people = len(todays_people)

def print_people(dct):
    string = ""
    for person in dct.keys():
        string +=  "\n" + person + " (" + ', '.join(dct[person]) + ")"
    return string

print("Today we have {} people: {}\n".format(N_people, print_people(res_group_log)))


group_size = [2,3]
n_groups = N_people//group_size[-1]
mod = N_people%group_size[-1]
if mod !=0:
    a = 1
else:
    a = 0

possible_rooms = []
costs_per_solution = []

for part in set_partitions(todays_people, n_groups+a):
    t = part
    if any([len(r) not in group_size for r in t]):
        # print("skipped:", t)
        pass
    else:
        possible_rooms.append(t)
        # print("added:", t)

min_cost = 1000
ideal_part = None
max_individual_costs = 0.
for room_list in possible_rooms:
    cost_rooms, individual_costs = calculate_total_cost(room_list)
    if cost_rooms<min_cost:
        min_cost = cost_rooms
        ideal_part = [room_list]
        max_individual_costs = max(individual_costs)
    elif cost_rooms == min_cost:
        if max(individual_costs) == max_individual_costs:
            ideal_part.append(room_list)
        elif max(individual_costs) < max_individual_costs:
            min_cost = cost_rooms
            ideal_part = [room_list]
            max_individual_costs = max(individual_costs)

print("Number of possible combinations: {}, number of minimum cost (= {}, max ind cost = {}) combinations: {}".format(len(possible_rooms), min_cost, max_individual_costs, len(ideal_part)))

for i,part in enumerate(ideal_part):
    print(i, part)

if i > 0:
    print("Picking a random combination!\n")
    ind = np.random.randint(0, i)
    selected = ideal_part[ind]
else:
    selected = ideal_part[0]

for n,room in enumerate(selected):
    print("Room {} \n{}\n".format(n+1, ('\n').join(room)))


val = input("Confirm rooms? (press 'y' and the current rooms will be added to the database)\n")
if val == "y":
    print("printing the rooms to the {} file...".format(filename))
    with open(filename, "a") as f:
        for room in selected:
            f.write("\n"+", ".join(room))
    print("Done.")
