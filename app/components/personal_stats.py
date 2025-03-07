import streamlit as st
from services.data_service import load_data
from utils.plot_utils import scatter_plot, bar_plot
from utils.style_utils import create_box, apply_custom_styles

def render_personal_stats():
    """Renderiza o componente de estatísticas pessoais."""
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Carregar dados
    data = load_data('certificados.csv')

    # Tabela simplificada
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

    st.divider()

    # Layout flexível para gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(scatter_plot(data), use_container_width=True)
    with col2:
        st.plotly_chart(bar_plot(data), use_container_width=True)

    st.divider()

    # Estatísticas
    st.write("### 📊 Estatísticas")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Total de Horas", f"{data['hours'].sum()} ⏳")
    with col4:
        st.metric("Média de Horas por Certificado", f"{data['hours'].mean():.1f} ⏳")

    st.divider()

    # Competências em caixas com sombra
    st.write("#### 🛠️ Competências Desenvolvidas")
    st.markdown("Principais competências que desenvolvi ao longo dos cursos, projetos e vivência profissional:")

    st.markdown("""
    <div class="container">
        <div class="custom-box">
            <h4>🖥️ Desenvolvimento Full Stack</h4>
            <ul>
                <li>Front-end: Angular, React, JavaScript, TypeScript, HTML, CSS.</li>
                <li>Back-end: APIs REST, Node.js, Express.js, Java.</li>
                <li>Integração entre front-end e back-end.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>🛠️ Ferramentas de Desenvolvimento</h4>
            <ul>
                <li>Git e GitHub: Controle de versão, branching, resolução de conflitos.</li>
                <li>Docker: Containerização de aplicações.</li>
                <li>Figma: Prototipagem de interfaces.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>📊 Gestão e Metodologias</h4>
            <ul>
                <li>Gestão Ágil: Scrum, Kanban, SIPOC, VSM.</li>
                <li>Liderança e Gestão de Pessoas.</li>
                <li>Mindset Empreendedor.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>🤖 Inteligência Artificial e Automação</h4>
            <ul>
                <li>LLMs (Large Language Models): Uso de LangChain para pipelines avançados.</li>
                <li>IA Generativa: Midjourney e ChatGPT.</li>
                <li>Automação com n8n.</li>
            </ul>
        </div>
        <div class="custom-box">
            <h4>📚 Outras Habilidades</h4>
            <ul>
                <li>HTTP/HTTPS: Entendimento profundo do protocolo HTTP e suas versões.</li>
                <li>TypeScript: Evolução do JavaScript com tipagem estática.</li>
                <li>Deploy de aplicações: Vercel, configuração de CI/CD.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()