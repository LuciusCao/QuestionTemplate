from docx import Document


class Templizer:
    def __init__(self, docx_path):
        self.doc = Document(docx_path)
