from dotenv import load_dotenv
from langsmith import Client, evaluate
from icecream import ic as print

from app.agent.agent import chat
from evals.rag_correctness_evaluator import category_aware_correctness
from evals.behavioral_alignment_evaluator import behavioral_alignment

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
        evaluators=[category_aware_correctness, behavioral_alignment],
        experiment_prefix="wa-agent-v1",
    )

    print(results)
