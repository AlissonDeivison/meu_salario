import plotly.express as px

def scatter_plot(data):
    """Cria um gráfico de dispersão."""
    fig = px.scatter(
        data,
        x='date',
        y='hours',
        color='title',
        hover_data=['title', 'description'],
        title='📊 Horas de Certificados por Data'
    )
    fig.update_layout(showlegend=False)
    return fig

def bar_plot(data):
    """Cria um gráfico de barras."""
    fig = px.bar(
        data.sort_values('date'),
        x='date',
        y='hours',
        color='title',
        title='📈 Progressão de Horas'
    )
    fig.update_layout(showlegend=False)
    return fig

def line_plot(data):
    """Cria um gráfico de linhas para comparação salarial."""
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