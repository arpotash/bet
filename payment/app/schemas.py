from pydantic import BaseModel, Field


class CardSchemas(BaseModel):
    uuid: str = Field(example="ec286570-d2b2-4a0b-8fb8-5875d85f68fc")
    amount: float = Field(example=100.00)
