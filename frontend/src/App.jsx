import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";


/* ============================================================
   SMALL HELPERS
   ============================================================ */

function formatScore(value) {
  const number = Number(value || 0);

  if (Number.isInteger(number)) {
    return number;
  }

  return number.toFixed(2);
}


function getScoreClass(score) {
  const value = Number(score || 0);

  if (value >= 80) {
    return "score-good";
  }

  if (value >= 50) {
    return "score-medium";
  }

  return "score-low";
}


function getPercentage(value, maximum) {
  if (!maximum) {
    return 0;
  }

  return Math.min(
    100,
    Math.max(
      0,
      (Number(value || 0) / Number(maximum)) * 100
    )
  );
}


function safeArray(value) {
  return Array.isArray(value) ? value : [];
}


function safeString(value) {
  if (value === null || value === undefined) {
    return "";
  }

  return String(value);
}


/* ============================================================
   APP
   ============================================================ */

export default function App() {

  /* ----------------------------------------------------------
     THEME
  ---------------------------------------------------------- */

  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("resume-analyzer-dark-mode") === "true";
  });


  /* ----------------------------------------------------------
     NAVIGATION
  ---------------------------------------------------------- */

  const [activePage, setActivePage] = useState("dashboard");


  /* ----------------------------------------------------------
     RESUME ANALYSIS
  ---------------------------------------------------------- */

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  /* ----------------------------------------------------------
     HISTORY
  ---------------------------------------------------------- */

  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");

  const [historyResult, setHistoryResult] = useState(null);


  /* ----------------------------------------------------------
     ANALYTICS
  ---------------------------------------------------------- */

  const [analytics, setAnalytics] = useState(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [analyticsError, setAnalyticsError] = useState("");


  /* ----------------------------------------------------------
     JOB MATCHING
  ---------------------------------------------------------- */

  const [jobDescription, setJobDescription] = useState("");
  const [jobResult, setJobResult] = useState(null);
  const [jobLoading, setJobLoading] = useState(false);
  const [jobError, setJobError] = useState("");


  /* ==========================================================
     THEME EFFECT
     ========================================================== */

  useEffect(() => {

    localStorage.setItem(
      "resume-analyzer-dark-mode",
      darkMode
    );

  }, [darkMode]);


  /* ==========================================================
     FETCH HISTORY
     ========================================================== */

  async function loadHistory() {

    setHistoryLoading(true);
    setHistoryError("");

    try {

      const response = await fetch(
        `${API_URL}/history`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not load history."
        );
      }

      setHistory(
        safeArray(data.history)
      );

    } catch (err) {

      console.error(err);

      setHistoryError(
        err.message || "Could not load history."
      );

    } finally {

      setHistoryLoading(false);

    }
  }


  /* ==========================================================
     FETCH ANALYTICS
     ========================================================== */

  async function loadAnalytics() {

    setAnalyticsLoading(true);
    setAnalyticsError("");

    try {

      const response = await fetch(
        `${API_URL}/analytics`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not load analytics."
        );
      }

      setAnalytics(data);

    } catch (err) {

      console.error(err);

      setAnalyticsError(
        err.message || "Could not load analytics."
      );

    } finally {

      setAnalyticsLoading(false);

    }
  }


  /* ==========================================================
     INITIAL DATA
     ========================================================== */

  useEffect(() => {

    loadHistory();
    loadAnalytics();

  }, []);


  /* ==========================================================
     FILE SELECT
     ========================================================== */

  function handleFileChange(event) {

    const selectedFile =
      event.target.files?.[0];

    setError("");
    setResult(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (
      selectedFile.type !== "application/pdf"
      &&
      !selectedFile.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {

      setError(
        "Please select a PDF resume."
      );

      setFile(null);

      return;
    }

    setFile(selectedFile);
  }


  /* ==========================================================
     ANALYZE RESUME
     ========================================================== */

  async function analyzeResume() {

    if (!file) {

      setError(
        "Please select a PDF resume first."
      );

      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const response = await fetch(
        `${API_URL}/analyze-resume`,
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Resume analysis failed."
        );
      }

      setResult(data);

      setActivePage(
        "analysis-result"
      );

      await loadHistory();
      await loadAnalytics();

    } catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Resume analysis failed."
      );

    } finally {

      setLoading(false);

    }
  }


  /* ==========================================================
     DELETE HISTORY
     ========================================================== */

  async function deleteHistory(historyId) {

    const confirmed =
      window.confirm(
        "Delete this resume analysis from history?"
      );

    if (!confirmed) {
      return;
    }

    try {

      const response = await fetch(
        `${API_URL}/history/${historyId}`,
        {
          method: "DELETE"
        }
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Could not delete history."
        );
      }

      if (
        historyResult?.history_id ===
        historyId
      ) {

        setHistoryResult(null);
      }

      await loadHistory();
      await loadAnalytics();

    } catch (err) {

      console.error(err);

      setHistoryError(
        err.message ||
        "Could not delete history."
      );

    }
  }


  /* ==========================================================
     OPEN HISTORY RECORD
     ========================================================== */

  async function openHistory(historyId) {

    setHistoryLoading(true);
    setHistoryError("");

    try {

      const response = await fetch(
        `${API_URL}/history/${historyId}`
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Could not open saved analysis."
        );
      }

      if (data.legacy) {

        setHistoryError(
          data.message ||
          "Complete analysis is not available for this record."
        );

        return;
      }

      setHistoryResult(data);

      setActivePage(
        "history-result"
      );

    } catch (err) {

      console.error(err);

      setHistoryError(
        err.message ||
        "Could not open saved analysis."
      );

    } finally {

      setHistoryLoading(false);

    }
  }


  /* ==========================================================
     NAVIGATION
     ========================================================== */

  function goToPage(page) {

    setActivePage(page);

    setError("");
    setHistoryError("");
    setAnalyticsError("");
    setJobError("");
  }


  function goToDashboard() {

    setActivePage("dashboard");

    setError("");
    setHistoryError("");
    setAnalyticsError("");
    setJobError("");
  }


  function startNewAnalysis() {

    setFile(null);
    setResult(null);
    setError("");

    setActivePage(
      "analyze"
    );
  }


  /* ==========================================================
     JOB MATCHING
     ========================================================== */

  async function handleJobMatch() {

    if (!jobDescription.trim()) {

      setJobError(
        "Please enter a job description."
      );

      return;
    }

    if (!result?.resume_text) {

      setJobError(
        "Please analyze a resume first."
      );

      return;
    }

    setJobLoading(true);
    setJobError("");
    setJobResult(null);

    try {

      const response = await fetch(
        `${API_URL}/job-match`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            resume_text:
              result.resume_text,
            job_description:
              jobDescription
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Job matching failed."
        );
      }

      setJobResult(data);

    } catch (err) {

      console.error(err);

      setJobError(
        err.message ||
        "Job matching failed."
      );

    } finally {

      setJobLoading(false);

    }
  }


  /* ==========================================================
     RESUME DATA
     ========================================================== */

  const displayedResult =
    result || historyResult;


  const resumeData =
    displayedResult?.resume_data || {};


  const technicalSkills =
    safeArray(
      displayedResult?.skills
    );


  const softSkills =
    safeArray(
      displayedResult?.soft_skills
    );


  const recommendations =
    safeArray(
      displayedResult?.recommendations
    );


  /* ==========================================================
     PROJECT COUNT
     ========================================================== */

  /*
     IMPORTANT:

     We DO NOT count lines here.

     The backend now returns:

       score.project_count

     Therefore Shubham's five projects will
     display as 5 instead of counting GitHub
     links/descriptions.
  */

  const projectCount = Number(
    displayedResult?.score?.project_count ??
    0
  );


  const projectTitles =
    safeArray(
      displayedResult?.score?.project_titles
    );


  /* ==========================================================
     SCORE
     ========================================================== */

  const totalScore = Number(
    displayedResult?.score?.total || 0
  );


  /* ==========================================================
     APP CLASS
     ========================================================== */

  const appClassName =
    darkMode
      ? "app dark-app"
      : "app";


  /* ==========================================================
     RENDER
     ========================================================== */

  return (

    <div className={appClassName}>

      {/* ======================================================
          HEADER
          ====================================================== */}

      <header className="app-header">

        <div
          className="brand"
          onClick={goToDashboard}
        >

          <div className="brand-icon">
            AI
          </div>

          <div>
            <h2>
              Resume Analyzer
            </h2>

            <span>
              NLP Powered
            </span>
          </div>

        </div>


        <nav className="desktop-nav">

          <button
            className={
              activePage === "dashboard"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              goToPage("dashboard")
            }
          >
            Dashboard
          </button>


          <button
            className={
              activePage === "analyze"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              goToPage("analyze")
            }
          >
            Analyze Resume
          </button>


          <button
            className={
              activePage === "job-matching"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              goToPage("job-matching")
            }
          >
            Job Matching
          </button>


          <button
            className={
              activePage === "history" ||
              activePage === "history-result"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              goToPage("history")
            }
          >
            History
          </button>


          <button
            className={
              activePage === "analytics"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              goToPage("analytics")
            }
          >
            Analytics
          </button>

        </nav>


        <button
          className="theme-button"
          onClick={() =>
            setDarkMode(
              previous => !previous
            )
          }
          title={
            darkMode
              ? "Switch to light mode"
              : "Switch to dark mode"
          }
        >
          {darkMode ? "☀" : "☾"}
        </button>

      </header>


      {/* ======================================================
          MAIN
          ====================================================== */}

      <main className="page-content">


        {/* ====================================================
            DASHBOARD
            ==================================================== */}

        {activePage === "dashboard" && (

          <>

            <div className="welcome-section">

              <div>

                <span className="small-label">
                  AI RESUME ANALYZER
                </span>

                <h1>
                  Analyze your resume with NLP
                </h1>

                <p>
                  Extract resume information,
                  evaluate important sections,
                  and compare your skills with
                  a job description.
                </p>

              </div>

              <button
                className="primary-button"
                onClick={startNewAnalysis}
              >
                + Analyze New Resume
              </button>

            </div>


            <div className="dashboard-grid">


              <div className="dashboard-card">

                <div className="card-icon">
                  ↑
                </div>

                <h3>
                  Resume Analysis
                </h3>

                <p>
                  Upload a PDF resume and let
                  the NLP pipeline extract
                  important information.
                </p>

                <button
                  className="primary-button"
                  onClick={startNewAnalysis}
                >
                  Analyze Resume
                </button>

              </div>


              <div className="dashboard-card">

                <div className="card-icon">
                  #
                </div>

                <h3>
                  Job Matching
                </h3>

                <p>
                  Compare your analyzed resume
                  with a job description and
                  identify matched and missing
                  skills.
                </p>

                <button
                  className="secondary-button"
                  onClick={() =>
                    goToPage("job-matching")
                  }
                >
                  Match Job
                </button>

              </div>


              <div className="dashboard-card">

                <div className="card-icon">
                  ↺
                </div>

                <h3>
                  Analysis History
                </h3>

                <p>
                  View previously analyzed
                  resumes and open their saved
                  results.
                </p>

                <button
                  className="secondary-button"
                  onClick={() =>
                    goToPage("history")
                  }
                >
                  View History
                </button>

              </div>


              <div className="dashboard-card">

                <div className="card-icon">
                  ↗
                </div>

                <h3>
                  Analytics
                </h3>

                <p>
                  See average resume score,
                  highest score, skills statistics,
                  and score distribution.
                </p>

                <button
                  className="secondary-button"
                  onClick={() =>
                    goToPage("analytics")
                  }
                >
                  View Analytics
                </button>

              </div>

            </div>


            <div className="recent-analysis-card">

              <div>

                <span className="small-label">
                  RECENT ANALYSES
                </span>

                <h3>
                  {history.length > 0
                    ? `${history.length} resume${
                        history.length === 1
                          ? ""
                          : "s"
                      } analyzed`
                    : "No resumes analyzed yet"}
                </h3>

                <p>
                  {history.length > 0
                    ? "Open History to view saved resume analyses."
                    : "Upload your first resume to begin."}
                </p>

              </div>

              {history.length > 0 && (

                <button
                  className="secondary-button"
                  onClick={() =>
                    goToPage("history")
                  }
                >
                  Open History
                </button>

              )}

            </div>

          </>

        )}


        {/* ====================================================
            ANALYZE RESUME
            ==================================================== */}

        {activePage === "analyze" && (

          <>

            <div className="page-heading">

              <div>

                <span className="small-label">
                  NLP ANALYSIS
                </span>

                <h1>
                  Analyze Resume
                </h1>

                <p>
                  Upload a PDF resume to extract
                  personal information, education,
                  skills, projects, experience and
                  certifications.
                </p>

              </div>

            </div>


            <div className="upload-card">

              <div className="upload-icon">
                ↑
              </div>

              <h2>
                Upload your resume
              </h2>

              <p>
                PDF files only
              </p>


              <label className="file-button">

                Choose PDF

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                  style={{
                    display: "none"
                  }}
                />

              </label>


              {file && (

                <div className="selected-file">

                  <div>

                    <strong>
                      {file.name}
                    </strong>

                    <span>
                      {(
                        file.size / 1024
                      ).toFixed(1)} KB
                    </span>

                  </div>


                  <button
                    className="remove-button"
                    onClick={() =>
                      setFile(null)
                    }
                  >
                    Remove
                  </button>

                </div>

              )}


              {error && (

                <div className="error-message">
                  {error}
                </div>

              )}


              <button
                className="primary-button analyze-button"
                onClick={analyzeResume}
                disabled={
                  !file || loading
                }
              >

                {loading
                  ? "Analyzing..."
                  : "Analyze Resume"}

              </button>

            </div>

          </>

        )}


        {/* ====================================================
            ANALYSIS RESULT
            ==================================================== */}

        {activePage === "analysis-result" &&
          displayedResult && (

          <ResumeResult
            data={displayedResult}
            resumeData={resumeData}
            technicalSkills={technicalSkills}
            softSkills={softSkills}
            recommendations={recommendations}
            projectCount={projectCount}
            projectTitles={projectTitles}
            totalScore={totalScore}
            onBack={startNewAnalysis}
            onJobMatching={() =>
              goToPage("job-matching")
            }
          />

        )}


        {/* ====================================================
            HISTORY
            ==================================================== */}

        {activePage === "history" && (

          <>

            <div className="page-heading">

              <div>

                <span className="small-label">
                  SAVED ANALYSES
                </span>

                <h1>
                  Resume History
                </h1>

                <p>
                  View and manage your previous
                  resume analyses.
                </p>

              </div>

              <button
                className="primary-button"
                onClick={startNewAnalysis}
              >
                + New Analysis
              </button>

            </div>


            {historyError && (

              <div className="error-message">
                {historyError}
              </div>

            )}


            {historyLoading ? (

              <div className="loading-card">
                Loading history...
              </div>

            ) : history.length === 0 ? (

              <div className="empty-card">

                <div className="empty-icon">
                  ↺
                </div>

                <h2>
                  No analysis history
                </h2>

                <p>
                  Analyze a resume and it will
                  appear here.
                </p>

                <button
                  className="primary-button"
                  onClick={startNewAnalysis}
                >
                  Analyze Resume
                </button>

              </div>

            ) : (

              <div className="history-list">

                {history.map(item => (

                  <div
                    className="history-item"
                    key={item.id}
                  >

                    <div className="history-main">

                      <div className="history-file-icon">
                        PDF
                      </div>

                      <div>

                        <h3>
                          {item.filename}
                        </h3>

                        <p>
                          {item.analyzed_at}
                        </p>

                        <span>
                          {item.skills_count} technical
                          skill
                          {item.skills_count === 1
                            ? ""
                            : "s"} detected
                        </span>

                      </div>

                    </div>


                    <div className="history-score">

                      <strong
                        className={
                          getScoreClass(
                            item.score
                          )
                        }
                      >
                        {formatScore(item.score)}
                      </strong>

                      <small>
                        /100
                      </small>

                    </div>


                    <div className="history-actions">

                      <button
                        className="secondary-button"
                        onClick={() =>
                          openHistory(
                            item.id
                          )
                        }
                      >
                        View
                      </button>

                      <button
                        className="delete-button"
                        onClick={() =>
                          deleteHistory(
                            item.id
                          )
                        }
                      >
                        Delete
                      </button>

                    </div>

                  </div>

                ))}

              </div>

            )}

          </>

        )}


        {/* ====================================================
            HISTORY RESULT
            ==================================================== */}

        {activePage === "history-result" &&
          historyResult && (

          <>

            <button
              className="back-button"
              onClick={() =>
                goToPage("history")
              }
            >
              ← Back to History
            </button>


            <div className="result-header">

              <div>

                <span className="small-label">
                  SAVED ANALYSIS
                </span>

                <h1>
                  {historyResult.filename}
                </h1>

                <p>
                  Analyzed on{" "}
                  {historyResult.analyzed_at}
                </p>

              </div>

              <div className="result-actions">

                <button
                  className="secondary-button"
                  onClick={() =>
                    goToPage(
                      "job-matching"
                    )
                  }
                >
                  Job Matching
                </button>

                <button
                  className="primary-button"
                  onClick={startNewAnalysis}
                >
                  Analyze Another
                </button>

              </div>

            </div>


            <ResumeResult
              data={historyResult}
              resumeData={
                historyResult.resume_data ||
                {}
              }
              technicalSkills={
                safeArray(
                  historyResult.skills
                )
              }
              softSkills={
                safeArray(
                  historyResult.soft_skills
                )
              }
              recommendations={
                safeArray(
                  historyResult.recommendations
                )
              }
              projectCount={
                Number(
                  historyResult.score?.project_count ??
                  0
                )
              }
              projectTitles={
                safeArray(
                  historyResult.score?.project_titles
                )
              }
              totalScore={
                Number(
                  historyResult.score?.total ||
                  0
                )
              }
              onBack={() =>
                goToPage("history")
              }
              onJobMatching={() =>
                goToPage(
                  "job-matching"
                )
              }
              hideHeader
            />

          </>

        )}


        {/* ====================================================
            ANALYTICS
            ==================================================== */}

        {activePage === "analytics" && (

          <>

            <div className="page-heading">

              <div>

                <span className="small-label">
                  RESUME STATISTICS
                </span>

                <h1>
                  Analytics
                </h1>

                <p>
                  Statistics based on your
                  analyzed resumes.
                </p>

              </div>

              <button
                className="secondary-button"
                onClick={loadAnalytics}
              >
                Refresh
              </button>

            </div>


            {analyticsError && (

              <div className="error-message">
                {analyticsError}
              </div>

            )}


            {analyticsLoading ? (

              <div className="loading-card">
                Loading analytics...
              </div>

            ) : analytics ? (

              <>

                <div className="analytics-stats">

                  <div className="analytics-card">

                    <span>
                      Total Resumes
                    </span>

                    <strong>
                      {analytics.total_resumes || 0}
                    </strong>

                  </div>


                  <div className="analytics-card">

                    <span>
                      Average Score
                    </span>

                    <strong>
                      {formatScore(
                        analytics.average_score
                      )}
                    </strong>

                  </div>


                  <div className="analytics-card">

                    <span>
                      Highest Score
                    </span>

                    <strong>
                      {formatScore(
                        analytics.highest_score
                      )}
                    </strong>

                  </div>


                  <div className="analytics-card">

                    <span>
                      Average Skills
                    </span>

                    <strong>
                      {formatScore(
                        analytics.average_skills
                      )}
                    </strong>

                  </div>

                </div>


                <div className="content-card">

                  <div className="section-title">

                    <div className="section-title-icon">
                      %
                    </div>

                    <h2>
                      Score Distribution
                    </h2>

                  </div>


                  <div className="distribution-list">

                    {Object.entries(
                      analytics.score_distribution ||
                      {}
                    ).map(
                      ([range, count]) => {

                        const total =
                          Number(
                            analytics.total_resumes ||
                            0
                          );

                        const percentage =
                          total > 0
                            ? (
                                Number(count) /
                                total
                              ) * 100
                            : 0;

                        return (

                          <div
                            className="score-row"
                            key={range}
                          >

                            <div className="distribution-label">

                              <span>
                                {range}
                              </span>

                              <strong>
                                {count}
                              </strong>

                            </div>

                            <div className="progress-track">

                              <div
                                className="progress-fill"
                                style={{
                                  width:
                                    `${percentage}%`
                                }}
                              />

                            </div>

                          </div>

                        );

                      }
                    )}

                  </div>

                </div>


                <div className="content-card">

                  <div className="section-title">

                    <div className="section-title-icon">
                      ↕
                    </div>

                    <h2>
                      Resume Comparison
                    </h2>

                  </div>


                  {safeArray(
                    analytics.records
                  ).length === 0 ? (

                    <div className="empty-small">
                      No resume records available.
                    </div>

                  ) : (

                    <div className="analytics-table">

                      <div className="table-header">

                        <span>
                          Resume
                        </span>

                        <span>
                          Score
                        </span>

                        <span>
                          Skills
                        </span>

                        <span>
                          Date
                        </span>

                      </div>


                      {safeArray(
                        analytics.records
                      ).map(record => (

                        <div
                          className="table-row"
                          key={record.id}
                        >

                          <strong>
                            {record.filename}
                          </strong>

                          <span>
                            {formatScore(
                              record.score
                            )}
                            /100
                          </span>

                          <span>
                            {record.skills_count}
                          </span>

                          <span>
                            {record.analyzed_at}
                          </span>

                        </div>

                      ))}

                    </div>

                  )}

                </div>

              </>

            ) : (

              <div className="empty-card">
                No analytics data available.
              </div>

            )}

          </>

        )}


        {/* ====================================================
            JOB MATCHING
            ==================================================== */}

        {activePage === "job-matching" && (

          <>

            <div className="page-heading">

              <div>

                <span className="small-label">
                  NLP JOB MATCHING
                </span>

                <h1>
                  Job Matching
                </h1>

                <p>
                  Compare your analyzed resume
                  with a job description.
                </p>

              </div>

            </div>


            {!result?.resume_text &&
              !historyResult?.resume_text ? (

              <div className="empty-card">

                <div className="empty-icon">
                  #
                </div>

                <h2>
                  Analyze a resume first
                </h2>

                <p>
                  Job matching requires the
                  extracted resume text.
                </p>

                <button
                  className="primary-button"
                  onClick={startNewAnalysis}
                >
                  Analyze Resume
                </button>

              </div>

            ) : (

              <>

                <div className="content-card">

                  <div className="section-title">

                    <div className="section-title-icon">
                      #
                    </div>

                    <h2>
                      Job Description
                    </h2>

                  </div>


                  <textarea
                    className="job-textarea"
                    placeholder={
                      "Paste the job description here...\n\nExample:\nWe are looking for a Python developer with experience in React, FastAPI, SQL, Git and Machine Learning."
                    }
                    value={jobDescription}
                    onChange={event =>
                      setJobDescription(
                        event.target.value
                      )
                    }
                  />


                  {jobError && (

                    <div className="error-message">
                      {jobError}
                    </div>

                  )}


                  <button
                    className="primary-button"
                    onClick={handleJobMatch}
                    disabled={
                      jobLoading
                    }
                  >

                    {jobLoading
                      ? "Comparing..."
                      : "Compare Resume with Job"}

                  </button>

                </div>


                {jobResult && (

                  <>

                    <div className="match-score-card">

                      <span>
                        JOB MATCH SCORE
                      </span>

                      <strong>
                        {formatScore(
                          jobResult.match_percentage
                        )}
                        %
                      </strong>

                      <p>
                        Based on detected skills
                        in the resume and job
                        description.
                      </p>

                    </div>


                    <div className="content-card">

                      <div className="section-title">

                        <div className="section-title-icon">
                          ✓
                        </div>

                        <h2>
                          Matched Skills
                        </h2>

                      </div>


                      {safeArray(
                        jobResult.matched_skills
                      ).length > 0 ? (

                        <div className="skill-tags">

                          {safeArray(
                            jobResult.matched_skills
                          ).map(
                            (skill, index) => (

                              <span
                                className="skill-tag matched"
                                key={`${skill}-${index}`}
                              >
                                {skill}
                              </span>

                            )
                          )}

                        </div>

                      ) : (

                        <p className="muted">
                          No matching skills detected.
                        </p>

                      )}

                    </div>


                    <div className="content-card">

                      <div className="section-title">

                        <div className="section-title-icon">
                          !
                        </div>

                        <h2>
                          Missing Skills
                        </h2>

                      </div>


                      {safeArray(
                        jobResult.missing_skills
                      ).length > 0 ? (

                        <div className="skill-tags">

                          {safeArray(
                            jobResult.missing_skills
                          ).map(
                            (skill, index) => (

                              <span
                                className="skill-tag missing"
                                key={`${skill}-${index}`}
                              >
                                {skill}
                              </span>

                            )
                          )}

                        </div>

                      ) : (

                        <p className="muted">
                          No missing skills detected
                          from the supported skill list.
                        </p>

                      )}

                    </div>


                    <div className="content-card">

                      <div className="section-title">

                        <div className="section-title-icon">
                          ✓
                        </div>

                        <h2>
                          Skills Detected in Job
                        </h2>

                      </div>


                      {safeArray(
                        jobResult.job_skills
                      ).length > 0 ? (

                        <div className="skill-tags">

                          {safeArray(
                            jobResult.job_skills
                          ).map(
                            (skill, index) => (

                              <span
                                className="skill-tag"
                                key={`${skill}-${index}`}
                              >
                                {skill}
                              </span>

                            )
                          )}

                        </div>

                      ) : (

                        <p className="muted">
                          No supported technical
                          skills were detected.
                        </p>

                      )}

                    </div>

                  </>

                )}

              </>

            )}

          </>

        )}

      </main>

    </div>
  );
}


/* ============================================================
   RESUME RESULT COMPONENT
   ============================================================ */

function ResumeResult({
  data,
  resumeData,
  technicalSkills,
  softSkills,
  recommendations,
  projectCount,
  projectTitles,
  totalScore,
  onBack,
  onJobMatching,
  hideHeader = false
}) {

  const score =
    data?.score || {};


  const education =
    safeString(
      resumeData?.education
    );


  const experience =
    safeString(
      resumeData?.experience
    );


  const certifications =
    safeString(
      resumeData?.certifications
    );


  const summary =
    safeString(
      resumeData?.summary
    );


  const objective =
    safeString(
      resumeData?.objective
    );


  const additionalInformation =
    safeString(
      resumeData?.additional_information
    );


  return (

    <>

      {!hideHeader && (

        <>

          <button
            className="back-button"
            onClick={onBack}
          >
            ← Back
          </button>


          <div className="result-header">

            <div>

              <span className="small-label">
                ANALYSIS RESULT
              </span>

              <h1>
                {data.filename ||
                  "Resume Analysis"}
              </h1>

              <p>
                {data.analyzed_at ||
                  "Resume processed successfully."}
              </p>

            </div>


            <div className="result-actions">

              <button
                className="secondary-button"
                onClick={onJobMatching}
              >
                Job Matching
              </button>

              <button
                className="primary-button"
                onClick={onBack}
              >
                Analyze Another
              </button>

            </div>

          </div>

        </>

      )}


      {/* ======================================================
          TOP STAT CARDS
          ====================================================== */}

      <div className="stats-grid">

        <div className="stat-card">

          <div className="stat-icon">
            ◎
          </div>

          <div>

            <span>
              Resume Score
            </span>

            <strong
              className={
                getScoreClass(
                  totalScore
                )
              }
            >
              {formatScore(
                totalScore
              )}/100
            </strong>

            <small>
              Overall score
            </small>

          </div>

        </div>


        <div className="stat-card">

          <div className="stat-icon">
            &lt;&gt;
          </div>

          <div>

            <span>
              Technical Skills
            </span>

            <strong>
              {technicalSkills.length}
            </strong>

            <small>
              Skills detected
            </small>

          </div>

        </div>


        <div className="stat-card">

          <div className="stat-icon">
            □
          </div>

          <div>

            <span>
              Projects
            </span>

            <strong>
              {projectCount}
            </strong>

            <small>
              Projects detected
            </small>

          </div>

        </div>


        <div className="stat-card">

          <div className="stat-icon">
            ↗
          </div>

          <div>

            <span>
              Analysis
            </span>

            <strong>
              Complete
            </strong>

            <small>
              {data.history_id
                ? "Saved analysis"
                : "Resume processed"}
            </small>

          </div>

        </div>

      </div>


      {/* ======================================================
          SCORE
          ====================================================== */}

      <div className="content-card score-card">

        <div className="section-heading">

          <div>

            <span className="section-label">
              OVERALL RESUME SCORE
            </span>

            <div className="big-score">

              {formatScore(
                totalScore
              )}

              <span>
                /100
              </span>

            </div>

            <p>
              Your score is calculated using
              information detected from your
              resume.
            </p>

          </div>


          <div className="score-circle">

            {formatScore(
              totalScore
            )}

          </div>

        </div>

      </div>


      {/* ======================================================
          PERSONAL INFORMATION
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ♙
          </div>

          <h2>
            Personal Information
          </h2>

        </div>


        <div className="info-grid">

          <div className="info-box">

            <div className="info-icon">
              ♙
            </div>

            <div>

              <span>
                Name
              </span>

              <strong>
                {resumeData.name ||
                  "Not detected"}
              </strong>

            </div>

          </div>


          <div className="info-box">

            <div className="info-icon">
              ✉
            </div>

            <div>

              <span>
                Email
              </span>

              <strong>
                {resumeData.email ||
                  "Not detected"}
              </strong>

            </div>

          </div>


          <div className="info-box">

            <div className="info-icon">
              ☎
            </div>

            <div>

              <span>
                Phone
              </span>

              <strong>
                {resumeData.phone ||
                  "Not detected"}
              </strong>

            </div>

          </div>

        </div>

      </div>


      {/* ======================================================
          SCORE BREAKDOWN
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ◈
          </div>

          <h2>
            Score Breakdown
          </h2>

        </div>


        <div className="score-breakdown">

          <ScoreRow
            label="Technical Skills"
            value={score.skills}
            maximum={30}
          />

          <ScoreRow
            label="Education"
            value={score.education}
            maximum={15}
          />

          <ScoreRow
            label="Experience"
            value={score.experience}
            maximum={20}
          />

          <ScoreRow
            label="Projects"
            value={score.projects}
            maximum={15}
          />

          <ScoreRow
            label="Certifications"
            value={score.certifications}
            maximum={10}
          />

          <ScoreRow
            label="Completeness"
            value={score.completeness}
            maximum={10}
          />

        </div>

      </div>


      {/* ======================================================
          SUMMARY / OBJECTIVE
          ====================================================== */}

      {(summary || objective) && (

        <div className="content-card">

          <div className="section-title">

            <div className="section-title-icon">
              ≡
            </div>

            <h2>
              Professional Profile
            </h2>

          </div>


          <div className="section-content">

            {summary && (

              <>

                <strong>
                  Summary
                </strong>

                <p>
                  {summary}
                </p>

              </>

            )}


            {objective && (

              <>

                <strong>
                  Objective
                </strong>

                <p>
                  {objective}
                </p>

              </>

            )}

          </div>

        </div>

      )}


      {/* ======================================================
          EDUCATION
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ♢
          </div>

          <h2>
            Education
          </h2>

        </div>


        {education ? (

          <div className="section-content">

            {education
              .split("\n")
              .filter(Boolean)
              .map(
                (line, index) => (

                  <p
                    key={index}
                  >
                    {line}
                  </p>

                )
              )}

          </div>

        ) : (

          <p className="muted">
            Education information was not detected.
          </p>

        )}

      </div>


      {/* ======================================================
          TECHNICAL SKILLS
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            &lt;&gt;
          </div>

          <h2>
            Technical Skills
          </h2>

        </div>


        {technicalSkills.length > 0 ? (

          <div className="skill-tags">

            {technicalSkills.map(
              (skill, index) => (

                <span
                  className="skill-tag"
                  key={`${skill}-${index}`}
                >
                  {skill}
                </span>

              )
            )}

          </div>

        ) : (

          <p className="muted">
            No technical skills detected.
          </p>

        )}

      </div>


      {/* ======================================================
          SOFT SKILLS
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ♡
          </div>

          <h2>
            Soft Skills
          </h2>

        </div>


        {softSkills.length > 0 ? (

          <div className="skill-tags">

            {softSkills.map(
              (skill, index) => (

                <span
                  className="skill-tag"
                  key={`${skill}-${index}`}
                >
                  {skill}
                </span>

              )
            )}

          </div>

        ) : (

          <p className="muted">
            No soft skills detected.
          </p>

        )}

      </div>


      {/* ======================================================
          PROJECTS
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            □
          </div>

          <h2>
            Projects
          </h2>

        </div>


        {projectCount > 0 ? (

          <>

            <p className="muted">
              {projectCount} project
              {projectCount === 1
                ? ""
                : "s"} detected
            </p>


            {projectTitles.length > 0 ? (

              <div className="section-content">

                {projectTitles.map(
                  (project, index) => (

                    <p
                      key={`${project}-${index}`}
                    >
                      <strong>
                        {index + 1}.
                      </strong>{" "}
                      {project}
                    </p>

                  )
                )}

              </div>

            ) : (

              <p className="muted">
                Project count detected, but
                project titles were not saved.
              </p>

            )}

          </>

        ) : (

          <p className="muted">
            No projects detected.
          </p>

        )}

      </div>


      {/* ======================================================
          EXPERIENCE
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ◷
          </div>

          <h2>
            Experience
          </h2>

        </div>


        {experience ? (

          <div className="section-content">

            {experience
              .split("\n")
              .filter(Boolean)
              .map(
                (line, index) => (

                  <p
                    key={index}
                  >
                    {line}
                  </p>

                )
              )}

          </div>

        ) : (

          <p className="muted">
            No experience detected.
          </p>

        )}

      </div>


      {/* ======================================================
          CERTIFICATIONS
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ✓
          </div>

          <h2>
            Certifications
          </h2>

        </div>


        {certifications ? (

          <div className="section-content">

            {certifications
              .split("\n")
              .filter(Boolean)
              .map(
                (line, index) => (

                  <p
                    key={index}
                  >
                    {line}
                  </p>

                )
              )}

          </div>

        ) : (

          <p className="muted">
            No certifications detected.
          </p>

        )}

      </div>


      {/* ======================================================
          ADDITIONAL INFORMATION
          ====================================================== */}

      {additionalInformation && (

        <div className="content-card">

          <div className="section-title">

            <div className="section-title-icon">
              +
            </div>

            <h2>
              Additional Information
            </h2>

          </div>


          <div className="section-content">

            {additionalInformation
              .split("\n")
              .filter(Boolean)
              .map(
                (line, index) => (

                  <p
                    key={index}
                  >
                    {line}
                  </p>

                )
              )}

          </div>

        </div>

      )}


      {/* ======================================================
          RECOMMENDATIONS
          ====================================================== */}

      <div className="content-card">

        <div className="section-title">

          <div className="section-title-icon">
            ✦
          </div>

          <h2>
            Recommendations
          </h2>

        </div>


        {recommendations.length > 0 ? (

          <div className="recommendations">

            {recommendations.map(
              (recommendation, index) => (

                <div
                  className="recommendation"
                  key={index}
                >

                  <span>
                    ✓
                  </span>

                  <p>
                    {recommendation}
                  </p>

                </div>

              )
            )}

          </div>

        ) : (

          <p className="muted">
            No recommendations available.
          </p>

        )}

      </div>

    </>

  );
}


/* ============================================================
   SCORE ROW
   ============================================================ */

function ScoreRow({
  label,
  value,
  maximum
}) {

  const numericValue =
    Number(value || 0);

  const percentage =
    getPercentage(
      numericValue,
      maximum
    );

  return (

    <div className="score-row">

      <div className="score-row-top">

        <span>
          {label}
        </span>

        <strong>
          {formatScore(
            numericValue
          )}
          /{maximum}
        </strong>

      </div>


      <div className="progress-track">

        <div
          className="progress-fill"
          style={{
            width:
              `${percentage}%`
          }}
        />

      </div>

    </div>

  );
}