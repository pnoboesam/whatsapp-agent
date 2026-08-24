def find_tool_runs(run, tool_name):
    matches = []

    for child in run.child_runs:
        if child.name == tool_name:
            matches.append(child)

        matches.extend(
            find_tool_runs(child, tool_name)
        )

    return matches


def require_kb_search(run, example):
    """
    Verify that kb_search was used for examples where
    the dataset category requires a knowledge-base lookup.
    """

    category = example.metadata.get("category", "")

    #KB lookup is expected for these categories.
    if category not in {"rag", "no_answer"}:
        return {
            "key": "kb_search_required",
            "score": 1,
            "comment":(
                f"KB lookup was not required for category "
                f"'{category}'."
            )
        }

    kb_runs = find_tool_runs(
        run,
        "kb_search",
    )

    if not kb_runs:
        return {
            "key": "kb_search_required",
            "score": 0,
            "comment": (
                f"Category '{category}' requires kb_search, "
                "but kb_search was not called."
            ),
        }

    return {
        "key": "kb_search_required",
        "score": 1,
        "comment": (
            f"Category '{category}' requires kb_search "
            "and kb_search was called."
        ),
    }


def lead_tool_usage(run, example):
    """
    Verify that append_lead_details was used correctly
    during the lead-booking workflow.
    """

    requires_lead_tool = example.metadata.get(
        "requires_lead_tool",
        False,
    )

    lead_tool_runs = find_tool_runs(
        run,
        "append_lead_details",
    )

    # Tool is not expected for this example.
    if not requires_lead_tool:
        return {
            "key": "lead_tool_usage",
            "score": 1,
            "comment": (
                "append_lead_details was not required "
                "for this example."
            ),
        }

    # No lead tool call
    if not lead_tool_runs:
        return {
            "key": "lead_tool_usage",
            "score": 0,
            "comment": "append_lead_details was required but not called.",
        }

    # Tool should normally be called exactly once
    if len(lead_tool_runs) > 1:
        return {
            "key": "lead_tool_usage",
            "score": 0,
            "comment": (
                f"append_lead_details was called "
                f"{len(lead_tool_runs)} times; expected once."
            ),
        }

    tool_run = lead_tool_runs[0]

    tool_inputs = tool_run.inputs or {}

    required_fields = [
        "full_name",
        "phone_number",
        "location",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not tool_inputs.get(field)
    ]

    if missing_fields:
        return {
            "key": "lead_tool_usage",
            "score": 0,
            "comment": (
                "append_lead_details was called, but "
                f"required fields were missing: {missing_fields}"
            ),
        }

    return {
        "key": "lead_tool_usage",
        "score": 1,
        "comment": (
            "append_lead_details was called exactly once "
            "with all required lead details."
        ),
    }



