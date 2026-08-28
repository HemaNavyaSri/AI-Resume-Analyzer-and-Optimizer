import re


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

    escaped_skill = re.escape(
        skill.lower()
    )

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


def extract_skills_from_job_description(
    job_description
):

    normalized_text = normalize_text(
        job_description
    )

    found_skills = []

    for skill in SKILLS_DATABASE:

        if skill_exists(
            skill,
            normalized_text
        ):
            found_skills.append(skill)

    return found_skills