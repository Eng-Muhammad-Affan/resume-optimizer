import uvicorn
from fastapi import FastAPI, File , UploadFile , Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from shutil import copyfileobj
import pdfplumber
import io
from starlette.responses import JSONResponse
import os
from agents import Agent ,Runner
from config import 


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

class OutputType (BaseModel):
    content:str
    error_message:str | None = None
    error:bool = False

agent = Agent(
    name="Resume Optimizer bot",
    instructions="You're the resume optimizer agent , your main goal is to optimize resume according to the provided job description which user will provide to you. For example : If job requires proficiency of candidate in typescript , you'll optimize his resume according to it. Note that if job description is targetting the role that is not mentioned in cv content like if user provides job description for data science and in the resume , python and relevant skills are not mentioned , please dont work on it "
)

@app.post("/optimize")
async def optimize_resume(
    resume: UploadFile = File(...),
    description: str = Form(...)
):
    """
    Accepts a resume PDF and a job description.
    Extracts the content of the PDF and prints it in Markdown format.
    """
    print(f"Received job description: {description}")
    
    # Read the content of the uploaded PDF file
    try:
        # The file is a stream, so we read its content into memory
        file_content = await resume.read()
        print("File content : ", file_content)
        
        # Use io.BytesIO to treat the in-memory content as a file
        pdf_file = io.BytesIO(file_content)
        print("pdf_file : ",pdf_file)        
        # Use a string buffer to build the Markdown content
        markdown_content = ""
        
        # Use pdfplumber to open and process the PDF
        with pdfplumber.open(pdf_file) as pdf:
            # Iterate through each page of the PDF
            for page in pdf.pages:
                print("page : ",page)
                # Extract text from the page
                text = page.extract_text()
                print("extracted text : ",text)
                if text:
                    # Append the text to our markdown string, adding a new section
                    # for each page.
                    markdown_content += f"# Page {page.page_number}\n\n"
                    markdown_content += text + "\n\n"
        
        # Print the extracted markdown content
        print("--- Extracted PDF Content (Markdown) ---")
        print(markdown_content)
        print("--- End of Extracted Content ---")

        # You can now use markdown_content for your AI processing logic
        # For example:
        # optimized_content = call_llm(markdown_content, description)
        
        # For this example, we'll return a placeholder
        optimized_content = "This is the AI-generated optimized resume content."
        
        return JSONResponse(content={
            "message": "Optimization successful! PDF content extracted and printed.", 
            "optimized_resume_content": optimized_content
        })

    except Exception as e:
        return JSONResponse(content={"message": f"An error occurred: {str(e)}"}, status_code=500)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)