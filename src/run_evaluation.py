import sys, getopt
import matplotlib.pyplot as plt
from bad_luck_metric import evaluate_metric

def main():
    #init league with your own league ID, year, cookies here
    #see readme to find these values yourself
    id_val = -1
    year_val = -1
    s2_val = ''
    swid_val = ''

    try:
        ptiles, fig, ax = evaluate_metric(id_val, year_val, s2_val, swid_val)
        #print percentiles
        for p in ptiles:
            print(p)
        #show graph
        plt.show()
    except Exception:
        print('Evaluation failed. Check the README to ensure your values are valid')

if __name__ == "__main__":
    main()