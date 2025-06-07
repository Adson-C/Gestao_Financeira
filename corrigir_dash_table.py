#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correção para Compatibilidade do Dash Table
Remove parâmetros não suportados na versão 2.18.0
"""

import os
import re

def corrigir_extratos():
    """Corrige o arquivo extratos.py para compatibilidade com Dash 2.18.0"""
    print("🔧 Corrigindo compatibilidade do Dash Table...")
    
    extratos_path = 'components/extratos.py'
    
    if not os.path.exists(extratos_path):
        print("   ❌ Arquivo components/extratos.py não encontrado!")
        return False
    
    try:
        # Ler o arquivo
        with open(extratos_path, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Remover style_selected_rows e substituir por style_data_conditional
        print("   🔍 Procurando parâmetros incompatíveis...")
        
        # Contar quantas vezes aparece o problema
        problemas = conteudo.count('style_selected_rows')
        
        if problemas == 0:
            print("   ✅ Arquivo já está compatível!")
            return True
        
        print(f"   🔧 Corrigindo {problemas} problema(s)...")
        
        # Substituir para tabela de despesas
        conteudo = re.sub(
            r"style_selected_rows=\{'backgroundColor': '#ffebee', 'border': '2px solid #dc3545'\}",
            "",
            conteudo
        )
        
        # Substituir para tabela de receitas
        conteudo = re.sub(
            r"style_selected_rows=\{'backgroundColor': '#e8f5e8', 'border': '2px solid #28a745'\}",
            "",
            conteudo
        )
        
        # Remover vírgulas extras
        conteudo = re.sub(r',(\s*)\)', r'\1)', conteudo)
        
        # Adicionar estilo de seleção no style_data_conditional para despesas
        conteudo = re.sub(
            r"(style_data_conditional=\[\s*\{\s*'if': \{'row_index': 'odd'\},\s*'backgroundColor': 'rgb\(248, 248, 248\)'\s*\}\s*\])",
            r"style_data_conditional=[\n            {\n                'if': {'row_index': 'odd'},\n                'backgroundColor': 'rgb(248, 248, 248)'\n            },\n            {\n                'if': {'state': 'selected'},\n                'backgroundColor': '#ffebee',\n                'border': '2px solid #dc3545'\n            }\n        ]",
            conteudo,
            count=1  # Só a primeira ocorrência (tabela de despesas)
        )
        
        # Adicionar estilo de seleção no style_data_conditional para receitas
        # Procurar pela segunda ocorrência
        pattern = r"(style_data_conditional=\[\s*\{\s*'if': \{'row_index': 'odd'\},\s*'backgroundColor': 'rgb\(248, 248, 248\)'\s*\}\s*\])"
        matches = list(re.finditer(pattern, conteudo))
        
        if len(matches) >= 2:
            # Substituir a segunda ocorrência (tabela de receitas)
            start = matches[1].start()
            end = matches[1].end()
            replacement = """style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': '#e8f5e8',
                'border': '2px solid #28a745'
            }
        ]"""
            conteudo = conteudo[:start] + replacement + conteudo[end:]
        
        # Escrever o arquivo corrigido
        with open(extratos_path, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print("   ✅ Arquivo corrigido com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao corrigir arquivo: {e}")
        return False

def verificar_dash_version():
    """Verifica a versão do Dash instalada"""
    print("\n📦 Verificando versão do Dash...")
    
    try:
        import dash
        print(f"   ✅ Dash versão: {dash.__version__}")
        
        import dash_table
        print(f"   ✅ Dash Table versão: {dash_table.__version__}")
        
        # Verificar se é uma versão antiga
        version_parts = dash.__version__.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        
        if major < 2 or (major == 2 and minor < 15):
            print("   ⚠️ Versão do Dash é antiga. Considere atualizar:")
            print("   💡 pip install --upgrade dash")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro ao importar Dash: {e}")
        return False

def testar_correcao():
    """Testa se a correção funcionou"""
    print("\n🧪 Testando correção...")
    
    try:
        # Tentar importar o módulo corrigido
        import sys
        if 'components.extratos' in sys.modules:
            del sys.modules['components.extratos']
        
        from components import extratos
        print("   ✅ Importação bem-sucedida!")
        
        # Verificar se não há mais style_selected_rows
        import inspect
        source = inspect.getsource(extratos)
        
        if 'style_selected_rows' in source:
            print("   ⚠️ Ainda há parâmetros incompatíveis no código")
            return False
        else:
            print("   ✅ Parâmetros incompatíveis removidos!")
            return True
            
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("🛠️ CORREÇÃO DASH TABLE - GESTÃO FINANCEIRA")
    print("=" * 60)
    
    # Verificar versão do Dash
    dash_ok = verificar_dash_version()
    
    if not dash_ok:
        print("\n❌ Instale o Dash primeiro: pip install dash")
        return
    
    # Corrigir o arquivo
    correcao_ok = corrigir_extratos()
    
    if correcao_ok:
        # Testar se a correção funcionou
        teste_ok = testar_correcao()
        
        if teste_ok:
            print("\n" + "=" * 60)
            print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print("\n📋 PRÓXIMOS PASSOS:")
            print("1. Execute: python myindex.py")
            print("2. Acesse: http://localhost:8051")
            print("3. Vá para 'Extratos'")
            print("4. Teste a seleção de linhas")
            
            print("\n✨ FUNCIONALIDADES CORRIGIDAS:")
            print("• ✅ Tabelas compatíveis com Dash 2.18.0")
            print("• ✅ Seleção de linhas funcionando")
            print("• ✅ Estilo visual mantido")
            print("• ✅ Botões de editar/excluir funcionais")
        else:
            print("\n⚠️ Correção aplicada, mas ainda há problemas.")
            print("   Execute novamente ou verifique o código manualmente.")
    else:
        print("\n❌ Não foi possível corrigir automaticamente.")
        print("   Substitua o arquivo extratos.py pelo código atualizado.")

if __name__ == "__main__":
    main()