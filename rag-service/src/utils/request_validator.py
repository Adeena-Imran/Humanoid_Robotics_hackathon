from typing import List
from ..schemas import RagChatRequest
from .api_errors import BadRequestException
from pydantic import ValidationError

# Define allowed query types based on current implementation
ALLOWED_QUERY_TYPES = ["chat", "explanation", "subagent"]

class RequestValidator:
    """
    Validates incoming API request payloads, ensuring required fields are present
    and values adhere to predefined constraints.
    """

    @staticmethod
    def validate_chat_payload(request: RagChatRequest):
        """
        Validates the payload for the POST /chat endpoint.

        Args:
            request: The incoming RagChatRequest object.

        Raises:
            BadRequestException: If any validation rule is violated.
        """
        if not request.text and request.query_type != "chapter_summary": # Allow empty text for chapter_summary if no specific query
            raise BadRequestException(code="VALIDATION_ERROR", message="text (query) is required.", target="text")

        if request.query_type not in ALLOWED_QUERY_TYPES:
            raise BadRequestException(code="VALIDATION_ERROR", message=f"Invalid query_type. Must be one of {', '.join(ALLOWED_QUERY_TYPES)}.", target="query_type")

        # Additional specific validations based on query_type can be added here
        if request.query_type == "subagent":
            if not request.text or ":" not in request.text:
                raise BadRequestException(code="VALIDATION_ERROR", message="For 'subagent' query_type, 'text' must be in 'subagent_name: skill_name' format.", target="text")
        
        # We can also add validation for chapter_id if query_type is chapter_summary
        # if request.query_type == "chapter_summary" and not request.chapter_id:
        #     raise BadRequestException(code="VALIDATION_ERROR", message="chapter_id is required for 'chapter_summary' query_type.", target="chapter_id")
