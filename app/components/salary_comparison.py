import streamlit as st
import pandas as pd
import plotly.express as px
from utils.plot_utils import line_plot

def render_salary_comparison():
    """Renderiza o componente de comparação salarial."""
    # Dados de exemplo para o comparativo de salários
    salarios = pd.DataFrame({
        "Cargo": ["Júnior", "Pleno", "Sênior"],
        "Média Salarial (R$)": [4000, 7500, 12000],
        "Seu Salário": [3500, None, None]
    })

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

    st.divider()