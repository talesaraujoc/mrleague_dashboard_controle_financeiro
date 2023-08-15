from dash import dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


import plotly as plt
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_ag_grid as dag

# Servidor
load_figure_template("bootstrap")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# DataFrame =================

from globals import *

# Pré-layout ================

card_receita = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Receitas", className="card-title"),
            html.H3(id='receita-valor')
        ]
    ),
    style={}
)

card_despesa= dbc.Card(
    dbc.CardBody(
        [
            html.H5("Despesas", className="card-title"),
            html.H3(id='despesa-valor')
        ]
    ),
    style={}
)

card_resultado_mes= dbc.Card(
    dbc.CardBody(
        [
            html.H5("Balanço (=)", className="card-title"),
            html.H3(id='balanco-valor')
        ]
    ),
    style={}
)


# Layout ====================
app.layout = html.Div([
        dbc.Row(dcc.Dropdown(options=lista_meses, value=lista_meses[-1], id='disparador-geral-meses')),
        
        dbc.Row([dbc.Col([card_resultado_mes], lg=4), dbc.Col([card_receita], lg=4), dbc.Col([card_despesa], lg=4)]),
        
        dbc.Row()
])


# Callbacks =================
@app.callback(
    Output('receita-valor', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_receita(mes):
    if mes == 'Ano':
        valor = df_receitas['VALOR'].sum()
        return valor
    else:
        df_receita_mes = df_receitas.loc[df_receitas['COMPETÊNCIA']==mes]
        valor = df_receita_mes['VALOR'].sum()
        return valor


@app.callback(
    Output('despesa-valor', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_despesa(mes):
    if mes == 'Ano':
        valor = df_despesas['VALOR'].sum()
        return valor
    else:
        df_despesa_mes = df_despesas.loc[df_despesas['COMPETÊNCIA']==mes]
        valor = df_despesa_mes['VALOR'].sum()
        return valor
    

@app.callback(
    Output('balanco-valor', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_balanco(mes):
    if mes == 'Ano':
        valor_receita = df_receitas['VALOR'].sum()
        valor_despesa = df_despesas['VALOR'].sum()
        valor_final = valor_receita - valor_despesa
        return valor_final
    else:
        df_receita_m = df_receitas.loc[df_receitas['COMPETÊNCIA']==mes]
        x_receita = df_receita_m['VALOR'].sum()
        
        df_despesa_m = df_despesas.loc[df_despesas['COMPETÊNCIA']==mes]
        x_despesa = df_despesa_m['VALOR'].sum()
        
        y_final = x_receita - x_despesa
        return y_final
        
        
# Servidor
if __name__=='__main__':
    app.run_server(debug=True)