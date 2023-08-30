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
update_grafico = {'margin': {'l':0, 'r':0, 't': 10, 'b':0}}

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

card_saldo_att= dbc.Card(
    dbc.CardBody(
        [
            html.H6("Saldo 23'", className="card-title"),
            html.H4(f"R${df_year_cashflow['caixa'].iloc[-1]}")
        ]
    ),
    style={}
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
        
        dbc.Row([dbc.Col([card_receita], lg=3), dbc.Col([card_despesa], lg=3), dbc.Col([card_resultado_mes], lg=3), dbc.Col(card_saldo_att, lg=3)], style={'margin-top':'10px'}),
        
        dbc.Row([
                dbc.Col(dcc.Dropdown(options=lista_drop_esquerda, value=lista_drop_esquerda[0], id='dpd-01-r3/c1', clearable=False, style={"width": "200px", 'textAlign': 'center'}), lg=6), 
                dbc.Col([dcc.Dropdown(id='dpd-02-r3/c2')], lg=6)
                ], style={'margin-top':'10px'}),
        
        dbc.Row([dbc.Col([dcc.Graph(id='grafico-01-r4/c1', config={"displayModeBar": False, "showTips": False})], lg=7), dbc.Col(
                                                                                                                                [
                                                                                                                                html.Div(id='disparador_texto')
                                                                                                                                    ], 
                                                                                                                                 lg=5)]),
        
        dbc.Row([dbc.Col([html.H5('Evolução Caixa'), dcc.Graph(figure=fig_evolucao_caixa, config={"displayModeBar": False, "showTips": False})], lg=6), dbc.Col([html.H5('Check | Mensalidades')], lg=6)])
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
            if parametro_dir == 'Fluxo caixa mes/mes':

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
        
        if parametro_esq == 'Análise':
            if parametro_dir == 'Despesas por Categoria':
                fig = go.Figure(data=go.Pie(labels=df_despesas_target_beta['CATEGORIA'], values=df_despesas_target_beta['VALOR_DESPESA'], hole=0.6))
                
                fig.update_layout(height=350)
                fig.update_layout(update_grafico)
                
                return fig
            else:
                fig = go.Figure(data=go.Pie(labels=df_receitas_target_beta['CATEGORIA'], values=df_receitas_target_beta['VALOR_RECEITA'], hole=0.6))
                
                fig.update_layout(height=350)
                fig.update_layout(update_grafico)
                
                return fig
        else:
            if parametro_dir == 'Fluxo caixa mes/mes':

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
            receita_mensalidade = df_filter_incomes_detail[df_filter_incomes_detail['CATEGORIA']=='MENSALIDADE']['VALOR_RECEITA'].values
            receita_mensalidade = receita_mensalidade[0]
            receita_diaristas = df_filter_incomes_detail[df_filter_incomes_detail['CATEGORIA']=='DIARISTAS']['VALOR_RECEITA'].values
            receita_diaristas = receita_diaristas[0]
                
            card = dbc.Card([dbc.Row([dbc.Row(dbc.Col(dbc.CardBody(html.H6('Receitas por categoria')), lg=12)), 
                                        dbc.Row([dbc.Col(dbc.CardBody([html.Header('Mensalistas'), 
                                                                        html.Header('Diaristas')]), lg=6), 
                                                dbc.Col(dbc.CardBody([html.Header(f"R$ {receita_mensalidade}"), 
                                                                        html.Header(f"R$ {receita_diaristas}")]), lg=6)])
                                        ])
                                ])
            return card
        
        elif parametro == 'Despesas por categoria':
            despesa_campo = df_filter_expenses_detail[df_filter_expenses_detail['CATEGORIA']=='Campo']['VALOR_DESPESA'].values
            despesa_campo = despesa_campo[0]
            despesa_juiz = df_filter_expenses_detail[df_filter_expenses_detail['CATEGORIA']=='Juíz']['VALOR_DESPESA'].values
            despesa_juiz = despesa_juiz[0]
            despesa_goleiro = df_filter_expenses_detail[df_filter_expenses_detail['CATEGORIA']=='Goleiro']['VALOR_DESPESA'].values
            despesa_goleiro = despesa_goleiro[0]

            card = dbc.Card([dbc.Row([dbc.Row(dbc.Col(dbc.CardBody(html.H6('Despesas por categoria')), lg=12)), 
                                        dbc.Row([dbc.Col(dbc.CardBody([html.Header('Campo'), 
                                                                        html.Header('Juíz'),
                                                                        html.Header('Goleiro'),
                                                                        ]), lg=6), 
                                                dbc.Col(dbc.CardBody([html.Header(f"R$ {despesa_campo}"), 
                                                                        html.Header(f"R$ {despesa_juiz}"),
                                                                        html.Header(f"R$ {despesa_goleiro}"),

                                                                        ]), lg=6)])
                                        ])
                                ])
            return card
        
        elif parametro == 'Fluxo caixa mes/mes':
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
        
            card = dbc.Card([dbc.Row(dbc.CardBody([
                                        dbc.Row(dbc.Col(html.H6("Balanço mensal"), lg=12)),
                                        dbc.Row([
                                                dbc.Col([html.Header("Jan"),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Fev"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Mar"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Abr"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ],style={'margin':'0px'}, lg=2), 
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
                                                dbc.Col([html.Header("Mai"),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Jun"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Jul"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Ago"),
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
                                                dbc.Col([html.Header("Set"),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Out"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Nov"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Dez"),
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
                                    ]))
                            ])
            return card
        
        
        else:
            
            card = dbc.Card([dbc.Row(dbc.CardBody([dbc.Row(dbc.Col(html.H6("Cashflow 2023'"), lg=12)), 
                                    dbc.Row([dbc.Col(
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
                                                    ], lg=6), 
                                            dbc.Col(
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

                                                    ], lg=6)])
                                    ]))
                            ])
            return card
        

    
    
    else:   
        if parametro == 'Receitas por categoria':
            df_resp = df_filter_incomes_months.loc[df_filter_incomes_months['COMPETÊNCIA']==mes]
            
            receita_mensalidade = df_resp[df_resp['CATEGORIA']=='MENSALIDADE']['VALOR_RECEITA'].values
            receita_mensalidade = receita_mensalidade[0]
            receita_diaristas = df_resp[df_resp['CATEGORIA']=='DIARISTAS']['VALOR_RECEITA'].values
            receita_diaristas = receita_diaristas[0]
                
            card = dbc.Card([dbc.Row([dbc.Row(dbc.Col(dbc.CardBody(html.H6('Receitas por categoria')), lg=12)), 
                                        dbc.Row([dbc.Col(dbc.CardBody([html.Header('Mensalistas'), 
                                                                        html.Header('Diaristas')]), lg=6), 
                                                dbc.Col(dbc.CardBody([html.Header(f"R$ {receita_mensalidade}"), 
                                                                        html.Header(f"R$ {receita_diaristas}")]), lg=6)])
                                        ])
                                ])
            return card
            
        elif parametro == 'Despesas por categoria':
            df_resp_b = df_filter_expenses_months.loc[df_filter_expenses_months['COMPETÊNCIA']==mes]
            
            despesa_campo = df_resp_b[df_resp_b['CATEGORIA']=='Campo']['VALOR_DESPESA'].values
            despesa_campo = despesa_campo[0]
            despesa_juiz = df_resp_b[df_resp_b['CATEGORIA']=='Juíz']['VALOR_DESPESA'].values
            despesa_juiz = despesa_juiz[0]
            despesa_goleiro = df_resp_b[df_resp_b['CATEGORIA']=='Goleiro']['VALOR_DESPESA'].values
            despesa_goleiro = despesa_goleiro[0]

            card = dbc.Card([dbc.Row([dbc.Row(dbc.Col(dbc.CardBody(html.H6('Despesas por categoria')), lg=12)), 
                                        dbc.Row([dbc.Col(dbc.CardBody([html.Header('Campo'), 
                                                                        html.Header('Juíz'),
                                                                        html.Header('Goleiro'),
                                                                        ]), lg=6), 
                                                dbc.Col(dbc.CardBody([html.Header(f"R$ {despesa_campo}"), 
                                                                        html.Header(f"R$ {despesa_juiz}"),
                                                                        html.Header(f"R$ {despesa_goleiro}"),

                                                                        ]), lg=6)])
                                        ])
                                ])
            return card
            
        elif parametro == 'Fluxo caixa mes/mes':
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
        
            card = dbc.Card([dbc.Row(dbc.CardBody([
                                        dbc.Row(dbc.Col(html.H6("Balanço mensal"), lg=12)),
                                        dbc.Row([
                                                dbc.Col([html.Header("Jan"),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Fev"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Mar"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Abr"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa")
                                                                    ],style={'margin':'0px'}, lg=2), 
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
                                                dbc.Col([html.Header("Mai"),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Jun"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Jul"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Ago"),
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
                                                dbc.Col([html.Header("Set"),
                                                                    html.Header('Receita'), 
                                                                    html.Header('Despesa'),
                                                                    html.Br(),
                                                                    html.Header("Out"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Nov"),
                                                                    html.Header("Receita"),
                                                                    html.Header("Despesa"),
                                                                    html.Br(),
                                                                    html.Header("Dez"),
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
                                    ]))
                            ])
            return card
            
            
        else:
            card = dbc.Card([dbc.Row(dbc.CardBody([dbc.Row(dbc.Col(html.H6("Cashflow 2023'"), lg=12)), 
                                    dbc.Row([dbc.Col(
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
                                                    ], lg=6), 
                                            dbc.Col(
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

                                                    ], lg=6)])
                                    ]))
                            ])
            return card
        
        
# Servidor
if __name__=='__main__':
    app.run_server(debug=True)