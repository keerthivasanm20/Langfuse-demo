
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain.agents import AgentExecutor
from langchain.evaluation import AgentTrajectoryEvaluator

from llm_bedrock import build_agent

agent_executor = AgentExecutor(agent=build_agent(), tools=[], verbose=True)

config = RunEvalConfig(
    evaluators=[AgentTrajectoryEvaluator.EVAL_CRITERIA],
)

run_on_dataset(
    dataset_name="langchain/agent-eval-sample",  # Use a sample from LangChainHub or create your own
    agent_executor=agent_executor,
    evaluation_config=config,
    experiment_prefix="guarded-agent-benchmark"
)