from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.document_engine.exporters import (
    create_docx,
    create_pdf,
    create_txt
)

from backend.models import (
    DocumentRequest,
    DocumentResponse,
    ExportRequest
)


router = APIRouter()


def get_generator():

    try:

        return GeminiDocumentGenerator()

    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate(
    request: DocumentRequest
):

    generator = get_generator()

    try:

        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    return DocumentResponse(
        document_type=request.document_type,
        content=content
    )


@router.post("/export/txt")
def export_txt(
    request: ExportRequest
):

    return Response(
        content=create_txt(
            request.content
        ),

        media_type="text/plain; charset=utf-8",

        headers={
            "Content-Disposition":
            'attachment; filename="legal_document.txt"'
        }
    )


@router.post("/export/docx")
def export_docx(
    request: ExportRequest
):

    logo_path = (
        Path(__file__).resolve()
        .parents[1]
        / "assets"
        / "logo.png"
    )

    logo = (
        str(logo_path)
        if logo_path.exists()
        else None
    )

    data = create_docx(
        content=request.content,
        document_type=request.document_type,
        logo_path=logo
    )

    return Response(
        content=data,

        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),

        headers={
            "Content-Disposition":
            'attachment; filename="legal_document.docx"'
        }
    )


@router.post("/export/pdf")
def export_pdf(
    request: ExportRequest
):

    data = create_pdf(
        content=request.content,
        document_type=request.document_type
    )

    return Response(
        content=data,

        media_type="application/pdf",

        headers={
            "Content-Disposition":
            'attachment; filename="legal_document.pdf"'
        }
    )