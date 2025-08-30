import json
import os
from typing import Any

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
  #text(size: 12pt, fill: blue, weight: "extrabold")[Problem Statement #counter(heading).display()] \\
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

        need_to_know: str = data.get("need_to_know", "")
        original_problem_statement: str = data.get("original_problem_statement", "")
        category: str = data.get("category", "")
        problem_statement: str = data.get("problem_statement", "")
        idea: str = data.get("idea", "")
        usps: list[str] = data.get("usps", [])
        problem_resolution: str = data.get("problem_resolution", "")
        how_it_works: str = data.get("how_it_works", "")
        feasibility_points: list[str] = data.get("feasibility_points", [])
        viability_points: list[str] = data.get("viability_points", [])
        impact_points: list[str] = data.get("impact_points", [])
        beneficiaries: list[str] = data.get("beneficiaries", [])

        typst_lines = [
            f"= {original_problem_statement} ({category})",
            "",
            "== Need to Know",
            f"{need_to_know}",
            "",
            "== Description",
            f"{problem_statement}",
            "",
            "== Idea",
            f"{idea}",
            "",
            "== Problem Resolution",
            f"{problem_resolution}",
            "",
            "== How It Works",
            f"{how_it_works}",
            "",
            "== Unique Selling Points",
        ]
        if usps:
            typst_lines.extend(f"- {usp}" for usp in usps)
        typst_lines.append("== Feasibility and Viability")
        if feasibility_points:
            typst_lines.extend(f"- {point}" for point in feasibility_points)
        if viability_points:
            typst_lines.extend(f"- {point}" for point in viability_points)
        typst_lines.append("")
        typst_lines.append("== Impact and Beneficiaries")
        if impact_points:
            typst_lines.extend(f"- {point}" for point in impact_points)
        if beneficiaries:
            typst_lines.extend(f"- {b}" for b in beneficiaries)
        typst_lines.append("")
        typst_lines.append("#pagebreak()")
        typst_content = "\n".join(typst_lines)

        typst_template += typst_content
        typst_template += "\n\n"
with open(f"output/final.typ", "w") as out_f:
    out_f.write(typst_template)
    os.system(f"typst compile output/final.typ pdfs/final.pdf > /dev/null 2>&1")
print(f"Processed {file}")

