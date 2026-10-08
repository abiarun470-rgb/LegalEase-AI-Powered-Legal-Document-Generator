import os
import time
from typing import Optional

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:
    """
    Generates legal document drafts using Gemini.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        self.api_key = (
            api_key
            or os.getenv("GOOGLE_API_KEY")
        )

        self.model_name = (
            model_name
            or os.getenv(
                "GEMINI_MODEL",
                "gemini-3.8-flash"
            )
        )

        if not self.api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    @staticmethod
    def build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str
    ) -> str:

        return f"""
You are LegalEase, an AI legal-document drafting assistant.

Create a professional legal document draft.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

TERMS AND CONDITIONS:
{terms}

IMPORTANT INSTRUCTIONS:

1. Use only facts supplied by the user.

2. Do not invent names, addresses, dates,
   money amounts, jurisdictions, or other
   material facts.

3. If important information is missing,
   use a clear placeholder such as:

   [GOVERNING LAW]
   [ADDRESS]
   [PAYMENT AMOUNT]

4. Start with a clear document title.

5. Use numbered sections.

6. Use descriptive section headings.

7. Include the parties.

8. Include the effective date.

9. Accurately incorporate the supplied terms.

10. Add only generally applicable clauses
    necessary for a coherent document.

11. Include signature blocks when appropriate.

12. Do not cite statutes, cases, regulations,
    or legal authorities unless supplied by
    the user.

13. Do not claim that a lawyer reviewed or
    approved the document.

14. Clearly identify the result as an
    AI-generated draft.

15. Return plain document text only.

16. Do not use Markdown code fences.

17. Do not provide legal advice.

The final document should be reviewed by
a qualified legal professional before use.
"""

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str
    ) -> str:

        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date
        )

        max_attempts = 5

        delays = [
            5,
            10,
            20,
            40
        ]

        last_error = None

        for attempt in range(1, max_attempts + 1):

            try:

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if not text or not text.strip():
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return text.strip()

            except Exception as exc:

                last_error = exc

                error_text = str(exc)

                # Retry temporary server/capacity errors
                is_retryable = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                )

                if not is_retryable:
                    raise RuntimeError(
                        f"Gemini request failed: {exc}"
                    ) from exc

                if attempt == max_attempts:
                    break

                time.sleep(
                    delays[attempt - 1]
                )

        raise RuntimeError(
            "Gemini is temporarily unavailable "
            "after multiple attempts. "
            f"Last error: {last_error}"
        )