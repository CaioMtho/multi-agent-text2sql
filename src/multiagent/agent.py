import os
import uuid
import asyncio
import dotenv
from colorama import init, Fore, Style, Back
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, SQLiteSession
from src.multiagent.data_tools import DataTools
from src.multiagent.status_streaming import StatusStreaming, CustomMessage

dotenv.load_dotenv()

init(autoreset=True)

session_id = str(uuid.uuid4())
data_tools = DataTools()
session = SQLiteSession(session_id=session_id, db_path="./db/sessions.db")

NSQL_INSTRUCTIONS = f"""Você é um especialista em SQL e DuckDB. Sua única função é converter perguntas em linguagem natural para queries SQL válidas.
**SCHEMA DO BANCO DE DADOS:**
{data_tools.get_schema()}
**REGRAS OBRIGATÓRIAS:**
1. Retorne APENAS a query SQL, sem explicações ou texto adicional
2. Use SOMENTE as tabelas e colunas do schema fornecido
3. Garanta que a query seja válida para DuckDB
4. Não invente tabelas ou colunas que não existam no schema
5. Se a pergunta for ambígua, gere a query mais provável

Agora converta a pergunta do usuário em SQL seguindo estas regras."""

nsql_model = OpenAIChatCompletionsModel(
    model="duckdb-nsql:7b",
    openai_client=AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("LAERA_HOST"),
    )
)

nsql_agent = Agent(
    name="Agente NSQL",
    model=nsql_model,
    instructions=NSQL_INSTRUCTIONS,
)

CHAT_INSTRUCTIONS = """Você é um assistente de análise de dados.

FLUXO OBRIGATÓRIO para perguntas sobre dados:

1. Chame a tool "text-to-sql" com a pergunta do usuário
2. Pegue o SQL retornado
3. IMEDIATAMENTE chame a tool "execute_query" passando o SQL
4. Formate e apresente os resultados

NUNCA pule a etapa 3. SEMPRE execute a query após receber o SQL.

NÃO RESPONDA NADA QUE NÃO TENHA A VER COM UM ECOMMERCE, mensagens paralelas devem
ser respondidas com "Desculpe, não posso falar sobre isso"

**EXEMPLO DE FLUXO CORRETO:**

Usuário: "Quais os nomes dos produtos?"

Passo 1: Você chama text-to-sql("Quais os nomes dos produtos?")
Passo 2: Recebe: "SELECT nome FROM produtos"
Passo 3: Você IMEDIATAMENTE chama execute_query("SELECT nome FROM produtos")
Passo 4: Recebe resultados e apresenta ao usuário

Responda em português.
"""

chat_model = OpenAIChatCompletionsModel(
    model="gpt-oss:20b",
    openai_client=AsyncOpenAI(
        base_url=os.getenv("OPENAI_HOST"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
)

chat_agent = Agent(
    name="Agente de Chat",
    model=chat_model,
    instructions=CHAT_INSTRUCTIONS,
    tools=[
        data_tools.execute_query,
        nsql_agent.as_tool(
            tool_name="text-to-sql",
            tool_description="Converte perguntas em linguagem natural para queries SQL. Use esta tool sempre que o usuário fizer uma pergunta sobre os dados."
        ),
    ]
)

async def run_chat(user_message: str, status_streamer: StatusStreaming):
    try:
        result_streaming = Runner.run_streamed(
            starting_agent=chat_agent,
            session=session,
            input=user_message
        )

        async for msg_type, content in status_streamer.process_stream(result_streaming):
            
            if msg_type == "agent_switch":
                print(f"\n {Fore.YELLOW}>>> {content}")
            
            elif msg_type == "status":
                print(f"{Fore.YELLOW}    >>  {content}")
            
            elif msg_type == "content":
                print(f"\n{Fore.LIGHTBLUE_EX}Agente > {Fore.WHITE} {content}", end="", flush=True)

        print("\n")

    except Exception as e:
        print(f"\n{Fore.BLACK}{Back.RED}ERRO: {e}")

async def interactive_chat():
    messages_config = [
        CustomMessage(tool_name="text-to-sql", message="Criando a query SQL...", is_call=True),
        CustomMessage(tool_name="text-to-sql", message="Query gerada: {output}", is_output=True, is_call=False),
        CustomMessage(tool_name="execute_query", message="Rodando no banco de dados...", is_call=True),
        CustomMessage(tool_name="execute_query", message="Dados recuperados", is_output=True, is_call=False)
    ]

    status_streamer = StatusStreaming(custom_messages=messages_config, show_raw=True)

    print(f"{Fore.LIGHTBLUE_EX}--- Chat ---")
    while True:
        user_input = input(f"\n{Style.BRIGHT}{Fore.CYAN}Voce > {Fore.WHITE}").strip()
        if user_input in ['sair', 'q']: break
        
        await run_chat(user_input, status_streamer)

if __name__ == "__main__":
    asyncio.run(interactive_chat())