def apply_custom_styles():
    """Aplica estilos CSS personalizados para melhor responsividade."""
    return """
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
        width: calc(50% - 10px); /* 2 colunas com espaçamento */
        box-sizing: border-box;
    }

    .custom-box h4 {
        color: #2E86C1;
        margin-top: 0;
    }

    /* 🔹 Ajuste para tablets (largura menor que 768px) */
    @media (max-width: 768px) {
        .custom-box {
            width: 100%; /* Ocupa 100% da largura */
        }
    }

    /* 🔹 Ajuste para celulares menores (largura menor que 480px) */
    @media (max-width: 480px) {
        .container {
            gap: 10px; /* Reduz o espaçamento para melhor uso do espaço */
        }
        .custom-box {
            padding: 15px; /* Reduz o padding para evitar excesso de espaço */
        }
    }
    </style>
    """

def create_box(title, content):
    """Cria uma caixa estilizada."""
    return f"""
    <div class="custom-box">
        <h4>{title}</h4>
        {content}
    </div>
    """
