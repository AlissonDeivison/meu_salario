import streamlit as st
import pandas as pd
import plotly.express as px
from services.data_service import load_data
from utils.style_utils import apply_custom_styles

# Funções de visualização


def scatter_plot(data):
    """Cria um gráfico de dispersão ajustado para remover outliers."""
    # Detectar outliers usando IQR
    q1 = data['hours'].quantile(0.25)
    q3 = data['hours'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_data = data[(data['hours'] >= lower_bound) &
                          (data['hours'] <= upper_bound)]

    fig = px.scatter(filtered_data, x='date', y='hours',
                     color='title', title="Horas de Certificados por Data")
    fig.update_traces(marker=dict(size=8, opacity=0.7))
    fig.update_layout(template="plotly_dark")
    return fig


def bar_plot(data):
    """Cria um gráfico de barras ajustado para progressão mensal."""
    data['month'] = pd.to_datetime(
        data['date']).dt.to_period('M')  # Agrupar por mês
    monthly_hours = data.groupby('month')['hours'].sum().reset_index()
    monthly_hours['month'] = monthly_hours['month'].astype(str)

    fig = px.bar(monthly_hours, x='month', y='hours',
                 title="Progressão Mensal de Horas", text_auto=True)
    fig.update_traces(marker_color='blue', opacity=0.7)
    fig.update_layout(template="plotly_dark")
    return fig

# Função principal


def render_personal_stats():
    """Renderiza o componente de estatísticas pessoais."""
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Carregar dados
    data = load_data('certificados.csv')

    # Expander para certificados
    with st.expander("ℹ️ **Meus certificados**", expanded=True):
        st.write("### 📋 Certificados e Carga Horária")
        st.dataframe(
            data[['title', 'hours']],
            column_config={
                "title": "Título do Certificado",
                "hours": st.column_config.NumberColumn(
                    "Horas",
                    format="%.1f ⏳",
                    help="Carga horária total do certificado/projeto"
                )
            },
            hide_index=True,
            use_container_width=True
        )

    # Expander para gráficos
    with st.expander("📊 **Análises de horas**"):
        st.plotly_chart(scatter_plot(data), use_container_width=True)
        st.plotly_chart(bar_plot(data), use_container_width=True)

    st.divider()

    # Estatísticas gerais
    st.write("### 📊 Estatísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Horas", f"{data['hours'].sum()} ⏳")
    with col2:
        st.metric("Média de Horas por Certificado",
                  f"{data['hours'].mean():.1f} ⏳")

def render_competenses():
    
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Competências desenvolvidas
    st.write("#### 🛠️ Competências Desenvolvidas")
    st.markdown("""
    <div class="container">
        <div class="custom-box">
            <h4>🖥️ Desenvolvimento Full Stack</h4>
            <ul>
                <li>Front-end: React (componentização, hooks, arquivos estáticos), Angular (CRUD, Angular Material).</li>
                <li>Back-end: APIs REST com Node.js e Express.js.</li>
                <li>Manipulação de arquivos estáticos e integração entre front-end e back-end.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>📌 Desenvolvimento Web</h4>
            <ul>
                <li>JavaScript avançado: manipulação do DOM, programação assíncrona, Node.js.</li>
                <li>TypeScript: boas práticas, tipagem estática, configuração de projetos.</li>
                <li>HTTP: arquitetura, segurança (HTTPS), versões HTTP/2 e HTTP/3.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>🛠️ Ferramentas e Versionamento</h4>
            <ul>
                <li>Git e GitHub: versionamento, branching, resolução de conflitos.</li>
                <li>Docker: criação e gerenciamento de containers.</li>
                <li>Figma: prototipagem de layouts para sites e aplicações.</li>
                <li>Deploy: Vercel, CI/CD.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>📊 Gestão e Metodologias Ágeis</h4>
            <ul>
                <li>Gestão Ágil: Scrum, Kanban, SIPOC, VSM.</li>
                <li>Liderança e Gestão de Pessoas.</li>
                <li>Mindset Empreendedor e Estratégias de Inovação.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>🤖 Inteligência Artificial e Automação</h4>
            <ul>
                <li>IA Generativa: Midjourney, ChatGPT.</li>
                <li>Desenvolvimento de agentes de IA com n8n.</li>
                <li>Criação de pipelines avançados com LangChain.</li>
                <li>Implantação de IA generativa com Dify.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>🚀 Projetos Estratégicos</h4>
            <ul>
                <li>Projeto Atlas de Oportunidade: mapeamento e desenvolvimento de soluções tecnológicas.</li>
                <li>Participação em eventos e painéis de inovação.</li>
                <li>Primeiro lugar no ranking nacional do aplicativo Flexge.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_soft_skills():
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Soft skills
    st.write("#### 💬 Um pouco sobre")
    st.markdown("""
    <div class="container">
        <div class="custom-box">
            <h4>🤝 Trabalho em Equipe</h4>
            <p>Gosto de dividir tarefas e colaborar. Quando não conheço o assunto, escuto atentamente; quando conheço, exponho meu ponto de vista de forma clara.</p>
        </div>
        <div class="custom-box">
            <h4>🎤 Comunicação</h4>
            <p>Me sinto confortável apresentando em público, já gravei aulas para cursos de Sistemas de Informação.</p>
        </div>
        <div class="custom-box">
            <h4>🧑‍🏫 Liderança</h4>
            <p>Tenho experiência liderando equipes e trabalhando com estagiários, ensinando tecnologias e padrões de projeto.</p>
        </div>
        <div class="custom-box">
            <h4>📋 Organização e Processos</h4>
            <p>Prefiro seguir processos bem estruturados e evito improvisos sempre que possível.</p>
        </div>
        <div class="custom-box">
            <h4>📌 Gestão de Prioridades</h4>
            <p>Não utilizo ferramentas de organização pessoal, priorizo minhas tarefas conforme são solicitadas.</p>
        </div>
        <div class="custom-box">
            <h4>📚 Aprendizado Contínuo</h4>
            <p>Tenho certa resistência a mudanças tecnológicas, mas me adapto quando necessário. Aprender faz parte do meu dia a dia.</p>
        </div>
        <div class="custom-box">
            <h4>💡 Inovação</h4>
            <p>Já tentei inovar em algumas situações, mas sei que ainda preciso me dedicar mais a isso.</p>
        </div>
        <div class="custom-box">
            <h4>⚡ Tomada de Decisão</h4>
            <p>Em momentos que exigem decisões rápidas, priorizo resolver o problema de forma objetiva.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
