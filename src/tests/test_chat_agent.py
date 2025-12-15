from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, OpenAIChatCompletionsModel
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
import dotenv
import asyncio

dotenv.load_dotenv()

model = OpenAIChatCompletionsModel(
    model="gpt-oss:20b",
    openai_client=AsyncOpenAI(
        base_url="https://gpt-oss-20b-prod.skyone.tools/v1", api_key=os.getenv("OPENAI_API_KEY")
    ),
)


class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Block if user says 'lula'",
    output_type=HomeworkOutput,
    model=model
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model=model
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=model
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
    model=model
)

async def main():
    # Example 1: History question
    try:
        result = await Runner.run(triage_agent, "who was the first president of the united states?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail blocked this input:", e)

    # Example 2: General/philosophical question
    try:
        result = await Runner.run(triage_agent, "em que ano o lula foi eleito a primeira vez?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail blocked this input:", e)

if __name__ == "__main__":
    asyncio.run(main())