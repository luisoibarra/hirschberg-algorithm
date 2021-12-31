import os
from typing import Dict, Tuple
import time

def load_data(directory:str=None) -> Dict[int,Tuple[str,str]]:
    """
    Devuelve el conjunto de datos guardado en `directory`

    El formato de los datos es el siguiente:

    Numero1
    String11  
    String12
    Numero2
    String21  
    String22
    ...
    """
    if directory is None:
        directory = os.path.join(os.path.dirname(__file__) ,"data", "strings.txt")
    
    data = {}
    raw_data = ""
    
    with open(directory) as file:
        raw_data = file.read()
    
    data_lines = [x for x in raw_data.splitlines() if x]
    
    for i in range(0, len(data_lines), 3):
        number_of_paragraphs = int(data_lines[i])
        str1 = data_lines[i+1]
        str2 = data_lines[i+2]
        data[number_of_paragraphs] = (str1, str2)
    
    return data

def time_it(fun):
    """
    Devuelve el resultado de la función y el tiempo que se demoró la ejecución de esta
    """
    def f(*args, **kwargs):
        init = time.time()
        value = fun(*args, **kwargs)
        delta = time.time() - init
        return value, delta
    return f