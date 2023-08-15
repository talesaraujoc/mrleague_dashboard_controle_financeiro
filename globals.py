import pandas as pd

#dataframes
df_receitas = pd.read_excel('data/receitas_2022.xlsx')
df_despesas = pd.read_excel('data/despesas_2022.xlsx')




# lista meses
lista_meses = df_receitas['COMPETÊNCIA'].unique().tolist()
lista_meses.append('Ano')