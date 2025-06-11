import pulp as pp
import pandas as pd


import re
from typing import List, Tuple


from src.config import (
    PROFISSIONALS_FILEPATH,
    DAYS_WEEK_FILEPATH,
    SHIFT_FILEPATH
)
from src.utils import cleanShell


class ProfProblemSolver:

    """Representa um solucionador de problema de otimização de profissionais"""

    @staticmethod
    def organizeData(*filepaths, merge_columns: List[str]) -> pd.DataFrame:

        """Organiza todos os dados do problema em um DataFrame do pandas

        Parameters
        ----------
        *filepaths : str
            Caminhos dos arquivos csv contendo os dados
        
        merge_columns : List[str]
            Colunas para fazer a junção dos dados. O tamanho da lista precisa ser n-1, em que 'n' é o número de caminhos passados em *filepaths
        
        Returns
        -------
        pandas.DataFrame
            Estrutura com os dados juntos

        """

        dfs = []
        
        # Dados
        for filepath in filepaths:

            dfs.append(pd.read_csv(filepath))
        
        if len(merge_columns) >= 1:

            df = dfs[0].merge(
                dfs[1], 
                how="inner",
                on=merge_columns[0]
            )

        # Juntando todos os dados em um único dataframe
        for i, merge_column in enumerate(merge_columns[1:], start=2):

            df = df.merge(
                dfs[i],
                how="inner",
                on=merge_column
            )
        
        return df
    
    def buildModel() -> pp.LpProblem:

        """Constroi o modelo do problema

        Returns
        -------
        pulp.LpProblem
            Problema com a função objetivo, variáveis de decisão e as restrições
        
        Variáveis de decisão: x_{p}_{d}_{t}
            - p ∈ df["profissional"].unique
            - d ∈ df["dia"].unique
            - t ∈ df["turno"].unique
        Função objetivo: max z = ∑ x_p_d_t
        Restrição 1 - Demanda para cada dia da semana
            x_p_d_t <= demanda dia da semana
        Restrição 2 - Demanda para cada turno
            x_p_d_t <= demanda turno
        Restrição 3 - Tempo de trabalho dos profissionais
            tempo_medio_servico (min) * x_p_d_t <= tempo_expediente (h) * 60

        """

        df = ProfProblemSolver.organizeData(
            PROFISSIONALS_FILEPATH,
            DAYS_WEEK_FILEPATH,
            SHIFT_FILEPATH,
            merge_columns=["dia", "turno"]
            )
        
        # Padrões de expressão regular para obter partes do nome das variáveis
        profissional_pattern = re.compile(r"\d(?=_\d_[M|T|N])")
        day_week_pattern = re.compile(r"(?<=x_\d_)\d(?=_[M|T|N])")
        shift_pattern = re.compile(r"(?<=x_\d_\d_)[M|T|N]")


        # Definição do problema
        problem = pp.LpProblem("Otimização de profissionais", pp.LpMaximize)

        # Variáveis de decisão
        # x_{p}_{d}_{t}
        variables = [
            pp.LpVariable(f"x_{df['profissional'][index]}_{df['dia'][index]}_{df['turno'][index]}", lowBound=0, cat="Integer")
            for index in df.index
            ]

        # Função objetivo
        # max z = ∑ x_p_d_t
        # p ∈ df["profissional"].unique
        # d ∈ df["dia"].unique
        # t ∈ df["turno"].unique
        problem += pp.lpSum(sum(variables))

        # Restrição 1 - Demanda para cada dia da semana
        # x_p_d_t <= demanda dia da semana
        for day_week in sorted(df["dia"].unique()):

            demand = df[df["dia"] == day_week]["demanda_x"].values[0]

            context_variables = list(
                filter(
                    lambda x: str(day_week) == day_week_pattern.search(x.getName()).group(), 
                    variables
                    )
                    )

            for variable in context_variables:

                problem += pp.lpSum(variable) <= demand

        # Restrição 2 - Demanda para cada turno
        # x_p_d_t <= demanda turno
        for shift in df["turno"].unique():

            demand = df[df["turno"] == shift]["demanda_y"].values[0]

            shift_pattern = re.compile(r"(?<=x_\d_\d_)[M|T|N]")

            context_variables = list(
                filter(
                    lambda x: str(shift) == shift_pattern.search(x.getName()).group(), 
                    variables
                    )
                    )

            for variable in context_variables:

                problem += pp.lpSum(variable) <= demand

        # Restrição 3 - Tempo de trabalho dos profissionais
        # tempo_medio_servico (min) * x_p_d_t <= tempo_expediente (h) * 60
        for index in df.index:

            p = df["profissional"][index]
            d = df["dia"][index]
            t = df["turno"][index]
            mean_time_service = df["tempo_medio_atendimento"][index]
            office_hours = df["tempo_expediente"][index]

            context_variable = list(
                filter(
                    lambda x: x.getName() == f"x_{p}_{d}_{t}", 
                    variables
                    )
                    )[0]

            problem += pp.lpSum(mean_time_service * context_variable) <= office_hours * 60
        
        return problem
    
    def findOptimalSolution(problem: pp.LpProblem) -> Tuple[List[pp.LpVariable], float]:

        """Busca a solução ótima do problema passado como argumento

        Parameters
        ----------
        problem : pulp.LpProblem
            Problema que se deseja encontrar a solução ótima
        
        Returns
        -------
        List[pulp.LpVariable]
            Lista com as variáveis contendo seus respectivos valores da solução ótima
        float
            Solução ótima da função objetivo

        """

        problem.solve()

        cleanShell()

        return problem.variables(), problem.objective.value()