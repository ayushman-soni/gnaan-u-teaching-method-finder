# 📖 Gnaan U — Teaching Method Finder
### Complete Project Specification & Internship Deliverables Handover
**Submitted by:** Ayushman Soni  
**Project:** Curriculum Analysis & Teaching Method Finder Prototype for Maharashtra State Board Textbooks  
**Deliverables Covered:** D1 to D9  

---

## 📌 1. Project Overview & Objective
This project implements the **Gnaan U Teaching Method Finder**, an automated curriculum analysis tool that parses Maharashtra State Board textbooks (Grades 1 through 12 across Science, Mathematics, Social Studies, and Languages) to identify, validate, and document **genuine Teaching Methods**.

Rather than simple keyword extraction, the system enforces Gnaan U's strict 5-pillar pedagogical definition to distinguish reproducible, evidence-backed instructional routines from vague teaching advice, isolated assessment questions, and standalone resources.

### The 3 Pedagogical Validation States:
1. **`VALID_METHOD`**: Complete instructional procedure with concrete steps, specific materials, active student effort, and an explicit connection between activity and conceptual learning.
2. **`REVIEW_REQUIRED`**: Meaningful instructional intent or exploratory prompt is present, but procedural steps, recording protocols, or the theoretical connection are incomplete or ambiguous in the source text (e.g. *Plant Identification in Grade 7 Science*).
3. **`REJECTED`**: Generic advice (*"Teacher should discuss"*, *"Use a diagram"*), standalone resources (*"Educational Video CD"*), or isolated end-of-chapter questions.

---

## 📁 2. Deliverables Handover Directory (D1 – D9)

| Deliverable | File / Directory | Description |
| :--- | :--- | :--- |
| **D1: Prompt & Guidelines** | [`D1_PROMPT_GUIDELINES.md`](D1_PROMPT_GUIDELINES.md)<br>[`prompts.py`](prompts.py) | Final prompt and operational rules document: 5 pillars, rejection criteria, few-shot calibration, and strict schema. |
| **D2: Working Prototype** | [`app.py`](app.py) | Interactive web application with PDF ingestion, scan scope controls, primary structured table output, and drill-down inspection. |
| **D3: Extraction Pipeline** | [`pipeline.py`](pipeline.py)<br>[`models.py`](models.py) | Page-level text extraction with artifact cleaning (no header/number leakage), metadata tracking, and deduplication. |
| **D4: Structured Data Output** | [`exports/gnaan_u_methods_mh_grade7.json`](exports/gnaan_u_methods_mh_grade7.json)<br>[`exports/gnaan_u_methods_mh_grade7.csv`](exports/gnaan_u_methods_mh_grade7.csv) | Machine-readable exports adhering to all 18 Section 16 fields. |
| **D5: Textbook Demonstration** | [`sample_data/mh_grade7_science_sample.pdf`](sample_data/mh_grade7_science_sample.pdf)<br>[`run_demo_export.py`](run_demo_export.py) | End-to-end execution on Maharashtra Grade 7 Science (Chromatography, Magnetism, Plant Identification). |
| **D6: Evaluation Test Cases** | [`evaluation/test_cases.json`](evaluation/test_cases.json) | Curated benchmark dataset labeled across 4 categories (valid method, incomplete, resource, non-method). |
| **D7: Evaluation Report** | [`evaluation/evaluation_report.md`](evaluation/evaluation_report.md) | Benchmark report showing **100% classification accuracy (8/8 test cases)** with zero hallucinations. |
| **D8: Setup Documentation** | [`README.md`](README.md)<br>[`requirements.txt`](requirements.txt) | Complete installation and environment execution guide. |
| **D9: End-to-End Demo** | See [Section 5 below](#-5-demo-workflow-d9) | Step-by-step verification and delivery walkthrough. |

---

## 💻 3. Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Pip

### Install Dependencies
```bash
cd "C:\Users\Ayushman Soni\.gemini\antigravity\scratch\gnaan_u_teaching_method_finder"
pip install -r requirements.txt
```

---

## 🚀 4. How to Run the Application

### Launch the Web Prototype (Primary Structured Table View):
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

1. Click **"🚀 Load MH Grade 7 Demo"** (or upload any Maharashtra textbook PDF).
2. Click **"🔍 Find Teaching Methods"**.
3. The system directly presents the **Structured Table View** containing all validated candidates, page references, and reasons.
4. Download the full dataset as **CSV** or **JSON** using the export buttons.

### Run the Evaluation Benchmark Suite:
```bash
python evaluation/run_evaluation.py
```
Runs the automated test suite across all 8 benchmark test cases with 100% precision.

---

## 🎬 5. Demo Workflow (D9)

1. **Input**: User uploads a Maharashtra textbook (or loads Grade 7 Science demo).
2. **Text Processing**: Text layer is cleaned of running headers, repeated numbers (`10 10`), and OCR artifacts (`K...`).
3. **Extraction & Validation**: The pipeline extracts procedures and tests them against Gnaan U criteria.
4. **Structured Table Presentation**: Instantly renders columns for *Method Name*, *Validation Status*, *Learning Focus*, *Procedure Steps*, *Student Effort*, *Resources*, *Location*, *Source Evidence*, and *Validation Reason*.
5. **Auditing**: Teacher/auditor can inspect specific cards or download the complete CSV/JSON library.
