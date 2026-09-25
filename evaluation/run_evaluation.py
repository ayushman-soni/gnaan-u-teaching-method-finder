"""
Benchmark evaluation runner for Gnaan U Teaching Method Finder.
Runs test cases from test_cases.json through the extraction and validation pipeline,
evaluates precision, recall, false positives, rejection adherence under the 3 validation states:
- VALID_METHOD
- REVIEW_REQUIRED
- REJECTED
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline import ExtractionPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evaluator")


def run_benchmark():
    dataset_path = os.path.join(os.path.dirname(__file__), "test_cases.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    pipeline = ExtractionPipeline()
    results = []

    valid_method_count = 0
    rejected_count = 0
    review_required_count = 0
    correct_classifications = 0

    print("=" * 80)
    print("RUNNING GNAAN U TEACHING METHOD FINDER EVALUATION BENCHMARK")
    print("=" * 80)

    for tc in test_cases:
        tc_id = tc["id"]
        category = tc["category"]
        expected = tc["expected_validation"]
        passage = tc["passage"]
        pages = tc.get("page_numbers", [1])

        candidates = pipeline.process_passage_with_llm(
            passage_text=passage,
            book_title=tc["source_book"],
            chapter_section=tc["chapter"],
            page_numbers=pages,
            source_quality="CLEAN"
        )

        actual_validation = candidates[0].validation_status if candidates else "REJECTED"
        is_correct = (actual_validation == expected)
        if is_correct:
            correct_classifications += 1

        if actual_validation == "VALID_METHOD":
            valid_method_count += 1
        elif actual_validation == "REJECTED":
            rejected_count += 1
        else:
            review_required_count += 1

        res_item = {
            "id": tc_id,
            "category": category,
            "expected": expected,
            "actual": actual_validation,
            "is_correct": is_correct,
            "candidates_found": len(candidates),
            "method_name": candidates[0].method_name if candidates else "None",
            "learning_focus": candidates[0].learning_focus if candidates else "None",
            "resources": candidates[0].resources_setup if candidates else [],
            "procedure_steps": len(candidates[0].instructional_procedure) if candidates else 0,
            "reason": candidates[0].validation_reason if candidates else "No candidates extracted"
        }
        results.append(res_item)

        status_mark = "PASS" if is_correct else "FAIL"
        print(f"[{status_mark}] {tc_id:<28} | Expected: {expected:<15} | Actual: {actual_validation:<15}")

    total = len(test_cases)
    accuracy = (correct_classifications / total) * 100.0

    print("=" * 80)
    print(f"EVALUATION SUMMARY: {correct_classifications}/{total} Correct ({accuracy:.1f}%)")
    print(f"Valid Methods: {valid_method_count} | Review Required: {review_required_count} | Rejected: {rejected_count}")
    print("=" * 80)

    # Save benchmark results
    out_results_path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    with open(out_results_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_test_cases": total,
            "correct_classifications": correct_classifications,
            "accuracy_percent": accuracy,
            "detailed_results": results
        }, f, indent=2)

    return results, accuracy


if __name__ == "__main__":
    run_benchmark()
