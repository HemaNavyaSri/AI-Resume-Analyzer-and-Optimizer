import re

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS_DATABASE = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Flask",
    "Django",
    "Streamlit",
    "React",
    "Node.js",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "Data Science",
    "Data Analysis",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "OpenCV",
    "Keras",
    "Power BI",
    "Tableau",
    "Excel",
    "Linux",
    "REST API",
    "API",
    "DSA",
    "Data Structures",
    "Algorithms",
    "OOP",
    "Object Oriented Programming",
    "Cyber Security",
    "Cloud Computing",
    "Generative AI",
    "LLM",
    "Large Language Models",
    "Transformers"
]


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\-\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def skill_exists(skill, text):

    skill_lower = skill.lower()

    escaped_skill = re.escape(skill_lower)

    pattern = (
        r"(?<![a-z0-9])"
        + escaped_skill
        + r"(?![a-z0-9])"
    )

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


def extract_skills(text):

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILLS_DATABASE:

        if skill_exists(
            skill,
            normalized_text
        ):

            found_skills.append(skill)

    return found_skills


def calculate_match_score(
    resume_text,
    job_description
):

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform([
        resume_text,
        job_description
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


def calculate_skill_match(
    resume_skills,
    job_skills
):

    if not job_skills:
        return 0

    resume_skills_lower = [
        skill.lower()
        for skill in resume_skills
    ]

    matched_count = 0

    for skill in job_skills:

        if skill.lower() in resume_skills_lower:
            matched_count += 1

    score = (
        matched_count
        / len(job_skills)
    ) * 100

    return round(score, 2)


def analyze_resume(
    pdf_path,
    job_description
):

    resume_text = extract_text_from_pdf(
        pdf_path
    )

    if not resume_text.strip():
        raise ValueError(
            "No readable text was found in the PDF."
        )

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matching_skills = []

    missing_skills = []

    resume_skills_lower = [
        skill.lower()
        for skill in resume_skills
    ]

    for skill in job_skills:

        if skill.lower() in resume_skills_lower:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    text_match_score = calculate_match_score(
        resume_text,
        job_description
    )

    skill_match_score = calculate_skill_match(
        resume_skills,
        job_skills
    )

    if job_skills:

        final_score = round(
            (
                text_match_score * 0.4
                + skill_match_score * 0.6
            ),
            2
        )

    else:

        final_score = text_match_score

    if final_score >= 80:

        recommendation = (
            "Excellent match! Your resume is strongly "
            "aligned with the job description."
        )

    elif final_score >= 60:

        recommendation = (
            "Good match. Consider adding relevant "
            "skills and keywords from the job description."
        )

    elif final_score >= 40:

        recommendation = (
            "Moderate match. Your resume needs more "
            "relevant skills and job-specific keywords."
        )

    else:

        recommendation = (
            "Low match. Consider tailoring your resume "
            "specifically for this job description."
        )

    return {
        "match_score": final_score,
        "text_match_score": text_match_score,
        "skill_match_score": skill_match_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }