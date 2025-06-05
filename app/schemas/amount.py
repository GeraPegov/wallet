from pydantic import BaseModel, Field

class Amount(BaseModel):
    amount: int = Field(..., min_length=1, max_length=10**7)