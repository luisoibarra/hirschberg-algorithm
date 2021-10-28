import numpy as np
from typing import Callable, List, Tuple

def needleman_wunsch_space_efficient(str1: str, str2: str, fun_cost: Callable[[str,str],float], gap_cost: float)-> List[float]:
    """
    # Algoritmo de Needleman-Wunsch.  
    
    Calcula la distancia de Needleman–Wunsch devolviendo la última fila de la matriz de cálculo
    usando solo dos filas para las operaciones. Para saber el resultado final indexar el resultado
    en el último índice.
    """
    score = np.zeros((2,len(str2)+1))
    # Caso base, cadena vacía con str2: Se inserta la letra correspondiente
    for j in range(1, len(str2)+1): 
        score[0,j] = score[0,j-1] + gap_cost
    for i in range(1, len(str1)+1):
        # Se calcula el primer elemento a partir de la fila anterior
        score[1,0] = score[0,0] + gap_cost
        for j in range(1, len(str2)+1):
            sub_score = score[0, j-1] + fun_cost(str1[i-1], str2[j-1]) # Copiar/Subst
            del_score = score[0, j] + gap_cost # Borrar
            ins_score = score[1, j-1] + gap_cost # Insertar
            score[1,j] = max(sub_score, del_score, ins_score)
        score[0,:] = score[1,:] # Copia la fila de abajo para la primera posición para ahorar espacio
    return score[1]

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

def hirschberg(str1: str, str2: str, cost_fun: Callable[[str,str],float], gap_cost:float) -> Tuple[float,str,str]:
    """
    # Algoritmo de Hirschberg.  
    
    Devuelve el costo y la alineación global de `str1` y `str2` que maximiza 
    la función de costo `cost_fun` con un coste de hueco de `gap_cost`.
    """
    upper_transcription = ""
    lower_transcription = ""
    cost = 0
    # En caso de que sea el str1 vacío sería llenar de huecos la primera transcripción
    if len(str1) == 0: 
        upper_transcription = '-'*len(str2)
        lower_transcription = str2
        return gap_cost*len(str2), upper_transcription, lower_transcription
    # En caso de que sea el str2 vacío sería llenar de huecos la segunda transcripción
    if len(str2) == 0:
        upper_transcription = str1
        lower_transcription = '-'*len(str1)
        return gap_cost*len(str1), upper_transcription, lower_transcription
    # Si uno de los dos tiene tamaño 1 el algoritmo NW realiza el trabajo con la complejidad espacial requerida
    if len(str1) == 1 or len(str2) == 1:
        cost,upper_transcription,lower_transcription = needleman_wunsch(str1, str2, cost_fun, gap_cost)
    else:
        middle_1 = len(str1)//2
        left_score = needleman_wunsch_space_efficient(str1[:middle_1], str2, cost_fun, gap_cost)
        right_score = needleman_wunsch_space_efficient(str1[middle_1:][::-1], str2[::-1], cost_fun, gap_cost)
        middle_2,_ = max([x for x in enumerate(left_score+right_score[::-1])],key=lambda x: x[1])

        cost_l,upper_transcription_l,lower_transcription_l = \
            hirschberg(str1[:middle_1], str2[:middle_2], cost_fun, gap_cost)
        cost_r,upper_transcription_r,lower_transcription_r = \
            hirschberg(str1[middle_1:], str2[middle_2:], cost_fun, gap_cost)

        # Uniendo resultados
        cost = cost_l + cost_r
        upper_transcription = upper_transcription_l + upper_transcription_r
        lower_transcription = lower_transcription_l + lower_transcription_r
    return cost, upper_transcription, lower_transcription

def longest_common_subsequence(str1: str, str2: str) -> str:
    """
    # Subsecuencia común más larga (LCS)
    
    Devuelve una LCS partiendo del algoritmo de Hirschberg.
    """
    x = hirschberg(str1, str2, lambda x,y: 1 if x==y else 0, 0)
    cost, trans1, trans2 = x
    lcs = ""
    for i,j in zip(trans1, trans2):
        lcs += i if i == j else ""
    return lcs
    
def levenshtein(str1: str, str2: str) -> Tuple[float,str]:
    """
    # Distancia de Levenshtein
    
    Devualve la distancia de Levenshtein y la transcripción de la 
    cadena partiendo del algoritmo de Hirschberg.  
    """
    
    x = hirschberg(str1, str2, lambda x,y: 0 if x==y else -1, -1)
    cost, trans1, trans2 = x
    transc = ""
    for i,j in zip(trans1, trans2):
        if i == '-':
            transc += 'd'
        elif j=='-':
            transc += 'i'
        elif i == j:
            transc += 'c'
        else:
            transc += 's'
    return -cost, transc

cost_matrix = {
    ("A","A"): 10,
    ("A","G"): -1, 
    ("A","C"): -3, 
    ("A","T"): -4, 
    ("G","A"): -1, 
    ("G","G"): 7, 
    ("G","C"): -5, 
    ("G","T"): -3, 
    ("C","A"): -3, 
    ("C","G"): -3, 
    ("C","C"): 9, 
    ("C","T"): 0, 
    ("T","A"): -4, 
    ("T","G"): -3, 
    ("T","C"): 0, 
    ("T","T"): 8, 
}

fun_cost = lambda x,y: cost_matrix[x,y]

gap_cost = -5

data_set = [
    ("AGTACGCA","TATGC", lambda x,y: 2 if x==y else -1, -2),
    ("","AGACTAGTTAC",fun_cost,gap_cost),
    ("CGAGACGT","",fun_cost,gap_cost),
    ("CGAGACGT","A",fun_cost,gap_cost),
    ("A","CGAGACGT",fun_cost,gap_cost),
    ("CGAGACGT","AGACTAGTTAC",fun_cost,gap_cost),
    ("AGACTAGTTAC","CGAGACGT",fun_cost,gap_cost),
]


def print_results(result):
    cost, trans1, trans2 = result
    print("Costo:", cost)
    print("Transición")
    up = ""
    middle = ""
    down = ""
    for x,y in zip(trans1, trans2):
        up += x
        middle += "|" if x==y else " "
        down += y
    print(up)
    print(middle)
    print(down)

def main():
    for x in data_set:
        print("Original NW")
        print_results(needleman_wunsch(*x))
        print()
        print("Hirschberg")
        print_results(hirschberg(*x))


levenshtein("sitting","kitten") # 3
levenshtein("asfsdfasdsdvdsavadvvfevaevavfassaf","hmssbavdvADfabadvsdvzvdDsaagf") # 23