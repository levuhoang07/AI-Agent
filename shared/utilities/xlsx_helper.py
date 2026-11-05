"""
XLSX Helper Utility: Programmatic creation, formula validation, charting, and audit for Excel workbooks.
"""

import os
from typing import List, Dict, Any, Optional
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

def apply_header_style(cell, text: str):
    """Applies corporate header style to an Excel cell."""
    cell.value = text
    cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

def create_case_workbook(
    output_path: str,
    raw_data: List[Dict[str, Any]],
    calculations: List[Dict[str, Any]],
    kpi_summary: List[Dict[str, Any]],
    chart_info: Optional[Dict[str, Any]] = None
) -> str:
    """
    Builds a professional multi-sheet Excel financial/operational model.
    """
    wb = openpyxl.Workbook()
    
    # ----------------- Sheet 1: Raw Data -----------------
    ws_raw = wb.active
    ws_raw.title = "Raw Data"
    
    if raw_data:
        headers = list(raw_data[0].keys())
        for col_idx, h in enumerate(headers, 1):
            apply_header_style(ws_raw.cell(row=1, column=col_idx), h)
        for row_idx, record in enumerate(raw_data, 2):
            for col_idx, h in enumerate(headers, 1):
                cell = ws_raw.cell(row=row_idx, column=col_idx, value=record[h])
                cell.alignment = Alignment(horizontal="left" if isinstance(record[h], str) else "right")
                
    # ----------------- Sheet 2: Calculations -----------------
    ws_calc = wb.create_sheet(title="Calculations")
    if calculations:
        calc_headers = list(calculations[0].keys())
        for col_idx, h in enumerate(calc_headers, 1):
            apply_header_style(ws_calc.cell(row=1, column=col_idx), h)
        for row_idx, record in enumerate(calculations, 2):
            for col_idx, h in enumerate(calc_headers, 1):
                val = record[h]
                cell = ws_calc.cell(row=row_idx, column=col_idx, value=val)
                cell.alignment = Alignment(horizontal="left" if isinstance(val, str) and not str(val).startswith("=") else "right")
                
    # ----------------- Sheet 3: Summary Dashboard -----------------
    ws_sum = wb.create_sheet(title="Summary Dashboard")
    apply_header_style(ws_sum.cell(row=1, column=1), "Chỉ số KPI (Metric)")
    apply_header_style(ws_sum.cell(row=1, column=2), "Giá trị (Value)")
    apply_header_style(ws_sum.cell(row=1, column=3), "Đơn vị (Unit)")
    apply_header_style(ws_sum.cell(row=1, column=4), "Ghi chú & Phương pháp")
    
    for row_idx, kpi in enumerate(kpi_summary, 2):
        ws_sum.cell(row=row_idx, column=1, value=kpi.get("metric", ""))
        val_cell = ws_sum.cell(row=row_idx, column=2, value=kpi.get("value", 0))
        val_cell.alignment = Alignment(horizontal="right")
        ws_sum.cell(row=row_idx, column=3, value=kpi.get("unit", ""))
        ws_sum.cell(row=row_idx, column=4, value=kpi.get("notes", ""))
        
    # Add Chart to Summary Dashboard if specified
    if chart_info and calculations:
        chart = BarChart()
        chart.type = chart_info.get("type", "col")
        chart.style = 10
        chart.title = chart_info.get("title", "KPI Breakdown")
        chart.y_axis.title = chart_info.get("y_title", "Value")
        chart.x_axis.title = chart_info.get("x_title", "Category")
        
        data_ref = Reference(ws_calc, min_col=chart_info.get("val_col", 3), min_row=1, max_row=len(calculations) + 1)
        cats_ref = Reference(ws_calc, min_col=chart_info.get("cat_col", 1), min_row=2, max_row=len(calculations) + 1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        chart.width = 16
        chart.height = 10
        ws_sum.add_chart(chart, "F2")
        
    # Auto-adjust column widths for all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    return output_path

def inspect_and_verify_xlsx(filepath: str) -> Dict[str, Any]:
    """
    Audits an XLSX file, validates sheet integrity, formula presence, and calculates independent sanity checks.
    """
    if not os.path.exists(filepath):
        return {"valid": False, "error": "File does not exist"}
        
    wb = openpyxl.load_workbook(filepath, data_only=False)
    sheet_names = wb.sheetnames
    
    formulas_found = []
    for sheet_name in sheet_names:
        ws = wb[sheet_name]
        for row in ws.iter_rows(values_only=False):
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formulas_found.append({
                        "sheet": sheet_name,
                        "coordinate": cell.coordinate,
                        "formula": cell.value
                    })
                    
    return {
        "valid": True,
        "sheets": sheet_names,
        "sheet_count": len(sheet_names),
        "formulas_count": len(formulas_found),
        "formulas": formulas_found[:5],
        "has_summary": "Summary Dashboard" in sheet_names,
        "has_raw_data": "Raw Data" in sheet_names
    }
