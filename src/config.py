import os

PROJECT_DIRPATH = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIRPATH = os.path.join(
    PROJECT_DIRPATH,
    "data"
)

PROFISSIONALS_FILEPATH = os.path.join(
    DATA_DIRPATH,
    "dados_profissionais.csv"
)

DAYS_WEEK_FILEPATH = os.path.join(
    DATA_DIRPATH,
    "dados_dias_semana.csv"
)

SHIFT_FILEPATH = os.path.join(
    DATA_DIRPATH,
    "dados_turnos.csv"
)