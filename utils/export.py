from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
import re


def _parse_ppt_outline(text: str) -> list[dict]:
    """Extract slide title + bullets from writer output."""
    slides = []
    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Detect slide headings like "Slide 1:", "## Slide 1", "**Slide 1**"
        if re.match(r"^(slide\s*\d+|##|\*\*slide)", line, re.IGNORECASE):
            if current:
                slides.append(current)
            title = re.sub(r"^[#*\s]*(slide\s*\d*:?\s*)?", "", line, flags=re.IGNORECASE).strip("* :")
            current = {"title": title or line, "bullets": []}
        elif current is not None and line.startswith(("-", "•", "*")):
            current["bullets"].append(line.lstrip("-•* "))
        elif current is not None:
            current["bullets"].append(line)
    if current:
        slides.append(current)
    return slides


def export_ppt(writer_text: str, topic: str, output_dir: Path) -> Path:
    prs = Presentation()
    blank_layout = prs.slide_layouts[1]  # title + content

    # Title slide
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = topic
    title_slide.placeholders[1].text = "AI Research Assistant"

    slides = _parse_ppt_outline(writer_text)
    if not slides:
        # Fallback: one slide per paragraph
        for para in writer_text.split("\n\n")[:10]:
            if para.strip():
                slide = prs.slides.add_slide(blank_layout)
                slide.shapes.title.text = para[:60]
                slide.placeholders[1].text = para
    else:
        for s in slides:
            slide = prs.slides.add_slide(blank_layout)
            slide.shapes.title.text = s["title"][:100]
            tf = slide.placeholders[1].text_frame
            tf.text = ""
            for bullet in s["bullets"][:8]:
                p = tf.add_paragraph()
                p.text = bullet[:200]
                p.level = 0

    path = output_dir / f"{topic[:40].replace(' ', '_')}.pptx"
    prs.save(path)
    return path


def export_markdown(content: str, topic: str, output_dir: Path) -> Path:
    path = output_dir / f"{topic[:40].replace(' ', '_')}.md"
    path.write_text(f"# {topic}\n\n{content}", encoding="utf-8")
    return path


def export_docx(content: str, topic: str, output_dir: Path) -> Path:
    from docx import Document
    doc = Document()
    doc.add_heading(topic, 0)
    for para in content.split("\n\n"):
        if para.strip():
            doc.add_paragraph(para.strip())
    path = output_dir / f"{topic[:40].replace(' ', '_')}.docx"
    doc.save(path)
    return path


def export_pdf(content: str, topic: str, output_dir: Path) -> Path:
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, topic[:80], ln=True)
    pdf.set_font("Helvetica", size=11)
    for line in content.splitlines():
        pdf.multi_cell(0, 8, line[:200] if line.strip() else "")
    path = output_dir / f"{topic[:40].replace(' ', '_')}.pdf"
    pdf.output(str(path))
    return path


def export_all(writer_text: str, reviewer_text: str, topic: str, formats: list[str], output_dir: Path) -> dict:
    output_dir.mkdir(exist_ok=True)
    exported = {}
    if "pptx" in formats:
        exported["pptx"] = export_ppt(writer_text, topic, output_dir)
    if "md" in formats:
        exported["md"] = export_markdown(reviewer_text, topic, output_dir)
    if "docx" in formats:
        exported["docx"] = export_docx(reviewer_text, topic, output_dir)
    if "pdf" in formats:
        exported["pdf"] = export_pdf(reviewer_text, topic, output_dir)
    return exported
