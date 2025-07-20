# agentapp/langchain_backend/agent.py
import boto3
from langchain.agents import initialize_agent, Tool
from langchain_aws import ChatBedrock
import vars
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains.llm_math.base import LLMMathChain
from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate

# Initialize Langfuse client with constructor arguments
from langfuse import Langfuse


def build_agent():
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
        verbose=True
    )
    return agent

from langfuse.langchain import CallbackHandler
agent = build_agent()

langfuse = Langfuse(
    public_key=vars.LANGFUSE_PUBLIC_KEY,
    secret_key=vars.LANGFUSE_SECRET_KEY,
    host=vars.LANGFUSE_HOST
)

langfuse_handler = CallbackHandler()

response = agent.run({"tell me about cricket"}, callbacks=[langfuse_handler])


langfuse.flush()