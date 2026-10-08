from backend.document_engine.exporters import (
    create_docx,
    create_pdf,
    create_txt
)


def test_txt_export():

    data = create_txt(
        "Hello LegalEase"
    )

    assert data == b"Hello LegalEase"


def test_docx_export():

    data = create_docx(
        "SECTION 1\nThis is a draft.",
        "NDA"
    )

    assert data.startswith(
        b"PK"
    )


def test_pdf_export():

    data = create_pdf(
        "SECTION 1\nThis is a draft.",
        "NDA"
    )

    assert data.startswith(
        b"%PDF"
    )