"""
QA Validator Utility: Performs Cross-Format Consistency and Quality Gate verifications across DOCX, XLSX, and PPTX.
"""

import os
from typing import Dict, List, Any
from docx_helper import inspect_docx
from xlsx_helper import inspect_and_verify_xlsx
from pptx_helper import inspect_pptx
from docx import Document
import openpyxl
from pptx import Presentation

def cross_validate_deliverables(
    docx_path: str,
    xlsx_path: str,
    pptx_path: str,
    key_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validates cross-format consistency across DOCX, XLSX, and PPTX.
    Verifies that key numbers and terms appear consistently across all three deliverables.
    """
    results = {
        "docx_audit": inspect_docx(docx_path),
        "xlsx_audit": inspect_and_verify_xlsx(xlsx_path),
        "pptx_audit": inspect_pptx(pptx_path),
        "metric_consistency": {},
        "all_formats_valid": False,
        "consistency_score": 0.0
    }
    
    if not (results["docx_audit"].get("valid") and 
            results["xlsx_audit"].get("valid") and 
            results["pptx_audit"].get("valid")):
        results["all_formats_valid"] = False
        return results
        
    results["all_formats_valid"] = True
    
    # Read text from DOCX
    doc = Document(docx_path)
    docx_full_text = " ".join([p.text for p in doc.paragraphs] + [cell.text for t in doc.tables for row in t.rows for cell in row.cells])
    
    # Read text from PPTX
    prs = Presentation(pptx_path)
    pptx_full_text = " ".join([shape.text_frame.text for s in prs.slides for shape in s.shapes if shape.has_text_frame])
    
    # Read text from XLSX
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    xlsx_values = []
    for sheet in wb.sheetnames:
        for row in wb[sheet].iter_rows(values_only=True):
            for v in row:
                if v is not None:
                    xlsx_values.append(str(v))
    xlsx_full_text = " ".join(xlsx_values)
    
    # Check each metric
    matched_count = 0
    total_metrics = len(key_metrics)
    
    for metric_name, expected_val in key_metrics.items():
        val_str = str(expected_val)
        in_docx = val_str in docx_full_text
        in_xlsx = val_str in xlsx_full_text
        in_pptx = val_str in pptx_full_text
        
        is_consistent = in_docx and in_xlsx and in_pptx
        if is_consistent:
            matched_count += 1
            
        results["metric_consistency"][metric_name] = {
            "expected_value": expected_val,
            "in_docx": in_docx,
            "in_xlsx": in_xlsx,
            "in_pptx": in_pptx,
            "consistent": is_consistent
        }
        
    results["consistency_score"] = (matched_count / total_metrics * 100) if total_metrics > 0 else 100.0
    return results

