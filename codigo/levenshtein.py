from typing import Tuple
from hirschberg import hirschberg
from utils import load_data, time_it

def levenshtein_hirschberg(str1: str, str2: str) -> Tuple[float,str]:
    """
    # Distancia de Levenshtein
    
    Devuelve la distancia de Levenshtein y la transcripción de la 
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

def levenshtein(str1: str, str2: str) -> int:
    """ 
    # Distancia de Levenshtein
    
    Devuelve la distancia de Levenshtein mediante el algoritmo clásico de 
    programación dinámica.
    """

    rows = len(str1)+1
    cols = len(str2)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    # Caso base
    for i in range(1, rows):
        dist[i][0] = i

    # Caso base
    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if str1[row-1] == str2[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # Borrar
                                 dist[row][col-1] + 1,      # Insertar
                                 dist[row-1][col-1] + cost) # Substituir

    return dist[row][col]

def test_levenshtein():
    data = load_data()
    levenshtein_hirschberg_time = time_it(levenshtein_hirschberg)
    levenshtein_time = time_it(levenshtein)
    tests_results = []
    for n in data:
        str1,str2 = data[n]
        (levenshtein_dist_h,_), levenshtein_h_time = levenshtein_hirschberg_time(str1, str2)
        levenshtein_dist, levenshtein_no_h_time = levenshtein_time(str1, str2)
        # Parrafos, Longitud Str1, Lngitud Str2, Resultado Heirschberg, Tiempo Heirschberg, Resultado No Heirschberg, Tiempo No Heirschberg
        tests_results.append((n, len(str1), len(str2), levenshtein_dist_h, levenshtein_h_time, levenshtein_dist, levenshtein_no_h_time))
    
    return tests_results

def user_interaction_levenshtein():
    print("Comparando algoritmo Levenshtein")
    print()
    str1 = input("Escriba la primera cadena: ")
    str2 = input("Escriba la segunda cadena: ")
    levenshtein_hirschberg_time = time_it(levenshtein_hirschberg)
    levenshtein_time = time_it(levenshtein)
    (_, lev_transcription), lcs_h_time = levenshtein_hirschberg_time(str1, str2)
    lcs_length, lcs_no_h_time = levenshtein_time(str1, str2)
    print("La transcripción fue:", lev_transcription)
    print("La distancia de Levenshtein es:", lcs_length)
    print("Los tiempos de los algoritmos fueron:")
    print("Levenshtein (Hirscherg):", lcs_h_time)
    print("Levenshtein:", lcs_no_h_time)

if __name__ == '__main__':
    test_levenshtein()