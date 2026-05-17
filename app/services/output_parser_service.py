import json
import re


# Service for parsing and sanitizing raw text output,
# specifically to extract and validate JSON content.
class OutputParserService:
    """
    Service for parsing and sanitizing raw text output,
    specifically to extract and validate JSON content.
    """

    @staticmethod
    def extract_json(
        raw_output: str
    ) -> str:
        """
        Extracts and sanitizes JSON content from a raw string,
        removing markdown fences and validating the JSON structure.

        Args:
            raw_output (str): The raw string potentially containing JSON, often from an LLM.
        Returns:
            str: The cleaned and validated JSON string.
        Raises:
            json.JSONDecodeError: If the extracted content is not valid JSON.
        """

        # ------------------------------------
        # Remove markdown fences
        # ------------------------------------

        cleaned = raw_output.strip()

        cleaned = re.sub(
            r"^```json",
            "",
            cleaned,
            flags=re.MULTILINE
        )

        cleaned = re.sub(
            r"^```",
            "",
            cleaned,
            flags=re.MULTILINE
        )

        cleaned = re.sub(
            r"```$",
            "",
            cleaned,
            flags=re.MULTILINE
        )

        cleaned = cleaned.strip()

        # ------------------------------------
        # Validate JSON
        # ------------------------------------

        json.loads(cleaned)

        return cleaned