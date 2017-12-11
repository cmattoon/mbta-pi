"""
Utility Functions

"""
from typing import List


def ptable(data : List[List], sep : str = "\t", sort_by : int = None):
    """
    Pretty-prints a table
    """
    if sort_by is not None:
        data.sort(key=lambda x: x[sort_by])
        
    # The max length of column i
    cmax = [0 for i in range(len(data[0]))]
    for row in data:
        for i, m in enumerate(cmax):
            cmax[i] = max(m, len(str(row[i])))

    for row in data:
        cells = ["{}".format(row[i]).ljust(cmax[i]) for i in range(len(row))]
        print(sep.join(cells))
            
                
