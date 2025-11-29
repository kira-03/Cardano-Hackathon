"""
PDF Generator - Creates professional exchange listing proposals
Uses ReportLab for PDF generation
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from datetime import datetime
from typing import Dict, Any, List, Optional
import os
import io

# Professional color palette
COLORS = {
    'primary': colors.HexColor('#0F172A'),       # Slate 900
    'secondary': colors.HexColor('#1E293B'),     # Slate 800
    'accent': colors.HexColor('#3B82F6'),        # Blue 500
    'accent_light': colors.HexColor('#DBEAFE'),  # Blue 100
    'success': colors.HexColor('#10B981'),       # Emerald 500
    'warning': colors.HexColor('#F59E0B'),       # Amber 500
    'danger': colors.HexColor('#EF4444'),        # Red 500
    'muted': colors.HexColor('#64748B'),         # Slate 500
    'light': colors.HexColor('#F8FAFC'),         # Slate 50
    'border': colors.HexColor('#E2E8F0'),        # Slate 200
    'cardano': colors.HexColor('#0033AD'),       # Cardano Blue
}

class PDFGenerator:
    def __init__(self):
        self.output_dir = "outputs/pdfs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _get_grade_color(self, grade: str) -> colors.Color:
        """Get color based on grade"""
        grade_colors = {
            'A': COLORS['success'],
            'B': colors.HexColor('#22C55E'),
            'C': COLORS['warning'],
            'D': colors.HexColor('#F97316'),
            'F': COLORS['danger']
        }
        return grade_colors.get(grade, COLORS['muted'])
    
    def _get_priority_color(self, priority: str) -> colors.Color:
        """Get color based on priority"""
        return {
            'high': COLORS['danger'],
            'medium': COLORS['warning'],
            'low': COLORS['success']
        }.get(priority.lower(), COLORS['muted'])
    
    def _create_score_gauge(self, score: float, size: int = 120) -> Drawing:
        """Create a circular score gauge"""
        d = Drawing(size, size)
        center = size / 2
        radius = size / 2 - 10
        
        # Background circle
        d.add(Circle(center, center, radius, fillColor=COLORS['light'], strokeColor=COLORS['border'], strokeWidth=2))
        
        # Score arc would require more complex drawing - simplified to text
        d.add(String(center, center + 5, f"{score:.0f}", fontSize=24, fontName='Helvetica-Bold', fillColor=COLORS['primary'], textAnchor='middle'))
        d.add(String(center, center - 15, "/ 100", fontSize=10, fontName='Helvetica', fillColor=COLORS['muted'], textAnchor='middle'))
        
        return d
    
    def _get_resource_link(self, category: str) -> Optional[Dict[str, str]]:
        """Get helpful resource links based on recommendation category"""
        resources = {
            "Liquidity": {
                "url": "https://app.minswap.org/liquidity",
                "text": "Add Liquidity on Minswap DEX"
            },
            "Holder Distribution": {
                "url": "https://docs.cardano.org/native-tokens/learn",
                "text": "Cardano Token Distribution Guide"
            },
            "Metadata": {
                "url": "https://developers.cardano.org/docs/native-tokens/token-registry",
                "text": "Cardano Token Registry Standards"
            },
            "Marketing": {
                "url": "https://twitter.com/CardanoStiftung",
                "text": "Cardano Community Engagement"
            },
            "Security": {
                "url": "https://docs.cardano.org/plutus/learn-about-plutus",
                "text": "Smart Contract Security Best Practices"
            },
            "Volume": {
                "url": "https://cardanoscan.io",
                "text": "Track Trading Activity on CardanoScan"
            }
        }
        return resources.get(category)
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create professional paragraph styles"""
        base_styles = getSampleStyleSheet()
        
        return {
            'title': ParagraphStyle(
                'Title',
                parent=base_styles['Heading1'],
                fontSize=32,
                textColor=COLORS['primary'],
                spaceAfter=8,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                leading=38
            ),
            'subtitle': ParagraphStyle(
                'Subtitle',
                parent=base_styles['Normal'],
                fontSize=14,
                textColor=COLORS['muted'],
                spaceAfter=24,
                alignment=TA_CENTER,
                fontName='Helvetica'
            ),
            'section_heading': ParagraphStyle(
                'SectionHeading',
                parent=base_styles['Heading2'],
                fontSize=16,
                textColor=COLORS['primary'],
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold',
                borderPadding=0
            ),
            'subsection': ParagraphStyle(
                'Subsection',
                parent=base_styles['Heading3'],
                fontSize=12,
                textColor=COLORS['secondary'],
                spaceAfter=8,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            ),
            'body': ParagraphStyle(
                'Body',
                parent=base_styles['Normal'],
                fontSize=10,
                textColor=COLORS['secondary'],
                spaceAfter=8,
                leading=14,
                alignment=TA_JUSTIFY
            ),
            'body_small': ParagraphStyle(
                'BodySmall',
                parent=base_styles['Normal'],
                fontSize=9,
                textColor=COLORS['muted'],
                spaceAfter=6,
                leading=12
            ),
            'label': ParagraphStyle(
                'Label',
                parent=base_styles['Normal'],
                fontSize=8,
                textColor=COLORS['muted'],
                fontName='Helvetica-Bold',
                spaceAfter=2
            ),
            'value': ParagraphStyle(
                'Value',
                parent=base_styles['Normal'],
                fontSize=11,
                textColor=COLORS['primary'],
                fontName='Helvetica-Bold'
            ),
            'grade_large': ParagraphStyle(
                'GradeLarge',
                parent=base_styles['Normal'],
                fontSize=48,
                textColor=COLORS['success'],
                fontName='Helvetica-Bold',
                alignment=TA_CENTER
            ),
            'footer': ParagraphStyle(
                'Footer',
                parent=base_styles['Normal'],
                fontSize=8,
                textColor=COLORS['muted'],
                alignment=TA_CENTER
            ),
            'link': ParagraphStyle(
                'Link',
                parent=base_styles['Normal'],
                fontSize=9,
                textColor=COLORS['accent'],
                spaceAfter=4
            ),
            'normal': base_styles['Normal']
        }
        
    async def generate_proposal(
        self,
        analysis_id: str,
        proposal_data: Dict[str, Any],
        token_analysis: Dict[str, Any],
        exchange_requirements: List[Any],
        recommendations: List[Any]
    ) -> Optional[str]:
        """Generate exchange listing proposal PDF - Legacy method"""
        # Call the new method with adapted data
        return await self.generate_analysis_report(analysis_id, proposal_data)
    
    async def generate_analysis_report(
        self,
        analysis_id: str,
        analysis_data: Dict[str, Any]
    ) -> Optional[str]:
        """Generate professional analysis report PDF"""
        try:
            filename = f"analysis_{analysis_id}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF document with professional margins
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=40
            )
            
            story = []
            styles = self._create_styles()
            
            # ============ COVER PAGE ============
            story.append(Spacer(1, 1.5 * inch))
            
            # Logo placeholder - brand header
            story.append(Paragraph(
                "CROSS-CHAIN NAVIGATOR",
                ParagraphStyle('Brand', parent=styles['normal'], fontSize=10, textColor=COLORS['accent'], 
                              alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=8, letterSpacing=3)
            ))
            
            story.append(Paragraph("Token Analysis Report", styles['title']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Token name and symbol
            token_name = analysis_data.get('token_name', 'Unknown Token')
            token_symbol = analysis_data.get('token_symbol', '???')
            story.append(Paragraph(
                f"<b>{token_name}</b> ({token_symbol})",
                ParagraphStyle('TokenName', parent=styles['normal'], fontSize=20, textColor=COLORS['primary'], 
                              alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
            ))
            
            # Policy ID
            policy_id = analysis_data.get('policy_id', '')
            story.append(Paragraph(
                f"{policy_id[:24]}...{policy_id[-8:]}" if len(policy_id) > 32 else policy_id,
                ParagraphStyle('PolicyID', parent=styles['normal'], fontSize=9, textColor=COLORS['muted'], 
                              alignment=TA_CENTER, fontName='Courier', spaceAfter=30)
            ))
            
            # Date
            story.append(Paragraph(
                f"Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}",
                styles['subtitle']
            ))
            
            story.append(Spacer(1, 0.5 * inch))
            
            # Score Card Box
            readiness_score = analysis_data.get('readiness_score', {})
            total_score = readiness_score.get('total_score', 0)
            grade = readiness_score.get('grade', 'N/A')
            grade_color = self._get_grade_color(grade)
            
            score_box_data = [
                [
                    Paragraph(f"<font size='48' color='{grade_color.hexval()}'><b>{grade}</b></font>", 
                             ParagraphStyle('Grade', alignment=TA_CENTER)),
                    Paragraph(f"<font size='14' color='#0F172A'><b>Listing Readiness Score</b></font><br/>"
                             f"<font size='32' color='#0F172A'><b>{total_score:.0f}</b></font>"
                             f"<font size='14' color='#64748B'>/100</font>",
                             ParagraphStyle('Score', alignment=TA_CENTER, leading=20))
                ]
            ]
            
            score_table = Table(score_box_data, colWidths=[2.5 * inch, 3.5 * inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), COLORS['light']),
                ('BOX', (0, 0), (-1, -1), 1, COLORS['border']),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TOPPADDING', (0, 0), (-1, -1), 20),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ]))
            story.append(score_table)
            
            story.append(PageBreak())
            
            # ============ EXECUTIVE SUMMARY ============
            story.append(Paragraph("Executive Summary", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            executive_summary = analysis_data.get('executive_summary', 'No summary available.')
            story.append(Paragraph(executive_summary, styles['body']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Next Steps
            next_steps = analysis_data.get('next_steps', [])
            if next_steps:
                story.append(Paragraph("Priority Action Items", styles['subsection']))
                for i, step in enumerate(next_steps[:5], 1):
                    story.append(Paragraph(
                        f"<b>{i}.</b> {step}",
                        ParagraphStyle('Step', parent=styles['body'], leftIndent=15, spaceAfter=6)
                    ))
            
            story.append(Spacer(1, 0.3 * inch))
            
            # ============ TOKEN METRICS ============
            story.append(Paragraph("Token Metrics", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            metrics = analysis_data.get('metrics', {})
            
            # Format helper
            def format_number(val):
                if val is None:
                    return "N/A"
                if isinstance(val, (int, float)):
                    if val >= 1_000_000:
                        return f"${val/1_000_000:.2f}M"
                    elif val >= 1_000:
                        return f"${val/1_000:.2f}K"
                    return f"${val:.2f}"
                return str(val)
            
            def format_percent(val):
                if val is None:
                    return "N/A"
                return f"{val:.1f}%"
            
            # Use simple key-value pairs instead of complex table
            metrics_items = [
                ("Total Supply", metrics.get('total_supply', 'N/A')),
                ("Circulating Supply", metrics.get('circulating_supply', 'N/A')),
                ("Holder Count", str(metrics.get('holder_count', 'N/A'))),
                ("Top 10% Concentration", format_percent(metrics.get('top_10_concentration'))),
                ("Top 50% Concentration", format_percent(metrics.get('top_50_concentration'))),
                ("Liquidity (USD)", format_number(metrics.get('liquidity_usd'))),
                ("24h Volume", format_number(metrics.get('volume_24h'))),
                ("Metadata Score", format_percent(metrics.get('metadata_score', 0) * 100 if metrics.get('metadata_score') else None)),
            ]
            
            # Create two-column layout manually
            for i in range(0, len(metrics_items), 2):
                row_data = []
                
                # Left column
                left_item = metrics_items[i]
                row_data.extend([
                    Paragraph(f"<b>{left_item[0]}:</b>", 
                             ParagraphStyle('MetricLabel', parent=styles['normal'], fontSize=9, 
                                          textColor=COLORS['muted'], fontName='Helvetica-Bold')),
                    Paragraph(str(left_item[1]), 
                             ParagraphStyle('MetricValue', parent=styles['normal'], fontSize=9, 
                                          textColor=COLORS['secondary']))
                ])
                
                # Right column (if exists)
                if i + 1 < len(metrics_items):
                    right_item = metrics_items[i + 1]
                    row_data.extend([
                        Paragraph(f"<b>{right_item[0]}:</b>", 
                                 ParagraphStyle('MetricLabel', parent=styles['normal'], fontSize=9, 
                                              textColor=COLORS['muted'], fontName='Helvetica-Bold')),
                        Paragraph(str(right_item[1]), 
                                 ParagraphStyle('MetricValue', parent=styles['normal'], fontSize=9, 
                                              textColor=COLORS['secondary']))
                    ])
                else:
                    row_data.extend(["", ""])
                
                # Create table for this row
                row_table = Table([row_data], colWidths=[1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch])
                row_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(row_table)
            
            story.append(Spacer(1, 0.3 * inch))
            
            # ============ SCORE BREAKDOWN ============
            story.append(Paragraph("Readiness Score Breakdown", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            score_categories = [
                ('liquidity_score', 'Liquidity'),
                ('holder_distribution_score', 'Holder Distribution'),
                ('metadata_score', 'Metadata Quality'),
                ('security_score', 'Security'),
                ('supply_stability_score', 'Supply Stability'),
                ('market_activity_score', 'Market Activity')
            ]
            
            # Simple list format instead of complex table
            for key, label in score_categories:
                score_val = readiness_score.get(key, 0)
                if score_val >= 80:
                    rating = "Excellent"
                    rating_color = COLORS['success']
                elif score_val >= 60:
                    rating = "Good"
                    rating_color = colors.HexColor('#22C55E')
                elif score_val >= 40:
                    rating = "Fair"
                    rating_color = COLORS['warning']
                else:
                    rating = "Needs Work"
                    rating_color = COLORS['danger']
                
                # Create a simple row for each score
                score_row = Table([[
                    Paragraph(f"<b>{label}</b>", 
                             ParagraphStyle('ScoreLabel', parent=styles['normal'], fontSize=10, 
                                          textColor=COLORS['secondary'], fontName='Helvetica-Bold')),
                    Paragraph(f"<b>{score_val:.0f}</b>/100", 
                             ParagraphStyle('ScoreValue', parent=styles['normal'], fontSize=10, 
                                          textColor=COLORS['primary'], alignment=TA_CENTER)),
                    Paragraph(f"<font color='{rating_color.hexval()}'><b>{rating}</b></font>", 
                             ParagraphStyle('ScoreRating', parent=styles['normal'], fontSize=10, 
                                          textColor=rating_color))
                ]], colWidths=[2.5 * inch, 1.5 * inch, 1.8 * inch])
                
                score_row.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (0, 0), (-1, -1), COLORS['light'] if score_categories.index((key, label)) % 2 else colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.5, COLORS['border']),
                ]))
                story.append(score_row)
            
            story.append(PageBreak())
            
            # ============ EXCHANGE REQUIREMENTS ============
            exchange_reqs = analysis_data.get('exchange_requirements', [])
            if exchange_reqs:
                story.append(Paragraph("Exchange Requirements Analysis", styles['section_heading']))
                story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
                
                # Group by exchange
                exchanges = {}
                for req in exchange_reqs:
                    exchange_name = req.get('exchange', req.exchange if hasattr(req, 'exchange') else 'Unknown')
                    if exchange_name not in exchanges:
                        exchanges[exchange_name] = []
                    exchanges[exchange_name].append(req)
                
                for exchange_name, reqs in exchanges.items():
                    met_count = sum(1 for r in reqs if (r.get('meets_requirement') if isinstance(r, dict) else r.meets_requirement))
                    total_count = len(reqs)
                    
                    story.append(Paragraph(
                        f"<b>{exchange_name}</b> — {met_count}/{total_count} requirements met",
                        ParagraphStyle('ExchangeTitle', parent=styles['subsection'], textColor=COLORS['primary'], spaceAfter=8)
                    ))
                    
                    # List format instead of table for requirements
                    for req in reqs:
                        requirement = req.get('requirement', '') if isinstance(req, dict) else req.requirement
                        status = req.get('current_status', '') if isinstance(req, dict) else req.current_status
                        meets = req.get('meets_requirement', False) if isinstance(req, dict) else req.meets_requirement
                        
                        check_mark = "✓" if meets else "✗"
                        check_color = COLORS['success'] if meets else COLORS['danger']
                        
                        story.append(Paragraph(
                            f"<font color='{check_color.hexval()}'><b>{check_mark}</b></font> "
                            f"<b>{requirement}:</b> {status}",
                            ParagraphStyle('ReqItem', parent=styles['body'], fontSize=9, leftIndent=10, spaceAfter=4)
                        ))
                    
                    story.append(Spacer(1, 0.15 * inch))
            
            # ============ RECOMMENDATIONS ============
            recommendations = analysis_data.get('recommendations', [])
            if recommendations:
                story.append(PageBreak())
                story.append(Paragraph("Improvement Recommendations", styles['section_heading']))
                story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
                
                story.append(Paragraph(
                    "The following recommendations are prioritized to help improve your token's exchange listing readiness.",
                    styles['body_small']
                ))
                story.append(Spacer(1, 0.15 * inch))
                
                for i, rec in enumerate(recommendations[:8], 1):
                    category = rec.get('category', '') if isinstance(rec, dict) else rec.category
                    priority = rec.get('priority', 'medium') if isinstance(rec, dict) else rec.priority
                    issue = rec.get('issue', '') if isinstance(rec, dict) else rec.issue
                    recommendation = rec.get('recommendation', '') if isinstance(rec, dict) else rec.recommendation
                    impact = rec.get('estimated_impact', '') if isinstance(rec, dict) else rec.estimated_impact
                    
                    priority_color = self._get_priority_color(priority)
                    
                    # Recommendation header
                    story.append(Paragraph(
                        f"<font color='{priority_color.hexval()}'><b>[{priority.upper()}]</b></font> "
                        f"<b>{i}. {category}</b>",
                        ParagraphStyle('RecHeader', parent=styles['subsection'], spaceAfter=4)
                    ))
                    
                    # Issue and recommendation
                    story.append(Paragraph(f"<b>Issue:</b> {issue}", styles['body']))
                    story.append(Paragraph(f"<b>Action:</b> {recommendation}", styles['body']))
                    story.append(Paragraph(f"<b>Expected Impact:</b> {impact}", styles['body_small']))
                    
                    # Resource link
                    resource = self._get_resource_link(category)
                    if resource:
                        story.append(Paragraph(
                            f'<link href="{resource["url"]}" color="{COLORS["accent"].hexval()}"><u>{resource["text"]}</u></link>',
                            styles['link']
                        ))
                    
                    story.append(Spacer(1, 0.15 * inch))
            
            # ============ BRIDGE ROUTES ============
            bridge_routes = analysis_data.get('bridge_routes', [])
            if bridge_routes:
                story.append(PageBreak())
                story.append(Paragraph("Cross-Chain Bridge Routes", styles['section_heading']))
                story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
                
                recommended_chain = analysis_data.get('recommended_chain', '')
                if recommended_chain:
                    story.append(Paragraph(
                        f"<b>Recommended Target Chain:</b> {recommended_chain}",
                        ParagraphStyle('Recommended', parent=styles['body'], textColor=COLORS['accent'], spaceAfter=12)
                    ))
                
                # Simple list format for bridge routes
                for i, route in enumerate(bridge_routes[:5], 1):
                    source = route.get('source_chain', '') if isinstance(route, dict) else route.source_chain
                    target = route.get('target_chain', '') if isinstance(route, dict) else route.target_chain
                    bridge = route.get('bridge_name', '') if isinstance(route, dict) else route.bridge_name
                    fee = route.get('estimated_fee', '') if isinstance(route, dict) else route.estimated_fee
                    time = route.get('estimated_time', '') if isinstance(route, dict) else route.estimated_time
                    trust = route.get('trust_model', '') if isinstance(route, dict) else route.trust_model
                    score = route.get('recommendation_score', 0) if isinstance(route, dict) else route.recommendation_score
                    
                    # Determine score color
                    if score >= 80:
                        score_color = COLORS['success']
                    elif score >= 60:
                        score_color = COLORS['warning']
                    else:
                        score_color = COLORS['danger']
                    
                    story.append(Paragraph(
                        f"<b>{i}. {source} → {target}</b>",
                        ParagraphStyle('RouteTitle', parent=styles['subsection'], fontSize=11, spaceAfter=4)
                    ))
                    
                    route_details = [
                        f"Bridge: {bridge}",
                        f"Fee: {fee}",
                        f"Time: {time}",
                        f"Trust Model: {trust.capitalize()}",
                        f"Score: <font color='{score_color.hexval()}'><b>{score:.0f}%</b></font>"
                    ]
                    
                    for detail in route_details:
                        story.append(Paragraph(
                            f"• {detail}",
                            ParagraphStyle('RouteDetail', parent=styles['body'], fontSize=9, 
                                         leftIndent=15, spaceAfter=2)
                        ))
                    
                    story.append(Spacer(1, 0.1 * inch))
            
            # ============ RESOURCES ============
            story.append(PageBreak())
            story.append(Paragraph("Helpful Resources", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            resources_list = [
                ("Cardano Developer Portal", "https://developers.cardano.org", "Official development documentation"),
                ("Blockfrost API", "https://docs.blockfrost.io", "On-chain data and analytics APIs"),
                ("Minswap DEX", "https://app.minswap.org", "Add liquidity and trade tokens"),
                ("CardanoScan", "https://cardanoscan.io", "Block explorer and analytics"),
                ("Binance Listing", "https://www.binance.com/en/support/faq/115003827011", "Binance listing requirements"),
                ("KuCoin Listing", "https://www.kucoin.com/news/en-digital-asset-listing", "KuCoin application process"),
            ]
            
            for title, url, desc in resources_list:
                story.append(Paragraph(
                    f'• <link href="{url}" color="{COLORS["accent"].hexval()}"><b><u>{title}</u></b></link> — {desc}',
                    ParagraphStyle('ResourceItem', parent=styles['body'], leftIndent=10, spaceAfter=6)
                ))
            
            # ============ FOOTER ============
            story.append(Spacer(1, 0.5 * inch))
            story.append(HRFlowable(width="100%", thickness=0.5, color=COLORS['border'], spaceAfter=12))
            
            story.append(Paragraph(
                "This report is generated for informational purposes only and does not constitute financial advice or guarantee exchange listing approval.",
                ParagraphStyle('Disclaimer', parent=styles['footer'], textColor=COLORS['muted'], spaceAfter=8)
            ))
            story.append(Paragraph(
                f"Cross-Chain Navigator Agent • Analysis ID: {analysis_id} • {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
                styles['footer']
            ))
            
            # Build PDF
            doc.build(story)
            
            return filepath
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    async def generate_mm_rfp(self, content: Dict[str, Any]) -> str:
        """
        Generate Market Maker RFP PDF
        """
        try:
            filename = f"mm_rfp_{content['project_name'].replace(' ', '_')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=40
            )
            
            story = []
            styles = self._create_styles()
            
            # Title
            story.append(Spacer(1, 0.5 * inch))
            story.append(Paragraph("Market Maker Request for Proposal", styles['title']))
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(
                f"{content['project_name']} ({content['token_symbol']})",
                styles['subtitle']
            ))
            story.append(Spacer(1, 0.3 * inch))
            
            # Project Overview
            story.append(Paragraph("Project Overview", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            overview_items = [
                ("Project Name", content['project_name']),
                ("Token Symbol", content['token_symbol']),
                ("Blockchain", "Cardano"),
                ("Contact", content.get('contact', 'See below'))
            ]
            
            for label, value in overview_items:
                story.append(Paragraph(f"<b>{label}:</b> {value}", styles['body']))
            
            story.append(Spacer(1, 0.2 * inch))
            
            # Requirements
            story.append(Paragraph("Market Making Requirements", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            requirements = content.get('requirements', {})
            req_items = [
                ("Minimum Liquidity Depth", requirements.get('min_liquidity_depth', 'TBD')),
                ("Target Spread", requirements.get('target_spread', 'TBD')),
                ("Uptime Requirement", requirements.get('uptime_requirement', 'TBD')),
                ("Target Exchanges", ', '.join(requirements.get('exchanges', [])))
            ]
            
            for label, value in req_items:
                story.append(Paragraph(f"<b>{label}:</b> {value}", styles['body']))
            
            story.append(Spacer(1, 0.2 * inch))
            
            # Metrics
            story.append(Paragraph("Current Metrics", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            
            metrics = content.get('metrics', {})
            story.append(Paragraph(
                f"Current readiness score: <b>{metrics.get('readiness_scores', {}).get('total_score', 'N/A')}/100</b>",
                styles['body']
            ))
            
            story.append(Spacer(1, 0.3 * inch))
            
            # Contact
            story.append(Paragraph("Contact Information", styles['section_heading']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['border'], spaceAfter=12))
            story.append(Paragraph(f"Email: {content.get('contact', 'contact@example.com')}", styles['body']))
            
            # Footer
            story.append(Spacer(1, 0.5 * inch))
            story.append(HRFlowable(width="100%", thickness=0.5, color=COLORS['border'], spaceAfter=12))
            story.append(Paragraph(
                f"Generated on {datetime.utcnow().strftime('%B %d, %Y')}",
                styles['footer']
            ))
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error generating MM RFP: {e}")
            return ""
