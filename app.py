from dash import dash, html, dcc, ctx, Output, Input, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


import plotly as plt
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_ag_grid as dag

# Servidor
load_figure_template("minty")

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
server = app.server

# DataFrame =================

from globals import *

# Pré-layout ================

card_receita = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Receitas", className="card-title"),
            html.H4(id='receita-valor')
        ]
    ),
    style={}
)

card_despesa= dbc.Card(
    dbc.CardBody(
        [
            html.H6("Despesas", className="card-title"),
            html.H4(id='despesa-valor')
        ]
    ),
    style={}
)

card_resultado_mes= dbc.Card(
    dbc.CardBody(
        [
            html.H6("Balanço (=)", className="card-title"),
            html.H4(id='balanco-valor')
        ]
    ),
    style={}
)


# Layout ====================
app.layout = html.Div([
        dbc.Row(dcc.Dropdown(options=lista_meses, value=lista_meses[-1], id='disparador-geral-meses')),
        
        dbc.Row([dbc.Col([card_receita], lg=4), dbc.Col([card_despesa], lg=4), dbc.Col([card_resultado_mes], lg=4)]),
        
        dbc.Row([
                dbc.Col(dcc.Dropdown(options=lista_drop_esquerda, value=lista_drop_esquerda[0], id='dpd-01-r3/c1'), lg=6), 
                dbc.Col([dcc.Dropdown(id='dpd-02-r3/c2')], lg=6)
                ]),
        
        dbc.Row([dbc.Col([dcc.Graph(id='grafico-01-r4/c1')], lg=8), dbc.Col([dcc.Graph(id='grafico-02-r4/c2')], lg=4)])
])


# Callbacks =================
@app.callback(
    Output('receita-valor', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_receita(mes):
    if mes == 'Ano':
        valor = df_receitas['VALOR_RECEITA'].sum()
        valor = 'R${:.2f}'.format(valor)
        return valor
    else:
        df_receita_mes = df_receitas.loc[df_receitas['COMPETÊNCIA']==mes]
        valor = df_receita_mes['VALOR_RECEITA'].sum()
        valor = 'R${:.2f}'.format(valor)
        return valor


@app.callback(
    Output('despesa-valor', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_despesa(mes):
    if mes == 'Ano':
        valor = df_despesas['VALOR_DESPESA'].sum()
        valor = 'R${:.2f}'.format(valor)
        return valor
    else:
        df_despesa_mes = df_despesas.loc[df_despesas['COMPETÊNCIA']==mes]
        valor = df_despesa_mes['VALOR_DESPESA'].sum()
        valor = 'R${:.2f}'.format(valor)
        return valor
    

@app.callback(
    Output('balanco-valor', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_balanco(mes):
    if mes == 'Ano':
        valor_receita = df_receitas['VALOR_RECEITA'].sum()
        valor_despesa = df_despesas['VALOR_DESPESA'].sum()
        valor_final = valor_receita - valor_despesa
        valor_final = 'R${:.2f}'.format(valor_final)
        return valor_final
    else:
        df_receita_m = df_receitas.loc[df_receitas['COMPETÊNCIA']==mes]
        x_receita = df_receita_m['VALOR_RECEITA'].sum()
        
        df_despesa_m = df_despesas.loc[df_despesas['COMPETÊNCIA']==mes]
        x_despesa = df_despesa_m['VALOR_DESPESA'].sum()
        
        y_final = x_receita - x_despesa
        y_final = 'R${:.2f}'.format(y_final)
        return y_final
        
@app.callback(
    Output('dpd-02-r3/c2','options'),
    Input('dpd-01-r3/c1', 'value')
)
def update_dropdown_function(value):
    if value == 'Análise':
        return lista_filtragem_categoria
    else:
        return lista_tipo_fluxo_caixa
    
@app.callback(
    Output('dpd-02-r3/c2', 'value'),
    Input('dpd-02-r3/c2', 'options')
)
def set_drop(set):
    return set[0]

@app.callback(
    Output('grafico-01-r4/c1', 'figure'),
    Input('dpd-01-r3/c1', 'value'),
    Input('dpd-02-r3/c2', 'value'),
    Input('disparador-geral-meses', 'value')
)
def update_grafico_01(parametro_esq, parametro_dir, parametro_superior):  
    if parametro_superior == 'Ano':
        
        if parametro_esq == 'Análise':
            if parametro_dir == 'Despesas por Categoria':
                fig = go.Figure(data=go.Pie(labels=df_filter_expenses_detail['CATEGORIA'], values=df_filter_expenses_detail['VALOR_DESPESA'], hole=0.6))
                return fig
            else:
                fig = go.Figure(data=go.Pie(labels=df_filter_incomes_detail['CATEGORIA'], values=df_filter_incomes_detail['VALOR_RECEITA'], hole=0.6))
                return fig
                
        else:
            if parametro_dir == 'Fluxo caixa mes/mes':

                fig = make_subplots(rows=1, cols=1)

                fig.add_trace(go.Bar(x=df_receitas_graph_01['COMPETÊNCIA'], y=df_receitas_graph_01['VALOR_RECEITA'], showlegend=False, name='Receita'), row=1, col=1)

                fig.add_trace(go.Bar(x=df_despesas_graph_01['COMPETÊNCIA'], y=df_despesas_graph_01['VALOR_DESPESA'], showlegend=False, name='Despesa'), row=1, col=1)
                return fig
            else:
                fig_year_cashflow = go.Figure(data=go.Bar(x=df_year_cashflow['COMPETÊNCIA'], y=df_year_cashflow['CASH_FLOW']))
                return fig_year_cashflow
    
    else:
        df_receitas_target = df_receitas_graph_01.loc[df_receitas_graph_01['COMPETÊNCIA']==parametro_superior]
        df_despesas_target = df_despesas_graph_01.loc[df_despesas_graph_01['COMPETÊNCIA']==parametro_superior]
        
        df_receitas_target_beta = df_filter_incomes_months.loc[df_filter_incomes_months['COMPETÊNCIA']==parametro_superior]
        df_despesas_target_beta = df_filter_expenses_months.loc[df_filter_expenses_months['COMPETÊNCIA']==parametro_superior]
        
        if parametro_esq == 'Análise':
            if parametro_dir == 'Despesas por Categoria':
                fig = go.Figure(data=go.Pie(labels=df_despesas_target_beta['CATEGORIA'], values=df_despesas_target_beta['VALOR_DESPESA'], hole=0.6))
                return fig
            else:
                fig = go.Figure(data=go.Pie(labels=df_receitas_target_beta['CATEGORIA'], values=df_receitas_target_beta['VALOR_RECEITA'], hole=0.6))
                return fig
        else:
            if parametro_dir == 'Fluxo caixa mes/mes':

                fig = make_subplots(rows=1, cols=1)

                fig.add_trace(go.Bar(x=df_receitas_target['COMPETÊNCIA'], y=df_receitas_target['VALOR_RECEITA'], showlegend=False, name='Receita'), row=1, col=1)

                fig.add_trace(go.Bar(x=df_despesas_target['COMPETÊNCIA'], y=df_despesas_target['VALOR_DESPESA'], showlegend=False, name='Despesa'), row=1, col=1)
                return fig
            else:
                fig_year_cashflow = go.Figure(data=go.Bar(x=df_year_cashflow['COMPETÊNCIA'], y=df_year_cashflow['CASH_FLOW']))
                return fig_year_cashflow



# Servidor
if __name__=='__main__':
    app.run_server(debug=True)