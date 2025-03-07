# Usar imagem base do Python 3.10
FROM python:3.10-slim

# Atualizar pacotes do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar apenas o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt ./

# Atualizar o pip e instalar as dependências do projeto
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar a pasta de dados primeiro (garantindo que esteja no container)
COPY app/data/ /app/data/

# Copiar o restante dos arquivos do projeto
COPY . .

# Garantir permissões de leitura nos arquivos de dados
RUN chmod -R 755 /app/data

# Expor a porta utilizada pelo Streamlit (padrão 8501)
EXPOSE 8501

# Comando para iniciar a aplicação, garantindo que o Streamlit escute em todas as interfaces
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
