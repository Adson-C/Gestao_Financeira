# Gestão Financeira - Controle seus gastos

## 🎯 Sobre o Projeto
Sistema completo de gestão financeira pessoal desenvolvido em Python com Dash e Plotly. Permite controlar receitas e despesas de forma intuitiva e visual.

## ✨ Funcionalidades Implementadas

### 📊 Dashboard Principal
- **Cards de resumo**: Saldo total, receitas e despesas
- **Gráficos interativos**:
  - Linha temporal de receitas e despesas acumuladas
  - Gráfico de barras por período
  - Gráficos de pizza para receitas e despesas por categoria
- **Filtros dinâmicos**: Por categoria e período de análise

### 💰 Gestão de Receitas
- ✅ **Adicionar receitas** com descrição, valor, data e categoria
- ✅ **Editar receitas existentes** - NOVA FUNCIONALIDADE
- ✅ **Excluir receitas** - NOVA FUNCIONALIDADE
- ✅ **Categorização personalizada**
- ✅ **Marcação como recebida/pendente**
- ✅ **Receitas recorrentes**

### 💸 Gestão de Despesas
- ✅ **Adicionar despesas** com descrição, valor, data e categoria
- ✅ **Editar despesas existentes** - NOVA FUNCIONALIDADE
- ✅ **Excluir despesas** - NOVA FUNCIONALIDADE
- ✅ **Categorização personalizada**
- ✅ **Marcação como efetuada/pendente**
- ✅ **Despesas recorrentes**

### 📋 Extratos Detalhados
- **Tabelas interativas** com filtros e ordenação
- **Seleção de registros** para edição ou exclusão
- **Botões de ação** para cada operação
- **Cards de totais** por categoria
- **Gráficos de barras** por categoria

### 🎨 Interface e Usabilidade
- **Design responsivo** com Bootstrap
- **Tema personalizável** (claro/escuro)
- **Navegação intuitiva** entre páginas
- **Modais para operações** CRUD
- **Validação de dados** em tempo real

## 🚀 Como Usar

### Instalação
```bash
pip install -r requirements.txt
python myindex.py
```

### Acesso
- Abra o navegador em `http://localhost:8051`
- Navegue entre Dashboard e Extratos usando o menu lateral

### Adicionando Receitas/Despesas
1. Clique em **"+ Receita"** ou **"- Despesa"**
2. Preencha os campos obrigatórios
3. Selecione ou crie novas categorias
4. Marque as opções extras conforme necessário
5. Clique em **"Salvar"**

### Editando Registros - NOVA FUNCIONALIDADE
1. Vá para a página **"Extratos"**
2. Selecione um registro na tabela (clique na linha)
3. Clique em **"Editar Selecionado"**
4. Modifique os campos necessários no modal
5. Clique em **"Salvar"** para confirmar

### Excluindo Registros - NOVA FUNCIONALIDADE
1. Vá para a página **"Extratos"**
2. Selecione um registro na tabela (clique na linha)
3. Clique em **"Excluir Selecionado"**
4. O registro será removido permanentemente

### Gerenciando Categorias
1. No modal de receita/despesa
2. Expanda **"Adicionar/Remover Categorias"**
3. Adicione novas categorias ou remova existentes
4. As mudanças são salvas automaticamente

## 🛠 Melhorias Implementadas

### ✅ Sistema de Edição Completo
- Modais reutilizáveis para criação e edição
- Pré-preenchimento de campos ao editar
- Títulos dinâmicos nos modais
- Botão de cancelar para abortar operações

### ✅ Interface de Seleção
- Tabelas com seleção de linhas
- Botões habilitados/desabilitados conforme seleção
- Feedback visual de seleção

### ✅ Validação e Tratamento de Erros
- Validação de campos obrigatórios
- Tratamento de arquivos CSV ausentes
- Mensagens de erro informativas
- Fallbacks para dados corrompidos

### ✅ Experiência do Usuário
- Limpeza automática de campos ao criar novos registros
- Persistência de filtros entre páginas
- Loading states e feedback visual
- Layout responsivo para diferentes telas

## 📁 Estrutura do Projeto

```
gestao-financeira/
├── app.py                 # Configuração principal do Dash
├── myindex.py            # Layout principal e roteamento
├── globals.py            # Variáveis globais e dados
├── requirements.txt      # Dependências do projeto
├── components/
│   ├── sidebar.py        # Menu lateral e modais
│   ├── dashboards.py     # Página principal com gráficos
│   └── extratos.py       # Página de extratos e tabelas
├── assets/              # Imagens e estilos CSS
└── *.csv               # Arquivos de dados (gerados automaticamente)
```

## 💾 Persistência de Dados
- **df_receitas.csv**: Dados das receitas
- **df_despesas.csv**: Dados das despesas  
- **df_cat_receitas.csv**: Categorias de receitas
- **df_cat_despesas.csv**: Categorias de despesas

## 🎨 Temas e Personalização
- Suporte a temas claro e escuro
- Cores personalizáveis por categoria
- Ícones Font Awesome
- Componentes Bootstrap

## 🔄 Próximas Funcionalidades
- [ ] Relatórios em PDF
- [ ] Importação/Exportação de dados
- [ ] Metas financeiras
- [ ] Alertas de gastos
- [ ] Backup automático
- [ ] Múltiplos perfis de usuário

## 🐛 Correções Realizadas
- ✅ Tratamento de dados ausentes nas tabelas
- ✅ Validação de tipos de dados
- ✅ Sincronização de filtros entre páginas
- ✅ Correção de índices em operações de edição
- ✅ Melhoria na conversão de datas
- ✅ Otimização de callbacks do Dash

## 📞 Suporte
Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ por Adson Sá**

*Sistema de Gestão Financeira - Versão 2.0 com Edição Completa*