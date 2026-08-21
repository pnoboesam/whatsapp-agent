from collections import Counter, defaultdict
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

DATASET_NAME = "wa-agent-v1"
EXPERIMENT_NAME = "wa-agent-v1-1479dec5"

def main():
    client = Client()

    # Load dataset examples.
    dataset = client.read_dataset(dataset_name=DATASET_NAME)

    examples = {
        example.inputs["question"]: example
        for example in client.list_examples(dataset_id=dataset.id)
    }

    # Load experiment runs.
    runs = list(
        client.list_runs(
            project_name=EXPERIMENT_NAME,
            is_root=True,
        )
    )

    print(f"\nExperiment: {EXPERIMENT_NAME}")
    print(f"Runs: {len(runs)}")

    correctness_results = Counter()
    behavior_results = Counter()
    matrix = Counter()

    by_category = defaultdict(
        lambda: {
            "correctness": Counter(),
            "behavior": Counter(),
        }
    )

    disagreements = []

    for run in runs:
        question = run.inputs.get("question")

        example = examples.get(question)

        if example is None:
            print(f"\nWARNING: Dataset example not found: {question}")
            continue

        category = example.metadata.get("category", "unknown")

        # Get evaluator feedback attached to this run.
        feedback = list(
            client.list_feedback(
                run_id=run.id,
            )
        )

        correctness_value = None
        behavior_value = None

        for item in feedback:
            if item.key == "correctness":
                correctness_value = item.value

            elif item.key == "behavioral_alignment":
                behavior_value = item.value

        if correctness_value is not None:
            correctness_results[correctness_value] += 1
            by_category[category]["correctness"][correctness_value] += 1

        if behavior_value is not None:
            behavior_results[behavior_value] += 1
            by_category[category]["behavior"][behavior_value] += 1

        if correctness_value is not None and behavior_value is not None:
            matrix[(correctness_value, behavior_value)] += 1

        # Interesting disagreement:
        # RAG isn't perfect, but behavior is aligned.
        if (
            correctness_value is not None
            and behavior_value is not None
            and (
                correctness_value != "correct"
                or behavior_value != "aligned"
            )
        ):
            disagreements.append(
                (
                    question,
                    correctness_value,
                    behavior_value,
                    category,
                )
            )

    print("\n" + "=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)

    print("\nCorrectness")
    print_counts(correctness_results)

    print("\nBehavioral Alignment")
    print_counts(behavior_results)

    print("\n" + "=" * 60)
    print("RESULTS BY CATEGORY")
    print("=" * 60)

    for category, results in sorted(by_category.items()):
        print(f"\n[{category}]")

        print("  Correctness:")
        print_counts(results["correctness"], indent=4)

        print("  Behavior:")
        print_counts(results["behavior"], indent=4)

    print("\n" + "=" * 60)
    print("CASES REQUIRING REVIEW")
    print("=" * 60)

    if not disagreements:
        print("\nNone found.")

    for question, correctness, behavior, category in disagreements:
        print(f"\nQuestion: {question}")
        print(f"Category: {category}")
        print(f"Correctness: {correctness}")
        print(f"Behavior: {behavior}")

    print("\n" + "=" * 60)
    print("CORRECTNESS VS BEHAVIOR MATRIX")
    print("=" * 60)

    for (correctness, behavior), count in sorted(matrix.items()):
        print(
            f"{correctness:20} + "
            f"{behavior:20} = {count}"
        )


def print_counts(counter, indent=2):
    total = sum(counter.values())

    if total == 0:
        print(" " * indent + "No results")
        return

    for label, count in counter.most_common():
        percentage = count / total * 100

        print(
            " " * indent
            + f"{label}: {count}/{total} "
            f"({percentage:.1f}%)"
        )


if __name__ == "__main__":
    main()