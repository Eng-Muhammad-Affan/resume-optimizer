import PyPDF2
import io 
from docx import Document 

import streamlit as st 

class DocumentExtractor:
    """Extract content from PDF and Word documents"""
    
    @staticmethod
    def extract_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            st.error(f"Error extracting PDF: {str(e)}")
            return None
    
    @staticmethod
    def extract_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error extracting DOCX: {str(e)}")
            return None
    
    @staticmethod
    def extract_content(file_content: bytes, filename: str) -> tuple:
        """Extract content based on file type"""
        if filename.lower().endswith('.pdf'):
            content = DocumentExtractor.extract_from_pdf(file_content)
            return content, 'pdf'
        elif filename.lower().endswith('.docx'):
            content = DocumentExtractor.extract_from_docx(file_content)
            return content, 'docx'
        else:
            st.error("Unsupported file format. Please upload PDF or DOCX files.")
            return None, None
