import re


def chunk_by_dialogue(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Use regex to extract all content within <dialogue>...</dialogue> tags
    dialogues = re.findall(r'<dialogue>(.*?)</dialogue>', text, re.DOTALL)

    # Clean up and return
    return [dialogue.strip() for dialogue in dialogues if dialogue.strip()]
