def apply_custom_styles():
    """Aplica estilos CSS personalizados."""
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
        width: calc(50% - 10px); /* 2 colunas com gap de 20px */
        box-sizing: border-box;
    }
    .custom-box h4 {
        color: #2E86C1;
        margin-top: 0;
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