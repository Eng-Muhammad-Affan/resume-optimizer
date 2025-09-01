import uvicorn
from fastapi import FastAPI, File , UploadFile , Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Fruit(BaseModel):
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]
    
app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/optimize")
async def optimize_resume(
    resume: UploadFile = File(...),
    description: str = Form(...)
):
    # Process the uploaded file
    # You can save the file or read its content
    with open(f"temp_resume_{resume.filename}", "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
        
    # Get the job description from the form data
    print(f"Received job description: {description}")

    # --- Here you would add your AI logic to process the PDF and description ---
    # For now, let's just return a placeholder response
    
    optimized_content = "This is the AI-generated optimized resume content."
    
    return {"message": "Optimization successful!", "optimized_resume_content": 
    optimized_content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)