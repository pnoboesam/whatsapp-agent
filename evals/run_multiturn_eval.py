import uuid
from dotenv import load_dotenv
from langsmith import evaluate

from app.agent.agent import chat
from evals.trace_evaluators import lead_tool_usage

load_dotenv()

DATASET_NAME = "wa-agent-multiturn-v1"


def target(inputs: dict) -> dict:
    thread_id = f"eval-{uuid.uuid4()}"
    messages = inputs["messages"]

    responses = []

    for message in messages:
        response = chat(
            conversation_id=thread_id,
            wa_number="233500000000",
            message=message,
        )

        responses.append(response)

    return {
        "responses": responses,
        "answer": responses[-1],
    }


if __name__ == "__main__":
    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            lead_tool_usage,
        ],
        experiment_prefix="wa-agent-multiturn",
    )

    print(f"MULTITURN_EXPERIMENT_NAME={results.experiment_name}")