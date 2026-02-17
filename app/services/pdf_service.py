import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

def generate_report_pdf(report, transactions, output_path=None):
    """
    Generates a professional fintech-grade financial report.
    """
    if output_path is None:
        output_path = f"static/reports/report_{report.id}.pdf"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=styles['Normal'],
        fontSize=48,
        textColor=colors.HexColor("#2563eb"),
        alignment=1,
        fontName="Helvetica-Bold"
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor("#334155"),
        spaceBefore=20,
        spaceAfter=12,
        borderPadding=5,
        borderWidth=0,
        leftIndent=0
    )

    # 1. Header & Score
    elements.append(Paragraph("Financial Health Analysis", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(str(report.risk_score), score_style))
    elements.append(Paragraph("FINANCIAL HEALTH SCORE", ParagraphStyle('Sub', alignment=1, fontSize=10, textColor=colors.grey)))
    elements.append(Spacer(1, 30))

    # 2. Executive Summary
    summary = report.summary_data
    elements.append(Paragraph("Executive Summary", section_header))
    
    data = [
        ["Metric", "Value"],
        ["Total Income", f"${summary.get('total_income', 0):,.2f}"],
        ["Total Expenses", f"${summary.get('total_expense', 0):,.2f}"],
        ["Net Savings", f"${(summary.get('total_income', 0) - summary.get('total_expense', 0)):,.2f}"],
        ["Risk Level", summary.get('risk_level', 'Moderate')]
    ]
    
    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0,0), (1,0), colors.HexColor("#475569")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0"))
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    # 3. Risk Explanation
    elements.append(Paragraph("Risk Assessment", section_header))
    elements.append(Paragraph(summary.get('risk_analysis', "No detailed analysis available."), styles['Normal']))
    elements.append(Spacer(1, 20))

    # 4. Visual Breakdown (Chart)
    elements.append(Paragraph("Spending Category Breakdown", section_header))
    
    cat_data = summary.get('category_breakdown', {})
    if cat_data:
        drawing = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [list(cat_data.values())]
        bc.categoryAxis.categoryNames = list(cat_data.keys())
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(cat_data.values()) * 1.2
        bc.bars[0].fillColor = colors.HexColor("#3b82f6")
        drawing.add(bc)
        elements.append(drawing)

    # 5. AI Recommendations (Simulated logic for now)
    elements.append(PageBreak())
    elements.append(Paragraph("AI Recommendations for Improvement", section_header))
    
    recommendations = []
    if report.risk_score < 50:
        recommendations = [
            "• Immediate Action: Reduce discretionary spending in 'Dining Out' and 'Entertainment' by 50%.",
            "• Debt Strategy: Apply the 'Snowball Method' to clear high-interest debts first.",
            "• Emergency Fund: Aim to save $1,000 as a primary safety net."
        ]
    elif report.risk_score < 80:
        recommendations = [
            "• Optimization: Review recurring 'Utilities' or 'Misc' subscriptions to increase savings rate.",
            "• Investment: Direct 10% of net savings into a diversified index fund.",
            "• Essential Check: Compare grocery spending against local averages to find efficiencies."
        ]
    else:
        recommendations = [
            "• Wealth Building: Maximize contributions to tax-advantaged retirement accounts.",
            "• Portfolio Review: Ensure your asset allocation matches your long-term risk tolerance.",
            "• Estate Planning: Consider formalizing your long-term legacy strategy."
        ]
    
    for rec in recommendations:
        elements.append(Paragraph(rec, styles['Normal']))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    return output_path
