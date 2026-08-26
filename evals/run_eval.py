import uuid

from dotenv import load_dotenv
from langsmith import Client, evaluate

from app.agent.agent import chat
from evals.correctness_evaluator import category_aware_correctness
from evals.behavioral_alignment_evaluator import behavioral_alignment
from evals.trace_evaluators import require_kb_search

load_dotenv()

client = Client()
DATASET_NAME = "wa-agent-v1"

# Testing CI pipeline

def target(inputs: dict) -> dict:
    question = inputs["question"]

    answer = chat(
        thread_id=f"eval-{uuid.uuid4()}",
        message = question,
    )

    return {
        "answer": answer,
    }

if __name__ == "__main__":
    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            category_aware_correctness,
            behavioral_alignment,
            require_kb_search,
            ],
        experiment_prefix="wa-agent-v1",
    )

    print(f"EXPERIMENT_NAME={results.experiment_name}")

