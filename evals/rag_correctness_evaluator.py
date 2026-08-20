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


# RAG Correctness evaluator
def rag_correctness(
    inputs: dict,
    outputs: dict,
    reference_outputs: dict,
) -> dict:

    question = inputs["question"]
    agent_answer = outputs["answer"]
    reference_answer = reference_outputs["answer"]

    prompt = f"""
    You are an expert evaluator for a customer-service AI agent.

    Evaluate whether the agent's answer correctly answers the user's
    question and is consistent with the expected reference answer.

    QUESTION:
    {question}

    REFERENCE ANSWER:
    {reference_answer}

    AGENT ANSWER:
    {agent_answer}


    Classify the agent answer into exactly one of these categories:

    correct
    - Correctly answers the user's question.
    - Is consistent with the reference answer.
    - Contains the important facts required by the reference.
    - Minor differences in wording are acceptable.

    partially_correct
    - Contains some correct information but is incomplete.
    - Misses an important fact.
    - Contains a minor unsupported claim that does not completely
    invalidate the answer.

    incorrect
    - Gives factually incorrect information.
    - Contradicts the reference answer.
    - Fails to answer the user's question.
    - Invents important information not supported by the reference.

    Important:

    Do not require exact wording.

    Do not penalize differences in phrasing.

    Focus on factual correctness and completeness.

    Return exactly one category and a brief explanation.
    """

    result = structured_judge.invoke(prompt)

    return {
        "key": "rag_correctness",
        "value": result.category,
        "comment": result.explanation,
    }