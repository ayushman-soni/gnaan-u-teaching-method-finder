"""
Generates Deliverable D4 & D5 outputs:
Runs the pipeline on the sample Maharashtra Grade 7 Science textbook PDF,
and exports the structured results to JSON and CSV formats matching all Section 5 fields.
"""

import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(__file__))

from pipeline import ExtractionPipeline


def run_and_export():
    sample_pdf = os.path.join(os.path.dirname(__file__), "sample_data", "mh_grade7_science_sample.pdf")
    export_dir = os.path.join(os.path.dirname(__file__), "exports")
    os.makedirs(export_dir, exist_ok=True)

    csv_path = os.path.join(export_dir, "gnaan_u_methods_mh_grade7.csv")
    json_path = os.path.join(export_dir, "gnaan_u_methods_mh_grade7.json")

    print(f"Ingesting PDF: {sample_pdf}")
    pipeline = ExtractionPipeline()
    result = pipeline.run(sample_pdf, book_title="Maharashtra State Board Grade 7 Science")
    candidates = result["candidates"]

    print(f"Extracted and validated {len(candidates)} candidates from {result['scanned_pages']} pages.")
    for c in candidates:
        print(f" -> [{c.validation_status}] {c.method_name} ({c.pages_display})")

    # Export D4 outputs
    pipeline.export_csv(candidates, csv_path)
    pipeline.export_json(candidates, json_path)

    print(f"Exported CSV to: {csv_path}")
    print(f"Exported JSON to: {json_path}")
    return candidates


if __name__ == "__main__":
    run_and_export()
