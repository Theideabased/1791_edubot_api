from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from schemas import EducateRequest, EducateResponse
from services.content_service import content_service
from services.pdf_service import pdf_service
from config import settings
import os

router = APIRouter()

@router.post("/educate", response_model=EducateResponse)
async def generate_education_content(request: EducateRequest, background_tasks: BackgroundTasks):
    """
    Generate complete educational content including syllabus, modules, and quiz using Google Gemini.
    
    - **topic**: Topic for educational content generation (max 500 characters)
    - **api_key**: Your Gemini API key
    - **modules_count**: Number of modules in the syllabus (3-10)
    - **include_pdf**: Whether to generate a PDF export (optional)
    """
    try:
        # Generate educational content
        result = await content_service.generate_education_content(
            topic=request.topic,
            modules_count=request.modules_count,
            api_key=request.api_key
        )
        
        # Generate PDF if requested
        if request.include_pdf:
            try:
                # Convert result to dict for PDF generation
                education_data = {
                    "topic": result.topic,
                    "provider_used": result.provider_used,
                    "syllabus": result.syllabus.dict(),
                    "modules": [module.dict() for module in result.modules],
                    "quiz": result.quiz.dict()
                }
                
                pdf_path = pdf_service.generate_education_pdf(education_data)
                # Create a public URL for the PDF (adjust based on your deployment)
                result.pdf_url = f"/api/v1/download/pdf/{os.path.basename(pdf_path)}"
            except Exception as pdf_error:
                # Don't fail the entire request if PDF generation fails
                print(f"PDF generation failed: {pdf_error}")
                result.pdf_url = None
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/pdf/{filename}")
async def download_pdf(filename: str):
    """
    Download a generated PDF file.
    
    - **filename**: Name of the PDF file to download
    """
    pdf_path = os.path.join(settings.PDF_DIRECTORY, filename)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
