from hirschberg import user_interaction_hirschberg, test_hirschberg
from lcs import user_interaction_lcs, test_lcs
from levenshtein import user_interaction_levenshtein, test_levenshtein

def main():
    option_action = {
        "1": user_interaction_hirschberg,
        "2": user_interaction_levenshtein,
        "3": user_interaction_lcs
    }
    print("Introduzca el valor de lo que quiere hacer:")
    print("1: Comparar Hirschberg con Needleman-Wunsch")
    print("2: Comparar Levenshtein basado en Hirschberg con el clásico de DP")
    print("3: Comparar LCS basado en Hirschberg con el clásico de DP")
    print("Presione Ctrl+C para salir")
    while True:
        action = input("Acción a realizar: ")
        try:
            action = option_action[action]
            action()
        except Exception as ex:
            print("Ocurrió un error:")
            print(ex)
            print("Presione Ctrl+C para salir")

def run_comp():
    lcs_results = test_lcs()
    lev_results = test_levenshtein()
    hirs_results = test_hirschberg()

    def print_results(long, str_len1, str_len2, h_res, h_time, res, time):
        print("Longitud de la cadena de entrada 1:", str_len1)
        print("Longitud de la cadena de entrada 2:", str_len2)
        print("Resultado con la variante con Hirschberg:", h_res)
        print("Demora con la variante con Hirschberg:", h_time)
        print("Resultado sin la variante con Hirschberg:", res)
        print("Demora sin la variante con Hirschberg:", time)
        print()

    print("Algoritmo de LCS")
    print()
    for x in lcs_results:
        print_results(*x)

    print("Algoritmo de Levenstein")
    print()
    for x in lev_results:
        print_results(*x)

    print("Algoritmo de Hirschberg con Needleman-Wunsch")
    print()
    for x in hirs_results:
        print_results(*x)

if __name__ == "__main__":
    # run_comp()
    main()