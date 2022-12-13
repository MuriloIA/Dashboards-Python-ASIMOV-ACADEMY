######################################################################################################################
# -= PACOTES UTILIZADOS =-

# Importação, Manipulação e OPerações com matrizes de dados
import numpy as np
import pandas as pd

# Construção de gráficos interativos
import plotly.express as px
import plotly.graph_objects as go

# Construção do Dashboard
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output


######################################################################################################################
# -= CARGA E MANIPULAÇÃO DOS DADOS =-



######################################################################################################################
# -= LAYOUT DO DASHBOARD =-

# Instanciando o Dash
app = Dash(__name__)

# Criando layout
app.layout = dbc.Container(children=[



], fluid=True, style={"height": "100%"})

######################################################################################################################
# -= CALLBACKS =-


######################################################################################################################
# -= END =-
if __name__ == "__main__":
    app.run_server(debug=True)