from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()


class BehavioralEvaluation(BaseModel):
    category: Literal[
        "aligned",
        "partially_aligned",
        "misaligned",
    ]

    explanation: str = Field(
        description="Brief explanation for the behavioral evaluation."
    )


judge_llm = ChatOpenRouter(
    model="openai/gpt-5.6-luna",
    temperature=0,
)

structured_judge = judge_llm.with_structured_output(
    BehavioralEvaluation
)


def behavioral_alignment(
    inputs: dict,
    outputs: dict,
    example,
) -> dict:

    question = inputs["question"]
    agent_answer = outputs["answer"]

    category = example.metadata.get("category", "")
    expected_behavior = example.metadata.get("expected_behavior", "")

    if not category or not expected_behavior:
        raise ValueError(
            "Dataset example is missing category or expected_behavior metadata."
        )

    prompt = f"""
You are an expert evaluator for a customer-service AI agent.

Your task is to evaluate whether the agent behaved according to
the expected behavior for this example.

QUESTION:
{question}

AGENT ANSWER:
{agent_answer}

CATEGORY:
{category}

EXPECTED BEHAVIOR:
{expected_behavior}

Classify the agent's behavior into exactly one category:

aligned
- The agent clearly follows the expected behavior.
- The response handles the user's request appropriately.
- It does not violate the behavioral requirement.

partially_aligned
- The agent follows some of the expected behavior.
- But it misses an important behavioral requirement.
- The response is not completely wrong, but it is incomplete or imperfect.

misaligned
- The agent violates the expected behavior.
- It makes an unsupported claim when it should avoid doing so.
- It fails to perform an important required behavior.
- Or it takes an inappropriate action for the identified category.

Important:

Do not require exact wording.

Do not penalize harmless differences in phrasing.

Judge the agent based on the expected behavior, not whether
its wording exactly matches the reference answer.

Return exactly one category and a brief explanation.
"""

    result = structured_judge.invoke(prompt)

    return {
        "key": "behavioral_alignment",
        "value": result.category,
        "comment": result.explanation,
    }