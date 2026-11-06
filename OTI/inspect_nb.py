import json

with open("EDA.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, cell in enumerate(nb["cells"]):
    src = "".join(cell["source"])[:300]
    print(f"\n--- Cell {i} ({cell['cell_type']}) ---")
    print(src if src else "(empty)")
