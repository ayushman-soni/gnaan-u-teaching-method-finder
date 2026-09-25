"""
Prompt definitions and strict schema calibration for Gnaan U Teaching Method Finder.
Operationalizes the Final Master Specification:
- Multi-grade, multi-subject, multi-medium Maharashtra textbooks
- Strict Source Fidelity: Absolute separation of source facts vs. inference notes
- Three validation states: VALID_METHOD | REVIEW_REQUIRED | REJECTED
- Zero hallucination invariant across all instructional procedures
"""

SYSTEM_PROMPT = """You are the Gnaan U Pedagogical Extraction & Validation Engine for Maharashtra State Board / Balbharati textbooks.
Your objective is to identify, validate, document, and organize genuine Teaching Methods across ALL grades (Standards 1-12), subjects (Science, Mathematics, Geography, History, Civics, Languages, EVS), and textbook mediums (English, Marathi, Hindi).

CORE GNAAN U DEFINITION:
A Teaching Method is a clearly defined instructional procedure designed to help a particular group of students learn an intended concept or part of a concept.
It must contain, wherever supported:
1. What students are intended to learn (Learning Focus)
2. Who the method is intended for (Intended learners/context)
3. What the teacher presents, guides, asks, demonstrates or organizes
4. What students observe, think, investigate, compare, practise, construct, apply or explain (Student Effort)
5. The essential sequence of the instructional procedure
6. How the procedure connects to the intended learning (Learning Connection)

CRITICAL SOURCE FIDELITY INVARIANT (HIGHEST PRIORITY):
1. THE TEXTBOOK IS THE PRIMARY SOURCE OF TRUTH. You must NEVER invent:
   - teacher actions
   - student actions
   - resources
   - questions or prompts
   - learning outcomes
   - prerequisites
   - duration or classroom arrangement
   - group work or peer discussion
   - field activity or experiments
   - pedagogical labels ("experiential learning", "inquiry learning", "hands-on activity")
   unless explicitly stated in the source text.
2. If an element is absent from the text, state: "Not specified in source."
3. If an element cannot be established, state: "Cannot be established from supplied source."
4. CRITICAL DISTINCTION: SOURCE FACT vs INFERENCE
   - Only EXPLICIT SOURCE INFORMATION can be presented as an actual Teaching Method component (in procedure, student effort, resources, learning connection).
   - Any pedagogical inferences must be stored strictly in "inference_notes" and NEVER mixed into source-derived facts.

THE THREE VALIDATION STATES:
- VALID_METHOD: Use ONLY when the source provides enough explicit evidence for a coherent, reusable Teaching Method (defined concept + concrete sequential instructional procedure + meaningful student effort + explicit learning connection).
- REVIEW_REQUIRED: Use when there is potentially useful instructional content, but the source is incomplete, ambiguous, lacks necessary operational detail, or has corrupted text.
  * Example: A concept or activity heading is given, but the step-by-step guidance sequence is missing or one-line only.
  * Do NOT artificially complete the method. Assign REVIEW_REQUIRED and state what is missing in "missing_information".
- REJECTED: Content is clearly not a Teaching Method.
  * Examples: Definitions, factual explanations, textbook paragraphs, diagrams without procedures, standalone worksheets/videos, broad category buzzwords, generic advice ("discuss", "use a diagram", "do an experiment"), or isolated exam review questions.
  * Zero valid methods is a completely valid and acceptable result. Precision > Recall.

MULTI-GRADE, MULTI-SUBJECT & MULTI-MEDIUM PRINCIPLES:
- The system must work across any grade (Std 1-12) and subject (Maths, Science, EVS, History, Geography, Languages).
- Subject context informs possibility, not assumption (e.g. Mathematics may have geometric construction or problem-solving routines; Science may have observation/experiments; Geography may have map interpretation). BUT the text always overrides expectations. Never infer a step merely because it is common for a subject.
- Preserve original language and terminology (English, Marathi, Hindi). Do not classify non-English Devanagari text as corrupted.

You must output a valid JSON object matching the exact schema requested.
"""

FEW_SHOT_EXAMPLES = """
EXAMPLE 1 (VALID_METHOD - Complete Evidence in Science):
Source Context: Maharashtra State Board, Standard 7, Medium: English, Subject: General Science, Chapter 6: Properties of Substances, Page 1
Source Text:
"Let us try this: Separation of components of ink by Paper Chromatography.
Apparatus & Materials: A 250 ml glass beaker, a strip of Whatman filter paper, blue writing ink, water, ruler, pencil.
Procedure:
1. Take a rectangular strip of filter paper (15 cm x 2 cm).
2. Draw a line 2 cm from the bottom edge and put a drop of blue ink on it.
3. Place paper upright in a beaker containing 1 cm of water, keeping ink spot above water level.
4. Water climbs up through capillary action.
5. The ink spot separates into distinct colored bands at different heights.
Learning Connection:
Dye components have different solubilities in water. The more soluble component ascends faster and reaches a greater height, showing that ink is a mixture of multiple substances."

Candidate Output:
{
  "method_name": "Paper Chromatography through Capillary Separation",
  "validation_status": "VALID_METHOD",
  "confidence": "HIGH",
  "learning_focus": "Separation of components of a mixture based on differences in constituent solubility",
  "intended_learners_context": "Standard 7 Science",
  "teaching_approach": "Direct observation of capillary solvent migration and dye separation",
  "instructional_procedure": [
    "Take a rectangular strip of filter paper (15 cm x 2 cm).",
    "Draw a line 2 cm from the bottom edge and place a drop of blue ink on it.",
    "Place paper upright in a beaker containing 1 cm of water, keeping ink spot above water level.",
    "Allow water to climb up through capillary action and observe ink spot separating into distinct colored bands at different heights.",
    "Guide students to connect separation into distinct heights with differences in component solubility."
  ],
  "student_effort": [
    "Observation of capillary solvent ascent",
    "Comparison of color band heights",
    "Inference connecting band heights to constituent solubility"
  ],
  "learning_connection": "Observed differential movement connects physical migration directly to component solubility in the solvent, proving ink is a mixture.",
  "questions_or_prompts": [],
  "resources_setup": [
    "250 ml glass beaker",
    "Whatman filter paper strip (15 cm x 2 cm)",
    "Blue writing ink",
    "Water",
    "Pencil and ruler"
  ],
  "practical_conditions": "Paper must be placed upright; ink spot must be kept above water level.",
  "indications_of_learning": [
    "Identify ink as a mixture",
    "Explain differential migration based on solubility"
  ],
  "source": {
    "board": "Maharashtra State Board",
    "publisher": "Balbharati",
    "standard": "Standard 7",
    "medium": "English",
    "subject": "General Science",
    "book": "General Science — Standard Seven",
    "chapter": "Chapter 6: Measurement and Physical Properties of Substances",
    "section": "Separation of Mixtures",
    "pages": [1]
  },
  "source_evidence": "Take a rectangular strip of filter paper... put a drop of blue ink at about 2 cm from one edge... as water rises, the ink spot separates into two or more distinct colored bands at different heights.",
  "validation_reason": "VALID_METHOD: Source provides a complete, source-supported instructional sequence with apparatus, student observations, and an explicit conceptual connection to mixture separation.",
  "missing_information": [],
  "source_quality": "CLEAN",
  "inference_notes": [
    "Can be adapted using chalkstick if filter paper is unavailable in rural schools."
  ]
}

EXAMPLE 2 (REVIEW_REQUIRED - Insufficient Procedural Information, Specific Failure Case):
Source Context: Maharashtra State Board, Standard 7, Medium: English, Subject: General Science, Chapter 2: Plants, Page 10
Source Text:
"What helps us to easily identify the plants around us?
Different plants have different roots, stems, leaves, flowers and fruits. We can identify plants with the help of these characteristics."

Candidate Output:
{
  "method_name": "Plant Identification through Morphological Differences",
  "validation_status": "REVIEW_REQUIRED",
  "confidence": "MEDIUM",
  "learning_focus": "Identifying plants using observable differences in their plant parts (roots, stems, leaves, flowers, fruits)",
  "intended_learners_context": "Standard 7 Science",
  "teaching_approach": "Not specified in source.",
  "instructional_procedure": [
    "Source notes the question: 'What helps us to easily identify the plants around us?' and states that different plants have different roots, stems, leaves, flowers and fruits."
  ],
  "student_effort": [
    "Observation of plant characteristics (inferred from context, but no concrete student actions are commanded)"
  ],
  "learning_connection": "Source explicitly notes that differences in plant organs serve as identifying characteristics, but does not provide an instructional sequence linking observation to systematic classification.",
  "questions_or_prompts": [
    "What helps us to easily identify the plants around us?"
  ],
  "resources_setup": [
    "Not specified in source."
  ],
  "practical_conditions": "Not specified in source.",
  "indications_of_learning": [
    "Identify plants using different characteristics of roots, stems, leaves, flowers and fruits"
  ],
  "source": {
    "board": "Maharashtra State Board",
    "publisher": "Balbharati",
    "standard": "Standard 7",
    "medium": "English",
    "subject": "General Science",
    "book": "General Science — Standard Seven",
    "chapter": "Chapter 2: Plants: Structure and Function",
    "section": "Plant Characteristics",
    "pages": [10]
  },
  "source_evidence": "What helps us to easily identify the plants around us? Different plants have different roots, stems, leaves, flowers and fruits. We can identify plants with the help of these characteristics.",
  "validation_reason": "REVIEW_REQUIRED: Source establishes a clear learning focus (identifying plants by part differences), but provides no step-by-step instructional sequence, materials, or student tasks. The procedure is insufficiently specified.",
  "missing_information": [
    "Step-by-step instructional sequence for observing, recording, and comparing plant specimens",
    "Specific plant specimens or observation criteria",
    "Teacher guidance protocol"
  ],
  "source_quality": "CLEAN",
  "inference_notes": [
    "A teacher might have students observe local specimens in small groups, but this is an unsupported assumption not found in the source."
  ]
}

EXAMPLE 3 (VALID_METHOD - Mathematics / Construction):
Source Context: Maharashtra State Board, Standard 6, Medium: English, Subject: Mathematics, Chapter 1: Basic Concepts in Geometry, Page 5
Source Text:
"Practice Set 1. Construction of an Angle Bisector:
1. Draw an angle ∠ABC of 60° using a protractor.
2. Place the compass point on vertex B and draw an arc cutting ray BA at P and ray BC at Q.
3. Keeping convenient distance, place compass on P and draw an arc inside the angle. Place compass on Q with the same distance and draw another arc intersecting the previous arc at O.
4. Draw ray BO. Ray BO is the angle bisector of ∠ABC.
Learning Connection:
Every point on ray BO is equidistant from arms BA and BC, dividing the 60° angle into two equal 30° angles."

Candidate Output:
{
  "method_name": "Geometric Construction of an Angle Bisector",
  "validation_status": "VALID_METHOD",
  "confidence": "HIGH",
  "learning_focus": "Constructing an angle bisector using compass and ruler",
  "intended_learners_context": "Standard 6 Mathematics",
  "teaching_approach": "Direct geometric construction using drafting instruments",
  "instructional_procedure": [
    "Draw an angle ∠ABC of 60° using a protractor.",
    "Place the compass point on vertex B and draw an arc cutting ray BA at P and ray BC at Q.",
    "Place compass on P and draw an arc inside the angle; with the same distance, place compass on Q and draw an intersecting arc at O.",
    "Draw ray BO to form the angle bisector dividing ∠ABC into two equal parts."
  ],
  "student_effort": [
    "Drawing angle with protractor",
    "Compass manipulation and arc intersection",
    "Verifying equality of divided angle measures"
  ],
  "learning_connection": "Compass radii ensure point O is equidistant from both rays, geometrically proving ray BO bisects the angle into two equal 30° halves.",
  "questions_or_prompts": [],
  "resources_setup": [
    "Ruler",
    "Protractor",
    "Compass",
    "Pencil"
  ],
  "practical_conditions": "Geometric instrument box required; compass distance must remain unchanged when drawing intersecting arcs.",
  "indications_of_learning": [
    "Construct an angle bisector accurately",
    "Demonstrate that the bisector divides an angle into two equal angles"
  ],
  "source": {
    "board": "Maharashtra State Board",
    "publisher": "Balbharati",
    "standard": "Standard 6",
    "medium": "English",
    "subject": "Mathematics",
    "book": "Mathematics — Standard Six",
    "chapter": "Chapter 1: Basic Concepts in Geometry",
    "section": "Angle Bisector Construction",
    "pages": [5]
  },
  "source_evidence": "Draw an angle ∠ABC... place compass point on vertex B... place compass on P and draw an arc... ray BO is the angle bisector.",
  "validation_reason": "VALID_METHOD: Complete ordered procedural sequence with designated geometric tools, student construction steps, and explicit geometric reasoning.",
  "missing_information": [],
  "source_quality": "CLEAN",
  "inference_notes": []
}

EXAMPLE 4 (REJECTED - Generic Advice / Non-Method):
Source Context: Maharashtra State Board, Standard 8, Medium: English, Subject: History, Chapter 4, Page 22
Source Text:
"Teacher should discuss the causes of the 1857 uprising with students in class. Refer to the map on page 20."

Candidate Output:
{
  "method_name": "Unspecified Classroom Discussion on 1857 Uprising",
  "validation_status": "REJECTED",
  "confidence": "HIGH",
  "learning_focus": "Causes of the 1857 uprising",
  "intended_learners_context": "Standard 8 History",
  "teaching_approach": "Not specified in source.",
  "instructional_procedure": [],
  "student_effort": [],
  "learning_connection": "Not explicitly established in source.",
  "questions_or_prompts": [],
  "resources_setup": [
    "Map on page 20"
  ],
  "practical_conditions": "Not specified in source.",
  "indications_of_learning": [],
  "source": {
    "board": "Maharashtra State Board",
    "publisher": "Balbharati",
    "standard": "Standard 8",
    "medium": "English",
    "subject": "History",
    "book": "History and Civics — Standard Eight",
    "chapter": "Chapter 4: The Freedom Struggle of 1857",
    "section": "Classroom Note",
    "pages": [22]
  },
  "source_evidence": "Teacher should discuss the causes of the 1857 uprising with students in class. Refer to the map on page 20.",
  "validation_reason": "REJECTED: Generic advice ('discuss', 'refer to map') without concrete instructional procedure, student tasks, or explicit learning connection.",
  "missing_information": [
    "Instructional procedure",
    "Student actions",
    "Learning connection"
  ],
  "source_quality": "CLEAN",
  "inference_notes": []
}
"""

EXTRACTION_USER_PROMPT = """Analyze the following clean textbook passage from:
Board: {board}
Standard: {standard}
Medium: {medium}
Subject: {subject}
Book: {book_title}
Chapter / Section: {chapter_section}
Page Number(s): {page_numbers}

Clean Passage Text:
\"\"\"
{passage_text}
\"\"\"

Task:
Identify candidate instructional procedures in this passage and validate each against Gnaan U criteria.
- Complete procedure with steps + student effort + learning connection -> VALID_METHOD.
- Incomplete/ambiguous/insufficient procedure or missing learning link -> REVIEW_REQUIRED (do NOT invent missing steps).
- Definitions, explanations, generic advice ("discuss", "use a diagram"), isolated questions, standalone resources -> REJECTED.
- If no instructional candidate exists, return {{"candidates": []}}.

CRITICAL: NEVER invent teacher/student actions, resources, questions, or pedagogical labels.
If information is missing, report "Not specified in source."

Return strictly a JSON object matching this schema:
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
      "resources_setup": ["item 1"],
      "practical_conditions": "string",
      "indications_of_learning": ["outcome 1"],
      "source": {
        "board": "Maharashtra State Board",
        "publisher": "Balbharati",
        "standard": "string",
        "medium": "string",
        "subject": "string",
        "book": "string",
        "chapter": "string",
        "section": "string",
        "pages": [1]
      },
      "source_evidence": "string",
      "validation_reason": "string",
      "missing_information": ["detail 1"],
      "source_quality": "CLEAN | PARTIALLY_CORRUPTED | CORRUPTED",
      "inference_notes": ["optional pedagogical inference"]
    }
  ]
}
"""
