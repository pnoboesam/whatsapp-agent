from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

class EvaluationResult(BaseModel):
    category: Literal[
        "incorrect",
        "partially_correct",
        "correct",
    ]

    explanation: str = Field(
        description= "Brief explanation for the evaluation decision."
    )


# LLM Judge
judge_llm = ChatOpenRouter(
    model="openai/gpt-5.6-luna",
    temperature=0,
)

structured_judge = judge_llm.with_structured_output(EvaluationResult)


# Category Aware Correctness evaluator
def category_aware_correctness(
    inputs: dict,
    outputs: dict,
    reference_outputs: dict,
    example,
) -> dict:

    question = inputs["question"]
    agent_answer = outputs["answer"]
    reference_answer = reference_outputs["answer"]

    category = example.metadata.get("category", "")
    expected_behavior = example.metadata.get("expected_behavior", "")

    prompt = f"""
    You are an expert evaluator for a customer-service AI agent.

Evaluate whether the agent's response is correct for the user's question.

Use ALL of the following:

QUESTION:
{question}

CATEGORY:
{category}

EXPECTED BEHAVIOR:
{expected_behavior}

REFERENCE ANSWER:
{reference_answer}

AGENT ANSWER:
{agent_answer}


IMPORTANT:

The reference answer is the ground truth, but it is not necessarily
a response that the agent must reproduce word-for-word.

The expected behavior describes what the agent is supposed to do.

Evaluate according to the category:

RAG:
- Check factual correctness and completeness.
- The answer should provide the relevant information from the reference.
- Do not penalize harmless differences in wording.

NO_ANSWER:
- The agent should recognize when the requested information is not
  supported by the knowledge base.
- It must not invent facts or recommendations.
- A clarification question may be appropriate when the user's request
  is ambiguous.

LEAD_TOOL:
- The agent should correctly recognize appointment, consultation,
  or lead-generation intent.
- It should follow the expected behavior, including collecting
  required information when appropriate.
- Do not require exact wording.

CONVERSATION:
- The agent should respond naturally and appropriately to the user's
  conversational intent.
- It should clarify ambiguity when appropriate.
- It should not make unsupported diagnoses, recommendations, or claims.

A response can be correct even if it is better, clearer, or more
helpful than the reference, provided that it remains factually
supported and follows the expected behavior.

Classify the response into exactly one category:

correct
- Correctly answers or handles the user's request.
- Satisfies the expected behavior.
- Is consistent with the reference.
- Contains no important unsupported claims.

partially_correct
- Contains meaningful correct information but is incomplete.
- Misses an important part of the expected behavior.
- Contains a minor unsupported claim that does not invalidate
  the overall response.

incorrect
- Gives materially incorrect information.
- Contradicts the reference or expected behavior.
- Fails to address the user's request.
- Invents important unsupported information.
- Fails to follow a critical required behavior.

Do not require exact wording.
Do not penalize harmless differences in phrasing.

Return exactly one category and a brief explanation.
"""

    result = structured_judge.invoke(prompt)

    return {
        "key": "correctness",
        "value": result.category,
        "comment": result.explanation,
    }