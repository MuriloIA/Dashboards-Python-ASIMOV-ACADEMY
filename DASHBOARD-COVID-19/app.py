#################################################################################
# -= PACOTES UTILIZADOS =- #

# Carga, manipulação e operação com matrizes de dados
import numpy as np
import pandas as pd

# Construção de Gráficos
import plotly.express as px
import plotly.graph_objects as go

# Layout do Dashboard
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output


#################################################################################
# -= CARGA E MANIPULAÇÃO DO CONJUNTO DE DADOS =- #


#################################################################################
# -= LAYOUT DO DASHBOARD =- #

# Instanciando o Dash
app = Dash(__name__)

# Criando Layout
app.layout = dbc.Container(children=[

], fluid=True, style={"height": "100%"})


#################################################################################
# -= CALLBACKS =- #


#################################################################################
# -= END =- #
if __name__ == "__main__":
    app.run_server(debug=True)