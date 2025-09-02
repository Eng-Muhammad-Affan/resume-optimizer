import React, { useState } from 'react';
import axios from 'axios';

// Main application component
const Home: React.FC = () => {
  // State for managing form inputs and application status
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isOptimizing, setIsOptimizing] = useState<boolean>(false);
  const [optimizedResume, setOptimizedResume] = useState<string | null>(null);

  // Handle file input changes, ensuring only PDF files are accepted
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
    } else {
      setResumeFile(null);
      alert('Please upload a PDF file.');
    }
  };

  // Handle text area changes
  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(event.target.value);
  };

  // Simulate the optimization process with a loading state
const handleOptimize = async () => {
    if (!resumeFile || jobDescription.trim() === '') {
        // ... (existing alert)
        return;
    }

    setIsOptimizing(true);
    setOptimizedResume(null);

    const formData = new FormData();
    formData.append('resume', resumeFile); // 'resume' is the field name for the file
    formData.append('description', jobDescription); // You can also send other data

    try {

      const response = await axios.post('http://localhost:8000/optimize', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        // Assuming the response from the server contains the optimized resume
        setOptimizedResume(response.data.optimized_resume_content);
    } catch (error) {
        console.error("Optimization failed:", error);
        alert("An error occurred. Please try again.");
    } finally {
        setIsOptimizing(false);
    }
};

  const isButtonDisabled = !resumeFile || jobDescription.trim() === '' || isOptimizing;

  return (
    <div className="min-h-screen bg-slate-900 text-gray-200 p-4 sm:p-8 flex items-center justify-center font-sans">
      <div className="w-full max-w-4xl bg-slate-800 p-6 sm:p-10 rounded-3xl shadow-2xl space-y-8 border border-slate-700">

        {/* Header Section */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white leading-tight">AI Resume Optimizer</h1>
          <p className="text-sm sm:text-lg text-slate-400 max-w-2xl mx-auto">Tailor your resume for any job opening with the power of AI. Upload your PDF, paste the job requirements, and get a perfectly optimized resume.</p>
        </div>

        {/* Input Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Resume Upload Card */}
          <div className="bg-slate-700 p-6 rounded-2xl border-2 border-dashed border-slate-600 hover:border-sky-500 transition-colors duration-200 relative group">
            <label htmlFor="resume-file" className="block text-xl font-semibold mb-2 text-white">Upload Your Resume (PDF)</label>
            <input
              type="file"
              id="resume-file"
              accept=".pdf"
              onChange={handleFileChange}
              className="w-full text-sm text-slate-300
                         file:mr-4 file:py-2 file:px-4
                         file:rounded-full file:border-0
                         file:text-sm file:font-semibold
                         file:bg-slate-600 file:text-sky-300
                         hover:file:bg-slate-500
                         cursor-pointer
                         transition-all"
            />
            {resumeFile && (
              <p className="mt-4 text-sm text-sky-400">
                File selected: <span className="font-medium">{resumeFile.name}</span>
              </p>
            )}
            <p className="absolute bottom-4 right-4 text-sm text-slate-500 transition-opacity duration-200 group-hover:opacity-100 opacity-0">.pdf only</p>
          </div>

          {/* Job Description Text Area */}
          <div className="bg-slate-700 p-6 rounded-2xl border-2 border-dashed border-slate-600 hover:border-sky-500 transition-colors duration-200">
            <label htmlFor="job-description" className="block text-xl font-semibold mb-2 text-white">Paste Job Requirements</label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={handleTextChange}
              rows={8}
              placeholder="Copy and paste the job description or a list of requirements here..."
              className="w-full h-40 p-3 rounded-xl bg-slate-800 text-slate-300 placeholder-slate-500 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500 transition-all resize-none"
            ></textarea>
          </div>
        </div>

        {/* Optimization Button */}
        <div className="flex justify-center">
          <button
            onClick={handleOptimize}
            disabled={isButtonDisabled}
            className={`
              w-full sm:w-auto px-12 py-4 rounded-full font-bold text-lg
              shadow-lg transition-all duration-300 transform
              ${isButtonDisabled
                ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
                : 'bg-sky-600 text-white hover:bg-sky-500 hover:scale-105 active:bg-sky-700'
              }
              flex items-center justify-center space-x-2
            `}
          >
            {isOptimizing ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Optimizing...</span>
              </>
            ) : (
              <span>Optimize Resume</span>
            )}
          </button>
        </div>

        {/* Results Section */}
        {optimizedResume && (
          <div className="bg-slate-700 p-6 rounded-2xl mt-8 border border-slate-600">
            <h2 className="text-2xl font-bold text-white mb-4">Optimized Resume</h2>
            <div
              className="p-4 bg-slate-800 rounded-lg whitespace-pre-wrap text-slate-300 leading-relaxed overflow-x-auto"
              dangerouslySetInnerHTML={{ __html: optimizedResume.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
            />
            <p className="mt-4 text-sm text-slate-400">
              This is a draft. Always review and refine the content before using.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home