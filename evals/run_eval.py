from dotenv import load_dotenv
from langsmith import Client, evaluate
from icecream import ic as print

from app.agent.agent import chat
from evals.rag_correctness_evaluator import rag_correctness

load_dotenv()

client = Client()
DATASET_NAME = "wa-agent-v1"


def target(inputs: dict) -> dict:
    print(inputs)
    question = inputs["question"]

    answer = chat(
        thread_id=f"eval-{question}",
        message = question,
    )

    return {
        "answer": answer,
    }

if __name__ == "__main__":
    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[rag_correctness],
        experiment_prefix="wa-agent-v1",
    )

    print(results)
