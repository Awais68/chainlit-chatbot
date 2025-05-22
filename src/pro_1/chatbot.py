
import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

load_dotenv(find_dotenv())
gemini_api_key= os.getenv("GEMINI_API_KEY")



# STEP :1 PROVIDER
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# step 2 Model
model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=provider,
)
# config: Defined at Run Level
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
# step 3 agent
agent1 = Agent(
    instructions="You are a helpful assistant that can answer questions and task.",
    name= "Panaversity Support Agent"
)


# print(result.final_output)

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent1,
        input=message.content,
        run_config=run_config,
        # starting_agent=agent1
    )
    await cl.Message(content=result.final_output).send()