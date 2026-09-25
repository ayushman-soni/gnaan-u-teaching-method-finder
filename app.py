"""
Gnaan U — Teaching Method Finder
Internship Software Deliverable (D2 Prototype)
Submitted by: Ayushman Soni

Curriculum Analysis & Method Extractor for Maharashtra State Board Textbooks.
Ingests textbook PDFs, extracts structured teaching procedures, validates against
Gnaan U criteria (VALID_METHOD | REVIEW_REQUIRED | REJECTED), and displays
results in a clean, auditable structured table with instant CSV/JSON exports.
"""

import os
import json
import streamlit as st
import pandas as pd
import pymupdf

from pipeline import ExtractionPipeline
from models import TeachingMethodCandidate

# Page configuration
st.set_page_config(
    page_title="Gnaan U — Teaching Method Finder",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional Styling (Clean, human-built aesthetic)
st.markdown("""
<style>
    .project-header {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .project-meta {
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .intern-badge {
        background-color: #F1F5F9;
        color: #334155;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #CBD5E1;
    }
    .valid-badge {
        background-color: #DCFCE7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.82rem;
    }
    .review-badge {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.82rem;
    }
    .reject-badge {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.82rem;
    }
    .meta-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Project Setup & Controls
st.sidebar.markdown("### ⚙️ Parser Configuration")
api_key = st.sidebar.text_input(
    "API Key (Optional Cloud Mode)",
    type="password",
    help="Enter Gemini API Key if using cloud parser. Leave blank for deterministic offline rule extraction.",
    value=os.getenv("GEMINI_API_KEY", "")
)

backend_model = st.sidebar.selectbox(
    "Parser Engine",
    ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Table Rows")
validation_filter = st.sidebar.radio(
    "Filter by Status",
    ["All Candidates", "VALID_METHOD", "REVIEW_REQUIRED", "REJECTED"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Gnaan U Validation Definitions:**
- 🟢 **VALID_METHOD**: Complete, evidence-backed reusable procedure with steps, materials, and learning connection.
- 🟡 **REVIEW_REQUIRED**: Instructional intent is present, but procedure, recording criteria, or learning theory is incomplete in text.
- 🔴 **REJECTED**: Clearly not a method (definitions, generic talk, isolated questions, resource lists).
""")

st.sidebar.markdown("---")
st.sidebar.caption("Gnaan U Teaching Method Finder | Prototype Deliverable")

# Header Section
st.markdown('<div class="project-header">📖 Gnaan U — Teaching Method Finder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="project-meta">Maharashtra State Board Curriculum Extractor & Method Library &nbsp;|&nbsp; '
    '<span class="intern-badge">Student / Intern Submission: Ayushman Soni</span></div>',
    unsafe_allow_html=True
)

# Sample file path
sample_pdf_path = os.path.join(os.path.dirname(__file__), "sample_data", "mh_grade7_science_sample.pdf")

# Controls row
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload Maharashtra Textbook PDF (Balbharati / eBalbharati)",
        type=["pdf"],
        help="Upload an official Maharashtra State Board textbook PDF."
    )

with col2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    load_sample = st.button("🚀 Load MH Grade 7 Demo", use_container_width=True)

target_pdf = None
book_title_display = "Maharashtra State Board Textbook"

if uploaded_file is not None:
    target_pdf = uploaded_file
    book_title_display = uploaded_file.name
elif load_sample or "loaded_sample" in st.session_state:
    st.session_state["loaded_sample"] = True
    target_pdf = sample_pdf_path
    book_title_display = "Maharashtra State Board Grade 7 Science (Sample Chapters)"

# PDF Metadata Inspection & Scan Range Configuration
if target_pdf:
    try:
        if isinstance(target_pdf, str):
            doc = pymupdf.open(target_pdf)
        else:
            bytes_data = target_pdf.read()
            target_pdf.seek(0)
            doc = pymupdf.open(stream=bytes_data, filetype="pdf")

        total_pdf_pages = len(doc)
        doc.close()

        st.markdown(f"""
        <div class="meta-box">
            <b>Document:</b> {book_title_display} &nbsp;|&nbsp; <b>Total Pages:</b> {total_pdf_pages}
        </div>
        """, unsafe_allow_html=True)

        sc1, sc2 = st.columns([2, 2])
        with sc1:
            scan_mode = st.radio("Extraction Scope", ["Full Book", "Custom Page Range"], horizontal=True)
        with sc2:
            if scan_mode == "Custom Page Range":
                page_start, page_end = st.slider(
                    "Select Pages to Process",
                    min_value=1,
                    max_value=total_pdf_pages,
                    value=(1, min(15, total_pdf_pages))
                )
                selected_range = (page_start, page_end)
            else:
                selected_range = (1, total_pdf_pages)
                st.caption(f"Processing all {total_pdf_pages} pages.")

        if st.button("🔍 Find Teaching Methods", type="primary", use_container_width=True):
            progress_bar = st.progress(0.0)
            status_text = st.empty()

            def update_progress(current, total, count):
                pct = min(1.0, current / total)
                progress_bar.progress(pct)
                status_text.text(f"Processing page {current} of {total}... Found {count} candidates.")

            pipeline = ExtractionPipeline(api_key=api_key, model_name=backend_model)
            result = pipeline.run(
                target_pdf,
                book_title=book_title_display,
                page_range=selected_range,
                progress_callback=update_progress
            )

            progress_bar.progress(1.0)
            status_text.text("Extraction complete!")

            candidates = result["candidates"]
            st.session_state["candidates"] = [c.model_dump() for c in candidates]
            st.session_state["result_meta"] = result
            st.rerun()

    except Exception as e:
        st.error(f"Error reading textbook PDF: {e}")

# Display Results: STRUCTURED TABLE AS PRIMARY VIEW
if "candidates" in st.session_state:
    raw_candidates = st.session_state["candidates"]
    candidates = [TeachingMethodCandidate(**c) for c in raw_candidates]

    st.markdown("---")

    # Metrics Summary
    total = len(candidates)
    valid_methods = sum(1 for c in candidates if c.validation_status == "VALID_METHOD")
    review_req = sum(1 for c in candidates if c.validation_status == "REVIEW_REQUIRED")
    rejected = sum(1 for c in candidates if c.validation_status == "REJECTED")

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Total Candidates", total)
    mcol2.metric("Valid Methods", valid_methods, delta="Gnaan U Verified", delta_color="normal")
    mcol3.metric("Review Required", review_req, delta="Needs Review", delta_color="off")
    mcol4.metric("Rejected (Non-Methods)", rejected, delta="-Filtered Out", delta_color="inverse")

    st.markdown("---")

    # Filter candidates
    filtered = candidates
    if validation_filter != "All Candidates":
        filtered = [c for c in candidates if c.validation_status == validation_filter]

    # Convert to Structured Table (DataFrame)
    flat_data = []
    for idx, c in enumerate(filtered, 1):
        flat_data.append({
            "#": idx,
            "Method Name": c.method_name,
            "Validation Status": c.validation_status,
            "Confidence": c.confidence,
            "Learning Focus": c.learning_focus,
            "Procedure Steps": " \u2192 ".join(c.instructional_procedure) if c.instructional_procedure else "Not specified in source.",
            "Student Effort": ", ".join(c.student_effort) if c.student_effort else "Not specified in source.",
            "Learning Connection": c.learning_connection,
            "Resources / Apparatus": ", ".join(c.resources_setup) if c.resources_setup else "Not specified in source.",
            "Location": f"{c.source.chapter} ({c.pages_display})",
            "Source Evidence": c.source_evidence,
            "Validation Reason": c.validation_reason,
            "Missing Details": "; ".join(c.missing_information) if c.missing_information else "None"
        })

    df_display = pd.DataFrame(flat_data)

    # Export Bar & Primary Table Header
    exp_col1, exp_col2, exp_col3 = st.columns([2, 1, 1])
    with exp_col1:
        st.subheader("📊 Structured Method Library (Primary Table View)")

    csv_bytes = df_display.to_csv(index=False).encode("utf-8")
    json_bytes = json.dumps(raw_candidates, indent=2).encode("utf-8")

    with exp_col2:
        st.download_button(
            "📥 Download Table as CSV",
            data=csv_bytes,
            file_name="gnaan_u_methods_table.csv",
            mime="text/csv",
            use_container_width=True
        )
    with exp_col3:
        st.download_button(
            "📥 Download Full JSON",
            data=json_bytes,
            file_name="gnaan_u_methods_full.json",
            mime="application/json",
            use_container_width=True
        )

    # 1. PRIMARY STRUCTURED TABLE
    if not df_display.empty:
        st.dataframe(
            df_display,
            use_container_width=True,
            height=380,
            column_config={
                "#": st.column_config.NumberColumn(width="small"),
                "Method Name": st.column_config.TextColumn(width="medium"),
                "Validation Status": st.column_config.TextColumn(width="small"),
                "Learning Focus": st.column_config.TextColumn(width="large"),
                "Procedure Steps": st.column_config.TextColumn(width="large"),
                "Resources / Apparatus": st.column_config.TextColumn(width="medium"),
                "Location": st.column_config.TextColumn(width="medium"),
                "Validation Reason": st.column_config.TextColumn(width="large")
            }
        )
    else:
        st.info(f"No entries found matching filter: '{validation_filter}'.")

    st.markdown("---")

    # 2. DETAIL DRILL-DOWN (Inspect specific candidate row)
    st.subheader("🔍 Detailed Candidate Inspector")
    method_names = [f"#{idx} — {c.method_name} ({c.validation_status})" for idx, c in enumerate(filtered, 1)]

    if method_names:
        selected_method_idx = st.selectbox("Select a candidate from the table to inspect details:", range(len(method_names)), format_func=lambda x: method_names[x])
        item = filtered[selected_method_idx]

        badge_class = "valid-badge" if item.validation_status == "VALID_METHOD" else ("review-badge" if item.validation_status == "REVIEW_REQUIRED" else "reject-badge")
        st.markdown(f"<span class='{badge_class}'>{item.validation_status}</span> &nbsp; <b>Confidence:</b> {item.confidence} &nbsp;|&nbsp; <b>Location:</b> {item.source.chapter} ({item.pages_display})", unsafe_allow_html=True)
        st.markdown(f"**Audit Verdict:** *{item.validation_reason}*")

        if item.missing_information:
            st.warning("**Missing Information in Source:**\n" + "\n".join(f"- {m}" for m in item.missing_information))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**🎯 Learning Focus:**\n{item.learning_focus}")
            st.markdown(f"**👥 Intended Learners & Context:**\n{item.intended_learners_context}")
            st.markdown(f"**💡 Approach:**\n{item.teaching_approach}")
            st.markdown("**📦 Resources:**")
            for r in item.resources_setup:
                st.markdown(f"- {r}")

        with c2:
            st.markdown("**🧠 Student Effort:**")
            for se in item.student_effort:
                st.markdown(f"- {se}")
            st.markdown(f"**🔗 Learning Connection:**\n{item.learning_connection}")
            if item.questions_or_prompts:
                st.markdown("**❓ Prompts / Questions:**")
                for q in item.questions_or_prompts:
                    st.markdown(f"- {q}")

        st.markdown("**📝 Ordered Instructional Procedure:**")
        if item.instructional_procedure:
            for s_idx, step in enumerate(item.instructional_procedure, 1):
                st.markdown(f"{s_idx}. {step}")
        else:
            st.markdown("*Not specified in source.*")

        st.info(f"**📖 Verified Source Evidence:**\n> \"{item.source_evidence}\"")

else:
    st.info("👆 Upload any Maharashtra State Board textbook PDF or click **'Load MH Grade 7 Demo'** and press **'Find Teaching Methods'** to generate the structured table.")
