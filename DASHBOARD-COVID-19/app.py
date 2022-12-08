#################################################################################
# -= PACOTES UTILIZADOS =- #

# Carga, manipulação e operação com matrizes de dados
import json
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

# Carga dos dados
df_states = pd.read_csv("https://raw.githubusercontent.com/asimov-academy/Dashboards/main/dashboard-covid-19/df_states.csv")
df_brasil = pd.read_csv("https://raw.githubusercontent.com/asimov-academy/Dashboards/main/dashboard-covid-19/df_brasil.csv")
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

df_states_ = df_states[df_states["data"] == "2020-05-13"]
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}


#################################################################################
# -= GRÁFICOS =- #

# Gráfico de mapa
fig = px.choropleth_mapbox(
    data_frame=df_states_, locations="estado", color="casosNovos", geojson=brazil_states, 
    color_continuous_scale="Redor", opacity=0.4, hover_data={"casosAcumulado": True, 
    "casosNovos": True, "obitosNovos": True, "estado": True}, center={"lat": -16.95, "lon": -47.78}
)


#################################################################################
# -= LAYOUT DO DASHBOARD =- #

# Instanciando o Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Criando Layout
app.layout = dbc.Container(children=[



], fluid=True, style={"height": "100%"})


#################################################################################
# -= CALLBACKS =- #


#################################################################################
# -= END =- #
if __name__ == "__main__":
    app.run_server(debug=True)