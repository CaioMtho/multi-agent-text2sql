from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, SQLiteSession
from src.multiagent.data_tools import DataTools
import os
import dotenv
import uuid
import asyncio

dotenv.load_dotenv()

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
    model="duckdb-nsql",
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
    model="llama3.1:8b",
    openai_client=AsyncOpenAI(
        base_url=os.getenv("OLLAMA_HOST"),
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

async def run_chat(user_message: str):
    print(f"\n{'=' * 60}")
    print(f"USUÁRIO: {user_message}")
    print(f"{'=' * 60}\n")

    try:
        result = await Runner.run(
            starting_agent=chat_agent,
            session=session,
            input = user_message
        )

        final_response = result.final_output

        print(f"\n{'=' * 60}")
        print(f"ASSISTENTE: {final_response}")
        print(f"{'=' * 60}\n")

        return final_response

    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return f"Desculpe, ocorreu um erro: {str(e)}"


async def interactive_chat():
    print("\n" + "=" * 60)
    print("CHAT")
    print("=" * 60)
    print("'sair' para encerrar\n")

    while True:
        try:
            user_input = input("Você: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\nEncerrando chat. Até logo!")
                break

            await run_chat(user_input)

        except KeyboardInterrupt:
            print("\n\nEncerrando chat. Até logo!")
            break
        except Exception as e:
            print(f"\n✗ Erro inesperado: {e}")

async def run_tests():
    test_questions = [
        "Olá! Como você está?",
        "Quais são os 5 produtos mais vendidos?",
        "Qual o valor total de vendas por mês?",
        "Quais clientes gastaram mais de 3000 reais?",
        "Qual a média de avaliação dos produtos?",
        "Quantos pedidos estão com status 'entregue'?",
    ]

    print("\n" + "=" * 60)
    print("EXECUTANDO TESTES AUTOMÁTICOS")
    print("=" * 60 + "\n")

    for question in test_questions:
        await run_chat(question)
        await asyncio.sleep(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(run_tests())
    else:
        asyncio.run(interactive_chat())