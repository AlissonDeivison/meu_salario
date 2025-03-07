import streamlit as st
from components.personal_stats import render_personal_stats
from components.salary_comparison import render_salary_comparison
from components.crewai_agent import kickoff  # Importando a função kickoff

# Configuração da página do Streamlit
st.set_page_config(layout="wide", page_title="Análise de Certificados e Salários", page_icon="📚")

# Título do app centralizado
st.markdown("<h1 style='text-align: center;'>📚 Resumo das Análises</h1>", unsafe_allow_html=True)

# Dropdown 1: Estatísticas Pessoais
with st.expander("📊 **Estatísticas Pessoais**", expanded=True):
    render_personal_stats()

# Dropdown 2: Comparativo de Salários
with st.expander("💼 **Comparativo de Salários**", expanded=False):
    render_salary_comparison()

# Receber a pergunta do usuário
user_question = st.text_input("Digite sua pergunta:")

if user_question:
    try:
        st.write("Executando a consulta ao agente...")

        # Executar a consulta e obter a resposta
        result = kickoff(user_question)

        if result:
            crew_json = result.get("crew", {})  # JSON do CrewAI
            context_info = result.get("context", "Sem contexto disponível")  # Contexto usado
            formatted_result = result.get("answer", "Resposta não encontrada")  # Resposta da IA

            # Exibir o contexto utilizado
            with st.expander("📜 **Contexto Utilizado**"):
                st.markdown(context_info)

            # Exibir o JSON do CrewAI
            with st.expander("📄 **Resposta JSON do Agente**"):
                st.json(crew_json)

            # Exibir a resposta formatada diretamente em Markdown
            with st.expander("📝 **Resposta Formatada**"):
                st.markdown(formatted_result)
        else:
            st.write("Nenhum resultado retornado.")
    except Exception as e:
        st.write(f"Ocorreu um erro: {str(e)}")
else:
    st.write("Por favor, preencha a pergunta.")

# Rodapé
st.markdown("---")
st.markdown("Feito por Alisson Deivison")
