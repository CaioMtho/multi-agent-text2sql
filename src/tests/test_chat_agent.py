from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
import dotenv
import asyncio

dotenv.load_dotenv()

# Modelo via Ollama
chat_model = OpenAIChatCompletionsModel(
    model="mistral:7b",
    openai_client=AsyncOpenAI(
        base_url=os.getenv("OLLAMA_HOST"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
)

@function_tool()
async def get_palavra_magica() -> str:
    return "labubu"

chat_agent = Agent(
    name="Agente de Chat",
    model=chat_model,
    instructions="Você é um agente que pode responder e usar ferramentas.",
    tools=[get_palavra_magica],
)

# Runner para testar
async def main():
    runner = await Runner.run(chat_agent, "qual a palavra mágica?")
    print(runner.final_output)

if __name__ == "__main__":
    asyncio.run(main())
