import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para usar o width total (DEVE SER A PRIMEIRA CHAMADA)
st.set_page_config(
    layout="wide", page_title="Análise de Certificados e Salários", page_icon="📚"
)

# Carregar dados
def load_data():
    data = pd.read_csv('certificates.csv')
    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    return data

# Gráfico de dispersão com legenda oculta
def scatter_plot(data):
    fig = px.scatter(
        data,
        x='date',
        y='hours',
        color='title',
        hover_data=['title', 'description'],
        title='📊 Horas de Certificados por Data'
    )
    fig.update_layout(showlegend=False)  # Ocultar legenda inicialmente
    return fig

# Gráfico de barras com legenda oculta
def bar_plot(data):
    fig = px.bar(
        data.sort_values('date'),
        x='date',
        y='hours',
        color='title',
        title='📈 Progressão de Horas'
    )
    fig.update_layout(showlegend=False)
    return fig

# Gráfico de linhas para o comparativo de salários
def line_plot(data):
    fig = px.line(
        data,
        x='Cargo',
        y='Média Salarial (R$)',
        title='📉 Comparação Salarial ao Longo do Tempo',
        markers=True,
        text='Média Salarial (R$)'
    )
    fig.add_hline(y=3500, line_dash="dash", line_color="red", annotation_text="Seu Salário Atual")
    fig.update_traces(textposition='top center')
    return fig

# Estilo CSS para as caixas com sombra
st.markdown("""
<style>
.container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
    width: 100%;
}
.custom-box {
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    width: calc(50% - 10px); /* 2 colunas com gap de 20px */
    box-sizing: border-box;
}
.custom-box h4 {
    color: #2E86C1;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)

# Função para criar uma caixa estilizada
def create_box(title, content):
    st.markdown(f"""
    <div class="custom-box">
        <h4>{title}</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Carregar dados
data = load_data()

# Título do app centralizado
st.markdown("<h1 style='text-align: center;'>📚 Resumo das Análises</h1>", unsafe_allow_html=True)

# Dropdown 1: Estatísticas Pessoais
with st.expander("📊 **Estatísticas Pessoais**", expanded=True):
    # Linha de separação
    st.divider()

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

    # Linha de separação
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

    # Container para as caixas de competências
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

# Dropdown 2: Comparativo de Salários
with st.expander("💼 **Comparativo de Salários**", expanded=False):
    st.write("🚧 **Em construção** 🚧")
    
    # Dados de exemplo para o comparativo de salários
    salarios = pd.DataFrame({
        "Cargo": ["Júnior", "Pleno", "Sênior"],
        "Média Salarial (R$)": [4000, 7500, 12000],
        "Seu Salário": [3500, None, None]
    })

    # Layout flexível para gráficos
    col5, col6 = st.columns(2)

    with col5:
        # Gráfico de barras para comparação salarial
        fig_bar = px.bar(
            salarios,
            x="Cargo",
            y="Média Salarial (R$)",
            title="📊 Comparação Salarial",
            text="Média Salarial (R$)"
        )
        fig_bar.add_hline(y=3500, line_dash="dash", line_color="red", annotation_text="Seu Salário Atual")
        st.plotly_chart(fig_bar, use_container_width=True)

    # with col6:
    #     # Gráfico de linhas para comparação salarial
    #     fig_line = line_plot(salarios)
    #     st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

# Rodapé
st.markdown("---")
st.markdown("Feito por Alisson Deivison")