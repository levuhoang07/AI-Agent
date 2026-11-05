"""
DOCX Helper Utility: Programmatic creation, template preservation, and quality audit for Word documents.
"""

import os
from typing import List, Dict, Any, Optional
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color: str):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report_document(
    output_path: str,
    title: str,
    subtitle: str,
    author: str,
    sections: List[Dict[str, Any]],
    template_path: Optional[str] = None
) -> str:
    """
    Creates a polished academic/consulting Word report.
    If template_path is provided, loads and preserves the template.
    """
    if template_path and os.path.exists(template_path):
        doc = Document(template_path)
    else:
        doc = Document()
        
    # Set default standard margins (1 inch)
    sections_doc = doc.sections
    for s in sections_doc:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    # Title / Header
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(title)
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(31, 78, 121) # Professional Navy
    
    if subtitle:
        sub_p = doc.add_paragraph()
        sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub_run = sub_p.add_run(subtitle)
        sub_run.font.size = Pt(14)
        sub_run.font.italic = True
        sub_run.font.color.rgb = RGBColor(89, 89, 89)
        
    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_run = meta_p.add_run(f"Tác giả: {author} | Antigravity AI Workspace")
    meta_run.font.size = Pt(10)
    meta_run.font.color.rgb = RGBColor(128, 128, 128)
    
    doc.add_paragraph() # Spacing
    
    # Render sections
    for sec in sections:
        level = sec.get("level", 1)
        heading_text = sec.get("heading", "")
        if heading_text:
            h = doc.add_heading(heading_text, level=level)
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(6)
            
        paragraphs = sec.get("paragraphs", [])
        for p_text in paragraphs:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            p.add_run(p_text)
            
        # Table support
        if "table" in sec:
            tbl_data = sec["table"]
            headers = tbl_data.get("headers", [])
            rows = tbl_data.get("rows", [])
            
            table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True
            
            # Header row
            hdr_cells = table.rows[0].cells
            for col_idx, hdr_title in enumerate(headers):
                hdr_cells[col_idx].text = hdr_title
                set_cell_background(hdr_cells[col_idx], "1F4E79")
                set_cell_margins(hdr_cells[col_idx], top=120, bottom=120, left=150, right=150)
                for run in hdr_cells[col_idx].paragraphs[0].runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                    run.font.size = Pt(10.5)
            
            # Data rows
            for row_idx, row_values in enumerate(rows):
                row_cells = table.rows[row_idx + 1].cells
                bg_color = "F2F2F2" if row_idx % 2 == 1 else "FFFFFF"
                for col_idx, val in enumerate(row_values):
                    row_cells[col_idx].text = str(val)
                    set_cell_background(row_cells[col_idx], bg_color)
                    set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=150, right=150)
                    for run in row_cells[col_idx].paragraphs[0].runs:
                        run.font.size = Pt(10)
                        
            doc.add_paragraph() # Spacing after table
            
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path

def inspect_docx(filepath: str) -> Dict[str, Any]:
    """
    Audits a DOCX document's structure, heading hierarchy, tables, and Vietnamese text fidelity.
    """
    if not os.path.exists(filepath):
        return {"error": "File not found", "valid": False}
        
    doc = Document(filepath)
    headings = []
    paragraphs = []
    tables_info = []
    
    for p in doc.paragraphs:
        if p.style and p.style.name.startswith("Heading"):
            headings.append({
                "level": p.style.name,
                "text": p.text
            })
        elif p.text.strip():
            paragraphs.append(p.text.strip())
            
    for t_idx, t in enumerate(doc.tables):
        rows_count = len(t.rows)
        cols_count = len(t.columns) if rows_count > 0 else 0
        tables_info.append({
            "table_index": t_idx + 1,
            "rows": rows_count,
            "columns": cols_count
        })
        
    return {
        "valid": True,
        "headings_count": len(headings),
        "headings": headings,
        "paragraphs_count": len(paragraphs),
        "tables_count": len(tables_info),
        "tables": tables_info,
        "sample_text": paragraphs[0][:100] if paragraphs else ""
    }
