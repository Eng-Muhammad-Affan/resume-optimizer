import time
from datetime import datetime
from typing import Any 

import streamlit as st 

def process_resume (
        uploaded_file:Any,
        additional_context:str,
        job_description:str,
        enhancement_level:str,
include_keywords:bool,
quantify_achievements:bool,
action_verbs:bool,
          ):
        """Function which processes resume , give it to AI , take the enhanced resume and write to a new pdf file """
        if not uploaded_file:
            st.error("Please upload a resume file")
        elif not job_description:
            st.error("Please provide a job description")
        else:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Extract content
                status_text.text("📄 Extracting content from resume...")
                progress_bar.progress(20)

                file_content = uploaded_file.read()

                from document_extractor import  DocumentExtractor
                extractor = DocumentExtractor()
                extracted_content, file_format = extractor.extract_content(file_content, uploaded_file.name)

                if not extracted_content:
                    st.error("Failed to extract content from the file")
                    st.stop()

                # Step 2: Prepare content
                status_text.text("🎯 Preparing for AI enhancement...")
                progress_bar.progress(40)

                # Combine with additional context
                full_resume_content = extracted_content
                if additional_context:
                    full_resume_content += f"\n\nAdditional Context:\n{additional_context}"

                # Add enhancement preferences
                enhancement_preferences = []
                if include_keywords:
                    enhancement_preferences.append("optimize for ATS keywords")
                if quantify_achievements:
                    enhancement_preferences.append("quantify achievements with numbers and metrics")
                if action_verbs:
                    enhancement_preferences.append("use strong action verbs")

                if enhancement_preferences:
                    job_description += f"\n\nEnhancement Preferences: Focus on {', '.join(enhancement_preferences)}."

                # Step 3: Process with OpenAI
                status_text.text("🤖 AI is analyzing and enhancing your resume...")
                progress_bar.progress(60)

                # Create the prompt based on enhancement level

                from build_prompt import build_prompt
                user_prompt = build_prompt(resume_content=full_resume_content , job_description=job_description , enhancement_level=enhancement_level)

                from agent.enhance_resume import enhance_resume
                result = enhance_resume(full_resume_content , user_prompt)

                if not result["success"]:
                    st.error(f"AI processing failed: {result.get('error', 'Unknown error')}")
                    st.stop()

                # Step 4: Display results
                progress_bar.progress(90)
                status_text.text("✅ Processing complete!")
                time.sleep(0.5)

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                # Display success message
                st.markdown('<div class="success-message">✨ Resume enhanced successfully!</div>', unsafe_allow_html=True)

                # Show changes summary
                st.markdown("### 📝 Summary of Changes")
                st.info(result["changes_summary"])

                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📄 Enhanced Resume", "📊 Comparison", "💾 Download"])

                with tab1:
                    st.markdown("### Enhanced Resume (Markdown)")
                    st.markdown(result["enhanced_resume"])

                with tab2:
                    st.markdown("### Original vs Enhanced")

                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.markdown("#### Original Resume")
                        st.text_area("Original", extracted_content, height=400, key="original")

                    with col_right:
                        st.markdown("#### Enhanced Resume")
                        st.text_area("Enhanced", result["enhanced_resume"], height=400, key="enhanced")

                with tab3:
                    st.markdown("### Download Enhanced Resume")

                    download_col1, download_col2, download_col3 = st.columns(3)

                    with download_col1:
                        # Download as Markdown
                        st.download_button(
                            label="📝 Download as Markdown",
                            data=result["enhanced_resume"],
                            file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                    with download_col2:
                        # Download as DOCX
                        from document_generator import DocumentGenerator
  
                        generator = DocumentGenerator()
  
                        docx_bytes = generator.create_docx_from_markdown(result["enhanced_resume"])
  
                        if docx_bytes:
                            st.download_button(
                                label="📄 Download as DOCX",
                                data=docx_bytes,
                                file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )

                    with download_col3:
                        # Copy to clipboard (using JavaScript)
                        st.markdown(f"""
                        <button onclick="navigator.clipboard.writeText(`{result['enhanced_resume'].replace('`', '\\`')}`)" 
                                    style="width:100%; padding:0.5rem; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                           color:white; border:none; border-radius:5px; cursor:pointer;">
                            📋 Copy to Clipboard
                        </button>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                progress_bar.empty()
                status_text.empty()
