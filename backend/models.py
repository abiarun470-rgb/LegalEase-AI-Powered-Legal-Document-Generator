from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(
        min_length=2,
        max_length=100
    )

    parties: str = Field(
        min_length=2,
        max_length=10000
    )

    terms: str = Field(
        min_length=2,
        max_length=20000
    )

    effective_date: str = Field(
        min_length=2,
        max_length=100
    )


class DocumentResponse(BaseModel):
    document_type: str
    content: str


class ExportRequest(BaseModel):
    document_type: str = Field(
        min_length=2,
        max_length=100
    )

    content: str = Field(
        min_length=2,
        max_length=100000
    )