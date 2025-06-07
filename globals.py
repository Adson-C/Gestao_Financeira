import pandas as pd
import os
from datetime import datetime

# Dataframe despesas e receitas
if ("df_despesas.csv" in os.listdir()) and ("df_receitas.csv" in os.listdir()):
    try:
        df_despesas = pd.read_csv("df_despesas.csv", index_col=0)
        df_receitas = pd.read_csv("df_receitas.csv", index_col=0)
        
        # Tratamento de datas - Garantindo que as datas sejam válidas
        df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], errors='coerce')
        df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], errors='coerce')
        
        # Remover linhas com datas inválidas ou futuras
        data_atual = pd.Timestamp.now()
        df_despesas = df_despesas[df_despesas["Data"] <= data_atual]
        df_receitas = df_receitas[df_receitas["Data"] <= data_atual]
        
    except Exception as e:
        print(f"Erro ao carregar arquivos CSV: {e}")
        # Criar estrutura padrão em caso de erro
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
    try:
        df_cat_despesa = pd.read_csv("df_cat_despesa.csv", index_col=0)
        df_cat_receita = pd.read_csv("df_cat_receita.csv", index_col=0)
        
        # Converter para lista de strings (não lista de listas)
        cat_receita = df_cat_receita['Categoria'].tolist()
        cat_despesa = df_cat_despesa['Categoria'].tolist()
        
    except Exception as e:
        print(f"Erro ao carregar categorias: {e}")
        # Criar categorias padrão
        cat_receita = ['Salário', 'Vale', 'VR alimentação']
        cat_despesa = ['Compras Mês', 'Estacionamento', 'Gasolina', 'Internet', 'Luz', 'Saúde']
        
        df_cat_receita = pd.DataFrame({'Categoria': cat_receita})
        df_cat_despesa = pd.DataFrame({'Categoria': cat_despesa})
        df_cat_despesa.to_csv("df_cat_despesa.csv")
        df_cat_receita.to_csv("df_cat_receita.csv")
else:
    # Categorias padrão
    cat_receita = ['Salário', 'Vale', 'VR alimentação']
    cat_despesa = ['Compras Mês', 'Estacionamento', 'Gasolina', 'Internet', 'Luz', 'Saúde']
    
    df_cat_receita = pd.DataFrame({'Categoria': cat_receita})
    df_cat_despesa = pd.DataFrame({'Categoria': cat_despesa})
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    df_cat_receita.to_csv("df_cat_receita.csv")

# Função auxiliar para salvar dados
def save_dataframes():
    """Função para salvar todos os dataframes nos arquivos CSV"""
    try:
        # Garantir que as datas sejam válidas antes de salvar
        data_atual = pd.Timestamp.now()
        df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], errors='coerce')
        df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], errors='coerce')
        
        df_despesas = df_despesas[df_despesas["Data"] <= data_atual]
        df_receitas = df_receitas[df_receitas["Data"] <= data_atual]
        
        df_despesas.to_csv("df_despesas.csv")
        df_receitas.to_csv("df_receitas.csv")
        df_cat_despesa.to_csv("df_cat_despesa.csv")
        df_cat_receita.to_csv("df_cat_receita.csv")
        return True
    except Exception as e:
        print(f"Erro ao salvar dataframes: {e}")
        return False