from pydantic import BaseModel


class RecognitionResponse(BaseModel):
    recognized_digit: str
    probability: float
