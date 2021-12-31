import numpy as np
from typing import Callable, List, Tuple
from needleman_wunsch import needleman_wunsch
from utils import load_data, time_it

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

def test_hirschberg():
    data = load_data()
    hirschberg_time = time_it(hirschberg)
    needleman_wunsch_time = time_it(needleman_wunsch)
    tests_results = []
    cost_fun, gap_cost = lambda x,y: 2 if x==y else -1, -2
    for n in data:
        str1,str2 = data[n]
        (hirschberg_val, _, _), hirschberg_actual_time = hirschberg_time(str1, str2, cost_fun, gap_cost)
        (needleman_wunsch_val, _, _), needleman_wunsch_actual_time = needleman_wunsch_time(str1, str2, cost_fun, gap_cost)
        # Parrafos, Longitud Str1, Lngitud Str2, Resultado Heirschberg, Tiempo Heirschberg, Resultado No Heirschberg, Tiempo No Heirschberg
        tests_results.append((n, len(str1), len(str2), hirschberg_val, hirschberg_actual_time, needleman_wunsch_val, needleman_wunsch_actual_time))
    
    return tests_results

def user_interaction_hirschberg():
    print("Comparando algoritmo Hirschberg y Needleman-Wunsch")
    print()
    str1 = input("Escriba la primera cadena: ")
    str2 = input("Escriba la segunda cadena: ")
    cost_fun, gap_cost = lambda x,y: 2 if x==y else -1, -2
    hirschberg_time = time_it(hirschberg)
    needleman_wunsch_time = time_it(needleman_wunsch)
    h, hirschberg_actual_time = hirschberg_time(str1, str2, cost_fun, gap_cost)
    n, needleman_wunsch_actual_time = needleman_wunsch_time(str1, str2, cost_fun, gap_cost)
    print("Resultados de Hirscherg")
    print_results(h)
    print("Resultados de Needleman-Wunsch")
    print_results(n)
    print("Los tiempos de los algoritmos fueron:")
    print("Hirscherg:", hirschberg_actual_time)
    print("Needleman-Wunsch:", needleman_wunsch_actual_time)

if __name__ == '__main__':
    test_hirschberg()