import requests
import base64
import os
import json
import pandas as pd
from datetime import datetime

class GitHubStorage:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.owner = os.environ.get('REPO_OWNER')
        self.repo = os.environ.get('REPO_NAME')
        self.enabled = all([self.token, self.owner, self.repo])
        
        if not self.enabled:
            print("⚠️ GitHub Storage desabilitado - variáveis de ambiente não configuradas")
    
    def _get_file_sha(self, filename):
        """Pega o SHA atual do arquivo no GitHub"""
        if not self.enabled:
            return None
            
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{filename}"
        headers = {'Authorization': f'token {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()['sha']
        except Exception as e:
            print(f"Erro ao obter SHA: {e}")
        return None
    
    def salvar_csv(self, filename, dataframe):
        """Salva DataFrame como CSV no GitHub"""
        if not self.enabled:
            # Fallback: salvar localmente
            dataframe.to_csv(filename)
            return True
        
        try:
            # Converter DataFrame para CSV string
            csv_content = dataframe.to_csv(index=True)
            
            # Codificar em base64
            content_encoded = base64.b64encode(csv_content.encode()).decode()
            
            # URL da API
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{filename}"
            
            # Headers
            headers = {
                'Authorization': f'token {self.token}',
                'Content-Type': 'application/json'
            }
            
            # Pegar SHA atual (se arquivo existir)
            sha = self._get_file_sha(filename)
            
            # Dados do commit
            data = {
                'message': f'🤖 Auto-update: {filename} - {datetime.now().strftime("%d/%m/%Y %H:%M")}',
                'content': content_encoded,
                'branch': 'main'
            }
            
            if sha:
                data['sha'] = sha
            
            # Fazer commit
            response = requests.put(url, headers=headers, data=json.dumps(data), timeout=15)
            
            if response.status_code in [200, 201]:
                print(f"✅ {filename} salvo no GitHub com sucesso!")
                return True
            else:
                print(f"❌ Erro ao salvar {filename}: {response.status_code}")
                # Fallback: salvar localmente
                dataframe.to_csv(filename)
                return False
                
        except Exception as e:
            print(f"❌ Erro no GitHub Storage: {e}")
            # Fallback: salvar localmente
            dataframe.to_csv(filename)
            return False
    
    def salvar_receitas(self, df_receitas):
        """Salva DataFrame de receitas"""
        return self.salvar_csv("df_receitas.csv", df_receitas)
    
    def salvar_despesas(self, df_despesas):
        """Salva DataFrame de despesas"""
        return self.salvar_csv("df_despesas.csv", df_despesas)
    
    def salvar_categorias_receitas(self, df_cat_receitas):
        """Salva categorias de receitas"""
        return self.salvar_csv("df_cat_receita.csv", df_cat_receitas)
    
    def salvar_categorias_despesas(self, df_cat_despesas):
        """Salva categorias de despesas"""
        return self.salvar_csv("df_cat_despesa.csv", df_cat_despesas)

# Instância global
github_storage = GitHubStorage()