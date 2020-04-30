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
            yield (ident, int(degree), what, 32.*float(value))


def plotting(what=None, filename=None, gflops=False, mdofs=False, title="Insert title here", doubleaxis=False):
    assert gflops or mdofs
    assert not (gflops and mdofs)

    fig, ax1 = plt.subplots()
    if doubleaxis:
        ax2 = ax1.twinx()


    def dataset(ax, horizontal, linestyle="-", color="b", dotstyle="o", label="Set label!", func=lambda x: x):
        csvfile = "./floprates.csv" if gflops else "./doftimes.csv"
        frame = pandas.DataFrame(handle(csvfile, "h{}.*".format(horizontal)), columns=("exec", "degree", "what", "value"))
        frame = frame[frame.what == what]

        x, y = list(zip(*sorted(zip(frame['degree'], frame['value']))))
        y = [func(i) for i in y]
        ax.plot(x, y, "{}{}{}".format(color, linestyle, dotstyle), label=label)


    # Trigger the individual plots
    dataset(ax1, 4, linestyle="-", color="b", dotstyle="o", label="fusion")
    dataset(ax1, 2, linestyle="-.", color="g", dotstyle="v", label="hybrid")
    dataset(ax1, 1, linestyle=":", color="r", dotstyle="s", label="splitting")

    # Add legends and labels and such
    ax1.set_ylim(bottom=0)
    ax1.set_xlabel("Polynomial degree", fontsize=18)
    ax1.set_ylabel("GFlops/s" if gflops else "MDoF/s", fontsize=18)

    if doubleaxis:
        dataset(ax2, 4, linestyle="-", color="b", dotstyle="o", label="fusion", func=lambda x : x/11.7)
        dataset(ax2, 2, linestyle="-.", color="g", dotstyle="v", label="hybrid", func=lambda x : x/11.7)
        dataset(ax2, 1, linestyle=":", color="r", dotstyle="s", label="splitting", func=lambda x : x/11.7)

        # Add legends and labels and such
        ax2.set_ylim(bottom=0)
        ax2.set_ylabel("% of peak performance", fontsize=18)

    plt.title(title, fontsize=18)
    plt.legend()

    plt.savefig(filename)
    plt.gcf().clear()


plotting(what="apply_jacobian",
         filename="haswell_poisson_gflops",
         gflops=True,
         title="Diffusion-reaction DG on Haswell - Full Operator",
         doubleaxis=True,
         )


plotting(what="apply_jacobian",
         filename="haswell_poisson_mdofs",
         mdofs=True,
         title="Diffusion-reaction DG on Haswell - Full Operator",
         )

plotting(what="jacobian_apply_volume_kernel",
         filename="haswell_poisson_volume_gflops",
         gflops=True,
         title="Diffusion-reaction DG on Haswell - Volumes",
         doubleaxis=True,
         )

plotting(what="jacobian_apply_volume_kernel",
         filename="haswell_poisson_volume_mdofs",
         mdofs=True,
         title="Diffusion-reaction DG on Haswell - Volumes",
         )

plotting(what="jacobian_apply_skeleton_kernel",
         filename="haswell_poisson_skeleton_gflops",
         gflops=True,
         title="Diffusion-reaction DG on Haswell - Facets",
         doubleaxis=True,
         )

plotting(what="jacobian_apply_skeleton_kernel",
         filename="haswell_poisson_skeleton_mdofs",
         mdofs=True,
         title="Diffusion-reaction DG on Haswell - Facets",
         )
