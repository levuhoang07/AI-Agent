"""
PPTX Helper Utility: Programmatic slide generation, template inspection, and visual QA metrics for PowerPoint.
"""

import os
from typing import List, Dict, Any, Optional
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation(
    output_path: str,
    title: str,
    subtitle: str,
    author: str,
    slides_data: List[Dict[str, Any]],
    template_path: Optional[str] = None
) -> str:
    """
    Builds a professional 16:9 PowerPoint presentation.
    """
    if template_path and os.path.exists(template_path):
        prs = Presentation(template_path)
    else:
        prs = Presentation()
        # Set 16:9 Widescreen dimensions
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1]
    
    # ----------------- Slide 1: Title Slide -----------------
    title_slide = prs.slides.add_slide(blank_layout)
    
    # Title Textbox
    tb = title_slide.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.33), Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Calibri"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(31, 78, 121) # Professional Navy
    p.alignment = PP_ALIGN.LEFT
    
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = Pt(22)
    p2.font.italic = True
    p2.font.color.rgb = RGBColor(89, 89, 89)
    p2.alignment = PP_ALIGN.LEFT
    
    # Presenter info
    tb_meta = title_slide.shapes.add_textbox(Inches(1.5), Inches(5.2), Inches(10.33), Inches(1.0))
    tf_meta = tb_meta.text_frame
    p_meta = tf_meta.paragraphs[0]
    p_meta.text = f"Báo cáo giải pháp: {author} | Antigravity AI Workspace"
    p_meta.font.size = Pt(14)
    p_meta.font.color.rgb = RGBColor(128, 128, 128)
    
    # ----------------- Subsequent Content Slides -----------------
    for s_info in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        
        # Slide Header Banner
        header_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.33), Inches(1.0))
        tf_h = header_box.text_frame
        p_h = tf_h.paragraphs[0]
        p_h.text = s_info.get("slide_title", "")
        p_h.font.name = "Calibri"
        p_h.font.size = Pt(28)
        p_h.font.bold = True
        p_h.font.color.rgb = RGBColor(31, 78, 121)
        
        # Content layout
        content_items = s_info.get("bullets", [])
        content_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(4.8))
        tf_c = content_box.text_frame
        tf_c.word_wrap = True
        
        for idx, item in enumerate(content_items):
            p_item = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
            p_item.text = f"• {item}"
            p_item.font.size = Pt(16)
            p_item.font.name = "Calibri"
            p_item.font.color.rgb = RGBColor(38, 38, 38)
            p_item.space_after = Pt(14)
            p_item.line_spacing = 1.2
            
        # Optional 2-Column or Table
        if "table" in s_info:
            tbl_data = s_info["table"]
            headers = tbl_data.get("headers", [])
            rows = tbl_data.get("rows", [])
            
            table_shape = slide.shapes.add_table(
                rows=len(rows) + 1,
                cols=len(headers),
                left=Inches(1.0),
                top=Inches(4.2),
                width=Inches(11.33),
                height=Inches(2.2)
            )
            table = table_shape.table
            for c_idx, h in enumerate(headers):
                cell = table.cell(0, c_idx)
                cell.text = h
                for p in cell.text_frame.paragraphs:
                    p.font.bold = True
                    p.font.size = Pt(13)
                    p.font.color.rgb = RGBColor(255, 255, 255)
                    
            for r_idx, row in enumerate(rows):
                for c_idx, val in enumerate(row):
                    cell = table.cell(r_idx + 1, c_idx)
                    cell.text = str(val)
                    for p in cell.text_frame.paragraphs:
                        p.font.size = Pt(12)
                        
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs.save(output_path)
    return output_path

def inspect_pptx(filepath: str) -> Dict[str, Any]:
    """
    Audits a PPTX file, checks slide count, layout preservation, shape density, and text overflow risks.
    """
    if not os.path.exists(filepath):
        return {"valid": False, "error": "File does not exist"}
        
    prs = Presentation(filepath)
    slide_count = len(prs.slides)
    slides_audit = []
    
    total_shapes = 0
    overflow_warnings = []
    
    for s_idx, slide in enumerate(prs.slides):
        shapes_in_slide = len(slide.shapes)
        total_shapes += shapes_in_slide
        slide_title = ""
        shape_texts = []
        
        for shape in slide.shapes:
            if shape.has_text_frame:
                txt = shape.text_frame.text.strip()
                if txt:
                    shape_texts.append(txt)
                    if not slide_title:
                        slide_title = txt.split("\n")[0][:40]
                    # Check text overflow hazard (> 600 characters in a single shape)
                    if len(txt) > 600:
                        overflow_warnings.append({
                            "slide": s_idx + 1,
                            "character_count": len(txt),
                            "preview": txt[:60] + "..."
                        })
                        
        slides_audit.append({
            "slide_index": s_idx + 1,
            "title": slide_title,
            "shapes_count": shapes_in_slide,
            "text_blocks_count": len(shape_texts)
        })
        
    return {
        "valid": True,
        "slide_count": slide_count,
        "total_shapes": total_shapes,
        "slides": slides_audit,
        "overflow_warnings_count": len(overflow_warnings),
        "overflow_warnings": overflow_warnings,
        "is_widescreen": abs(prs.slide_width.inches - 13.333) < 0.1
    }
