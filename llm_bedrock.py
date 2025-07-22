import boto3
from langchain.agents import initialize_agent, Tool
from langchain_aws import ChatBedrock
import vars
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains.llm_math.base import LLMMathChain
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from nemoguardrails import LLMRails, RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from langfuse import Langfuse
import vars
from langfuse import Langfuse
import os
os.environ["OPENAI_API_KEY"] = vars.OPENAI_API_KEY

def build_agent(callbacks=None):

    session = boto3.Session(
        aws_access_key_id=vars.AWS_ACCESS_KEY,
        aws_secret_access_key=vars.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )

    bedrock = session.client('bedrock-runtime')
    llm = ChatBedrock(
        client=bedrock,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # or your preferred model
        model_kwargs={
            "max_tokens": 512,
        }
    )
    tools = [
        Tool(name="Wikipedia", func=WikipediaAPIWrapper().run, description="Get knowledge."),
        Tool(name="Calculator", func=LLMMathChain(llm=llm).run, description="Do math."),
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        callbacks=callbacks
    )
    return agent

from langfuse.langchain import CallbackHandler
# agent = build_agent()

langfuse = Langfuse(
    public_key=vars.LANGFUSE_PUBLIC_KEY,
    secret_key=vars.LANGFUSE_SECRET_KEY,
    host=vars.LANGFUSE_HOST
)

langfuse_handler = CallbackHandler()

# Initialize Langfuse
langfuse = Langfuse(
    public_key=vars.LANGFUSE_PUBLIC_KEY,
    secret_key=vars.LANGFUSE_SECRET_KEY,
    host=vars.LANGFUSE_HOST
)

def run_guarded_query(query: str):
    try:
        # Load agent and guardrails config
        agent = build_agent(callbacks=[langfuse_handler])
        config = RailsConfig.from_path("guardrails")
        guardrails = RunnableRails(config)
        guarded_chain = guardrails | agent
        response = guarded_chain.invoke(query)
        langfuse.flush()
        return response
    except Exception as e:
        if "blocked" in str(e).lower():
            return "Sorry, your request was blocked due to unsafe or inappropriate content."
        return f"An error occurred: {e}"


if __name__ == "__main__":
    user_input = "What is the capital of France?"
    user_input = "are you dumb" # profanity input
    result = run_guarded_query(user_input)
    print(result)