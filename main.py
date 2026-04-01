import streamlit as st

## modules:
from document_extractor import DocumentExtractor
from document_generator import DocumentGenerator

from page_config import setup

# Page configuration
setup()

# Initialize processors
extractor = DocumentExtractor()
# 
generator = DocumentGenerator()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)
    st.title("⚙️ Settings")
    
    # Enhancement level
    enhancement_level = st.select_slider(
        "Enhancement Level",
        options=["conservative", "balanced", "aggressive"],
        value="balanced",
        help="Conservative: Minimal changes, Balanced: Moderate optimization, Aggressive: Heavy optimization for ATS"
    )
    
    st.divider()
    
    # About section
    st.markdown("### 📌 About")
    st.markdown("""
    This AI-powered tool helps you:
    - ✨ Optimize your resume for specific job descriptions
    - 🎯 Match keywords and requirements
    - 📈 Improve ATS compatibility
    - 💪 Enhance action verbs and achievements
    """)
    
    st.divider()
    
    # Tips
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Provide a detailed job description for best results
    - Review the enhanced resume before using
    - Adjust enhancement level based on your needs
    - Download in your preferred format
    """)
    
    st.divider()

# Main content
st.markdown("""
<div class="main-header">
    <h1>🚀 AI Resume Enhancer</h1>
    <p>Upload your resume and paste a job description to get an ATS-optimized version</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 Upload Resume")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx'],
        help="Upload your resume in PDF or DOCX format"
    )

with col2:
    st.markdown("### 📋 Job Description")
    
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste the complete job description here...",
        help="Include as much detail as possible for better optimization"
    )
    
    # Optional additional context
    additional_context = st.text_area(
        "Additional Context (Optional)",
        height=100,
        placeholder="Any additional information about your target role, company, or specific achievements you want to highlight...",
        help="Add any specific achievements or context you want to emphasize"
    )

# Enhancement options
st.markdown("### 🎯 Enhancement Options")
col3, col4, col5 = st.columns(3)

with col3:
    include_keywords = st.checkbox("Optimize for ATS keywords", value=True)
with col4:
    quantify_achievements = st.checkbox("Quantify achievements", value=True)
with col5:
    action_verbs = st.checkbox("Enhance action verbs", value=True)

# Process button
from process_resume import process_resume

if st.button("✨ Enhance Resume", type="primary", use_container_width=True):
    process_resume(
      uploaded_file,
        additional_context,
        job_description,
        enhancement_level,
        include_keywords,
        quantify_achievements,
        action_verbs)

# if st.button("✨ Enhance Resume", type="primary", use_container_width=True):
#     if not uploaded_file:
#         st.error("Please upload a resume file")
#     elif not job_description:
#         st.error("Please provide a job description")
#     else:
#         # Progress bar
#         progress_bar = st.progress(0)
#         status_text = st.empty()
        
#         try:
#             # Step 1: Extract content
#             status_text.text("📄 Extracting content from resume...")
#             progress_bar.progress(20)
            
#             file_content = uploaded_file.read()
#             extracted_content, file_format = extractor.extract_content(file_content, uploaded_file.name)
            
#             if not extracted_content:
#                 st.error("Failed to extract content from the file")
#                 st.stop()
            
#             # Step 2: Prepare content
#             status_text.text("🎯 Preparing for AI enhancement...")
#             progress_bar.progress(40)
            
#             # Combine with additional context
#             full_resume_content = extracted_content
#             if additional_context:
#                 full_resume_content += f"\n\nAdditional Context:\n{additional_context}"
            
#             # Add enhancement preferences
#             enhancement_preferences = []
#             if include_keywords:
#                 enhancement_preferences.append("optimize for ATS keywords")
#             if quantify_achievements:
#                 enhancement_preferences.append("quantify achievements with numbers and metrics")
#             if action_verbs:
#                 enhancement_preferences.append("use strong action verbs")
            
#             if enhancement_preferences:
#                 job_description += f"\n\nEnhancement Preferences: Focus on {', '.join(enhancement_preferences)}."
            
#             # Step 3: Process with OpenAI
#             status_text.text("🤖 AI is analyzing and enhancing your resume...")
#             progress_bar.progress(60)

#             from build_prompt import build_prompt
#             prompt = build_prompt(
#                 full_resume_content, 
#                 job_description,
#                 enhancement_level
#             )
            
#             from enhance_resume import enhance_resume
#             result = enhance_resume(full_resume_content)
            
#             if not result["success"]:
#                 st.error(f"Processing failed: {result.get('error', 'Unknown error')}")
#                 st.stop()
            
#             # Step 4: Display results
#             progress_bar.progress(90)
#             status_text.text("✅ Processing complete!")
#             time.sleep(0.5)
            
#             # Clear progress indicators
#             progress_bar.empty()
#             status_text.empty()
            
#             # Display success message
#             st.markdown('<div class="success-message">✨ Resume enhanced successfully!</div>', unsafe_allow_html=True)
            
#             # Show changes summary
#             st.markdown("### 📝 Summary of Changes")
#             st.info(result["changes_summary"])
            
#             # Create tabs for different views
#             tab1, tab2, tab3 = st.tabs(["📄 Enhanced Resume", "📊 Comparison", "💾 Download"])
            
#             with tab1:
#                 st.markdown("### Enhanced Resume (Markdown)")
#                 st.markdown(result["enhanced_resume"])
            
#             with tab2:
#                 st.markdown("### Original vs Enhanced")
                
#                 col_left, col_right = st.columns(2)
                
#                 with col_left:
#                     st.markdown("#### Original Resume")
#                     st.text_area("Original", extracted_content, height=400, key="original")
                
#                 with col_right:
#                     st.markdown("#### Enhanced Resume")
#                     st.text_area("Enhanced", result["enhanced_resume"], height=400, key="enhanced")
            
#             with tab3:
#                 st.markdown("### Download Enhanced Resume")
                
#                 download_col1, download_col2, download_col3 = st.columns(3)
                
#                 with download_col1:
#                     # Download as Markdown
#                     st.download_button(
#                         label="📝 Download as Markdown",
#                         data=result["enhanced_resume"],
#                         file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
#                         mime="text/markdown",
#                         use_container_width=True
#                     )
                
#                 with download_col2:
#                     # Download as DOCX
#                     docx_bytes = generator.create_docx_from_markdown(result["enhanced_resume"])
#                     if docx_bytes:
#                         st.download_button(
#                             label="📄 Download as DOCX",
#                             data=docx_bytes,
#                             file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
#                             mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#                             use_container_width=True
#                         )
                
#                 with download_col3:
#                     # Copy to clipboard (using JavaScript)
#                     st.markdown(f"""
#                     <button onclick="navigator.clipboard.writeText(`{result['enhanced_resume'].replace('`', '\\`')}`)" 
#                                 style="width:100%; padding:0.5rem; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
#                                        color:white; border:none; border-radius:5px; cursor:pointer;">
#                         📋 Copy to Clipboard
#                     </button>
#                     """, unsafe_allow_html=True)
            
#         except Exception as e:
#             st.error(f"An unexpected error occurred: {str(e)}")
#             progress_bar.empty()
#             status_text.empty()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p>Powered by OpenAI GPT-4 | Built with Streamlit</p>
    <p>⚠️ Always review the enhanced resume before submitting to employers</p>
</div>
""", unsafe_allow_html=True)