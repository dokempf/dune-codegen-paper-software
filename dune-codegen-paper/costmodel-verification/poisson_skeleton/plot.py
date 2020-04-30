#!/usr/bin/env python

import matplotlib
import csv

matplotlib.use("PDF")

from matplotlib import pyplot as plt

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams.update({'font.size': 22})

plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)

ident_to_cost = {}
ident_to_description = {}
ident_to_doftime = {}

reader = csv.reader(open("mapping.csv"),
                    delimiter=" ")
for line in reader:
    ident_to_cost[line[0]] = float(line[1])
    ident_to_description[line[0]] = line[2]
    
reader = csv.reader(open("doftimes.csv"),
                    delimiter=" ")
for line in reader:
    if line[2] == "residual_evaluation":
        ident_to_doftime[line[0]] = float(line[3]) * 32.
        
x = []
y = []
labels = []
distinct_costs = set(ident_to_cost.values())
for ident, cost in ident_to_cost.items():
    if cost in distinct_costs:
        x.append(cost)
        y.append(ident_to_doftime[ident])
        labels.append(ident_to_description[ident])
        distinct_costs.discard(cost)

plt.scatter(x,y)
plt.title("Cost model validation (skeleton)")
plt.xlabel("Cost model value")
plt.ylabel("MDoF/s")

plt.savefig("costmodel_poissonskeleton")
