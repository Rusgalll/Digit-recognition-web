import os

from app.endpoints_annotation import RecognitionResponse
from app.digit_model.image_format import recognize_digit

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

image_folder_path = os.path.join(os.path.dirname(__file__), "digit_model", "image")
os.makedirs(image_folder_path, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-file/", response_model=RecognitionResponse)
async def create_upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(image_folder_path, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        recognized_digit, probability = recognize_digit(file_path)

        return JSONResponse(content={"recognized_digit": recognized_digit, "probability": float(probability)},
                            status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'"error": {str(e)}')


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
