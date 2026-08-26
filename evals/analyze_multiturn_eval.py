import os

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

DATASET_NAME = "wa-agent-multiturn-v1"

EXPERIMENT_NAME = os.getenv("MULTITURN_EXPERIMENT_NAME")

if not EXPERIMENT_NAME:
    raise RuntimeError(
        "MULTITURN_EXPERIMENT_NAME environment variable is required."
    )

EXPECTED_EXAMPLES = 4
MIN_LEAD_TOOL_SUCCESS = 4


def main():
    client = Client()

    dataset = client.read_dataset(
        dataset_name=DATASET_NAME
    )

    examples = {
            example.inputs["messages"][0]: example
            for example in client.list_examples(dataset_id=dataset.id)
        }

    runs = list(
        client.list_runs(
            project_name=EXPERIMENT_NAME,
            is_root=True,
        )
    )

    if len(runs) != EXPECTED_EXAMPLES:
        raise RuntimeError(
            f"Expected {EXPECTED_EXAMPLES} evaluation runs, "
            f"but found {len(runs)}."
        )

    print(f"\nExperiment: {EXPERIMENT_NAME}")
    print(f"Runs: {len(runs)}")

    lead_tool_results = []

    for run in runs:
        opening_lead_message = run.inputs.get("messages")[0]
        example = examples.get(opening_lead_message)

        if example is None:
            raise RuntimeError(
                f"Dataset example not found: {opening_lead_message}"
            )
        
        feedback = list(
            client.list_feedback(
                run_id=run.id
            )
        )

        lead_tool_value = None

        for item in feedback:
            if item.key == "lead_tool_usage":
                lead_tool_value = item.score
                break

        if lead_tool_value is None:
            raise RuntimeError(
                f"No lead_tool_usage evaluation found "
                f"for run {run.id}."
            )

        lead_tool_results.append(
            {
                "run_id": run.id,
                "opening_message": opening_lead_message,
                "result": lead_tool_value
            }
        )

    success_count = sum(
        result["result"] == 1
        for result in lead_tool_results
    )

    failure_count = sum(
        result["result"] == 0
        for result in lead_tool_results
    )

    print("\n" + "=" * 60)
    print("MULTITURN LEAD TOOL RESULTS")
    print("=" * 60)

    print(
        f"\nSuccessful: "
        f"{success_count}/{EXPECTED_EXAMPLES}"
    )

    print(
        f"\nFailed: "
        f"{failure_count}/{EXPECTED_EXAMPLES}"
    )

    print("\n" + "=" * 60)
    print("CASES REQUIRING REVIEW")
    print("=" * 60)

    for result in lead_tool_results:
        if result["result"] == 0:
            print(
                f"\nRun: {result['run_id']}"
                f"\nRun's Example: {result['opening_message']}"
            )
            print(
                "lead_tool_usage: FAILED"
            )

    print("\n" + "=" * 60)
    print("REGRESSION CHECK")
    print("=" * 60)

    print(
        f"Lead tool success count: "
        f"{success_count}"
    )

    passed = (
        success_count >= MIN_LEAD_TOOL_SUCCESS
    )

    status = "PASS" if passed else "FAIL"

    print(f"{status}: Lead tool usage")

    if passed:
        print(
            "\nMULTITURN REGRESSION CHECK PASSED"
        )
    else:
        print(
            "\nMULTITURN REGRESSION CHECK FAILED"
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()