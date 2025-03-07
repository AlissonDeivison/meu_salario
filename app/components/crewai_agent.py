import openai
import os
import pandas as pd
from dotenv import load_dotenv
import litellm
from crewai import Agent, Task, Crew

# Carregar variáveis do ambiente
load_dotenv()

# Configurar chave da API da OpenAI no litellm
openai.api_key = os.getenv('OPENAI_API_KEY')
litellm.api_key = os.getenv('OPENAI_API_KEY')

# Caminho do arquivo de certificados
CERTIFICADOS_PATH = "app/data/certificados.csv"

def carregar_certificados():
    """
    Lê o arquivo CSV de certificados e gera um contexto estruturado para a IA.
    """
    if not os.path.exists(CERTIFICADOS_PATH):
        return "⚠️ Arquivo de certificados não encontrado."

    try:
        df = pd.read_csv(CERTIFICADOS_PATH)

        if df.empty:
            return "⚠️ O arquivo de certificados está vazio."

        # Selecionar apenas os certificados relevantes para o contexto
        certificados_info = "\n".join(
            [f"- **{row['title']}** (Conclusão: {row['date']}, {row['hours']} horas)\n  {row['description']}" 
             for _, row in df.iterrows()]
        )

        return f"📜 O usuário possui os seguintes certificados:\n\n{certificados_info}"
    except Exception as e:
        return f"⚠️ Erro ao ler o arquivo de certificados: {str(e)}"

def create_agents_and_tasks():
    """
    Cria os agentes e as tarefas para o CrewAI.
    """
    model_name = "gpt-4o-mini"

    # Agente de Contexto (Lê os certificados antes de responder)
    context_agent = Agent(
        role="Agente de Contexto",
        goal="Fornecer informações detalhadas sobre os certificados do usuário",
        backstory="Você é um especialista em certificações e cursos de tecnologia e fornecerá detalhes relevantes."
    )

    context_task = Task(
        description="Gerar um resumo dos certificados do usuário.",
        agent=context_agent,
        expected_output="Texto detalhado sobre os certificados concluídos e suas respectivas descrições.",
        model=model_name,
    )

    # Agente de Respostas (Considera o contexto antes de responder)
    response_agent = Agent(
        role="Assistente de Respostas",
        goal="Responder perguntas considerando os certificados do usuário",
        backstory="Você é um assistente especializado em carreira e certificações de tecnologia. Seu papel é fornecer respostas precisas e relevantes. Se for solicitado para mensurar um valor, forneça uma estimativa baseada nos certificados."
    )

    response_task = Task(
        description="Responder perguntas do usuário considerando seus certificados.",
        agent=response_agent,
        expected_output="Resposta em Markdown baseada nos certificados.",
        model=model_name,
    )

    crew = Crew(agents=[context_agent, response_agent], tasks=[context_task, response_task])

    return crew, context_task, response_task

def ask_openai(question, context):
    """
    Chama a API da OpenAI passando o contexto dos certificados e a pergunta do usuário.
    """
    try:
        response = litellm.completion(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Contexto sobre os certificados do usuário:\n{context}"},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Ocorreu um erro ao chamar a API da OpenAI: {str(e)}"

def kickoff(question):
    """
    Executa o Agente de Contexto antes da OpenAI para enriquecer a resposta.
    """
    crew, context_task, response_task = create_agents_and_tasks()

    # Carregar contexto dos certificados a partir do CSV
    context = carregar_certificados()

    # Chama a OpenAI com o contexto carregado
    result = ask_openai(question, context)

    return {
        "crew": crew.dict(),
        "context": context,
        "answer": result
    }
