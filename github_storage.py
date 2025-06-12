import requests
import base64
import os
import json
import pandas as pd
from datetime import datetime
import time

class GitHubStorage:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.owner = os.environ.get('REPO_OWNER')
        self.repo = os.environ.get('REPO_NAME')
        self.enabled = all([self.token, self.owner, self.repo])
        self.last_commit_time = {}  # Para evitar commits duplicados
        
        if not self.enabled:
            print("⚠️ GitHub Storage desabilitado - variáveis de ambiente não configuradas")
    
    def _should_commit(self, filename):
        """Verifica se deve fazer commit (evita spam de commits)"""
        now = time.time()
        last_time = self.last_commit_time.get(filename, 0)
        
        # Só permite commit a cada 30 segundos por arquivo
        if now - last_time < 30:
            return False
        
        self.last_commit_time[filename] = now
        return True
    
    def _get_file_content(self, filename):
        """Pega o conteúdo atual do arquivo no GitHub"""
        if not self.enabled:
            return None, None
            
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{filename}"
        headers = {'Authorization': f'token {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                content = base64.b64decode(data['content']).decode()
                return content, data['sha']
        except Exception as e:
            print(f"Erro ao obter conteúdo: {e}")
        return None, None
    
    def salvar_csv(self, filename, dataframe):
        """Salva DataFrame como CSV no GitHub (apenas se diferente)"""
        if not self.enabled:
            # Fallback: salvar localmente
            dataframe.to_csv(filename)
            return True
        
        # Verificar se deve fazer commit
        if not self._should_commit(filename):
            print(f"⏭️ Skipping commit for {filename} (too frequent)")
            return True
        
        try:
            # Converter DataFrame para CSV string
            new_csv_content = dataframe.to_csv(index=True)
            
            # Pegar conteúdo atual do GitHub
            current_content, sha = self._get_file_content(filename)
            
            # Se o conteúdo é igual, não faz commit
            if current_content == new_csv_content:
                print(f"📄 {filename} não modificado, skipping commit")
                return True
            
            # Codificar em base64
            content_encoded = base64.b64encode(new_csv_content.encode()).decode()
            
            # URL da API
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{filename}"
            
            # Headers
            headers = {
                'Authorization': f'token {self.token}',
                'Content-Type': 'application/json'
            }
            
            # Dados do commit
            data = {
                'message': f'📊 Update: {filename} - {datetime.now().strftime("%d/%m %H:%M")} [skip ci]',
                'content': content_encoded,
                'branch': 'main'
            }
            
            if sha:
                data['sha'] = sha
            
            # Fazer commit
            response = requests.put(url, headers=headers, data=json.dumps(data), timeout=15)
            
            if response.status_code in [200, 201]:
                print(f"✅ {filename} atualizado no GitHub!")
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