from dash import dash, html, dcc, Output, Input
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
update_grafico = {'margin': {'l':0, 'r':0, 't': 10, 'b':0}}

card_receita = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Receitas", style={'color':'green'}),
            html.H4(id='receita-valor')
        ], style={'padding-top':'8px', 'padding-bottom':'10px'}
    ),
    style={'width':'72%'}
)

card_despesa= dbc.Card(
    dbc.CardBody(
        [
            html.H6("Despesas", style={'color':'red'}),
            html.H4(id='despesa-valor')
        ], style={'padding-top':'8px', 'padding-bottom':'10px'}
    ),
    style={'width':'72%'}
)

card_resultado_mes= dbc.Card(
    dbc.CardBody(
        [
            html.H6("Balanço (=)", style={'color':'#6CB2F6'}),
            html.H4(id='balanco-valor')
        ], style={'padding-top':'8px', 'padding-bottom':'10px'}
    ),
    style={'width':'72%'}
)

saldo_att_number = 4315.58 + (df_year_cashflow['caixa'].iloc[-1])
card_saldo_att= dbc.Card(
    dbc.CardBody(
        [
            html.H6("Saldo 23'  + 22' (R$4.315)", style={'color':'blue'}),
            html.H4(f"R${saldo_att_number}")
        ], style={'padding-top':'8px', 'padding-bottom':'10px'}
    ),
    style={'width':'72%'}
)

fig_evolucao_caixa = go.Figure(go.Scatter(x=df_year_cashflow['COMPETÊNCIA'], y=df_year_cashflow['caixa']))
fig_evolucao_caixa = fig_evolucao_caixa.update_layout(height=300)
fig_evolucao_caixa = fig_evolucao_caixa.update_layout(update_grafico)


nome_receita = html.Header('Receita: ')
nome_despesa = html.Header('Despesa: ')

disparador = nome_receita

# Layout ====================
app.layout = html.Div([
        dbc.Row(dcc.Dropdown(options=lista_meses, value=lista_meses[-1], id='disparador-geral-meses', clearable=False, style={"width": "200px", 'border-radius': '20px', 'textAlign': 'center'}), justify='center', style={'margin-top':'5px'}),
        
        dbc.Row([
                dbc.Col(dbc.Row([card_receita], justify='center'), lg=3), 
                dbc.Col(dbc.Row([card_despesa], justify='center'), lg=3), 
                dbc.Col(dbc.Row([card_resultado_mes], justify='center'), lg=3), 
                dbc.Col(dbc.Row(card_saldo_att, justify='center'), lg=3)
                ], 
                style={'margin-top':'20px'}, justify='center'),
        
        dbc.Row([
                dbc.Col(dcc.Dropdown(options=lista_drop_esquerda, value=lista_drop_esquerda[0], id='dpd-01-r3/c1', clearable=False, style={"width": "250px", 'textAlign': 'center'}), lg=7), 
                dbc.Col(dcc.Dropdown(id='dpd-02-r3/c2', clearable=False, style={"width": "250px", 'textAlign': 'center'}), lg=5)
                ], 
                style={'margin-top':'10px', 'margin-left':'5px', 'margin_right':'5px', 'padding':'0px'}),
        
        dbc.Row([
                dbc.Col([dcc.Graph(id='grafico-01-r4/c1', config={"displayModeBar": False, "showTips": False})], lg=7), 
                dbc.Col([
                        html.Div(id='disparador_texto')
                            ],lg=5)
                ], 
                style={'margin-top':'10px', 'margin-left':'5px', 'margin_right':'5px', 'padding':'0px'}),
        
        dbc.Row([
                dbc.Col([html.H5('Evolução Caixa 23"'), dcc.Graph(figure=fig_evolucao_caixa, config={"displayModeBar": False, "showTips": False})], lg=7), 
                dbc.Col([html.H5('Check | Mensalidades'), html.Div(id='disparador_table')], lg=5)
                ],
                style={'margin-top':'10px', 'margin-left':'5px', 'margin_right':'5px', 'padding':'0px'})
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
    if value == 'Filtros':
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
        
        if parametro_esq == 'Filtros':
            if parametro_dir == 'Despesas por categoria':
                fig = go.Figure(data=go.Pie(labels=df_filter_expenses_detail['CATEGORIA'], values=df_filter_expenses_detail['VALOR_DESPESA'], hole=0.6))
                
                
                fig.update_layout(height=350)
                fig.update_layout(update_grafico)
                
                return fig
            else:
                fig = go.Figure(data=go.Pie(labels=df_filter_incomes_detail['CATEGORIA'], values=df_filter_incomes_detail['VALOR_RECEITA'], hole=0.6))
                
                fig.update_layout(height=350)
                fig.update_layout(update_grafico)
                
                return fig
                
        else:
            if parametro_dir == 'Fluxo caixa mês/mês':

                fig = make_subplots(rows=1, cols=1)

                fig.add_trace(go.Bar(x=df_receitas_graph_01['COMPETÊNCIA'], y=df_receitas_graph_01['VALOR_RECEITA'], showlegend=False, name='Receita'), row=1, col=1)

                fig.add_trace(go.Bar(x=df_despesas_graph_01['COMPETÊNCIA'], y=df_despesas_graph_01['VALOR_DESPESA'], showlegend=False, name='Despesa'), row=1, col=1)
                
                fig.update_layout(height=350)
                fig.update_layout(update_grafico)
                
                return fig
            else:
                fig_year_cashflow = go.Figure(data=go.Bar(x=df_year_cashflow['COMPETÊNCIA'], y=df_year_cashflow['CASH_FLOW']))
                
                fig_year_cashflow.update_layout(height=350)
                fig_year_cashflow.update_layout(update_grafico)
                
                return fig_year_cashflow
    
    else:
        df_receitas_target = df_receitas_graph_01.loc[df_receitas_graph_01['COMPETÊNCIA']==parametro_superior]
        df_despesas_target = df_despesas_graph_01.loc[df_despesas_graph_01['COMPETÊNCIA']==parametro_superior]
        
        df_receitas_target_beta = df_filter_incomes_months.loc[df_filter_incomes_months['COMPETÊNCIA']==parametro_superior]
        df_despesas_target_beta = df_filter_expenses_months.loc[df_filter_expenses_months['COMPETÊNCIA']==parametro_superior]
        
        if parametro_esq == 'Filtros':
            if parametro_dir == 'Despesas por categoria':
                fig_x = go.Figure(data=go.Pie(labels=df_despesas_target_beta['CATEGORIA'], values=df_despesas_target_beta['VALOR_DESPESA'], hole=0.6))
                
                
                fig_x.update_layout(height=350)
                fig_x.update_layout(update_grafico)
                
                return fig_x
            else:
                fig_k = go.Figure(data=go.Pie(labels=df_receitas_target_beta['CATEGORIA'], values=df_receitas_target_beta['VALOR_RECEITA'], hole=0.6))
                
                fig_k.update_layout(height=350)
                fig_k.update_layout(update_grafico)
                
                return fig_k
        else:
            if parametro_dir == 'Fluxo caixa mês/mês':

                fig = make_subplots(rows=1, cols=1)

                fig.add_trace(go.Bar(x=df_receitas_target['COMPETÊNCIA'], y=df_receitas_target['VALOR_RECEITA'], showlegend=False, name='Receita'), row=1, col=1)

                fig.add_trace(go.Bar(x=df_despesas_target['COMPETÊNCIA'], y=df_despesas_target['VALOR_DESPESA'], showlegend=False, name='Despesa'), row=1, col=1)
                
                fig.update_layout(height=350)
                fig.update_layout(update_grafico)
                
                return fig
            else:
                fig_year_cashflow = go.Figure(data=go.Bar(x=df_year_cashflow['COMPETÊNCIA'], y=df_year_cashflow['CASH_FLOW']))
                
                fig_year_cashflow.update_layout(height=350)
                fig_year_cashflow.update_layout(update_grafico)
                return fig_year_cashflow

@app.callback(
    Output('disparador_texto', 'children'),
    Input('dpd-02-r3/c2', 'value'),
    Input('disparador-geral-meses', 'value')
)
def update_texto(parametro, mes):
    
    
    if mes == 'Ano':
        if parametro == 'Receitas por categoria':
            receita_mensalidade = df_filter_incomes_detail[df_filter_incomes_detail['CATEGORIA']=='MENSALIDADE']['VALOR_RECEITA'].sum()
            
            receita_diaristas = df_filter_incomes_detail[df_filter_incomes_detail['CATEGORIA']=='DIARISTAS']['VALOR_RECEITA'].sum()
            
                
            card = dbc.Card([dbc.Row([
                                        dbc.Row(html.H6('Receitas por categoria', style={'margin-top':'10px', 'margin-left':'30px'}), justify='center'), 
                                        dbc.Row([
                                                dbc.Col(dbc.CardBody([
                                                                        html.Header('Mensalistas'), 
                                                                        html.Header('Diaristas')
                                                                        ], style={'padding-top':'0px'}), lg=3), 
                                                dbc.Col(dbc.CardBody([
                                                                    html.Header(f"R$ {receita_mensalidade}"), 
                                                                    html.Header(f"R$ {receita_diaristas}")
                                                                    ], style={'padding-top':'0px'}), lg=2),
                                                dbc.Col([html.Div()], lg=3),
                                                dbc.Col([html.Div()], lg=4)
                                                ], style={'margin-top':'10px'})
                                        ])
                                ], style={'height':'420px'})
            return card
        
        elif parametro == 'Despesas por categoria':
            despesa_campo = df_filter_expenses_detail[df_filter_expenses_detail['CATEGORIA']=='Campo']['VALOR_DESPESA'].sum()
            
            despesa_juiz = df_filter_expenses_detail[df_filter_expenses_detail['CATEGORIA']=='Juíz']['VALOR_DESPESA'].sum()
            
            despesa_goleiro = df_filter_expenses_detail[df_filter_expenses_detail['CATEGORIA']=='Goleiro']['VALOR_DESPESA'].sum()
            

            card = dbc.Card([dbc.Row([
                                        dbc.Row(html.H6('Despesas por categoria', style={'margin-top':'10px', 'margin-left':'30px'}), justify='center'), 
                                        dbc.Row([
                                                dbc.Col(dbc.CardBody([
                                                                        html.Header('Campo'), 
                                                                        html.Header('Juíz'),
                                                                        html.Header('Goleiro'),
                                                                        ], style={'padding-top':'0px'}), lg=3), 
                                                dbc.Col(dbc.CardBody([
                                                                        html.Header(f"R$ {despesa_campo}"), 
                                                                        html.Header(f"R$ {despesa_juiz}"),
                                                                        html.Header(f"R$ {despesa_goleiro}")
                                                                        ], style={'padding-top':'0px'}), lg=2),
                                                dbc.Col([html.Div()], lg=3),
                                                dbc.Col([html.Div()], lg=4)
                                                ], style={'margin-top':'10px'})
                                        ])
                                ], style={'height':'420px'})
            return card
        
        elif parametro == 'Fluxo caixa mês/mês':
            jan = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Janeiro']
            jan_receita = jan['VALOR_RECEITA'].sum()
            jan_despesa = jan['VALOR_DESPESA'].sum()
            
            fev = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Feveiro']
            fev_receita = fev['VALOR_RECEITA'].sum()
            fev_despesa = fev['VALOR_DESPESA'].sum()
            
            mar = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Março']
            mar_receita = mar['VALOR_RECEITA'].sum()
            mar_despesa = mar['VALOR_DESPESA'].sum()
            
            abr = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Abril']
            abr_receita = abr['VALOR_RECEITA'].sum()
            abr_despesa = abr['VALOR_DESPESA'].sum()
            
            mai = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Maio']
            mai_receita = mai['VALOR_RECEITA'].sum()
            mai_despesa = mai['VALOR_DESPESA'].sum()
            
            jun = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Junho']
            jun_receita = jun['VALOR_RECEITA'].sum()
            jun_despesa = jun['VALOR_DESPESA'].sum()
            
            jul = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Julho']
            jul_receita = jul['VALOR_RECEITA'].sum()
            jul_despesa = jul['VALOR_DESPESA'].sum()
            
            ago = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Agosto']
            ago_receita = ago['VALOR_RECEITA'].sum()
            ago_despesa = ago['VALOR_DESPESA'].sum()
            
            set = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Setembro']
            set_receita = set['VALOR_RECEITA'].sum()
            set_despesa = set['VALOR_DESPESA'].sum()
            
            out = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Outubro']
            out_receita = out['VALOR_RECEITA'].sum()
            out_despesa = out['VALOR_DESPESA'].sum()
            
            nov = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Novembro']
            nov_receita = nov['VALOR_RECEITA'].sum()
            nov_despesa = nov['VALOR_DESPESA'].sum()
            
            dez = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Dezembro']
            dez_receita = dez['VALOR_RECEITA'].sum()
            dez_despesa = dez['VALOR_DESPESA'].sum()
        
            card = dbc.Card([dbc.Row([
                                        dbc.Row(html.H6("Balanço mensal", style={'margin-top':'10px', 'margin-left':'30px'})),
                                        dbc.Row([
                                                dbc.Col([html.Header("Jan", style={'color':'#A039F6'}),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Fev", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Mar", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Abr", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ], lg=2), 
                                                dbc.Col([html.Br(),
                                                                    html.Header(f"R${jan_receita}"), 
                                                                    html.Header(f"R${jan_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${fev_receita}"),
                                                                    html.Header(f"R${fev_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${mar_receita}"),
                                                                    html.Header(f"R${mar_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${abr_receita}"),
                                                                    html.Header(f"R${abr_despesa}")
                                                                    ], lg=2),
                                                dbc.Col([html.Header("Mai", style={'color':'#A039F6'}),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Jun", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Jul", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Ago", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ], lg=2), 
                                                dbc.Col([html.Br(),
                                                                    html.Header(f"R${mai_receita}"), 
                                                                    html.Header(f"R${mai_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${jun_receita}"),
                                                                    html.Header(f"R${jun_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${jul_receita}"),
                                                                    html.Header(f"R${jul_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${ago_receita}"),
                                                                    html.Header(f"R${ago_despesa}")
                                                                    ], lg=2),
                                                dbc.Col([html.Header("Set", style={'color':'#A039F6'}),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Out", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Nov", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Dez", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ], lg=2), 
                                                dbc.Col([html.Br(),
                                                                    html.Header(f"R${set_receita}"), 
                                                                    html.Header(f"R${set_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${out_receita}"),
                                                                    html.Header(f"R${out_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${nov_receita}"),
                                                                    html.Header(f"R${nov_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${dez_receita}"),
                                                                    html.Header(f"R${dez_despesa}"),
                                                                    ], lg=2),

                                            ])
                                    ])
                            ])
            return card
        
        
        else:
            
            card = dbc.Card([
                                dbc.Row(
                                            [
                                            dbc.Row(html.H6("Cashflow 2023'", style={'margin-top':'10px', 'margin-left':'30px'})), 
                                            dbc.Row(
                                                [
                                                dbc.Col(dbc.CardBody(
                                                        [ 
                                                        html.Header('Janeiro', style={'color':'#A039F6'}),
                                                        html.Header('Fevereiro', style={'color':'#A039F6'}),
                                                        html.Header('Março', style={'color':'#A039F6'}),
                                                        html.Header('Abril', style={'color':'#A039F6'}),
                                                        html.Header('Maio', style={'color':'#A039F6'}),
                                                        html.Header('Junho', style={'color':'#A039F6'}),
                                                        html.Header('Julho', style={'color':'#A039F6'}),
                                                        html.Header('Agosto', style={'color':'#A039F6'}),
                                                        html.Header('Setembro', style={'color':'#A039F6'}),
                                                        html.Header('Outubro', style={'color':'#A039F6'}),
                                                        html.Header('Novembro', style={'color':'#A039F6'}),
                                                        html.Header('Dezembro', style={'color':'#A039F6'}),
                                                        ], style={'padding-top':'0px'}), lg=3), 
                                                dbc.Col(dbc.CardBody(
                                                        [
                                                        html.Header(f"R${janeiro_cashflow}"), 
                                                        html.Header(f"R${fevereiro_cashflow}"),
                                                        html.Header(f"R${marco_cashflow}"),
                                                        html.Header(f"R${abril_cashflow}"),
                                                        html.Header(f"R${maio_cashflow}"),
                                                        html.Header(f"R${junho_cashflow}"),
                                                        html.Header(f"R${julho_cashflow}"),
                                                        html.Header(f"R${agosto_cashflow}"),
                                                        html.Header(f"R${setembro_cashflow}"),
                                                        html.Header(f"R${outubro_cashflow}"),
                                                        html.Header(f"R${novembro_cashflow}"),
                                                        html.Header(f"R${dezembro_cashflow}"),
                                                        ], style={'padding-top':'0px'}), lg=2),
                                                dbc.Col([html.Div()], lg=3),
                                                dbc.Col([html.Div()], lg=4)
                                                ], style={'margin-top':'10px'})
                                            ]
                                    )
                            ], style={'height':'420px'})
            return card
        

    
    
    else:   
        if parametro == 'Receitas por categoria':
            df_resp = df_filter_incomes_months.loc[df_filter_incomes_months['COMPETÊNCIA']==mes]
            
            receita_mensalidade = df_resp[df_resp['CATEGORIA']=='MENSALIDADE']['VALOR_RECEITA'].sum()
            
            receita_diaristas = df_resp[df_resp['CATEGORIA']=='DIARISTAS']['VALOR_RECEITA'].sum()
            
                
            card = dbc.Card([dbc.Row([
                                        dbc.Row(html.H6('Receitas por categoria', style={'margin-top':'10px', 'margin-left':'30px'}), justify='center'), 
                                        dbc.Row([
                                                dbc.Col(dbc.CardBody([
                                                                        html.Header('Mensalistas'), 
                                                                        html.Header('Diaristas')
                                                                        ], style={'padding-top':'0px'}), lg=3), 
                                                dbc.Col(dbc.CardBody([
                                                                    html.Header(f"R$ {receita_mensalidade}"), 
                                                                    html.Header(f"R$ {receita_diaristas}")
                                                                    ], style={'padding-top':'0px'}), lg=2),
                                                dbc.Col([html.Div()], lg=3),
                                                dbc.Col([html.Div()], lg=4)
                                                ], style={'margin-top':'10px'})
                                        ])
                                ], style={'height':'420px'})
            return card
            
        elif parametro == 'Despesas por categoria':
            df_resp_b = df_filter_expenses_months.loc[df_filter_expenses_months['COMPETÊNCIA']==mes]
            
            despesa_campo = df_resp_b[df_resp_b['CATEGORIA']=='Campo']['VALOR_DESPESA'].sum()
            
            despesa_juiz = df_resp_b[df_resp_b['CATEGORIA']=='Juíz']['VALOR_DESPESA'].sum()
            
            despesa_goleiro = df_resp_b[df_resp_b['CATEGORIA']=='Goleiro']['VALOR_DESPESA'].sum()
            

            card = dbc.Card([dbc.Row([
                                        dbc.Row(html.H6('Despesas por categoria', style={'margin-top':'10px', 'margin-left':'30px'}), justify='center'), 
                                        dbc.Row([
                                                dbc.Col(dbc.CardBody([
                                                                        html.Header('Campo'), 
                                                                        html.Header('Juíz'),
                                                                        html.Header('Goleiro'),
                                                                        ], style={'padding-top':'0px'}), lg=3), 
                                                dbc.Col(dbc.CardBody([
                                                                        html.Header(f"R$ {despesa_campo}"), 
                                                                        html.Header(f"R$ {despesa_juiz}"),
                                                                        html.Header(f"R$ {despesa_goleiro}")
                                                                        ], style={'padding-top':'0px'}), lg=2),
                                                dbc.Col([html.Div()], lg=3),
                                                dbc.Col([html.Div()], lg=4)
                                                ], style={'margin-top':'10px'})
                                        ])
                                ], style={'height':'420px'})
            return card
            
        elif parametro == 'Fluxo caixa mês/mês':
            jan = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Janeiro']
            jan_receita = jan['VALOR_RECEITA'].sum()
            jan_despesa = jan['VALOR_DESPESA'].sum()
            
            fev = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Feveiro']
            fev_receita = fev['VALOR_RECEITA'].sum()
            fev_despesa = fev['VALOR_DESPESA'].sum()
            
            mar = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Março']
            mar_receita = mar['VALOR_RECEITA'].sum()
            mar_despesa = mar['VALOR_DESPESA'].sum()
            
            abr = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Abril']
            abr_receita = abr['VALOR_RECEITA'].sum()
            abr_despesa = abr['VALOR_DESPESA'].sum()
            
            mai = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Maio']
            mai_receita = mai['VALOR_RECEITA'].sum()
            mai_despesa = mai['VALOR_DESPESA'].sum()
            
            jun = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Junho']
            jun_receita = jun['VALOR_RECEITA'].sum()
            jun_despesa = jun['VALOR_DESPESA'].sum()
            
            jul = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Julho']
            jul_receita = jul['VALOR_RECEITA'].sum()
            jul_despesa = jul['VALOR_DESPESA'].sum()
            
            ago = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Agosto']
            ago_receita = ago['VALOR_RECEITA'].sum()
            ago_despesa = ago['VALOR_DESPESA'].sum()
            
            set = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Setembro']
            set_receita = set['VALOR_RECEITA'].sum()
            set_despesa = set['VALOR_DESPESA'].sum()
            
            out = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Outubro']
            out_receita = out['VALOR_RECEITA'].sum()
            out_despesa = out['VALOR_DESPESA'].sum()
            
            nov = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Novembro']
            nov_receita = nov['VALOR_RECEITA'].sum()
            nov_despesa = nov['VALOR_DESPESA'].sum()
            
            dez = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Dezembro']
            dez_receita = dez['VALOR_RECEITA'].sum()
            dez_despesa = dez['VALOR_DESPESA'].sum()
        
            card = dbc.Card([dbc.Row([
                                        dbc.Row(html.H6("Balanço mensal", style={'margin-top':'10px', 'margin-left':'30px'})),
                                        dbc.Row([
                                                dbc.Col([html.Header("Jan", style={'color':'#A039F6'}),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Fev", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Mar", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Abr", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ], lg=2), 
                                                dbc.Col([html.Br(),
                                                                    html.Header(f"R${jan_receita}"), 
                                                                    html.Header(f"R${jan_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${fev_receita}"),
                                                                    html.Header(f"R${fev_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${mar_receita}"),
                                                                    html.Header(f"R${mar_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${abr_receita}"),
                                                                    html.Header(f"R${abr_despesa}")
                                                                    ], lg=2),
                                                dbc.Col([html.Header("Mai", style={'color':'#A039F6'}),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Jun", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Jul", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Ago", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ], lg=2), 
                                                dbc.Col([html.Br(),
                                                                    html.Header(f"R${mai_receita}"), 
                                                                    html.Header(f"R${mai_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${jun_receita}"),
                                                                    html.Header(f"R${jun_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${jul_receita}"),
                                                                    html.Header(f"R${jul_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${ago_receita}"),
                                                                    html.Header(f"R${ago_despesa}")
                                                                    ], lg=2),
                                                dbc.Col([html.Header("Set", style={'color':'#A039F6'}),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Out", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Nov", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Dez", style={'color':'#A039F6'}),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ], lg=2), 
                                                dbc.Col([html.Br(),
                                                                    html.Header(f"R${set_receita}"), 
                                                                    html.Header(f"R${set_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${out_receita}"),
                                                                    html.Header(f"R${out_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${nov_receita}"),
                                                                    html.Header(f"R${nov_despesa}"),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Header(f"R${dez_receita}"),
                                                                    html.Header(f"R${dez_despesa}"),
                                                                    ], lg=2),

                                            ])
                                    ])
                            ])
            return card
            
            
        else:
            card = dbc.Card([
                                dbc.Row(
                                            [
                                            dbc.Row(html.H6("Cashflow 2023'", style={'margin-top':'10px', 'margin-left':'30px'})), 
                                            dbc.Row(
                                                [
                                                dbc.Col(dbc.CardBody(
                                                        [ 
                                                        html.Header('Janeiro'),
                                                        html.Header('Fevereiro'),
                                                        html.Header('Março'),
                                                        html.Header('Abril'),
                                                        html.Header('Maio'),
                                                        html.Header('Junho'),
                                                        html.Header('Julho'),
                                                        html.Header('Agosto'),
                                                        html.Header('Setembro'),
                                                        html.Header('Outubro'),
                                                        html.Header('Novembro'),
                                                        html.Header('Dezembro'),
                                                        ], style={'padding-top':'0px'}), lg=3), 
                                                dbc.Col(dbc.CardBody(
                                                        [
                                                        html.Header(f"R${janeiro_cashflow}"), 
                                                        html.Header(f"R${fevereiro_cashflow}"),
                                                        html.Header(f"R${marco_cashflow}"),
                                                        html.Header(f"R${abril_cashflow}"),
                                                        html.Header(f"R${maio_cashflow}"),
                                                        html.Header(f"R${junho_cashflow}"),
                                                        html.Header(f"R${julho_cashflow}"),
                                                        html.Header(f"R${agosto_cashflow}"),
                                                        html.Header(f"R${setembro_cashflow}"),
                                                        html.Header(f"R${outubro_cashflow}"),
                                                        html.Header(f"R${novembro_cashflow}"),
                                                        html.Header(f"R${dezembro_cashflow}"),
                                                        ], style={'padding-top':'0px'}), lg=2),
                                                dbc.Col([html.Div()], lg=3),
                                                dbc.Col([html.Div()], lg=4)
                                                ], style={'margin-top':'10px'})
                                            ]
                                    )
                            ], style={'height':'420px'})
            return card
        

@app.callback(
    Output('disparador_table', 'children'),
    Input('disparador-geral-meses', 'value')
)
def update_table(mes):
    if mes == 'Ano':
        columnDefs = [
                {'field': 'PLAYER', 'width': 200, 'autosize': True},
                {'field': 'PAGTO', 'width': 120}
            ]
        
        df_table_x = df_table.groupby('PLAYER').agg({'PAGTO':'sum'})
        df_table_x = df_table_x.reset_index()
        
        table = dag.AgGrid(id="check-table", rowData=df_table_x.to_dict("records"), columnDefs=columnDefs, defaultColDef={"resizable": True, "sortable": True}, style={'height':'285px', 'width':'50%'})
        
        return table
    
    else:
        df_table_y = df_table.loc[df_table['COMPETÊNCIA']==mes]
        columnDefs = [
                {'field': 'PLAYER', 'width': 200, 'autosize': True},
                {'field': 'STATUS', 'width': 120}
            ]
        
        table_y = dag.AgGrid(id="check-table", rowData=df_table_y.to_dict("records"), columnDefs=columnDefs, defaultColDef={"resizable": True, "sortable": True}, style={'height':'285px', 'width':'50%'})
        
        return table_y

# Servidor
if __name__=='__main__':
    app.run_server(debug=False)