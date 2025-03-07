import streamlit as st
from components.personal_stats import render_personal_stats
from components.salary_comparison import render_salary_comparison



# Configuração da página
st.set_page_config(layout="wide", page_title="Análise de Certificados e Salários", page_icon="📚")

# Título do app centralizado
st.markdown("<h1 style='text-align: center;'>📚 Resumo das Análises</h1>", unsafe_allow_html=True)

# Dropdown 1: Estatísticas Pessoais
with st.expander("📊 **Estatísticas Pessoais**", expanded=True):
    render_personal_stats()

# Dropdown 2: Comparativo de Salários
with st.expander("💼 **Comparativo de Salários**", expanded=False):
    render_salary_comparison()

# Rodapé
st.markdown("---")
st.markdown("Feito por Alisson Deivison")