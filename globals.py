import pandas as pd

#dataframes
df_receitas = pd.read_excel('data/receitas_2023.xlsx')
df_despesas = pd.read_excel('data/despesas_2023.xlsx')

#table
df_table = pd.read_excel('data/controle_mensais_2023.xlsx')
df_table['PAGTO'] = df_table['PAGTO'].apply(lambda x: float(x))

#primeira alteração dataset
df_receitas.rename(columns={"VALOR": "VALOR_RECEITA"}, inplace=True)
df_despesas.rename(columns={"VALOR":'VALOR_DESPESA'}, inplace=True)

#segunda alteração dataset
df_receitas['MES'] = df_receitas['DATA'].apply(lambda x: x.month)
df_despesas['MES'] = df_despesas['DATA'].apply(lambda x: x.month)

#lista_receitas
lista_categorias_receitas = df_receitas['CATEGORIA'].unique()
#lista_despesas
lista_categorias_despesas = df_despesas['CATEGORIA'].unique()

# lista meses
lista_meses = df_receitas['COMPETÊNCIA'].unique().tolist()
lista_meses.append('Ano')

# lista opções gráficos
lista_drop_esquerda = ['Filtros', 'Fluxo de Caixa']
lista_filtragem_categoria = ['Receitas por categoria', 'Despesas por categoria']
lista_tipo_fluxo_caixa = ['Fluxo caixa mês/mês', 'Cashflow ano']


#fluxo caixa anual, dataframes:
df_receitas_graph_01 = df_receitas.groupby('COMPETÊNCIA', sort=False).agg({'VALOR_RECEITA':'sum'}).reset_index()
df_despesas_graph_01 = df_despesas.groupby('COMPETÊNCIA', sort=False).agg({'VALOR_DESPESA':'sum'}).reset_index()

#dataframe year_cashflow
df_year_cashflow = pd.merge(df_receitas_graph_01, df_despesas_graph_01, how='inner',on='COMPETÊNCIA')
df_year_cashflow['CASH_FLOW'] = df_year_cashflow['VALOR_RECEITA']-df_year_cashflow['VALOR_DESPESA']
df_year_cashflow['caixa'] = df_year_cashflow['CASH_FLOW'].cumsum()

janeiro_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Janeiro']['CASH_FLOW'].sum()
fevereiro_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Fevereiro']['CASH_FLOW'].sum()
marco_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Março']['CASH_FLOW'].sum()
abril_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Abril']['CASH_FLOW'].sum()
maio_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Maio']['CASH_FLOW'].sum()
junho_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Junho']['CASH_FLOW'].sum()
julho_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Julho']['CASH_FLOW'].sum()
agosto_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Agosto']['CASH_FLOW'].sum()
setembro_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Setembro']['CASH_FLOW'].sum()
outubro_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Outubro']['CASH_FLOW'].sum()
novembro_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Novembro']['CASH_FLOW'].sum()
dezembro_cashflow = df_year_cashflow[df_year_cashflow['COMPETÊNCIA']=='Dezembro']['CASH_FLOW'].sum()
            

#dataframe analise receitas/despesas
df_filter_incomes_detail = df_receitas.groupby('CATEGORIA').agg({'VALOR_RECEITA':'sum'})
df_filter_incomes_detail = df_filter_incomes_detail.reset_index()

df_filter_expenses_detail = df_despesas.groupby('CATEGORIA').agg({'VALOR_DESPESA':'sum'})
df_filter_expenses_detail = df_filter_expenses_detail.reset_index()

df_filter_expenses_months = df_despesas.groupby(['COMPETÊNCIA','CATEGORIA']).agg({'VALOR_DESPESA':'sum'})
df_filter_expenses_months = df_filter_expenses_months.reset_index()

df_filter_incomes_months = df_receitas.groupby(['COMPETÊNCIA','CATEGORIA']).agg({'VALOR_RECEITA':'sum'})
df_filter_incomes_months = df_filter_incomes_months.reset_index()


