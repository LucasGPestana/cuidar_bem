import pulp as pp


import os
from typing import List

def cleanShell() -> None:

    """Limpa o terminal, usando o comando clear referente ao SO
    
    """

    os.system("cls" if os.sys.platform.startswith("win") else "clear")

def showResults(variables: List[pp.LpVariable], optimal: float, slack_variables_values: List[float]) -> str:

    """Mostra o nome das variáveis e seus respectivos valores, a solução ótima e as variáveis de folga

    Parameters
    ----------
    variables : List[pulp.LpVariable]
        Variáveis contendo informações do nome e do valor
    optimal : float
        Solução ótima da função objetivo 
    slack_variables_values : List[float]
        Valores das variáveis de folga
    
    Returns
    -------
    str
        Saída estruturada contendo as informações
    
    """

    content = ""

    content += f"{'Nome':<10} | {'Valor':>7}\n"

    for variable in variables:

        content += f"{variable.getName():<10} | {variable.value():7.0f}\n"
    
    content += f"Solução Ótima: {optimal:.0f}\n"

    content += "Variáveis de Folga\n"
    
    for i, value in enumerate(slack_variables_values, start=1):

        content += f"S{i}: {value}\n"
    
    return content


