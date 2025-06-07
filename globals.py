import pandas as pd
import os

# Dataframe despesas e receitas
if ("df_despesas.csv" in os.listdir()) and ("df_receitas.csv" in os.listdir()):
     df_despesas = pd.read_csv("df_despesas.csv", index_col=0)
     df_receitas = pd.read_csv("df_receitas.csv", index_col=0)
     
     # Tratamento de datas - Especificando o formato explicitamente
     df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], format='%Y-%m-%d', errors='coerce')
     df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], format='%Y-%m-%d', errors='coerce')
     
     # Convertendo para tipo date
     df_despesas["Data"] = df_despesas["Data"].apply(lambda x: x.date() if pd.notna(x) else None)
     df_receitas["Data"] = df_receitas["Data"].apply(lambda x: x.date() if pd.notna(x) else None)
     
else:
    data_structure = {
        'Valor': [], 
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descricão': [],
    }
    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)
    df_despesas.to_csv("df_despesas.csv")
    df_receitas.to_csv("df_receitas.csv")
    
# Dataframe categorias
if ("df_cat_despesa.csv" in os.listdir()) and ("df_cat_receita.csv" in os.listdir()):
    df_cat_despesa = pd.read_csv("df_cat_despesa.csv", index_col=0)
    df_cat_receita = pd.read_csv("df_cat_receita.csv", index_col=0)
    cat_receita = df_cat_receita.values.tolist()
    cat_despesa = df_cat_despesa.values.tolist()
else:
    cat_receita = {'Categoria': ['Salário', 'Vale', 'VR alimentacão']}
    cat_despesa = {'Categoria': ['Compras Mês', 'Estacionamento', 'Gasolina', 'Internet', 'Luz']}
    
    df_cat_receita = pd.DataFrame(cat_receita)
    df_cat_despesa = pd.DataFrame(cat_despesa)
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    df_cat_receita.to_csv("df_cat_receita.csv")