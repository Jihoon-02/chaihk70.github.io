from pathlib import Path
import zipfile

from docx import Document
from pypdf import PdfReader


docx_path = Path(r"E:\3D\chaihk70.github.io\output\docx\Choi_Jihoon_Resume_CoverLetter.docx")
pdf_path = Path(r"E:\3D\chaihk70.github.io\output\pdf\Choi_Jihoon_Resume_CoverLetter.pdf")

doc = Document(docx_path)
docx_text = " ".join(p.text for p in doc.paragraphs)
docx_text += " " + " ".join(cell.text for table in doc.tables for row in table.rows for cell in row.cells)
page_breaks = len(doc._element.xpath('.//w:br[@w:type="page"]'))
hyperlinks = len(doc._element.xpath(".//w:hyperlink"))
with zipfile.ZipFile(docx_path) as archive:
    zip_test = archive.testzip()
    embedded_media = [name for name in archive.namelist() if name.startswith("word/media/")]

reader = PdfReader(pdf_path)
pdf_text = " ".join(page.extract_text() or "" for page in reader.pages)
pdf_links = []
for page in reader.pages:
    for annot_ref in page.get("/Annots") or []:
        annot = annot_ref.get_object()
        if annot.get("/Subtype") == "/Link":
            uri = (annot.get("/A") or {}).get("/URI")
            if uri:
                pdf_links.append(uri)

keys = [
    "팀 프로젝트와 UE5 에셋 제작 경험",
    "구매 에셋 활용 및 컨버팅",
    "현직자 15명",
    "게임의 세계를 설득력 있게 만드는 3D 배경 아티스트",
]

print({
    "docx_bytes": docx_path.stat().st_size,
    "docx_paragraphs": len(doc.paragraphs),
    "docx_tables": len(doc.tables),
    "docx_page_breaks": page_breaks,
    "docx_hyperlinks": hyperlinks,
    "docx_embedded_media": embedded_media,
    "docx_zip_test": zip_test,
    "pdf_bytes": pdf_path.stat().st_size,
    "pdf_pages": len(reader.pages),
    "pdf_links": pdf_links,
    "docx_keys": {key: key in docx_text for key in keys},
    "pdf_keys": {key: key in pdf_text for key in keys},
})
