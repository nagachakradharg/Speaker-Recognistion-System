import pathlib
import sys
from markov import identify_speaker
import time
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import statistics

if __name__ == "__main__":
    """
    Runs performance tests and creates a graph comparing the performancwe of hashtable class and in-built dict

    Implementation:
    python proj/performance.py <filenameA> <filenameB> <filenameC> <max-k> <runs>

    Inputs(from command line):
        filenameA: speaker A speech file to create model
        filenameB: speaker B speech file to create model
        filenameC: speech string file to identify the speaker
        max_k: maximum value of k
        runs: number of performance runs
    """
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)
    frame = {'Implementation':[],
                 'K': [],
                 'Time': []}

    # open files & read text
    fileA = pathlib.Path(__file__).parent / filenameA
    fileB = pathlib.Path(__file__).parent / filenameB
    fileC = pathlib.Path(__file__).parent / filenameC

    # run performance tests
    for k in range(1, max_k + 1):
        for use_hashable in [True, False]:
            time_taken = []

            for run in range(runs):
                start = time.perf_counter()
                identify_speaker(fileA.read_text(), fileB.read_text(), fileC.read_text(), k, use_hashtable=use_hashable)
                time_taken.append(time.perf_counter() - start)

            # update each iteration statistics
            frame['Implementation'].append('hashtable' if use_hashable else 'dict')
            frame['K'].append(k)
            frame['Time'].append(statistics.mean(time_taken))

    table = pd.DataFrame({'Implementation' : pd.Series(frame['Implementation']),
                          'K': pd.Series(frame['K']),
                          f"Average Time (Runs={runs})": pd.Series(frame['Time'])})

    # save to execution_graph.png
    sb.pointplot(x="K", 
                y=f"Average Time (Runs={runs})",
                hue="Implementation",
                data=table,
                linestyles='-',
                markers='o')
    plt.grid(True)
    plt.savefig('execution_graph.png')