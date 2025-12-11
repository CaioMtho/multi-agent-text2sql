import os
import uuid
import asyncio
import dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, SQLiteSession, ItemHelpers
from src.multiagent.data_tools import DataTools

dotenv.load_dotenv()

last_tool_called=""

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
    model="duckdb-nsql:latest",
    openai_client=AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OLLAMA_HOST"),
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

Para conversas casuais, apenas responda normalmente.

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

def get_status_message(tool_name : str):
    if tool_name == "text-to-sql":
        return "Formulando consulta..."
    elif tool_name == "execute_query":
        return "Consultando o banco..."
    
def get_output_message(output : str, last_tool_called : str):
    if last_tool_called == "text-to-sql":
        return f"Consulta gerada: {output}"
    elif last_tool_called == "execute_query":
        return f"Resultado da query: {output}\n"
    return f"Output de {last_tool_called}: {output}"

async def run_chat(user_message: str):
    last_tool_called=""
    try:
        result_streaming = Runner.run_streamed(
            starting_agent=chat_agent,
            session=session,
            input=user_message
        )

        async for event in result_streaming.stream_events():
            if event.type == "agent_updated_stream_event":
                print(f"    >> Transferindo para o {event.new_agent.name}")
            
            elif event.type == "run_item_stream_event":
                item = event.item
                
                if item.type == "tool_call_item":
                    last_tool_called=item.raw_item.name
                    print(f"    >> {get_status_message(item.raw_item.name)}")
                
                elif item.type=="tool_call_output_item":
                    print(f"    >> {get_output_message(item.output, last_tool_called)}")

                elif item.type == "message_output_item":
                    content = ItemHelpers.text_message_output(item)
                    print(f"{content}")

    except Exception as e:
        print(f"\nERRO: {e}")

async def interactive_chat():
    print("\n" + "=" * 60)
    print("CHAT MULTIAGENTE")
    print("=" * 60)
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            user_input = input("Voce > ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\nEncerrando.")
                break

            await run_chat(user_input)

        except KeyboardInterrupt:
            print("\nEncerrando.")
            break
        except Exception as e:
            print(f"\nErro: {e}")

if __name__ == "__main__":
    asyncio.run(interactive_chat())