#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final - Verificação Rápida do Sistema
Valida se tudo está funcionando antes de executar
"""

import os
import pandas as pd
import importlib.util

def verificar_arquivo_extratos():
    """Verifica se o arquivo extratos.py foi atualizado corretamente"""
    print("🔍 Verificando extratos.py...")
    
    extratos_path = 'components/extratos.py'
    
    if not os.path.exists(extratos_path):
        print("   ❌ Arquivo components/extratos.py não encontrado!")
        return False
    
    try:
        with open(extratos_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar se tem as correções
        if 'Input("dropdown-receita"' in conteudo:
            print("   ❌ extratos.py ainda tem dependências do dashboard!")
            print("   💡 Substitua o arquivo pelo código corrigido")
            return False
        
        if 'Input("store-despesas", "data")' in conteudo and 'without dependency' not in conteudo:
            print("   ✅ extratos.py foi atualizado corretamente")
            return True
        else:
            print("   ⚠️ extratos.py pode não estar na versão correta")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao ler extratos.py: {e}")
        return False

def verificar_dados():
    """Verifica se há dados para exibir"""
    print("\n📊 Verificando dados...")
    
    arquivos_dados = [
        'df_receitas.csv',
        'df_despesas.csv',
        'df_cat_receita.csv',
        'df_cat_despesa.csv'
    ]
    
    dados_ok = True
    
    for arquivo in arquivos_dados:
        if os.path.exists(arquivo):
            try:
                df = pd.read_csv(arquivo)
                if len(df) > 0:
                    print(f"   ✅ {arquivo}: {len(df)} registros")
                else:
                    print(f"   ⚠️ {arquivo}: Vazio")
                    dados_ok = False
            except Exception as e:
                print(f"   ❌ {arquivo}: Erro - {e}")
                dados_ok = False
        else:
            print(f"   ❌ {arquivo}: Não encontrado")
            dados_ok = False
    
    return dados_ok

def verificar_imports():
    """Verifica se consegue importar os módulos"""
    print("\n📦 Verificando imports...")
    
    try:
        from app import app
        print("   ✅ app.py importado")
    except Exception as e:
        print(f"   ❌ Erro ao importar app.py: {e}")
        return False
    
    try:
        from components import extratos
        print("   ✅ components.extratos importado")
    except Exception as e:
        print(f"   ❌ Erro ao importar extratos: {e}")
        return False
    
    try:
        import dash_bootstrap_components as dbc
        print("   ✅ dash_bootstrap_components disponível")
    except Exception as e:
        print(f"   ❌ dash_bootstrap_components não encontrado: {e}")
        return False
    
    return True

def mostrar_instrucoes():
    """Mostra instruções de uso"""
    print("\n" + "="*60)
    print("📋 INSTRUÇÕES DE USO:")
    print("="*60)
    
    print("\n🚀 Para iniciar:")
    print("   python myindex.py")
    
    print("\n🌐 Acesse:")
    print("   http://localhost:8051")
    
    print("\n🎯 Para testar edição:")
    print("   1. Clique em 'Extratos' no menu lateral")
    print("   2. Clique em UMA LINHA da tabela")
    print("   3. Veja a linha ficar destacada")
    print("   4. Clique em '✏️ Editar Selecionado'")
    print("   5. Modal abre com dados pré-preenchidos")
    print("   6. Modifique e salve")
    
    print("\n📱 Interface esperada:")
    print("   • 💸 Tabela de Despesas (topo)")
    print("   • 📊 Gráfico de barras colorido")
    print("   • 💰 Card com total em reais")
    print("   • 💰 Tabela de Receitas (abaixo)")
    print("   • 📊 Gráfico de barras colorido")
    print("   • 💰 Card com total em reais")
    print("   • 🔘 Botões grandes e estilizados")

def main():
    """Função principal do teste"""
    print("🔬 TESTE FINAL - GESTÃO FINANCEIRA")
    print("="*60)
    
    # Executar verificações
    extratos_ok = verificar_arquivo_extratos()
    dados_ok = verificar_dados()
    imports_ok = verificar_imports()
    
    print("\n" + "="*60)
    print("📋 RESULTADO FINAL:")
    print("="*60)
    
    if extratos_ok and dados_ok and imports_ok:
        print("🎉 TUDO PERFEITO! Sistema pronto para uso!")
        mostrar_instrucoes()
        
    else:
        print("⚠️ PROBLEMAS ENCONTRADOS:")
        
        if not extratos_ok:
            print("\n🔧 SOLUÇÃO para extratos.py:")
            print("   1. Substitua components/extratos.py pelo código corrigido")
            print("   2. Execute novamente este teste")
        
        if not dados_ok:
            print("\n🔧 SOLUÇÃO para dados:")
            print("   1. Execute: python resolver_problemas.py")
            print("   2. Execute novamente este teste")
        
        if not imports_ok:
            print("\n🔧 SOLUÇÃO para imports:")
            print("   1. Execute: pip install -r requirements.txt")
            print("   2. Execute novamente este teste")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()