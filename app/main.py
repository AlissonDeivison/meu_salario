import streamlit as st
from components.personal_stats import render_personal_stats
from components.salary_comparison import render_salary_comparison
from components.crewai_agent import kickoff  # Importando a função kickoff

# Função para limpar e formatar a resposta
def clean_response(response):
    """
    Limpa a resposta removendo quebras de linha indesejadas e corrigindo formatação.
    """
    response = response.replace('\n', ' ')  # Substitui quebras de linha por espaço
    response = response.replace('R\n', 'R ')  # Corrige valores com "R" seguidos de quebra de linha
    response = ' '.join(response.split())  # Remove espaços extras
    return response

# Configuração da página do Streamlit
st.set_page_config(layout="wide", page_title="Análise de Certificados e Salários", page_icon="📚")

# Título do app centralizado
st.markdown("<h1 style='text-align: center;'>📚 Resumo das Análises</h1>", unsafe_allow_html=True)

# Dropdown 1: Estatísticas Pessoais (Adicionar funcionalidade)
with st.expander("📊 **Estatísticas Pessoais**", expanded=True):
    render_personal_stats()

# Dropdown 2: Comparativo de Salários (Adicionar funcionalidade)
with st.expander("💼 **Comparativo de Salários**", expanded=False):
    render_salary_comparison()

# Receber a pergunta do usuário
user_question = st.text_input("Digite sua pergunta:")

# Verificar se a pergunta foi preenchida
if user_question:
    try:
        st.write("Executando a consulta ao agente...")

        # Executar a consulta e obter a resposta
        result = kickoff(user_question)

        if result:
            # Verificar o tipo de resposta (se é um dicionário ou string)
            if isinstance(result, dict):
                formatted_result = clean_response(result.get('answer', 'Resposta não encontrada'))  # Acessando a resposta formatada
                raw_result = result  # Resposta bruta (JSON)

                # Exibir o resultado completo da consulta ao agente em um dropdown
                with st.expander("📄 **Resposta JSON do Agente**"):
                    st.json(raw_result)  # Exibe o JSON retornado pelo agente

                # Exibir a resposta formatada de forma limpa
                with st.expander("📝 **Resposta Formatada**"):
                    st.markdown(f"**Resposta:** {formatted_result}")
            else:
                st.write("Erro: a resposta não é um dicionário válido.", result)
        else:
            st.write("Nenhum resultado retornado.")
    except Exception as e:
        st.write(f"Ocorreu um erro: {str(e)}")
else:
    st.write("Por favor, preencha a pergunta.")

# Rodapé
st.markdown("---")
st.markdown("Feito por Alisson Deivison")
