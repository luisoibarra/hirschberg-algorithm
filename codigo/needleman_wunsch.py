import numpy as np
from typing import Callable, List, Tuple

def needleman_wunsch(str1: str, str2: str, cost_fun: Callable[[str,str],float], gap_cost:float) -> Tuple[float,str,str]:
    """
    # Algoritmo de Needleman-Wunsch.  
    
    Devuelve el costo y la alineación global de `str1` y `str2` que maximiza 
    la función de costo `cost_fun` con un coste de hueco de `gap_cost`. 
    """
    nw = np.zeros((len(str1)+1,len(str2)+1))
    subs_dict = {}
    # Casos bases
    for i in range(1, len(str1)+1):
        nw[i,0] = nw[i-1,0] + gap_cost
        subs_dict[i,0] = (i-1,0,str1[i-1],'-')
    # Casos bases
    for j in range(1, len(str2)+1):
        nw[0,j] = nw[0,j-1] + gap_cost
        subs_dict[0,j] = (0,j-1,'-',str2[j-1])
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            nw[i,j],subst_str1,subst_str2,from_i, from_j = max(
                (nw[i-1,j-1] + cost_fun(str1[i-1], str2[j-1]), str1[i-1],str2[j-1],i-1,j-1),
                (nw[i-1,j] + gap_cost, str1[i-1],'-',i-1,j),
                (nw[i,j-1] + gap_cost, '-',str2[j-1],i,j-1),
                key=lambda x: x[0]
            )
            subs_dict[i,j] = (from_i, from_j, subst_str1, subst_str2)
    
    i,j = len(str1), len(str2)
    subs1 = ""
    subs2 = ""
    while i != 0 or j != 0:
        i, j, sub1, sub2 = subs_dict[i,j]
        subs1 = sub1 + subs1    
        subs2 = sub2 + subs2
    return nw[len(str1), len(str2)], subs1, subs2
