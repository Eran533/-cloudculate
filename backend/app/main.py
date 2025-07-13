from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import logging
from app.scraper import scrape_aws_architectures
from app.parser import parse_architecture_data
from app.models import Architecture
from app.db import save_architectures_upsert, get_architectures

app = FastAPI(title="AWS Architecture Parser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider limiting origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")

@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/architectures", response_model=List[Architecture])
async def read_architectures() -> List[Architecture]:
    """
    Retrieve all saved AWS architectures, sorted by timestamp descending.
    """
    try:
        return get_architectures()
    except Exception as e:
        logger.error("Failed to retrieve architectures", exc_info=e)
        raise HTTPException(status_code=500, detail="Failed to retrieve architectures")

@app.post("/scrape", response_model=List[Architecture])
async def scrape_and_parse() -> List[Architecture]:
    try:
        print("Starting scrape_aws_architectures()")
        raw = scrape_aws_architectures()
        print(f"Scraped {len(raw)} raw architectures")

        max_items = 15
        raw_limited = raw[:max_items]  # Limit to first 15 items

        parsed = parse_architecture_data(raw_limited)
        print(f"Parsed {len(parsed)} architectures with AI enrichment")

        validated = []
        for i, item in enumerate(parsed):
            try:
                item["timestamp"] = datetime.utcnow()
                arch = Architecture(**item)
                validated.append(arch.dict())
            except Exception as err:
                print(f"Skipped invalid architecture at index {i}: {item.get('name')}")
                print(f"Error: {err}")

        print(f"Validated {len(validated)} architectures ready to save")

        result = save_architectures_upsert(validated)
        print(f"Upserted to MongoDB: {result.bulk_api_result if result else 'No operations performed'}")

        return validated

    except Exception as e:
        print("Scraping and parsing failed")
        print(e)
        raise HTTPException(status_code=500, detail="Scraping and parsing failed")
