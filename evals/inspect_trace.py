from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

EXPERIMENT_NAME = "wa-agent-v1-1479dec5"

def main():
    client = Client()

    root_runs = list(
        client.list_runs(
            project_name=EXPERIMENT_NAME,
            is_root=True,
        )
    )

    # Inspect the first evaluation example
    root = root_runs[0]

    print("=" * 70)
    print(f"ROOT RUN: {root.id}")
    print(f"TRACE ID: {root.trace_id}")
    print("=" * 70)

    trace_runs = list(
        client.list_runs(
            trace_id=root.trace_id,
        )
    )

    trace_runs.sort(
        key=lambda run: run.start_time or ""
    )

    for run in trace_runs:
        print("\n" + "-" * 70)
        print(f"NAME:      {run.name}")
        print(f"TYPE:      {run.run_type}")
        print(f"ID:        {run.id}")
        print(f"PARENT:    {run.parent_run_id}")
        print(f"START:     {run.start_time}")

        if run.inputs:
            print(f"INPUTS:    {run.inputs}")

        if run.outputs:
            print(f"OUTPUTS:   {run.outputs}")


if __name__ == "__main__":
    main()