from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        self.blockchain_blue = colors.HexColor('#0ea5e9')
        self.blockchain_purple = colors.HexColor('#8b5cf6')
        self.blockchain_teal = colors.HexColor('#14b8a6')
        self.success_color = colors.HexColor('#10b981')
        self.warning_color = colors.HexColor('#f59e0b')
        self.danger_color = colors.HexColor('#ef4444')
        self.dark_bg = colors.HexColor('#1e293b')
        self.card_bg = colors.HexColor('#f1f5f9')
        self.dark_text = colors.HexColor('#0f172a')
        self.border_color = colors.HexColor('#cbd5e1')
    
    def _create_header_footer(self, canvas_obj, doc):
        canvas_obj.saveState()
        canvas_obj.setFillColor(self.dark_bg)
        canvas_obj.rect(0, letter[1] - 0.4*inch, letter[0], 0.4*inch, fill=1, stroke=0)
        canvas_obj.setFillColor(colors.white)
        canvas_obj.setFont('Helvetica-Bold', 13)
        canvas_obj.drawString(0.6*inch, letter[1] - 0.26*inch, "⛓️ Cardano Cross-Chain Navigator")
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.HexColor('#94a3b8'))
        canvas_obj.drawRightString(letter[0] - 0.6*inch, letter[1] - 0.26*inch, 
                                   datetime.now().strftime('%b %d, %Y'))
        canvas_obj.setStrokeColor(self.blockchain_teal)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(0, letter[1] - 0.4*inch, letter[0], letter[1] - 0.4*inch)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(0.6*inch, 0.5*inch, letter[0] - 0.6*inch, 0.5*inch)
        canvas_obj.setFillColor(self.dark_text)
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.drawRightString(letter[0] - 0.6*inch, 0.35*inch, f"Page {doc.page}")
        canvas_obj.restoreState()
    
    def _create_score_badge(self, score: float, grade: str) -> Table:
        if grade in ['A', 'A+']:
            bg_color = self.success_color
        elif grade == 'B':
            bg_color = self.blockchain_blue
        elif grade == 'C':
            bg_color = self.warning_color
        else:
            bg_color = self.danger_color
        
        score_style = ParagraphStyle('ScoreStyle', fontSize=28, textColor=colors.white, alignment=TA_CENTER, leading=30)
        grade_style = ParagraphStyle('GradeStyle', fontSize=12, textColor=colors.white, alignment=TA_CENTER, leading=14)
        
        table_data = [
            [Paragraph(f"<b>{score:.0f}</b>", score_style)],
            [Paragraph(f"Grade {grade}", grade_style)]
        ]
        
        table = Table(table_data, colWidths=[1.3*inch], rowHeights=[0.65*inch, 0.35*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table
    
    def _create_info_card(self, title: str, content: str, icon: str = "📊") -> Table:
        title_style = ParagraphStyle('CardTitle', fontSize=10, textColor=self.dark_text, fontName='Helvetica-Bold', leading=12)
        content_style = ParagraphStyle('CardContent', fontSize=9, textColor=self.dark_text, leading=11)
        
        table_data = [
            [Paragraph(f"{icon} <b>{title}</b>", title_style)],
            [Paragraph(content, content_style)]
        ]
        
        table = Table(table_data, colWidths=[6.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.card_bg),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (0, 0), 10),
            ('TOPPADDING', (0, 1), (0, 1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 1.5, self.blockchain_teal),
            ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ]))
        return table
    
    async def generate_analysis_report(self, analysis_id: str, data: dict) -> str:
        filename = f"analysis_{analysis_id[:8]}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch, leftMargin=0.6*inch, rightMargin=0.6*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('ModernTitle', parent=styles['Heading1'], fontSize=24, textColor=self.blockchain_blue, spaceAfter=6, alignment=TA_LEFT, fontName='Helvetica-Bold')
        subtitle_style = ParagraphStyle('Subtitle', fontSize=11, textColor=colors.HexColor('#64748b'), spaceAfter=18, alignment=TA_LEFT)
        section_style = ParagraphStyle('SectionHeader', fontSize=14, textColor=self.blockchain_purple, spaceAfter=10, spaceBefore=16, fontName='Helvetica-Bold')
        body_style = ParagraphStyle('ModernBody', fontSize=9, textColor=self.dark_text, spaceAfter=8, alignment=TA_JUSTIFY, leading=12)
        
        story = []
        
        token_name = data.get('token_name', 'N/A')
        token_symbol = data.get('token_symbol', 'N/A')
        policy_id = data.get('policy_id', 'N/A')
        
        story.append(Paragraph(f"⛓️ {token_name} Analysis", title_style))
        story.append(Paragraph(f"{token_symbol} • ID: {analysis_id[:8]}", subtitle_style))
        
        info_table_data = [
            ['Policy ID', f"{policy_id[:32]}...{policy_id[-12:]}"],
            ['Generated', datetime.now().strftime('%B %d, %Y • %I:%M %p')],
            ['Network', 'Cardano Mainnet']
        ]
        
        info_table = Table(info_table_data, colWidths=[1.3*inch, 5.2*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.card_bg),
            ('TEXTCOLOR', (0, 0), (0, -1), self.dark_text),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, self.border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, self.border_color),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.25*inch))
        
        readiness_score = data.get('readiness_score', {})
        if readiness_score:
            total_score = readiness_score.get('total_score', 0)
            grade = readiness_score.get('grade', 'N/A')
            
            header_table = Table([[
                Paragraph("📊 Readiness Score", section_style),
                self._create_score_badge(total_score, grade)
            ]], colWidths=[5*inch, 1.5*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.15*inch))
        
        summary_text = data.get('executive_summary', 'No summary available.')
        story.append(self._create_info_card('Executive Summary', summary_text, '💼'))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("🏦 Exchange Requirements", section_style))
        
        requirements = data.get('exchange_requirements', [])
        if requirements:
            grouped = {}
            for req in requirements:
                exchange = req.get('exchange', 'Unknown')
                if exchange not in grouped:
                    grouped[exchange] = []
                grouped[exchange].append(req)
            
            for exchange, reqs in grouped.items():
                story.append(Spacer(1, 0.1*inch))
                
                exchange_header_style = ParagraphStyle('ExchangeHeader', fontSize=11, textColor=colors.white, fontName='Helvetica-Bold', leading=14)
                header_table = Table([[Paragraph(f"🔗 {exchange}", exchange_header_style)]], colWidths=[6.5*inch])
                header_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), self.blockchain_purple),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('ROUNDEDCORNERS', [6, 6, 0, 0]),
                ]))
                story.append(header_table)
                
                table_data = []
                for req in reqs:
                    requirement = req.get('requirement', 'N/A')
                    current_status = req.get('current_status', 'N/A')
                    meets = req.get('meets_requirement', False)
                    
                    status_color = self.success_color if meets else self.danger_color
                    status_icon = '✓' if meets else '✗'
                    
                    status_cell = Table([[Paragraph(status_icon, ParagraphStyle('center', alignment=TA_CENTER, fontSize=12, textColor=colors.white))]], 
                                      colWidths=[0.4*inch], rowHeights=[0.35*inch])
                    status_cell.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), status_color),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
                    ]))
                    
                    req_style = ParagraphStyle('ReqStyle', fontSize=9, textColor=self.dark_text, leading=11)
                    table_data.append([status_cell, Paragraph(f"<b>{requirement}</b>", req_style), Paragraph(current_status, req_style)])
                
                col_widths = [0.5*inch, 2.9*inch, 3.1*inch]
                req_table = Table(table_data, colWidths=col_widths)
                req_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('BOX', (0, 0), (-1, -1), 1, self.border_color),
                    ('INNERGRID', (0, 0), (-1, -1), 0.5, self.border_color),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.card_bg]),
                    ('ROUNDEDCORNERS', [0, 0, 6, 6]),
                ]))
                story.append(req_table)
                story.append(Spacer(1, 0.12*inch))
        
        story.append(PageBreak())
        
        story.append(Paragraph("💡 Recommendations", section_style))
        recommendations = data.get('recommendations', [])
        if recommendations:
            rec_data = []
            for i, rec in enumerate(recommendations, 1):
                rec_text = rec.get('recommendation', str(rec)) if isinstance(rec, dict) else str(rec)
                priority = rec.get('priority', 'medium') if isinstance(rec, dict) else 'medium'
                
                if priority == 'high':
                    badge_color = self.danger_color
                    badge_text = 'HIGH'
                elif priority == 'medium':
                    badge_color = self.warning_color
                    badge_text = 'MED'
                else:
                    badge_color = colors.HexColor('#6b7280')
                    badge_text = 'LOW'
                
                badge = Table([[Paragraph(badge_text, ParagraphStyle('badge', fontSize=7, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER))]],
                            colWidths=[0.45*inch], rowHeights=[0.22*inch])
                badge.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), badge_color),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROUNDEDCORNERS', [4, 4, 4, 4]),
                ]))
                
                rec_style = ParagraphStyle('RecStyle', fontSize=9, textColor=self.dark_text, leading=11)
                rec_data.append([badge, Paragraph(rec_text, rec_style)])
            
            rec_table = Table(rec_data, colWidths=[0.6*inch, 5.9*inch])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1.5, self.blockchain_teal),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, self.border_color),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.card_bg]),
                ('ROUNDEDCORNERS', [6, 6, 6, 6]),
            ]))
            story.append(rec_table)
        else:
            story.append(self._create_info_card('Status', 'No specific recommendations at this time.', '✅'))
        
        story.append(Spacer(1, 0.18*inch))
        
        story.append(Paragraph("🎯 Next Steps", section_style))
        next_steps = data.get('next_steps', [])
        if next_steps:
            steps_data = []
            for i, step in enumerate(next_steps, 1):
                clean_step = str(step).replace('[HIGH]', '').replace('[MEDIUM]', '').replace('[EXCHANGE]', '').strip()
                
                num_style = ParagraphStyle('NumStyle', fontSize=10, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER)
                num_cell = Table([[Paragraph(str(i), num_style)]], colWidths=[0.35*inch], rowHeights=[0.35*inch])
                num_cell.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), self.blockchain_blue),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROUNDEDCORNERS', [20, 20, 20, 20]),
                ]))
                
                step_style = ParagraphStyle('StepStyle', fontSize=9, textColor=self.dark_text, leading=11)
                steps_data.append([num_cell, Paragraph(clean_step, step_style)])
            
            steps_table = Table(steps_data, colWidths=[0.5*inch, 6*inch])
            steps_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1.5, self.blockchain_teal),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, self.border_color),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.card_bg]),
                ('ROUNDEDCORNERS', [6, 6, 6, 6]),
            ]))
            story.append(steps_table)
        else:
            story.append(self._create_info_card('Status', 'No specific next steps identified.', '✅'))
        
        doc.build(story, onFirstPage=self._create_header_footer, onLaterPages=self._create_header_footer)
        return filepath
