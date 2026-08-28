from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
    KeepTogether
)

from xml.sax.saxutils import escape


def format_text(text):
    """
    Converts normal text into PDF-safe text.
    Preserves line breaks.
    """

    if not text:
        return ""

    text = escape(str(text).strip())

    return text.replace("\n", "<br/>")


def create_section_title(title, style):
    """
    Creates a professional section heading
    with a horizontal line below it.
    """

    heading = Paragraph(title, style)

    line = HRFlowable(
        width="100%",
        thickness=0.6,
        color=colors.HexColor("#666666"),
        spaceBefore=1,
        spaceAfter=5
    )

    return [heading, line]


def generate_resume_pdf(resume_data, output_path):

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,

        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,

        title=f"{resume_data.get('name', 'Resume')} Resume",
        author=resume_data.get("name", "")
    )

    styles = getSampleStyleSheet()

    # ------------------------------------------------
    # NAME STYLE
    # ------------------------------------------------

    name_style = ParagraphStyle(
        "ResumeName",

        parent=styles["Normal"],

        fontName="Helvetica-Bold",

        fontSize=16,

        leading=19,

        textColor=colors.HexColor("#1F1F1F"),

        alignment=TA_LEFT,

        spaceAfter=2
    )

    # ------------------------------------------------
    # CONTACT STYLE
    # ------------------------------------------------

    contact_style = ParagraphStyle(
        "ContactStyle",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=8,

        leading=10,

        textColor=colors.HexColor("#333333"),

        alignment=TA_RIGHT
    )

    # ------------------------------------------------
    # LEFT CONTACT STYLE
    # ------------------------------------------------

    left_contact_style = ParagraphStyle(
        "LeftContactStyle",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=8,

        leading=10,

        textColor=colors.HexColor("#333333"),

        alignment=TA_LEFT
    )

    # ------------------------------------------------
    # SECTION HEADING
    # ------------------------------------------------

    section_style = ParagraphStyle(
        "SectionHeading",

        parent=styles["Normal"],

        fontName="Helvetica-Bold",

        fontSize=10,

        leading=12,

        textColor=colors.HexColor("#222222"),

        spaceBefore=7,

        spaceAfter=2
    )

    # ------------------------------------------------
    # BODY STYLE
    # ------------------------------------------------

    body_style = ParagraphStyle(
        "ResumeBody",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=8.5,

        leading=11,

        textColor=colors.HexColor("#222222"),

        spaceAfter=2
    )

    # ------------------------------------------------
    # BOLD PROJECT STYLE
    # ------------------------------------------------

    project_style = ParagraphStyle(
        "ProjectStyle",

        parent=body_style,

        fontSize=8.5,

        leading=11,

        spaceAfter=2
    )

    story = []

    # ================================================
    # NAME + CONTACT
    # ================================================

    name = escape(
        resume_data.get("name", "")
    )

    email = escape(
        resume_data.get("email", "")
    )

    phone = escape(
        resume_data.get("phone", "")
    )

    location = escape(
        resume_data.get("location", "")
    )

    linkedin = escape(
        resume_data.get("linkedin", "")
    )

    github = escape(
        resume_data.get("github", "")
    )

    # Left side: Name + LinkedIn + GitHub

    left_content = []

    if name:
        left_content.append(
            Paragraph(
                name,
                name_style
            )
        )

    if linkedin:
        left_content.append(
            Paragraph(
                f"LinkedIn: {linkedin}",
                left_contact_style
            )
        )

    if github:
        left_content.append(
            Paragraph(
                f"GitHub: {github}",
                left_contact_style
            )
        )

    # Right side: Email + Phone + Location

    right_content = []

    if email:
        right_content.append(
            Paragraph(
                f"Email: {email}",
                contact_style
            )
        )

    if phone:
        right_content.append(
            Paragraph(
                f"Mobile: {phone}",
                contact_style
            )
        )

    if location:
        right_content.append(
            Paragraph(
                location,
                contact_style
            )
        )

    contact_table = Table(
        [
            [
                left_content,
                right_content
            ]
        ],

        colWidths=[
            85 * mm,
            85 * mm
        ]
    )

    contact_table.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                )
            ]
        )
    )

    story.append(contact_table)

    story.append(
        Spacer(
            1,
            4
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.HexColor("#555555"),
            spaceBefore=0,
            spaceAfter=4
        )
    )

    # ================================================
    # SKILLS SUMMARY
    # ================================================

    skills = resume_data.get(
        "skills",
        []
    )

    if skills:

        section = []

        section.extend(
            create_section_title(
                "SKILLS SUMMARY",
                section_style
            )
        )

        skills_text = "  •  ".join(
            escape(str(skill))
            for skill in skills
            if str(skill).strip()
        )

        if skills_text:

            section.append(
                Paragraph(
                    skills_text,
                    body_style
                )
            )

        story.append(
            KeepTogether(section)
        )

    # ================================================
    # PROJECTS
    # ================================================

    projects = resume_data.get(
        "projects",
        ""
    )

    if projects and projects.strip():

        story.extend(
            create_section_title(
                "PROJECTS",
                section_style
            )
        )

        project_lines = [
            line.strip()
            for line in projects.split("\n")
            if line.strip()
        ]

        for line in project_lines:

            # First part before ":" is treated as project name
            if ":" in line:

                project_name, description = line.split(
                    ":",
                    1
                )

                formatted_line = (
                    f"<b>{escape(project_name.strip())}</b>"
                    f": {escape(description.strip())}"
                )

            else:

                formatted_line = (
                    f"• {escape(line)}"
                )

            story.append(
                Paragraph(
                    formatted_line,
                    project_style
                )
            )

    # ================================================
    # EDUCATION
    # ================================================

    education = resume_data.get(
        "education",
        ""
    )

    if education and education.strip():

        story.extend(
            create_section_title(
                "EDUCATION",
                section_style
            )
        )

        education_lines = [
            line.strip()
            for line in education.split("\n")
            if line.strip()
        ]

        for line in education_lines:

            story.append(
                Paragraph(
                    f"• {escape(line)}",
                    body_style
                )
            )

    # ================================================
    # EXPERIENCE / INTERNSHIP
    # ================================================

    experience = resume_data.get(
        "experience",
        ""
    )

    if experience and experience.strip():

        story.extend(
            create_section_title(
                "EXPERIENCE / INTERNSHIP",
                section_style
            )
        )

        experience_lines = [
            line.strip()
            for line in experience.split("\n")
            if line.strip()
        ]

        for line in experience_lines:

            if ":" in line:

                title, description = line.split(
                    ":",
                    1
                )

                formatted_line = (
                    f"<b>{escape(title.strip())}</b>"
                    f": {escape(description.strip())}"
                )

            else:

                formatted_line = (
                    f"• {escape(line)}"
                )

            story.append(
                Paragraph(
                    formatted_line,
                    body_style
                )
            )

    # ================================================
    # CERTIFICATIONS & ACHIEVEMENTS
    # ================================================

    achievements = resume_data.get(
        "achievements",
        ""
    )

    if achievements and achievements.strip():

        story.extend(
            create_section_title(
                "CERTIFICATIONS & ACHIEVEMENTS",
                section_style
            )
        )

        achievement_lines = [
            line.strip()
            for line in achievements.split("\n")
            if line.strip()
        ]

        for line in achievement_lines:

            story.append(
                Paragraph(
                    f"• {escape(line)}",
                    body_style
                )
            )

    # ================================================
    # BUILD PDF
    # ================================================

    document.build(story)