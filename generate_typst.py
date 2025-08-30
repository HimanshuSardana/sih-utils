import json
import os
from typing import Any, List

files = os.listdir("ideas")
print(files)

typst_template = f"""
#import "@preview/zebraw:0.5.5": *
#show: zebraw
#let title = "Authentication"
#set heading(numbering: "I.1")

#show heading.where(level: 1): it => block[
  #text(font: "Montserrat", size: 26pt, fill: blue)[#it.body]
  #v(-2mm)
  #line(length: 100%, stroke: (thickness: 0.0pt, paint: blue, dash: "dashed"))
  #v(1mm)
]

#show heading.where(level: 2): it => block[
  #set text(font: "Montserrat")
  #text(size: 12pt, fill: blue)[#it.body]
]

#show raw: set text(font: "Iosevka NF")

#show heading.where(level: 1): it => block[
  #set text(font: "Montserrat")
  #text(size: 12pt, fill: blue, weight: "extrabold")[Chapter #counter(heading).display()] \\
  #text(size: 20pt, weight: "extrabold")[#it.body]
  #v(-2mm)
  #line(length: 100%, stroke: (thickness: 1.5pt, paint: blue, dash: "dashed"))
  #v(1mm)
]

"""

for idx, file in enumerate(files):
    if file.endswith(".json"):
        with open(os.path.join("ideas", file), "r") as f:
            data: dict[str, Any] = json.load(f)

        problem_statement: str = data.get("problem_statement", "")
        idea: str = data.get("idea", "")
        problem_resolution: str = data.get("problem_resolution", "")
        how_it_works: str = data.get("how_it_works", "")
        feasibility_points: List[str] = data.get("feasibility_points", [])
        viability_points: List[str] = data.get("viability_points", [])
        impact_points: List[str] = data.get("impact_points", [])
        beneficiaries: List[str] = data.get("beneficiaries", [])

        typst_content = (
            "= Problem Statement\n"
            f"{problem_statement}\n\n"
            "== Idea\n"
            f"{idea}\n\n"
            "== Problem Resolution\n"
            f"{problem_resolution}\n\n"
            "== How It Works\n"
            f"{how_it_works}\n\n"
            "== Feasibility and Viability\n"
            + ("- " + "\n- ".join(feasibility_points) if feasibility_points else "")
            + ("\n- " + "\n- ".join(viability_points) if viability_points else "")
            + "\n\n"
            "== Impact and Beneficiaries\n"
            + ("- " + "\n- ".join(impact_points) if impact_points else "")
            + ("\n- " + "\n- ".join(beneficiaries) if beneficiaries else "")
            + "\n\n#pagebreak()\n"
        )

        typst_template += typst_content
with open(f"output/final.typ", "w") as out_f:
    out_f.write(typst_template)
    os.system(f"typst compile output/final.typ pdfs/final.pdf > /dev/null 2>&1")
print(f"Processed {file}")

