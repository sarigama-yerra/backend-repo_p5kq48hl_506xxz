from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os

from schemas import Message, Testimonial, Service
from database import db, create_document, get_documents

app = FastAPI(title="Creative Agency API", version="1.0.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"]) 
def root():
    return {"status": "ok", "message": "Creative Agency API running"}

@app.get("/test", tags=["health"]) 
def test_db():
    try:
        # Attempt a basic list on the database to ensure connection
        _ = db.list_collection_names()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Seed default services/testimonials if empty
@app.get("/seed", tags=["utils"]) 
def seed():
    try:
        services = list(get_documents("service", {}, limit=10))
        testimonials = list(get_documents("testimonial", {}, limit=10))
        if not services:
            default_services = [
                Service(title="Social Media Marketing", description="Data-driven campaigns with trend-jacking creative.", icon="Megaphone").dict(),
                Service(title="Brand Building", description="Positioning, identity systems, and storytelling.", icon="Sparkles").dict(),
                Service(title="Web Development", description="Fast, accessible, conversion-focused web experiences.", icon="Globe").dict(),
                Service(title="PPC Campaigns", description="ROI-obsessed paid search and social ads.", icon="BadgeDollarSign").dict(),
            ]
            for s in default_services:
                create_document("service", s)
        if not testimonials:
            default_testimonials = [
                Testimonial(author="Alex Rivera", role="CMO, NovaTech", quote="They turned our brand into a movement. Our CPA dropped 38% in a month.").dict(),
                Testimonial(author="Mina Park", role="Founder, Bloom & Co.", quote="Creative that actually converts. The team is a joy to work with.").dict(),
                Testimonial(author="Sam Patel", role="Head of Growth, ArcLabs", quote="From zero to consistent pipeline in 8 weeks. Unreal.").dict(),
            ]
            for t in default_testimonials:
                create_document("testimonial", t)
        return {"status": "ok", "seeded": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact form endpoint
@app.post("/contact", tags=["contact"]) 
def contact(message: Message):
    try:
        doc_id = create_document("message", message.dict())
        return {"status": "received", "id": str(doc_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Services
@app.get("/services", response_model=List[Service], tags=["content"]) 
def get_services():
    try:
        items = [Service(**doc) for doc in get_documents("service", {}, limit=50)]
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Testimonials
@app.get("/testimonials", response_model=List[Testimonial], tags=["content"]) 
def get_testimonials():
    try:
        items = [Testimonial(**doc) for doc in get_documents("testimonial", {}, limit=50)]
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
