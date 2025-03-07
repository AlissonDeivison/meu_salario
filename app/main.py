import streamlit as st
from components.personal_stats import render_personal_stats
from components.salary_comparison import render_salary_comparison
from components.crewai_agent import kickoff  # Importando a função kickoff

st.set_page_config(layout="wide", page_title="Análise de Certificados e Pesquisas", page_icon="📚")

st.markdown("<h1 style='text-align: center;'>📚 Resumo das Análises</h1>", unsafe_allow_html=True)

with st.expander("📊 **Estatísticas Pessoais**", expanded=True):
    render_personal_stats()

with st.expander("💼 **Comparativo de Salários**", expanded=False):
    render_salary_comparison()

# Campo de entrada para pergunta do usuário
user_question = st.text_input("Digite sua pergunta:")

if user_question:
    try:
        st.write("🔄 Buscando informações...")

        # Executar a consulta e obter a resposta
        result = kickoff(user_question)

        if result:
            context_info = result.get("context", "Sem contexto disponível")
            web_info = result.get("web_info", "Nenhuma informação da web encontrada.")
            formatted_result = result.get("answer", "Resposta não encontrada")

            # Exibir o contexto de certificados
            with st.expander("📜 **Contexto Utilizado (Certificados)**"):
                st.markdown(context_info)

            # Exibir a pesquisa na web
            with st.expander("🌐 **Pesquisa na Web**"):
                st.markdown(web_info)

            # Exibir a resposta formatada diretamente em Markdown
            with st.expander("📝 **Resposta Formatada**"):
                st.markdown(formatted_result)
        else:
            st.write("Nenhum resultado retornado.")
    except Exception as e:
        st.write(f"Ocorreu um erro: {str(e)}")
else:
    st.write("Por favor, preencha a pergunta.")

st.markdown("---")
st.markdown("Feito por Alisson Deivison")
