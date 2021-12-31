from hirschberg import hirschberg
from utils import load_data, time_it

def lcs_hirschberg(str1: str, str2: str) -> str:
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

def lcs(str1: str, str2: str) -> int:
    """
    # Subsecuencia común más larga (LCS)
    
    Devuelve la longitud de LCS partiendo del algoritmo clásico de programación dinámica.
    """
    m = len(str1)
    n = len(str2)
  
    L = [[None]*(n + 1) for i in range(m + 1)]
  
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif str1[i-1] == str2[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    return L[m][n]

def test_lcs():
    data = load_data()
    lcs_hirschberg_time = time_it(lcs_hirschberg)
    lcs_time = time_it(lcs)
    tests_results = []
    for n in data:
        str1,str2 = data[n]
        lcs_str, lcs_h_time = lcs_hirschberg_time(str1, str2)
        lcs_length, lcs_no_h_time = lcs_time(str1, str2)
        # Parrafos, Longitud Str1, Lngitud Str2, Resultado Heirschberg, Tiempo Heirschberg, Resultado No Heirschberg, Tiempo No Heirschberg
        tests_results.append((n, len(str1), len(str2), len(lcs_str), lcs_h_time, lcs_length, lcs_no_h_time))
    
    return tests_results

def user_interaction_lcs():
    print("Comparando algoritmo LCS")
    print()
    str1 = input("Escriba la primera cadena: ")
    str2 = input("Escriba la segunda cadena: ")
    lcs_hirschberg_time = time_it(lcs_hirschberg)
    lcs_time = time_it(lcs)
    lcs_str, lcs_h_time = lcs_hirschberg_time(str1, str2)
    lcs_length, lcs_no_h_time = lcs_time(str1, str2)
    print("La subsecuencia común más larga fue:", lcs_str)
    print("Con una longitud de:", lcs_length)
    print("Los tiempos de los algoritmos fueron:")
    print("LCS (Hirscherg):", lcs_h_time)
    print("LCS:", lcs_no_h_time)

if __name__ == '__main__':
    test_lcs()