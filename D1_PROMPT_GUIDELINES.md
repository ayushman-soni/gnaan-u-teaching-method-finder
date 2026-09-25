# Gnaan U — Teaching Method Finder: Guidelines & Prompt Specification (Deliverable D1)

## 1. Objective & Purpose
The Gnaan U Teaching Method Finder is an intelligent pedagogical extraction system designed to analyze educational textbooks (specifically the Maharashtra State Board curriculum) and identify, validate, and document **genuine Teaching Methods**.

The system is **NOT a keyword extractor**. It operationalizes Gnaan U's strict pedagogical criteria to distinguish a complete, reproducible, evidence-backed instructional procedure from generic teaching suggestions, standalone resources, isolated questions, or broad pedagogical buzzwords.

---

## 2. What Counts as a Genuine Teaching Method (The 5 Core Pillars)
An entry can only be validated with status **VALID_METHOD** if all five of the following pillars are concretely substantiated by evidence directly traceable to the textbook text:

1. **Specific Learning Focus**:
   - The exact curriculum concept, sub-concept, or cognitive skill students are expected to learn or understand.
   - *Example:* "Identifying plants using observable differences in their plant parts (roots, stems, leaves, flowers)" (do NOT use question titles or generic labels like "Hands-on investigation in...").

2. **Intended Learners & Context**:
   - Explicit target grade level (e.g., Grade 7 Science), prerequisites, instructional constraints, or environmental requirements stated in the curriculum. If absent: `"Not specified in source."`.

3. **Concrete Instructional Procedure**:
   - An ordered sequence of teacher guidance and student actions directly supported by the source.
   - Do NOT transform a one-line prompt into an invented lesson plan.

4. **Explicit Connection to Learning (Pedagogical Logic)**:
   - Clear articulation of *how* and *why* the physical actions, observations, or problem-solving steps generate the conceptual understanding.
   - If missing: `"Not explicitly established in source."`.

5. **Meaningful Student Effort**:
   - Active student cognitive effort: systematic observation, comparison, measurement, classification, calculation, prediction, or explanation.
   - Passive consumption (listening, copying notes, looking at a picture) does not qualify.

---

## 3. The Three Validation States

### State 1: `VALID_METHOD`
- The source provides sufficient evidence for a complete, coherent, reusable instructional procedure.
- All central operational steps, materials, student effort, and conceptual bridges are present and traceable.

### State 2: `REVIEW_REQUIRED`
- There is a potentially useful instructional intent or activity prompt, but the source is incomplete, ambiguous, corrupted, or lacks necessary operational detail or explicit conceptual grounding.
- *Example:* "What helps us to easily identify the plants around us? Observe the plants around you and discuss their parts with your classmates." -> `REVIEW_REQUIRED` because the operational recording protocol and guidance sequence are insufficiently specified.
- The system must explicitly document what is missing in `missing_information`.

### State 3: `REJECTED`
The content is clearly not a Teaching Method. Immediate rejections include:
1. **Generic Verbs without Procedure**: Sentences such as *"Discuss with peers"*, *"Use a diagram to explain"*, *"Show a chart"*, *"Do an experiment"*, or *"Teacher will ask questions"*.
2. **Resource Mentions Alone**: Merely listing a worksheet, video, test-tube, magnet, or textbook chapter without an instructional routine.
3. **Broad Category Labels**: Generic labels like *"Inquiry-based learning"*, *"Experiential learning"*, *"Group work"*, or *"Constructivism"*.
4. **Isolated Questions / End-of-Chapter Exercises**: Standalone test questions or summative exam reviews.

---

## 4. Zero-Hallucination & Text Quality Invariants
- **Rule of Strict Fidelity**: The model must **NEVER invent** materials, safety precautions, prerequisites, teacher actions, or procedural steps not supported by the textbook excerpt.
- **Traceability**: Every candidate must link directly to the verified `pages`, `chapter`, and provide a concise verbatim `source_evidence` quote without extraction artifacts (`[Page X]`, `10 10`, `K...`).
- **Source Quality**: Every extracted page is classified as `CLEAN`, `PARTIALLY_CORRUPTED`, or `CORRUPTED`. If extraction corruption affects validation, the candidate is marked `REVIEW_REQUIRED`.

---

## 5. System Extraction Schema (Section 16 Standard)

```json
{
  "candidates": [
    {
      "method_name": "string",
      "validation_status": "VALID_METHOD | REVIEW_REQUIRED | REJECTED",
      "confidence": "HIGH | MEDIUM | LOW",
      "learning_focus": "string",
      "intended_learners_context": "string",
      "teaching_approach": "string",
      "instructional_procedure": ["step 1", "step 2"],
      "student_effort": ["action 1", "action 2"],
      "learning_connection": "string",
      "questions_or_prompts": ["prompt 1"],
      "resources_setup": ["item 1", "item 2"],
      "practical_conditions": "string",
      "indications_of_learning": ["outcome 1"],
      "source": {
        "book": "string",
        "chapter": "string",
        "section": "string",
        "pages": [1]
      },
      "source_evidence": "string",
      "validation_reason": "string",
      "missing_information": ["missing detail 1"],
      "source_quality": "CLEAN | PARTIALLY_CORRUPTED | CORRUPTED"
    }
  ]
}
```
