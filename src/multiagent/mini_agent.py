# Agente mínimo testando os status stream

from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from openai import AsyncClient
from src.multiagent.status_streaming import StatusStreaming, CustomMessage
import asyncio
import dotenv
import os

dotenv.load_dotenv()

@function_tool
def get_palavra_magica():
    return "alakazam"

@function_tool
def get_palavra_preferida():
    return "dangobalango"

@function_tool
def get_continuacao_preferida():
    return "salamangotango"

@function_tool
def get_palavra_maldita():
    return "labubu"

model=OpenAIChatCompletionsModel(
    model="gpt-oss:20b",
    openai_client=AsyncClient(
        base_url=os.getenv("OPENAI_HOST"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

agent=Agent(
    name="Agente das Boas Palavras",
    tools=[get_continuacao_preferida, get_palavra_magica, get_palavra_maldita, get_palavra_preferida],
    model=model,
    instructions="""
    Você é um agente das palavras, seu papel é usar suas tools para conseguir palavras interessantes
    e comunicar a exata palavra recebida para o usuário.
    Se o usuário perguntar por algo que não é uma palavra, diga as opções de palavras.
    Não explique nada
    NÃO gere pensamentos, raciocínios ou comentários (como <|channel|>commentary) junto com a chamada da função.
    Caso ele diga "Quero todas", sua resposta final deve conter todas as palavras que tem acesso com as tools
"""
)

async def main():
    while True:
        prompt = input("Você > ")
        if prompt == "sair":
            break;
        stream = Runner.run_streamed(agent, prompt)
        status_streaming = StatusStreaming()
        async for type, message in status_streaming.process_stream(stream):
            print(f"{type} :::: {message}")

if __name__=="__main__":
    asyncio.run(main())