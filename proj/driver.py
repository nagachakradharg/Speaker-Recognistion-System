import sys
from markov import identify_speaker
import pathlib

if __name__ == "__main__":
    """
    Driver for the speaker recognition system which prints result output

    Implementation:
    python proj/driver.py <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>

    Inputs(from command line):
        FilenameA: Speaker A speech file to create model
        FilenameB: Speaker B speech file to create model
        FilenameC: Speech string file to identify the speaker
        k: Order k
        hashtable-or-dict: string indicating which implementation to use
    """
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # open files & read text
    fileA = pathlib.Path(__file__).parent / filenameA
    fileB = pathlib.Path(__file__).parent / filenameB
    fileC = pathlib.Path(__file__).parent / filenameC

    # call identify_speaker
    use_hashtable = True if hashtable_or_dict == "hashtable" else False
    probA, probB, result = identify_speaker(fileA.read_text(), fileB.read_text(), fileC.read_text(), k, use_hashtable=use_hashtable)

    # Output the results
    print(f"Speaker A: {probA}")
    print(f"Speaker B: {probB}")
    print(f"\nConclusion: Speaker {result} is most likely")
