from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1)
    uuid: UUID = Field(default_factory=uuid4)

    @field_validator("question")
    @classmethod
    def normalize_question(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("question must not be empty")
        return normalized
