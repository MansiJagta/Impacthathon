from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

from indian_id_validator.inference import process_id

app = FastAPI(title="Indian ID Validator Service")

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/extract-id/")
async def extract_id(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run inference
        result = process_id(
            image_path=file_path,
            save_json=False
        )

        # Remove file after processing
        os.remove(file_path)

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
