"""
Utility Functions

"""
from typing import List


def ptable(data : List[List], sep : str = "\t"):
    """
    Pretty-prints a table
    """
    # The max length of column i
    cmax = [0 for i in range(len(data))]
    for row in data:
        for i, m in enumerate(cmax):
            cmax[i] = max(m, len(row[i]))

    for row in data:
        cells = [row[i].ljust(cmax[i]) for i in range(len(ro))]
        print(sep.join(cells))
            
                
