## _____ Agentic modules ...
from agent.config import config 
from agents import Agent , Runner , ModelSettings

resume_agent = Agent(
    name="Resume Optimizer Agent",
    instructions="You are an expert resume writer specializing in ATS-friendly resume optimization. Return only the enhanced resume in markdown format.",
    model_settings=ModelSettings(
        temperature=0.7,
        max_tokens=4000
    )
)

def enhance_resume(original_resume_content: str , user_prompt:str) -> dict:
    """Send content to OpenAI for enhancement"""
    try:
        
        # Call OpenAI API
        enhanced_resume = Runner.run_sync(starting_agent=resume_agent ,input=user_prompt ,run_config=config)
        # Generate summary of changes
        changes_prompt = f"""
        Provide a brief summary (2-3 sentences) of the key changes made to this resume based on the job description.
        Keep it concise and focus on the main improvements.
        
        Original (excerpt): {original_resume_content}...
        Enhanced (excerpt): {enhanced_resume.final_output}...
        
        Summary of key changes:
        """
    
        changes_summary = Runner.run_sync(starting_agent=resume_agent,
                                          input=changes_prompt,
                                            run_config=config)
        return {
            "enhanced_resume": enhanced_resume.final_output ,
            "changes_summary": changes_summary.final_output,
            "success": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }