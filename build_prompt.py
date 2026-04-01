prompts = {
                "conservative": "Make minimal changes while ensuring key keywords from the job description are included. Maintain original structure closely.",
                "balanced": "Enhance the resume by highlighting relevant skills and experiences that match the job description. Use strong action verbs and quantify achievements where possible.",
                "aggressive": "Significantly optimize the resume for the job description. Restructure content to emphasize relevant experience. Add strong action verbs, quantify achievements, and optimize for ATS systems."
            }

def build_prompt(resume_content: str, job_description: str, enhancement_level: str = "balanced"):

    """This function collects details from user and return a complete user message to open ai 
    
     resume_content:Extracted text from pdf | word
    enhancement_level:given levels from select bar 
    job_description: Main job description to which AI should align the resume 
       """
    
    ## ____ Find enhancement level ...
    enhancement_instruction = prompts.get(enhancement_level, prompts["balanced"])

    ## ______ Construcing prompt ...
    prompt = f"""
            You are an expert resume writer and career coach. Your task is to enhance the following resume based on the job description provided.
            
            Enhancement Level: {enhancement_instruction}
            
            Please follow these instructions carefully:
            1. Preserve the original structure and format as much as possible
            2. Highlight relevant skills and experiences that match the job description
            3. Use strong action verbs and quantifiable achievements
            4. Optimize keywords from the job description
            5. Keep the length similar to the original resume
            6. Return ONLY the enhanced resume in markdown format, with no additional text or explanations
            
            Original Resume:
            {resume_content}
            
            Job Description:
            {job_description}
            
            Enhanced Resume (markdown format):
            """
    return prompt