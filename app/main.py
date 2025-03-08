import streamlit as st
from components.personal_stats import render_personal_stats, render_competenses, render_soft_skills
# Assumindo que a função kickoff está no arquivo crewai_agent
from components.crewai_agent import kickoff


# Função para gerar o resumo ou detalhamento sobre o usuário
def obter_resumo(tipo):
    if tipo == "resumo":
        pergunta = "Escreva um resumo sobre mim que seja atrativo para recrutadores, mas comece com uma saudação amigável dando boas-vindas e continuando com o resumo. Considerando que sou um desenvolvedor de software com foco em IA e WEB a partir do Angular atualmente e todos os meus certificados. Você deve responder como se fosse eu mesmo falando, ou seja, em primeira pessoa. Ao fim, convidar a pessoa para explorar mais informações disponíveis abaixo."
    else:
        pergunta = "Descreva detalhadamente sobre mim, incluindo minhas habilidades, certificações, experiência e qualificações."

    # Chama a função kickoff passando a pergunta e o tipo de descrição
    resposta = kickoff(pergunta, tipo)

    return resposta["answer"]


st.set_page_config(page_title="Portfólio", page_icon="👨‍💻", layout="wide")


# Verifique se a resposta já foi gerada e armazenada no session_state
if 'resumo_ou_detalhado' not in st.session_state:
    # Fazer a requisição automática com o tipo 'resumo' ao entrar na página
    st.session_state.resumo_ou_detalhado = obter_resumo("resumo")

# Exibir o resumo gerado pela LLM
st.sidebar.markdown(f"""
                    <div style="text-align: center;">
                    <img src="https://avatars.githubusercontent.com/u/102561569?v=4" width="250" style="border-radius: 20%;">
                    </div>
                    <div style="text-align: justify;">
                    <h2> Um pouco sobre mim </h2>
                    {st.session_state.resumo_ou_detalhado}
                    </div>
                    """, unsafe_allow_html=True)

# Melhorando a interação da sidebar com uma lista suspensa para outras seções
opcao = st.sidebar.selectbox("Explore mais sobre mim:",
                             ["Educação e Capacitação", "Habilidades Técnicas", "Soft Skills"])

# Definindo a interação das opções
if opcao == "Educação e Capacitação":
    st.markdown(""" 
                    <div style="text-align: justify;">
                    <h3>Educação e Capacitação</h3>

                    Recentemente, finalizei cursos avançados em <strong>TypeScript</strong> e <strong>desenvolvimento de aplicações com IA</strong>, incluindo a criação de fluxos de automação inteligente e pipelines para <strong>Large Language Models</strong>. 
                    Minha experiência prática é complementada por um forte entendimento dos fundamentos da web, incluindo <strong>HTTP</strong> e <strong>controle de versão com Git e GitHub</strong>.
                    Abaixo você pode conferir grande parte dos meus certificados e cursos realizados.
                    </div>
                    """, unsafe_allow_html=True)
    st.write("📊 **Estatísticas Pessoais**")
    render_personal_stats()

elif opcao == "Habilidades Técnicas":
    st.markdown("""
        <div style="text-align: justify;">
            <h3>🛠️ Habilidades Técnicas</h3>
            <ul>
                <li><strong>Desenvolvimento Web:</strong> React (componentização, hooks, estado, TypeScript), Angular (CRUD, Material Design), JavaScript avançado.</li>
                <li><strong>Inteligência Artificial:</strong> IA Generativa (Midjourney, ChatGPT), Automação Inteligente com n8n, pipelines avançados com LangChain.</li>
                <li><strong>Metodologias Ágeis:</strong> Gestão Ágil, Scrum, Kanban, SIPOC, VSM.</li>
                <li><strong>Controle de Versão:</strong> Git e GitHub (branching, versionamento, resolução de conflitos, colaboração).</li>
                <li><strong>Fundamentos Web:</strong> Protocolos HTTP/HTTPS, APIs REST, deploy em Vercel, CI/CD.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    render_competenses()
elif opcao == "Soft Skills":
    st.markdown(""" 
                    <div style="text-align: justify;">
                    <h3>Soft Skills</h3>

                    Sou um colaborador proativo, sempre em busca de aprender e implementar novas tecnologias, e tenho um histórico de participação em projetos de mapeamento de oportunidades tecnológicas. 
                    Estou preparado para enfrentar desafios complexos e contribuir para o sucesso de equipes dinâmicas e inovadoras.
                    </div>
                    """, unsafe_allow_html=True)
    render_soft_skills()

st.sidebar.markdown("""
                    <h2>Caso queira obter algum outro detalhe sobre mim, basta perguntar</h2>
                    """, unsafe_allow_html=True)
pergunta_especifica = st.sidebar.chat_input("Escreva sua pergunta aqui...")

if pergunta_especifica:
    resposta = kickoff(pergunta_especifica, "detalhado")
    st.sidebar.markdown(f"""
                        <div style="text-align: justify;">
                        <h3>Resposta:</h3>
                        {resposta["answer"]}
                        </div>
                        """, unsafe_allow_html=True)