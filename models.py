"""
Data models and Pydantic schemas for Gnaan U Teaching Method Finder.
Adheres strictly to the Gnaan U Final Master Specification:
- Universal: Works across ALL Maharashtra grades, subjects, and textbook mediums.
- Strict Source Fidelity: Absolute separation of source facts vs. inference notes.
- 3 Validation States: VALID_METHOD | REVIEW_REQUIRED | REJECTED.
- Comprehensive Source Metadata (Board, Publisher, Standard, Medium, Subject, Book, Chapter, Section, Pages).
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class SourceMetadata(BaseModel):
    board: str = Field(default="Maharashtra State Board", description="Educational board")
    publisher: str = Field(default="Balbharati", description="Textbook publisher")
    standard: str = Field(default="Not specified in source.", description="Grade/Standard e.g. Standard 7, Standard 4")
    medium: str = Field(default="English", description="Medium of instruction e.g. English, Marathi, Semi-English")
    subject: str = Field(default="Not specified in source.", description="Subject name e.g. Science, Mathematics, Geography")
    book: str = Field(..., description="Book title / document name")
    chapter: str = Field(default="Not specified in source.", description="Chapter name and number")
    section: str = Field(default="", description="Section name or header")
    pages: List[int] = Field(default_factory=list, description="List of 1-indexed page numbers")


class TeachingMethodCandidate(BaseModel):
    # Core Identification & Status
    method_name: str = Field(
        ...,
        description="A clear, source-grounded name describing the instructional procedure"
    )
    validation_status: Literal["VALID_METHOD", "REVIEW_REQUIRED", "REJECTED"] = Field(
        ...,
        description="VALID_METHOD (reusable complete method), REVIEW_REQUIRED (incomplete/ambiguous procedure), REJECTED (not a method)"
    )
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(
        ...,
        description="Confidence level in the extraction and validation verdict"
    )

    # Conceptual & Contextual Grounding
    learning_focus: str = Field(
        ...,
        description="Exact concept or part of concept addressed (do NOT copy question title or use generic boilerplate)"
    )
    intended_learners_context: str = Field(
        default="Not specified in source.",
        description="Grade/level and teaching conditions explicitly supported by source"
    )
    teaching_approach: str = Field(
        default="Not specified in source.",
        description="Description of the actual instructional approach supported by source (never invent pedagogical buzzwords)"
    )

    # Procedural Core (Source-supported sequence)
    instructional_procedure: List[str] = Field(
        default_factory=list,
        description="Ordered sequence of teacher guidance and student actions directly supported by the source"
    )
    student_effort: List[str] = Field(
        default_factory=list,
        description="Cognitive and physical actions students perform (e.g. observation, comparison, measurement) explicitly supported by source"
    )
    learning_connection: str = Field(
        default="Not explicitly established in source.",
        description="How the actions develop the intended concept. If not established: 'Not explicitly established in source.'"
    )

    # Scaffolding & Setup
    questions_or_prompts: List[str] = Field(
        default_factory=list,
        description="Reasoning prompts or questions explicitly stated in the source"
    )
    resources_setup: List[str] = Field(
        default_factory=lambda: ["Not specified in source."],
        description="Specific materials/apparatus supported by source. If none: ['Not specified in source.']"
    )
    practical_conditions: str = Field(
        default="Not specified in source.",
        description="Duration, environment, or precautions explicitly mentioned in the source"
    )
    indications_of_learning: List[str] = Field(
        default_factory=lambda: ["Not specified in source."],
        description="What students should be able to explain, identify, calculate, or demonstrate as stated by source"
    )

    # Provenance & Evidence Traceability
    source: SourceMetadata = Field(
        ...,
        description="Structured source metadata containing board, publisher, standard, medium, subject, book, chapter, and page numbers"
    )
    source_evidence: str = Field(
        ...,
        description="Clean, traceable verbatim source quote or faithful excerpt without artifacts or repeated headers"
    )

    # Validation Audit & Separation of Inference
    validation_reason: str = Field(
        ...,
        description="Detailed justification of why it is VALID_METHOD, REVIEW_REQUIRED, or REJECTED"
    )
    missing_information: List[str] = Field(
        default_factory=list,
        description="Specific aspects (steps, learning link, resources, target outcomes) missing or ambiguous in source"
    )
    source_quality: Literal["CLEAN", "PARTIALLY_CORRUPTED", "CORRUPTED"] = Field(
        default="CLEAN",
        description="Quality of the extracted text layer: CLEAN, PARTIALLY_CORRUPTED, or CORRUPTED"
    )
    inference_notes: List[str] = Field(
        default_factory=list,
        description="Pedagogical inferences stored strictly separately from source facts. Never presented as source truth."
    )

    # Helper properties for UI / DataFrame compatibility
    @property
    def pages_display(self) -> str:
        if not self.source.pages:
            return "Unknown"
        if len(self.source.pages) == 1:
            return f"Page {self.source.pages[0]}"
        return f"Pages {self.source.pages[0]}-{self.source.pages[-1]}"

    def to_compact_dict(self) -> Dict[str, Any]:
        """Provides a compact, clean dictionary for the primary structured table view."""
        return {
            "Method Name": self.method_name,
            "Status": self.validation_status,
            "Confidence": self.confidence,
            "Standard": self.source.standard,
            "Subject": self.source.subject,
            "Medium": self.source.medium,
            "Learning Focus": self.learning_focus,
            "Procedure Steps": " \u2192 ".join(self.instructional_procedure) if self.instructional_procedure else "Not specified in source.",
            "Student Effort": ", ".join(self.student_effort) if self.student_effort else "Not specified in source.",
            "Resources": ", ".join(self.resources_setup) if self.resources_setup else "Not specified in source.",
            "Location": f"{self.source.chapter} ({self.pages_display})",
            "Validation Reason": self.validation_reason,
            "Missing Details": "; ".join(self.missing_information) if self.missing_information else "None"
        }

    def to_flat_dict(self) -> Dict[str, Any]:
        """Flattens all fields for detailed CSV/JSON export."""
        return {
            "method_name": self.method_name,
            "validation_status": self.validation_status,
            "confidence": self.confidence,
            "board": self.source.board,
            "publisher": self.source.publisher,
            "standard": self.source.standard,
            "medium": self.source.medium,
            "subject": self.source.subject,
            "book": self.source.book,
            "chapter": self.source.chapter,
            "section": self.source.section,
            "pages": self.pages_display,
            "learning_focus": self.learning_focus,
            "intended_learners_context": self.intended_learners_context,
            "teaching_approach": self.teaching_approach,
            "instructional_procedure": " | ".join(self.instructional_procedure) if self.instructional_procedure else "Not specified in source.",
            "student_effort": ", ".join(self.student_effort) if self.student_effort else "Not specified in source.",
            "learning_connection": self.learning_connection,
            "questions_or_prompts": " | ".join(self.questions_or_prompts) if self.questions_or_prompts else "None",
            "resources_setup": ", ".join(self.resources_setup) if self.resources_setup else "Not specified in source.",
            "practical_conditions": self.practical_conditions,
            "indications_of_learning": ", ".join(self.indications_of_learning) if self.indications_of_learning else "Not specified in source.",
            "source_evidence": self.source_evidence,
            "validation_reason": self.validation_reason,
            "missing_information": "; ".join(self.missing_information) if self.missing_information else "None",
            "source_quality": self.source_quality,
            "inference_notes": "; ".join(self.inference_notes) if self.inference_notes else "None"
        }


class MethodFinderResponse(BaseModel):
    candidates: List[TeachingMethodCandidate] = Field(
        default_factory=list,
        description="List of all detected instructional candidates with their validation assessment"
    )
