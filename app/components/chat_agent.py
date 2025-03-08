import streamlit as st
from components.personal_stats import render_personal_stats
from components.salary_comparison import render_salary_comparison
from components.crewai_agent import kickoff  

def get_summary_or_details(tipo: str):
    """
    Função para obter uma resposta da LLM baseada no tipo (resumo ou detalhado).
    - Se tipo for 'resumo', pede um resumo.
    - Se tipo for 'detalhado', segue o fluxo normal para obter uma resposta completa.
    """
    # Definir perguntas dependendo do tipo
    if tipo == "resumo":
        user_question = st.selectbox(
            "Escolha uma das perguntas abaixo:",
            [
                "Escreva um resumo sobre mim que seja atrativo para recrutadores. Considerando que sou um desenvolvedor de software com foco em IA e WEB atualmente e todos os meus certificados.",
            ]
        )
    elif tipo == "detalhado":
        user_question = st.selectbox(
            "Escolha uma das perguntas abaixo:",
            [
                "Escreva um resumo sobre mim que seja atrativo para recrutadores. Considerando que sou um desenvolvedor de software com foco em IA e WEB atualmente e todos os meus certificados.",
                "O que minhas certificações dizem sobre minha colocação no mercado de desenvolvimento?",
                "Quais as perspectivas para o mercado de IA no Brasil e como minhas competências podem ajudar?"
            ]
        )
    else:
        st.write("Tipo inválido. Por favor, escolha 'resumo' ou 'detalhado'.")
        return

    # Botão para iniciar a busca
    if st.button("Iniciar busca"):
        if user_question:
            try:
                # Exibir a mensagem indicando que a busca começou
                st.write("🔄 Buscando informações...")

                # Executar a consulta e obter a resposta
                result = kickoff(user_question, tipo)

                if result:
                    context_info = result.get("context", "Sem contexto disponível")
                    web_info = result.get("web_info", "Nenhuma informação da web encontrada.")
                    formatted_result = result.get("answer", "Resposta não encontrada")

                    # Atualizar o texto para mostrar os resultados
                    st.write("📊 Aqui estão os resultados da sua busca")

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
            st.write("Por favor, escolha uma pergunta.")
