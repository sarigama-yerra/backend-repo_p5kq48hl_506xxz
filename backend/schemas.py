from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Message(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=2000)

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "message": "I'd love to discuss a new campaign for our product launch."
            }
        }

class Testimonial(BaseModel):
    author: str = Field(..., min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=100)
    quote: str = Field(..., min_length=10, max_length=500)
    avatar_url: Optional[str] = None

class Service(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=400)
    icon: Optional[str] = Field(None, description="Lucide icon name")
