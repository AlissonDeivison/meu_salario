import openai
import os
from dotenv import load_dotenv
import litellm
from crewai import Agent, Task, Crew

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurar chave da API da OpenAI no litellm
openai.api_key = os.getenv('OPENAI_API_KEY')
litellm.api_key = os.getenv('OPENAI_API_KEY')  # Usando a mesma chave da OpenAI no litellm

def create_agent_and_task():
    """
    Cria o agente e a tarefa para o CrewAI.
    """
    model_name = "gpt-4o-mini"  # Especificando o modelo da OpenAI

    # Criar o agente
    agent = Agent(
        role='Assistente de Respostas',
        goal='Responder perguntas de forma clara e objetiva',
        backstory="Você é um assistente especializado em responder dúvidas sobre o mercado de trabalho de TI no Brasil",
    )

    # Criar a tarefa, incluindo o modelo e o provedor
    task = Task(
        description='Responder a pergunta do usuário de forma clara e objetiva.',
        agent=agent,
        expected_output="Texto de resposta clara e objetiva, na linguagem pt-BR, topificado e revisado. Exemplo de resposta esperada: 'Os salários para um desenvolvedor full stack no Brasil podem variar bastante de acordo com fatores como localização, nível de experiência, demanda do mercado e o porte da empresa. Abaixo está uma estimativa média dos salários que um desenvolvedor full stack pode esperar: 1. Júnior (0 a 2 anos de experiência): de R$ 3.500 a R$ 6.500 por mês. 2. Pleno (2 a 5 anos de experiência): de R$ 7.000 a R$ 12.000 por mês. 3. Sênior (5 a 10 anos de experiência): de R$ 12.000 a R$ 20.000 ou mais por mês.'",  # Exemplo esperado
        model=model_name,  
    )

    # Criar a Crew
    crew = Crew(agents=[agent], tasks=[task])

    return crew

def clean_response(response):
    """
    Limpa e formata a resposta para garantir que a moeda seja corretamente formatada.
    """
    # Substitui 'R\n' por 'R$' e corrige outras quebras de linha
    response = response.replace('R\n', 'R$ ').replace('R ', 'R$ ').replace('R$', 'R$')
    
    # Remove quebras de linha e múltiplos espaços
    response = ' '.join(response.split())
    
    # Corrige a formatação para valores numéricos com a moeda
    response = response.replace("R$", "R$ ").replace("aR", "a R$").replace("R  ", "R$  ")
    
    return response

def ask_openai(question):
    """
    Função para interagir com a API da OpenAI e obter a resposta.
    """
    try:
        # Chama a API da OpenAI com o modelo desejado via litellm
        response = litellm.completion(
            model="openai/gpt-4o-mini",  # Usando o modelo da OpenAI no litellm
            messages=[{"role": "user", "content": question}],
            max_tokens=200  # Permite mais tokens para uma resposta mais completa
        )

        # Extrai a resposta da IA
        answer = response.choices[0].message["content"].strip()
        
        # Limpa e formata a resposta antes de retornar
        return clean_response(answer)
    except Exception as e:
        return f"Ocorreu um erro ao chamar a API da OpenAI: {str(e)}"

def kickoff(question):
    """
    Função que inicia o processo, executando a tarefa do agente e obtendo a resposta.
    """
    crew = create_agent_and_task()
    
    # Chama a função ask_openai para obter a resposta à pergunta
    result = ask_openai(question)
    
    return result
