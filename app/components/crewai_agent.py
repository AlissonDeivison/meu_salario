import openai
import os
import pandas as pd
from dotenv import load_dotenv
import litellm
from crewai import Agent, Task, Crew
from duckduckgo_search import DDGS

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

        certificados_info = "\n".join(
            [f"- **{row['title']}** (Conclusão: {row['date']}, {row['hours']} horas)\n  {row['description']}" 
             for _, row in df.iterrows()]
        )

        return f"📜 O usuário possui os seguintes certificados:\n\n{certificados_info}"
    except Exception as e:
        return f"⚠️ Erro ao ler o arquivo de certificados: {str(e)}"

def pesquisar_na_web(query):
    """
    Faz uma pesquisa no DuckDuckGo e retorna um resumo dos principais resultados.
    """
    try:
        query_dev = f"{query} desenvolvimento programação software"
        with DDGS(headers={"User-Agent": "Mozilla/5.0"}) as ddgs:
            results = ddgs.text(query_dev, max_results=5, region="br-pt")

        if not results:
            return "⚠️ Nenhum resultado encontrado na pesquisa."

        pesquisa_resumo = "\n".join([f"- [{res['title']}]({res['href']}): {res['body']}" for res in results])

        return f"🔎 Aqui estão algumas informações da web sobre desenvolvedores:\n\n{pesquisa_resumo}"
    
    except Exception as e:
        return f"⚠️ Erro ao pesquisar na web: {str(e)}"

def create_agents_and_tasks(tipo: str):
    """
    Cria os agentes e as tarefas para o CrewAI, considerando o tipo de resposta (resumo ou detalhado).
    """
    model_name = "gpt-4o-mini"

    # Agente de Contexto (Certificados)
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

    # Agente de Pesquisa na Web
    web_search_agent = Agent(
        role="Agente de Pesquisa",
        goal="Buscar informações na web e fornecer contexto atualizado sobre tecnologia",
        backstory="Você é um pesquisador de informações atualizado, usando a internet para encontrar respostas relevantes."
    )

    web_search_task = Task(
        description="Realizar uma busca no DuckDuckGo sobre o mercado de tecnologia e trazer um resumo dos principais resultados.",
        agent=web_search_agent,
        expected_output="Resumo dos melhores resultados da pesquisa na web sobre o mercado de desenvolvedores.",
        model=model_name,
    )

    # Agente de Respostas (Resumido ou Detalhado)
    response_agent = Agent(
        role="Assistente de Respostas",
        goal="Responder perguntas considerando os certificados e a pesquisa na web",
        backstory="Você é um assistente especializado em carreira e certificações de tecnologia." 
    )

    response_task = Task(
        description="Responder perguntas do usuário considerando seus certificados e as informações da web.Importante: O nome do usuário é 'Alisson Deivison', você deve agir como se fosse ele e responder em primeira pessoa para quem quer que esteja perguntando. Caso a pergunta saia do contexto você deve simplesmente dizer que não pode responder ou não tem conhecimento a respeito",
        agent=response_agent,
        expected_output="Resposta baseada nos certificados do usuário e nas informações da web sobre o mercado de trabalho. ",
        model=model_name,
    )

    crew = Crew(agents=[context_agent, web_search_agent, response_agent], tasks=[context_task, web_search_task, response_task])

    return crew, context_task, web_search_task, response_task

def ask_openai(question, context, web_info, tipo):
    """
    Chama a API da OpenAI passando o contexto dos certificados, a pesquisa na web e a pergunta do usuário.
    Se o tipo for 'resumo', a resposta é mais concisa.
    """
    try:
        messages = [
            {"role": "system", "content": "Você é um assistente especializado em carreiras na área de tecnologia e desenvolvimento."},
            {"role": "system", "content": f"O usuário possui as seguintes certificações relevantes:\n{context}"},
            {"role": "system", "content": f"Com base na pesquisa de mercado sobre desenvolvedores:\n{web_info}"},
            {"role": "system", "content": "Seu nome é 'Alisson Deivison', você deve agir como se fosse ele e responder em primeira pessoa para quem quer que esteja perguntando. Caso a pergunta saia do contexto você deve simplesmente dizer que não pode responder ou não tem conhecimento a respeito"},
            {"role": "user", "content": question}
        ]

        max_tokens = 300 if tipo == "resumo" else 500
        
        response = litellm.completion(
            model="openai/gpt-4o-mini",
            messages=messages,
            temperature=0.1,
            max_tokens=max_tokens,
        )

        resposta = response.choices[0].message["content"].strip()
        resposta_corrigida = resposta.replace("$", "\$").replace("R$", "R\$")

        return resposta_corrigida
    except Exception as e:
        return f"Ocorreu um erro ao chamar a API da OpenAI: {str(e)}"

def kickoff(question, tipo):
    """
    Executa os Agentes de Contexto e Pesquisa na Web antes da OpenAI para enriquecer a resposta.
    Ajusta a resposta conforme o tipo de consulta (resumo ou detalhado).
    """
    crew, context_task, web_search_task, response_task = create_agents_and_tasks(tipo)

    # Carregar contexto dos certificados
    context = carregar_certificados()

    # Pesquisar na web sobre o assunto da pergunta
    web_info = pesquisar_na_web(question)

    # Chamar a OpenAI com ambos os contextos e tipo
    result = ask_openai(question, context, web_info, tipo)

    return {
        "crew": crew.dict(),
        "context": context,
        "web_info": web_info,
        "answer": result
    }
