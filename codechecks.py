from pathlib import Path
import nbformat
import html
import numpy as np
from types import SimpleNamespace
import jupytext 


from NB1 import (
    check_doorlopende_doos,
    check_harde_wanden,
    check_botsingsvoorwaarde,
    check_eindantwoord,
)


def get_tagged_cell(notebook_path, tag):
    nb = jupytext.read(notebook_path)

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue

        if tag in cell.metadata.get("tags", []):
            return cell.source

    raise ValueError(f"Geen codecel gevonden met tag {tag!r}")

# CODE BELOW FOR .IPYNB NOTEBOOKS, NOT FOR .MD FILES
# def get_tagged_cell(notebook_path, tag):
#     nb = nbformat.read(notebook_path, as_version=4)

#     for cell in nb.cells:
#         if tag in cell.metadata.get("tags", []):
#             return cell.source

#     raise ValueError(f"Geen cel gevonden met tag {tag!r}")

results = []


def check_cell(name, notebook_path, test_function, variable=None):

    try:
        # Find the tagged cell
        source = get_tagged_cell(notebook_path, name)

        # Provide dependencies for the student's code
        namespace = {
            "np": np,
            "dt": 0.1,
        }

        # Execute the student's code
        # Syntax errors are now caught by try/except
        exec(source, namespace)

        if variable is not None:
            # Retrieve a variable, e.g. num_botsingen
            student_object = namespace[variable]

        else:
            # Retrieve the function or class defined by the student
            objects = [
                value
                for key, value in namespace.items()
                if callable(value) and not key.startswith("__")
            ]

            if len(objects) != 1:
                raise ValueError(
                    f"Expected one function or class, found {len(objects)}."
                )

            student_object = objects[0]

        # Run the corresponding test from NB1.py
        test_function(student_object)

        results.append((name, True, ""))
        print(f"PASS: {name}")

    except Exception as exc:
        results.append((name, False, str(exc)))
        print(f"FAIL: {name}: {exc}")


# Run all checks
notebook_1 = "simulations/NB1_deeltjesmodel.md"

check_cell("NB1_doorlopendedoos", notebook_1, check_doorlopende_doos)

check_cell("NB1_hardewand", notebook_1, check_harde_wanden)

check_cell("NB1_botsingsvoorwaarde", notebook_1, check_botsingsvoorwaarde)

check_cell("NB1_eindantwoord", notebook_1, check_eindantwoord, variable="num_botsingen")


##### GENERATE MARKDOWN REPORT #####
output = Path("codechecks.md")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w") as f:
    f.write("# Notebook checks\n\n")
    f.write("| Check | Status | Details |\n")
    f.write("|-------|--------|---------|\n")

    for name, passed, message in results:
        status = "✅ PASS" if passed else "❌ FAIL"

        # Keep exception messages inside one Markdown table cell
        details = str(message).replace("|", r"\|").replace("\n", "<br>")

        f.write(f"| {name} | {status} | {details} |\n")
