#!/usr/bin/env python

import itertools
import pandas
import matplotlib
import re
import sys

matplotlib.use("PDF")

from matplotlib import pyplot as plt


def handle(filename, pattern):
    f = open(filename, "r")
    for line in f:
        if re.match(pattern, line):
            ident, degree, what, value = line.split()
            if int(degree) < 8:
            	yield (ident, int(degree), what, 32.*float(value))


def plotting(what=None, labels=None, filename=None, gflops=False, mdofs=False, title="Insert title here", doubleaxis=False):
    assert gflops or mdofs
    assert not (gflops and mdofs)

    fig, ax1 = plt.subplots()
    if doubleaxis:
        ax2 = ax1.twinx()

    def dataset(ax, w, linestyle="-", color="b", dotstyle="o", label="Set label!", func=lambda x: x):
        csvfile = "./floprates.csv" if gflops else "./doftimes.csv"
        frame = pandas.DataFrame(handle(csvfile, ".*"), columns=("exec", "degree", "what", "value"))
        frame = frame[frame.what == w]

        x, y = list(zip(*sorted(zip(frame['degree'], frame['value']))))
        y = [func(i) for i in y]
        ax.plot(x, y, "{}{}{}".format(color, linestyle, dotstyle), label=label)


    # Trigger the individual plots
    for w, l, c, d, label in zip(what, ("-", "-.", ":"), "bgr", "ovs", labels):
        dataset(ax1, w, linestyle=l, color=c, dotstyle=d, label=label)

    # Add legends and labels and such
    ax1.set_ylim(bottom=0)
    ax1.set_xlabel("Polynomial degree", fontsize=18)
    ax1.set_ylabel("GFlops/s" if gflops else "MDoF/s", fontsize=18)

    if doubleaxis:    
        for w, l, c, d, label in zip(what, ("-", "-.", ":"), "bgr", "ovs", labels):
            dataset(ax2, w, linestyle=l, color=c, dotstyle=d, label=label, func=lambda x: x/11.7)

        ax2.set_ylim(bottom=0)
        ax2.set_ylabel("% of peak performance", fontsize=18)

    plt.title(title, fontsize=18)
    plt.legend()

    plt.savefig(filename)
    plt.gcf().clear()


plotting(what=("apply_jacobian", "jacobian_apply_volume_kernel", "jacobian_apply_skeleton_kernel"),
         labels=("Operator Application", "Volume Integrals", "Skeleton integrals"),
         filename="haswell_stokes_gflops",
         gflops=True,
         title="Stokes DG on Haswell",
         doubleaxis=True,
         )


plotting(what=("apply_jacobian", "jacobian_apply_volume_kernel", "jacobian_apply_skeleton_kernel"),
         labels=("Operator Application", "Volume Integrals", "Skeleton integrals"),
         filename="haswell_stokes_mdofs",
         mdofs=True,
         title="Stokes DG on Haswell",
         )
