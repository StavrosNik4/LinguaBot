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


def save_multiple_dialogues_to_pdf(dialogues, topics, filename):
    """
    Saves a list of dialogues (each as a string) to a PDF,
    with each dialogue separated by a title/header that includes its topic.

    Parameters:
        dialogues (list of str): List of dialogues (each a multiline string).
        topics (list of str): List of topics (same length as dialogues).
        filename (str): Output PDF file path.
    """
    if len(dialogues) != len(topics):
        raise ValueError("The number of topics must match the number of dialogues.")

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for i, (dialogue, topic) in enumerate(zip(dialogues, topics), 1):
        # Title with dialogue number and topic
        title_text = f"<b>Dialogue {i} - Topic: {topic}</b>"
        title = Paragraph(title_text, styles["Heading2"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Each line of the dialogue
        for line in dialogue.strip().split("\n"):
            if line.strip():  # skip empty lines
                story.append(Paragraph(line.strip(), styles["Normal"]))
                story.append(Spacer(1, 6))

        story.append(Spacer(1, 24))  # Extra space between dialogues

    doc.build(story)
