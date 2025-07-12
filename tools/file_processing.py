import re

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def chunk_by_dialogue(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Use regex to extract all content within <dialogue>...</dialogue> tags
    dialogues = re.findall(r'<dialogue>(.*?)</dialogue>', text, re.DOTALL)

    # Clean up and return
    return [dialogue.strip() for dialogue in dialogues if dialogue.strip()]


# === Save to PDF using ReportLab ===
def save_dialogue_to_pdf(text, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Split dialogue into lines and wrap each line in a Paragraph
    for line in text.strip().split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 6))  # Add space between lines

    doc.build(story)


def save_multiple_dialogues_to_pdf(dialogues, filename):
    """
    Saves a list of dialogues (each as a string) to a PDF,
    with each dialogue separated by a title/header.
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for i, dialogue in enumerate(dialogues, 1):
        # Add a title for each dialogue
        title = Paragraph(f"<b>Dialogue {i}</b>", styles["Heading2"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Add each line of the dialogue as a paragraph
        for line in dialogue.strip().split("\n"):
            if line.strip():  # skip empty lines
                story.append(Paragraph(line.strip(), styles["Normal"]))
                story.append(Spacer(1, 6))

        # Add space between dialogues
        story.append(Spacer(1, 24))

    doc.build(story)
