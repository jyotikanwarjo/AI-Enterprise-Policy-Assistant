from pathlib import Path
import fitz

import streamlit as st
from rag import generate_answer


# Page configuration
st.set_page_config(
    page_title="Enterprise Policy Assistant",
    page_icon="📚",
    layout="wide"
)

DOCUMENTS_DIR = Path(__file__).resolve().parent / "Documents"


def validate_sources(sources):
    valid_sources = []
    invalid_sources = []
    seen = set()
    page_counts = {}

    for source in sources:
        filename = source.get("source")
        page = source.get("page")

        if (
            not isinstance(filename, str)
            or not isinstance(page, int)
            or isinstance(page, bool)
        ):
            invalid_sources.append(source)
            continue

        pdf_path = DOCUMENTS_DIR / filename

        if not pdf_path.is_file():
            invalid_sources.append(source)
            continue

        try:
            if filename not in page_counts:
                with fitz.open(pdf_path) as pdf:
                    page_counts[filename] = pdf.page_count

            if not 1 <= page <= page_counts[filename]:
                invalid_sources.append(source)
                continue

        except Exception:
            invalid_sources.append(source)
            continue

        key = (filename, page)

        if key not in seen:
            valid_sources.append({
                "source": filename,
                "page": page
            })
            seen.add(key)

    return valid_sources, invalid_sources

# Application title
st.title("📚 Enterprise Policy & SOP Intelligence Assistant")

st.write(
    "Ask questions about enterprise policies and SOPs. "
    "Get answers grounded in your uploaded documents."
)

st.divider()


# Sidebar
with st.sidebar:
    st.header("About this application")

    st.write(
        """
        This application uses Retrieval-Augmented Generation (RAG)
        to answer questions from enterprise policy documents.

        **Capabilities**
        - Policy question answering
        - Semantic document search
        - Source document references
        - Policy and SOP knowledge retrieval
        """
    )

    st.divider()

    st.caption("Training project | NovaTech Solutions")


# Question input
st.subheader("Ask a policy question")

question = st.text_area(
    "Enter your question:",
    placeholder="Example: What approvals are required for privileged access?",
    height=100
)


# Submit button
if st.button("Get Answer", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Searching documents and generating an answer..."):

            try:
                result = generate_answer(question)

                st.subheader("Answer")
                st.write(result["answer"])

                st.divider()

                st.subheader("Source References")

                sources = result.get("sources", [])

                valid_sources, invalid_sources = validate_sources(sources)

                if valid_sources:
                    for source in valid_sources:
                        st.write(
                            f"📄 **{source['source']}** "
                            f"| Page: {source['page']}"
                        )
                else:
                    st.warning(
                        "No source references could be validated. "
                        "Treat this answer as unverified."
                    )

                if invalid_sources:
                    st.warning(
                        f"{len(invalid_sources)} source reference(s) "
                        "failed validation. Review the answer before relying on it."
                    )

                st.caption(
                    "Source validation confirms that the referenced PDF and page "
                    "exist. It does not independently verify every answer claim."
                    )

            except Exception as error:
                st.error(
                    "An error occurred while processing your question."
                )
                st.exception(error)