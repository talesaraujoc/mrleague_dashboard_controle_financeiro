import pandas as pd

#dataframes
df_receitas = pd.read_excel('data/receitas_2022.xlsx')
df_despesas = pd.read_excel('data/despesas_2022.xlsx')

#primeira alteração dataset
df_receitas.rename(columns={"VALOR": "VALOR_RECEITA"}, inplace=True)
df_despesas.rename(columns={"VALOR":'VALOR_DESPESA'}, inplace=True)

# lista meses
lista_meses = df_receitas['COMPETÊNCIA'].unique().tolist()
lista_meses.append('Ano')

# lista opções gráficos
lista_drop_esquerda = ['Análise', 'Fluxo de Caixa']
lista_filtragem_categoria = ['Receitas por categoria', 'Despesas por Categoria']
lista_tipo_fluxo_caixa = ['Fluxo caixa mes/mes', 'Cashflow ano']


#fluxo caixa anual, dataframes:
df_receitas_graph_01 = df_receitas.groupby('COMPETÊNCIA', sort=False).agg({'VALOR_RECEITA':'sum'}).reset_index()
df_despesas_graph_01 = df_despesas.groupby('COMPETÊNCIA', sort=False).agg({'VALOR_DESPESA':'sum'}).reset_index()

#dataframe year_cashflow
df_year_cashflow = pd.merge(df_receitas_graph_01, df_despesas_graph_01, how='inner',on='COMPETÊNCIA')
df_year_cashflow['CASH_FLOW'] = df_year_cashflow['VALOR_RECEITA']-df_year_cashflow['VALOR_DESPESA']

