import os
import sys

from pathlib import Path

import requests
import streamlit as st

from dotenv import load_dotenv


# --------------------------------------------------
# Project path
# --------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


from backend.utils.sanitizer import (
    html_preview
)


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 24px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        AI-Powered Legal Document Generator
    </div>
    """,
    unsafe_allow_html=True
)


st.info(
    "LegalEase creates AI-generated drafts. "
    "Review the final document with a qualified "
    "legal professional before use."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚖️ LegalEase")

    st.caption(
        f"Backend: {BACKEND_URL}"
    )

    st.markdown(
        """
        ### Workflow

        **1.** Enter document details.

        **2.** Generate with Gemini 3.8 Flash.

        **3.** Edit the generated document.

        **4.** Preview the document.

        **5.** Download TXT, DOCX or PDF.
        """
    )


# --------------------------------------------------
# Document Details
# --------------------------------------------------

st.header(
    "Document Details"
)


col1, col2 = st.columns(2)


with col1:

    document_type = st.selectbox(
        "Document Type",

        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement (NDA)",
            "Employment Offer Letter",
            "Service Agreement",
            "Freelance Work Contract",
            "Business Agreement",
            "Other"
        ]
    )

    if document_type == "Other":

        document_type = st.text_input(
            "Specify document type"
        )


with col2:

    effective_date = st.text_input(
        "Effective Date",
        placeholder="October 1, 2026"
    )


# --------------------------------------------------
# Parties
# --------------------------------------------------

parties = st.text_area(
    "Parties Involved",

    height=120,

    placeholder=(
        "Jane Doe (Service Provider)\n"
        "TechNova Inc. (Client)"
    )
)


# --------------------------------------------------
# Terms
# --------------------------------------------------

terms = st.text_area(
    "Terms & Conditions",

    height=180,

    placeholder=(
        "Payment within 30 days of invoice; "
        "confidentiality must be maintained; "
        "either party may terminate with 15 days notice."
    )
)


# --------------------------------------------------
# Generate
# --------------------------------------------------

if st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
):

    if not all(
        [
            document_type.strip(),
            effective_date.strip(),
            parties.strip(),
            terms.strip()
        ]
    ):

        st.error(
            "Please complete document type, "
            "parties, terms, and effective date."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "effective_date":
                effective_date
        }

        try:

            with st.spinner(
                "Generating your legal draft..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=180
                )


            if response.ok:

                result = response.json()

                st.session_state.document = (
                    result["content"]
                )

                st.session_state.document_type = (
                    document_type
                )

                st.success(
                    "Document generated successfully."
                )

            else:

                try:

                    detail = (
                        response.json()
                        .get(
                            "detail",
                            response.text
                        )
                    )

                except ValueError:

                    detail = response.text

                st.error(
                    f"Backend error: {detail}"
                )


        except requests.RequestException as exc:

            st.error(
                "Cannot connect to the "
                f"FastAPI backend: {exc}"
            )


# --------------------------------------------------
# Generated document
# --------------------------------------------------

if "document" in st.session_state:

    st.divider()

    st.header(
        "Editable Document"
    )


    edited = st.text_area(

        "Edit the generated document",

        value=st.session_state.document,

        height=600,

        key="document_editor"
    )


    st.session_state.document = edited


    # --------------------------------------------------
    # Preview
    # --------------------------------------------------

    st.subheader(
        "Preview"
    )

    st.markdown(
        html_preview(edited),
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # Downloads
    # --------------------------------------------------

    st.subheader(
        "Downloads"
    )


    export_payload = {

        "document_type":
            st.session_state.document_type,

        "content":
            edited
    }


    c1, c2, c3 = st.columns(3)


    # TXT
    with c1:

        if st.button(
            "Prepare TXT"
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/export/txt",

                    json=export_payload,

                    timeout=30
                )

                if response.ok:

                    st.download_button(

                        "Download TXT",

                        response.content,

                        "legal_document.txt",

                        "text/plain"
                    )

                else:

                    st.error(
                        "TXT export failed."
                    )

            except requests.RequestException as exc:

                st.error(str(exc))


    # DOCX
    with c2:

        if st.button(
            "Prepare DOCX"
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/export/docx",

                    json=export_payload,

                    timeout=30
                )

                if response.ok:

                    st.download_button(

                        "Download DOCX",

                        response.content,

                        "legal_document.docx",

                        (
                            "application/"
                            "vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        )
                    )

                else:

                    st.error(
                        "DOCX export failed."
                    )

            except requests.RequestException as exc:

                st.error(str(exc))


    # PDF
    with c3:

        if st.button(
            "Prepare PDF"
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/export/pdf",

                    json=export_payload,

                    timeout=30
                )

                if response.ok:

                    st.download_button(

                        "Download PDF",

                        response.content,

                        "legal_document.pdf",

                        "application/pdf"
                    )

                else:

                    st.error(
                        "PDF export failed."
                    )

            except requests.RequestException as exc:

                st.error(str(exc))