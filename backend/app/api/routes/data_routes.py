"""
SatQuery AI - Sample Data & AI Data Catalog Routes
"""
import os
from pathlib import Path
from typing import Any, Dict, List
from fastapi import APIRouter, Request, Response, HTTPException
from app.core.config import settings
from app.schemas.response import APIResponse

router = APIRouter(prefix="/data", tags=["Data Catalog"])


@router.get("/features-guide-pdf")
async def download_features_guide_pdf():
    """Download the comprehensive SatQuery AI Master Features & SIH Documentation PDF."""
    potential_paths = [
        os.path.join(settings.BASE_DIR.parent, "SatQuery_AI_Complete_Features_Guide.pdf"),
        os.path.join(settings.BASE_DIR, "SatQuery_AI_Complete_Features_Guide.pdf"),
        os.path.join(os.getcwd(), "SatQuery_AI_Complete_Features_Guide.pdf"),
    ]
    
    pdf_path = None
    for p in potential_paths:
        if os.path.exists(p):
            pdf_path = p
            break

    if not pdf_path or not os.path.exists(pdf_path):
        # Auto-generate if missing
        from scripts.generate_features_pdf import create_features_pdf
        target = os.path.join(settings.BASE_DIR.parent, "SatQuery_AI_Complete_Features_Guide.pdf")
        create_features_pdf(target)
        pdf_path = target

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=SatQuery_AI_Complete_Features_Guide.pdf"
        }
    )


@router.get("/samples", response_model=APIResponse[List[Dict[str, Any]]])
async def list_sample_data(request: Request):
    """Return a discoverable list of bundled AI demo satellite sample files."""
    sample_dir = os.path.join(settings.BASE_DIR, "sample_data")
    sample_files = []

    if os.path.isdir(sample_dir):
        for filename in sorted(os.listdir(sample_dir)):
            if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff")):
                continue

            lower = filename.lower()
            if lower.startswith("optical"):
                modality = "optical"
                task = "single_image_vqa"
            elif lower.startswith("sar"):
                modality = "sar"
                task = "optical_sar_analysis"
            elif lower.startswith("t1"):
                modality = "optical"
                task = "temporal_change"
            elif lower.startswith("t2"):
                modality = "optical"
                task = "temporal_change"
            else:
                modality = "optical"
                task = "single_image_vqa"

            filepath = os.path.join(sample_dir, filename)
            sample_files.append({
                "name": filename,
                "modality": modality,
                "task": task,
                "size_bytes": os.path.getsize(filepath),
                "preview_url": f"/sample_data/{filename}",
                "description": f"Bundled {modality.upper()} remote sensing demo sample for SatQuery AI",
            })

    request_id = getattr(request.state, "request_id", "unknown")
    return APIResponse(success=True, data=sample_files, request_id=request_id)
