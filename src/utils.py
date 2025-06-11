import pulp as pp


import os
from typing import List

def cleanShell() -> None:

    """Limpa o terminal, usando o comando clear referente ao SO
    
    """

    os.system("cls" if os.sys.platform.startswith("win") else "clear")

def showResults(variables: List[pp.LpVariable], optimal: float) -> str:

    """Mostra o nome das variáveis e seus respectivos valores e a solução ótima

    Parameters
    ----------
    variables : List[pulp.LpVariable]
        Variáveis contendo informações do nome e do valor
    optimal : float
        Solução ótima da função objetivo 
    
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
    
    return content


