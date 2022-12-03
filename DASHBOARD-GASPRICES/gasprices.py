#######################################################################################
# -= PACOTES UTILIZADOS =-

# Manipulação e operações com matrizes de dados
import numpy as np
import pandas as pd

# Construção de gráficos
import plotly.express as px
import plotly.graph_objects as go

# Ferramentas para a construção do Dashboard
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO


#######################################################################################
# -= CARGA E PRÉ-PROCESSAMENTO DOS DADOS =-

def load_data():

    """
        Carga e pré-processamento dos dados. 
            - Função não paramética.
    """

    # Carregando os dados em um DataFrame do Pandas
    url   = "https://raw.githubusercontent.com/asimov-academy/Dashboards/main/gas-prices-dash/data_gas.csv"
    dados = pd.read_csv(url)

    # Erro no nome da coluna
    dados.rename(columns={' DATA INICIAL': 'DATA INICIAL'}, inplace=True)

    # Estabelecendo datas, simplificando-as estabelecendo a ordem do DF por elas
    dados['DATA INICIAL'] = pd.to_datetime(dados['DATA INICIAL'])
    dados['DATA FINAL']   = pd.to_datetime(dados['DATA FINAL'])
    dados['DATA MEDIA']   = ((dados['DATA FINAL'] - dados['DATA INICIAL'])/2) + dados['DATA INICIAL']
    dados                 = dados.sort_values(by='DATA MEDIA',ascending=True)
    dados.rename(columns = {'DATA MEDIA':'DATA'}, inplace = True)
    dados.rename(columns = {'PREÇO MÉDIO REVENDA': 'VALOR REVENDA (R$/L)'}, inplace=True)

    # Criando uma coluna de Ano
    dados["ANO"] = dados["DATA"].apply(lambda x: str(x.year))

    # Resetando o index por uma questão organizacional
    dados = dados.reset_index()

    # Filtrando pois só falaremos da gasolina comum
    dados = dados[dados.PRODUTO == 'GASOLINA COMUM'] # ou podemos deixar todos os produtos e depois utilizar como um filtro geral !!!!

    # Excluindo colunas que não usaremos
    dados.drop(['UNIDADE DE MEDIDA', 'COEF DE VARIAÇÃO REVENDA', 'COEF DE VARIAÇÃO DISTRIBUIÇÃO', 
        'NÚMERO DE POSTOS PESQUISADOS', 'DATA INICIAL', 'DATA FINAL', 'PREÇO MÁXIMO DISTRIBUIÇÃO', 'PREÇO MÍNIMO DISTRIBUIÇÃO', 
        'DESVIO PADRÃO DISTRIBUIÇÃO', 'MARGEM MÉDIA REVENDA', 'PREÇO MÍNIMO REVENDA', 'PREÇO MÁXIMO REVENDA', 'DESVIO PADRÃO REVENDA', 
        'PRODUTO', 'PREÇO MÉDIO DISTRIBUIÇÃO'], inplace=True, axis=1)

    # Retornando os dados já organizados
    return dados

# Chamando a função load_data()
dados = load_data()

# Transformando o DataFrame em um dicionário
df_store = dados.to_dict()


#######################################################################################
# -= CONSTRUÇÃO DO LAYOUT DO DASHBOARD =-

# Definindo os parâmetros gerais para todos os gráficos com plotly
main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "y": 0.9,
        "xanchor": "left",
        "x": 0.1,
        "title": {"text": None},
        "font": {"color": "white"},
        "bgcolor": "rgba(0, 0, 0, 0.5)"},
    "margin": {"l": 0, "r": 0, "t": 10, "b": 0}
}

# Definindo um estilo para todos os cards
tab_card = {"height": "100%"}

# Definindo os temas opcionais para este projeto
template_theme1 = "flatly"
template_theme2 = "vapor"
theme1 = dbc.themes.FLATLY
theme2 = dbc.themes.VAPOR

# Importando Estilo css para os objetos do dash_bootstrap_components
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")

# Instanciando o Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css])

# Construção do Layout
app.layout = dbc.Container(children=[

    # Armazenando os Datasets do projeto
    dcc.Store(id="dataset", data=df_store),
    dcc.Store(id="dataset_fixed", data=df_store),

    # -= LINHA 1 =-
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend(children="Análise de Preços de Gás")
                        ], sm=8),
                        dbc.Col([
                            html.I(className="fa fa-gas-pump", style={"font-size": "300%"})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[theme1, theme2]),
                            html.Legend(children="Asimov Academy")
                        ])
                    ], style={"magin-top": "10px"}),
                    dbc.Row([
                        dbc.Button(children="Visite o Site", href="https://asimov.academy/", target="_blank")
                    ], style={"margin-top": "10px"})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3(children="Máximos e Mínimos"),
                            dcc.Graph(id="static_maxmin", config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ], style=tab_card)
        ], sm=8, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6(children="Ano de análise:"),
                            dcc.Dropdown(
                                id="select_ano",
                                value=dados.at[dados.index[3], 'ANO'],
                                clearable=False,
                                className="dbc",
                                options=[
                                    {"label": x, "value": x} for x in dados['ANO'].unique()
                                ]
                            )
                        ], sm=6),
                        dbc.Col([
                            html.H6(children="Região de análise"),
                            dcc.Dropdown(
                                id="select_regiao",
                                value=dados.at[dados.index[1], 'REGIÃO'],
                                clearable=False,
                                className="dbc",
                                options=[
                                    {"label": x, "value": x} for x in dados["REGIÃO"].unique()
                                ]
                            )
                        ], sm=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="regiaobar_graph", config={"displayModeBar": False, "showTips": False})
                        ], sm=12, md=6),
                        dbc.Col([
                            dcc.Graph(id="estadobar_graph", config={"displayModeBar": False, "showTips": False})
                        ], sm=12, md=6)
                    ], style={"column-gap": "0px"})
                ])
            ], style=tab_card)
        ], sm=12, lg=7)
    ], class_name="g-2 my-auto"),

    # -= LINHA 2 =- #
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(children="Preço x Estado"),
                    html.H6(children="Comparação temporal entre estados"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_estado0",
                                value=[dados.at[dados.index[3], 'ESTADO'], dados.at[dados.index[13], 'ESTADO'], dados.at[dados.index[6], 'ESTADO']],
                                clearable=False,
                                className="dbc",
                                multi=True,
                                options=[
                                    {"label": x, "value": x} for x in dados['ESTADO'].unique()
                                ]
                            )
                        ], sm=10)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="animation_graph", config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(children="Comparação Direta"),
                    html.H6(children="Qual preço é o menor em um dado período de tempo?"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_estado1",
                                value=dados.at[dados.index[3], "ESTADO"],
                                clearable=False,
                                className="dbc",
                                options=[
                                    {"label": x, "value": x} for x in dados["ESTADO"].unique()
                                ]
                            )
                        ], sm=10, md=5),
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_estado2",
                                value=dados.at[dados.index[1], "ESTADO"],
                                clearable=False,
                                className="dbc",
                                options=[
                                    {"label": x, "value": x} for x in dados["ESTADO"].unique()
                                ]
                            )
                        ], sm=10, md=6)
                    ], style={"margin-top": "20px"}, justify="center"),
                    dcc.Graph(id="direct_comparison_graph", config={"displayModeBar": False, "showTips": False}),
                    html.P(id="desc_comparison", style={"color": "gray", "font-size": "80%"})
                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id="card1_indicators", config={"displayModeBar": False, "showTips": False}, style={"margin-top": "30px"})
                        ])
                    ], style=tab_card)
                ])
            ], justify="center", style={"padding-bottom": "7px", "height": "50%"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id="card2_indicators", config={"displayModeBar": False, "showTips": False}, style={"margin-top": "30px"})
                        ])
                    ], style=tab_card)
                ])
            ], justify="center", style={"height": "50%"})
        ], sm=12, lg=3, style={"height": "100%"})
    ], class_name="g-2 my-auto"),

    # -= LINHA 3 =- #
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.RangeSlider(
                                id="rangeslider",
                                marks={int(x): f'{x}' for x in dados["ANO"].unique()},
                                step=3,
                                min=2004,
                                max=2021,
                                className="dbc",
                                value=[2004, 2021],
                                dots=True,
                                pushable=3,
                                tooltip={"always_visible": False, "placement": "bottom"}
                            )
                        ], sm=12, md=10, style={"margin-top": "15px"}),
                    ], style={"height": "20%", "justify-content": "center"})
                ])
            ], style=tab_card)
        ])
    ], class_name="g-2 my-auto")

], fluid=True, style={"height": "100%"})


#######################################################################################
# -= CALLBACKS =-

# Callback para o gráfico de Máximos e Mínimos
@app.callback(
    Output("static_maxmin", "figure"),
    [
        Input("dataset", "data"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    ]
)
def func(data, toggle):

    # Instanciando o template selecionado pelo usuário
    template = template_theme1 if toggle else template_theme2
    
    # Transformando o dicionário de dados em um DataFrame 
    df = pd.DataFrame(data)

    # Máximos e Mínimos por ano
    max = df.groupby(["ANO"])["VALOR REVENDA (R$/L)"].max()
    min = df.groupby(["ANO"])["VALOR REVENDA (R$/L)"].min()

    # Concatenando os dados de máximos e mínimos criados acima
    final_df = pd.concat([max, min], axis=1)
    final_df.columns = ["Máximo", "Mínimo"]

    # Criando Gráfico de Linha
    fig = px.line(data_frame=final_df, x=final_df.index, y=final_df.columns, template=template)
    fig.update_layout(main_config, height=150, xaxis_title=None, yaxis_title=None)

    # Retornando o gráfico de linha
    return fig

# Callback para o gráfico de barras horizontais
@app.callback(
    [
        Output("regiaobar_graph", "figure"),
        Output("estadobar_graph", "figure")
    ],
    [
        Input("dataset_fixed", "data"),
        Input("select_ano", "value"),
        Input("select_regiao", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    ]
)
def graph1(data, ano, regiao, toggle):

    # Instanciando o template selecionado pelo usuário
    template = template_theme1 if toggle else template_theme2

    # Transformando o dicionário de dados em um DataFrame do Pandas
    df = pd.DataFrame(data)

    # Selecionando os dados segundo o Ano selecionado no DropDawn pelo usuário
    df_filtred = df[df["ANO"].isin([ano])]

    # Selecionando e agrupando os dados por região e estado
    df_regiao = df_filtred.groupby(["ANO", "REGIÃO"])["VALOR REVENDA (R$/L)"].mean().reset_index()
    df_estado = df_filtred.groupby(["ANO", "ESTADO", "REGIÃO"])["VALOR REVENDA (R$/L)"].mean().reset_index()
    df_estado = df_estado[df_estado["REGIÃO"].isin([regiao])]

    # Reordenando os dados
    df_regiao = df_regiao.sort_values(by=["VALOR REVENDA (R$/L)"], ascending=True)
    df_estado = df_estado.sort_values(by=["VALOR REVENDA (R$/L)"], ascending=True)

    # Arredondando para 2 casas decimais após a vírgula
    df_regiao["VALOR REVENDA (R$/L)"] = df_regiao["VALOR REVENDA (R$/L)"].round(decimals=2)
    df_estado["VALOR REVENDA (R$/L)"] = df_estado["VALOR REVENDA (R$/L)"].round(decimals=2)

    # Textos para a figura
    fig1_text = [f"{x} - R${y}" for x, y in zip(df_regiao["REGIÃO"].unique(), df_regiao["VALOR REVENDA (R$/L)"].unique())]
    fig2_text = [f"R${y} - {x}" for x, y in zip(df_estado["ESTADO"].unique(), df_estado["VALOR REVENDA (R$/L)"].unique())]

    # Criando os gráficos de barras horizontais
    
    # Gráfico 1 - Região
    fig1 = go.Figure(go.Bar(
        x=df_regiao["VALOR REVENDA (R$/L)"],
        y=df_regiao["REGIÃO"],
        orientation="h",
        text=fig1_text,
        textposition="auto",
        insidetextanchor="end",
        insidetextfont=dict(family="Times", size=12)
    ))

    # Gráfico 2 - Estado
    fig2 = go.Figure(go.Bar(
        x=df_estado["VALOR REVENDA (R$/L)"],
        y=df_estado["ESTADO"],
        orientation="h",
        text=fig2_text,
        insidetextanchor="end",
        insidetextfont=dict(family="Times", size=12)
    ))

    fig1.update_layout(main_config, yaxis={"showticklabels": False}, height=140, template=template)
    fig2.update_layout(main_config, yaxis={"showticklabels": False}, height=140, template=template)
    fig1.update_layout(xaxis_range=[df_regiao["VALOR REVENDA (R$/L)"].max(), df_regiao["VALOR REVENDA (R$/L)"].min() - 0.15])
    fig2.update_layout(xaxis_range=[df_estado["VALOR REVENDA (R$/L)"].min() - 0.15, df_estado["VALOR REVENDA (R$/L)"].max()])

    # Retornando os gráficos para exposição
    return [fig1, fig2]

# Preço x Estado
@app.callback(
    Output("animation_graph", "figure"),
    [
        Input("dataset", "data"),
        Input("select_estado0", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    ]
)
def animation(data, estados, toggle):

    # Instanciando o layout selecionado pelo usuário
    template = template_theme1 if toggle else template_theme2

    # Transformando o dicionário de dados em um Dataframe do Pandas
    df = pd.DataFrame(data)

    # Selecionando as observações com os estados de interesse
    mask = df["ESTADO"].isin(estados)

    # Construção do Gráfico
    fig = px.line(df[mask], x="DATA", y="VALOR REVENDA (R$/L)", color="ESTADO", template=template)
    fig.update_layout(main_config, height=425, xaxis_title=None)

    # Retornando o gráfico
    return fig

# grafico de comparação direta
@app.callback(
    [Output('direct_comparison_graph', 'figure'),
    Output('desc_comparison', 'children')],
    [Input('dataset', 'data'),
    Input('select_estado1', 'value'),
    Input('select_estado2', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def func(data, est1, est2, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)
    df1 = dff[dff.ESTADO.isin([est1])]
    df2 = dff[dff.ESTADO.isin([est2])]
    df_final = pd.DataFrame()
    
    df_estado1 = df1.groupby(pd.PeriodIndex(df1['DATA'], freq="M"))['VALOR REVENDA (R$/L)'].mean().reset_index()
    df_estado2 = df2.groupby(pd.PeriodIndex(df2['DATA'], freq="M"))['VALOR REVENDA (R$/L)'].mean().reset_index()

    df_estado1['DATA'] = pd.PeriodIndex(df_estado1['DATA'], freq="M")
    df_estado2['DATA'] = pd.PeriodIndex(df_estado2['DATA'], freq="M")

    df_final['DATA'] = df_estado1['DATA'].astype('datetime64[ns]')
    df_final['VALOR REVENDA (R$/L)'] = df_estado1['VALOR REVENDA (R$/L)']-df_estado2['VALOR REVENDA (R$/L)']
    
    fig = go.Figure()
    # Toda linha
    fig.add_scattergl(name=est1, x=df_final['DATA'], y=df_final['VALOR REVENDA (R$/L)'])
    # Abaixo de zero
    fig.add_scattergl(name=est2, x=df_final['DATA'], y=df_final['VALOR REVENDA (R$/L)'].where(df_final['VALOR REVENDA (R$/L)'] > 0.00000))

    # Updates
    fig.update_layout(main_config, height=350, template=template)
    fig.update_yaxes(range = [-0.7,0.7])

    # Annotations pra mostrar quem é o mais barato
    fig.add_annotation(text=f'{est2} mais barato',
        xref="paper", yref="paper",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
        align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
        x=0.1, y=0.75, showarrow=False)

    fig.add_annotation(text=f'{est1} mais barato',
        xref="paper", yref="paper",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            ),
        align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
        x=0.1, y=0.25, showarrow=False) 

    # Definindo o texto
    text = f"Comparando {est1} e {est2}. Se a linha estiver acima do eixo X, {est2} tinha menor preço, do contrário, {est1} tinha um valor inferior"
    return [fig, text]

# Indicator 1
@app.callback(
    Output("card1_indicators", "figure"),
    [
        Input("dataset", "data"),
        Input("select_estado1", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    ]
)
def card1(data, estado, toggle):

    # Definindo template selecionado pelo usuário
    template = template_theme1 if toggle else template_theme2

    # Transformando o dicionário de dados em um DataFrame do Pandas
    df = pd.DataFrame(data)

    # Selecionando apenas as observações referente ao estado selecionado
    df_final = df[df["ESTADO"].isin([estado])]

    data1 = str(int(df["ANO"].min()) - 1)
    data2 = df["ANO"].max()

    # Instanciando figura
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style= 'size: 60%'>{estado}</span><br><span style= 'font-size: 0.7em'>{data1} - {data2}</span>"},
        value=df_final.at[df_final.index[-1], 'VALOR REVENDA (R$/L)'],
        number={'prefix': 'R$', 'valueformat': '.2f'},
        delta={'relative': True, 'valueformat': '.1%', 'reference': df_final.at[df_final.index[0], 'VALOR REVENDA (R$/L)']}
    ))
    fig.update_layout(main_config, height=250, template=template)

    # Retornando o card indicator
    return fig

# Card Indicator 2
@app.callback(
    Output("card2_indicators", "figure"),
    [
        Input("dataset", "data"),
        Input("select_estado2", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    ]
)
def card2(data, estado, toggle):

    # Instanciando o layout selecionado pelo usuário
    template = template_theme1 if toggle else template_theme2

    # Transformando o dicionário de dados em um DataFrame do Pandas
    df = pd.DataFrame(data)
    df_final = df[df["ESTADO"].isin([estado])]

    data1 = str(int(df['ANO'].min()) - 1)
    data2 = df["ANO"].max()

    # Construindo o CardIndicators
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style= 'size: 60%'>{estado}</span><br><span style= 'font-size: 0.7em'>{data1} - {data2}</span>"},
        value=df_final.at[df_final.index[-1], 'VALOR REVENDA (R$/L)'],
        number={"prefix": "R$", "valueformat": ".2f"},
        delta={'relative': True, "valueformat": ".1%", "reference": df_final.at[df_final.index[0], "VALOR REVENDA (R$/L)"]}
    ))
    fig.update_layout(main_config, height=250, template=template)

    # Retornando o card
    return fig



#######################################################################################
# -= END =-
if __name__ == "__main__":
    app.run_server(debug=True)