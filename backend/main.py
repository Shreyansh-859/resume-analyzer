from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import inspect
import sqlite3
import json
from datetime import datetime

from resume.pdf_extractor import extract_text_from_pdf
from resume.resume_analyzer import (
    analyze_resume,
    generate_recommendations
)
from resume.skill_extractor import (
    extract_skills,
    extract_soft_skills
)
from resume.scoring import calculate_resume_score
from resume.job_matcher import analyze_job_match


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Resume Analyzer API",
    description="NLP Based Resume Analyzer and Job Matching System",
    version="3.1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE
# ============================================================

DATABASE = "resume_history.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resume_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            score REAL NOT NULL,
            skills_count INTEGER NOT NULL,
            analyzed_at TEXT NOT NULL
        )
        """
    )

    # Check existing columns
    cursor.execute(
        "PRAGMA table_info(resume_history)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    # Add result_json to older databases
    if "result_json" not in columns:
        cursor.execute(
            """
            ALTER TABLE resume_history
            ADD COLUMN result_json TEXT
            """
        )

    connection.commit()
    connection.close()


create_database()


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer API is running",
        "version": "3.1.0"
    }


# ============================================================
# ANALYZE RESUME
# ============================================================

@app.post("/analyze-resume")
async def analyze_resume_endpoint(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate PDF
    # --------------------------------------------------------

    if (
        file.content_type != "application/pdf"
        and not file.filename.lower().endswith(".pdf")
    ):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    try:

        # ----------------------------------------------------
        # Read uploaded PDF
        # ----------------------------------------------------

        pdf_bytes = await file.read()

        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )

        # ----------------------------------------------------
        # Extract text from PDF
        # ----------------------------------------------------

        resume_text = extract_text_from_pdf(
            pdf_bytes
        )

        if inspect.isawaitable(resume_text):
            resume_text = await resume_text

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF."
            )

        resume_text = str(
            resume_text
        ).strip()

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF."
            )

        # ----------------------------------------------------
        # Analyze resume sections
        # ----------------------------------------------------

        resume_data = analyze_resume(
            resume_text
        )

        if inspect.isawaitable(resume_data):
            resume_data = await resume_data

        # ----------------------------------------------------
        # TECHNICAL SKILLS
        #
        # IMPORTANT:
        # Search the COMPLETE resume text.
        #
        # We do NOT depend on:
        #
        # resume_data["skills"]
        #
        # because PDF layouts can sometimes cause the
        # section parser to return an empty Skills section.
        # ----------------------------------------------------

        skills = extract_skills(
            resume_text
        )

        if inspect.isawaitable(skills):
            skills = await skills

        # Make sure skills is always a list
        if not isinstance(skills, list):
            skills = []

        # ----------------------------------------------------
        # SOFT SKILLS
        #
        # Search the complete resume because a resume may not
        # have a dedicated "Soft Skills" heading.
        # ----------------------------------------------------

        soft_skills = extract_soft_skills(
            resume_text
        )

        if inspect.isawaitable(soft_skills):
            soft_skills = await soft_skills

        # Make sure soft_skills is always a list
        if not isinstance(soft_skills, list):
            soft_skills = []

        # ----------------------------------------------------
        # Store soft skills inside resume_data
        # ----------------------------------------------------

        resume_data["soft_skills"] = ", ".join(
            soft_skills
        )

        # ----------------------------------------------------
        # Calculate resume score
        # ----------------------------------------------------

        score = calculate_resume_score(
            resume_data,
            skills
        )

        if inspect.isawaitable(score):
            score = await score

        # ----------------------------------------------------
        # Missing skills
        # ----------------------------------------------------

        missing_skills = score.get(
            "missing_skills",
            []
        )

        if not isinstance(
            missing_skills,
            list
        ):
            missing_skills = []

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        recommendations = generate_recommendations(
            resume_data,
            skills,
            missing_skills
        )

        if inspect.isawaitable(recommendations):
            recommendations = await recommendations

        if not isinstance(
            recommendations,
            list
        ):
            recommendations = []

        # ----------------------------------------------------
        # Total score
        # ----------------------------------------------------

        total_score = score.get(
            "total",
            0
        )

        try:
            total_score = float(
                total_score
            )
        except (
            TypeError,
            ValueError
        ):
            total_score = 0.0

        # ----------------------------------------------------
        # Complete result
        # ----------------------------------------------------

        complete_result = {

            "success": True,

            "resume_text": resume_text,

            "resume_data": resume_data,

            # Technical skills
            "skills": skills,

            # Soft skills
            "soft_skills": soft_skills,

            # Score
            "score": score,

            # Recommendations
            "recommendations": recommendations
        }

        # ----------------------------------------------------
        # Save result to database
        # ----------------------------------------------------

        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()

        analyzed_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO resume_history
            (
                filename,
                score,
                skills_count,
                analyzed_at,
                result_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                file.filename,
                total_score,
                len(skills),
                analyzed_at,
                json.dumps(
                    complete_result,
                    ensure_ascii=False
                )
            )
        )

        history_id = cursor.lastrowid

        connection.commit()
        connection.close()

        # ----------------------------------------------------
        # Add database information to response
        # ----------------------------------------------------

        complete_result["history_id"] = (
            history_id
        )

        complete_result["filename"] = (
            file.filename
        )

        complete_result["analyzed_at"] = (
            analyzed_at
        )

        return complete_result

    # --------------------------------------------------------
    # HTTP errors
    # --------------------------------------------------------

    except HTTPException:
        raise

    # --------------------------------------------------------
    # Unexpected errors
    # --------------------------------------------------------

    except Exception as e:

        print(
            "Resume analysis error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Resume analysis failed: {str(e)}"
            )
        )


# ============================================================
# GET ALL HISTORY
# ============================================================

@app.get("/history")
def get_history():

    try:

        connection = sqlite3.connect(
            DATABASE
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                filename,
                score,
                skills_count,
                analyzed_at,

                CASE
                    WHEN result_json IS NOT NULL
                    THEN 1
                    ELSE 0
                END AS has_complete_analysis

            FROM resume_history

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        history = []

        for row in rows:

            history.append({

                "id": row["id"],

                "filename": row["filename"],

                "score": row["score"],

                "skills_count": row[
                    "skills_count"
                ],

                "analyzed_at": row[
                    "analyzed_at"
                ],

                "has_complete_analysis":
                    bool(
                        row[
                            "has_complete_analysis"
                        ]
                    )
            })

        return {
            "success": True,
            "history": history
        }

    except Exception as e:

        print(
            "History error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not load history: {str(e)}"
            )
        )


# ============================================================
# GET SINGLE HISTORY RECORD
# ============================================================

@app.get("/history/{history_id}")
def get_history_record(
    history_id: int
):

    try:

        connection = sqlite3.connect(
            DATABASE
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                filename,
                score,
                skills_count,
                analyzed_at,
                result_json

            FROM resume_history

            WHERE id = ?
            """,
            (history_id,)
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:

            raise HTTPException(
                status_code=404,
                detail="History record not found."
            )

        # ----------------------------------------------------
        # Older record
        # ----------------------------------------------------

        if not row["result_json"]:

            return {

                "success": False,

                "legacy": True,

                "message": (
                    "Complete analysis data is not "
                    "available for this older record."
                ),

                "history_id": row["id"],

                "filename": row["filename"],

                "score": row["score"],

                "skills_count": row[
                    "skills_count"
                ],

                "analyzed_at": row[
                    "analyzed_at"
                ]
            }

        # ----------------------------------------------------
        # Load saved result
        # ----------------------------------------------------

        result = json.loads(
            row["result_json"]
        )

        result["success"] = True

        result["history_id"] = (
            row["id"]
        )

        result["filename"] = (
            row["filename"]
        )

        result["analyzed_at"] = (
            row["analyzed_at"]
        )

        return result

    except HTTPException:
        raise

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail=(
                "Saved analysis data is corrupted."
            )
        )

    except Exception as e:

        print(
            "Single history error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not load analysis: {str(e)}"
            )
        )


# ============================================================
# ANALYTICS
# ============================================================

@app.get("/analytics")
def get_analytics():

    try:

        connection = sqlite3.connect(
            DATABASE
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                filename,
                score,
                skills_count,
                analyzed_at

            FROM resume_history

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        # ----------------------------------------------------
        # No records
        # ----------------------------------------------------

        if not rows:

            return {

                "success": True,

                "total_resumes": 0,

                "average_score": 0,

                "highest_score": 0,

                "average_skills": 0,

                "score_distribution": {

                    "0-20": 0,

                    "21-40": 0,

                    "41-60": 0,

                    "61-80": 0,

                    "81-100": 0
                },

                "records": []
            }

        # ----------------------------------------------------
        # Prepare records
        # ----------------------------------------------------

        records = []

        for row in rows:

            records.append({

                "id": row["id"],

                "filename": row[
                    "filename"
                ],

                "score": float(
                    row["score"]
                ),

                "skills_count": int(
                    row["skills_count"]
                ),

                "analyzed_at": row[
                    "analyzed_at"
                ]
            })

        # ----------------------------------------------------
        # Calculate statistics
        # ----------------------------------------------------

        scores = [
            float(row["score"])
            for row in rows
        ]

        skills = [
            int(row["skills_count"])
            for row in rows
        ]

        total_resumes = len(rows)

        average_score = (
            sum(scores)
            / total_resumes
        )

        highest_score = max(
            scores
        )

        average_skills = (
            sum(skills)
            / total_resumes
        )

        # ----------------------------------------------------
        # Score distribution
        # ----------------------------------------------------

        distribution = {

            "0-20": 0,

            "21-40": 0,

            "41-60": 0,

            "61-80": 0,

            "81-100": 0
        }

        for score_value in scores:

            if score_value <= 20:

                distribution["0-20"] += 1

            elif score_value <= 40:

                distribution["21-40"] += 1

            elif score_value <= 60:

                distribution["41-60"] += 1

            elif score_value <= 80:

                distribution["61-80"] += 1

            else:

                distribution["81-100"] += 1

        return {

            "success": True,

            "total_resumes":
                total_resumes,

            "average_score":
                round(
                    average_score,
                    2
                ),

            "highest_score":
                round(
                    highest_score,
                    2
                ),

            "average_skills":
                round(
                    average_skills,
                    2
                ),

            "score_distribution":
                distribution,

            "records":
                records
        }

    except Exception as e:

        print(
            "Analytics error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not load analytics: {str(e)}"
            )
        )


# ============================================================
# DELETE HISTORY RECORD
# ============================================================

@app.delete("/history/{history_id}")
def delete_history(
    history_id: int
):

    try:

        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM resume_history

            WHERE id = ?
            """,
            (history_id,)
        )

        deleted = cursor.rowcount

        connection.commit()

        connection.close()

        if deleted == 0:

            raise HTTPException(
                status_code=404,
                detail="History record not found."
            )

        return {

            "success": True,

            "message":
                "History record deleted."
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            "Delete history error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not delete history: {str(e)}"
            )
        )


# ============================================================
# JOB MATCHING REQUEST MODEL
# ============================================================

class JobMatchRequest(BaseModel):

    resume_text: str

    job_description: str


# ============================================================
# JOB MATCHING
# ============================================================

@app.post("/job-match")
async def job_match(
    request: JobMatchRequest
):

    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    if not request.resume_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Resume text is required."
        )

    # --------------------------------------------------------
    # Validate job description
    # --------------------------------------------------------

    if not request.job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description is required."
        )

    try:

        result = analyze_job_match(
            request.resume_text,
            request.job_description
        )

        if inspect.isawaitable(result):

            result = await result

        return {

            "success": True,

            **result
        }

    except Exception as e:

        print(
            "Job matching error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Job matching failed: {str(e)}"
            )
        )