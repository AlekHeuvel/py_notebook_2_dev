from pathlib import Path
import re

SOURCE = Path("simulations")
OUTPUT = Path("output")

for file in SOURCE.rglob("*.md"):
    content = file.read_text(encoding="utf-8")

    # Verwijder interne secties
    content = re.sub(
        r"### begin-solution.*?### end-solution\n",
        "# your code here\\n",
        content,
        flags=re.DOTALL
    )

    # Behoud directorystructuur
    destination = OUTPUT / file.relative_to(SOURCE)
    destination.parent.mkdir(parents=True, exist_ok=True)

    destination.write_text(content, encoding="utf-8")

    print(f"Processed: {file}")