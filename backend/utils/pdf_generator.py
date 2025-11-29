"""
PDF Generator - Creates professional exchange listing proposals
Uses ReportLab for PDF generation
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Dict, Any, List, Optional
import os

class PDFGenerator:
    def __init__(self):
        self.output_dir = "outputs/pdfs"
        os.makedirs(self.output_dir, exist_ok=True)
    
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
        
    async def generate_proposal(
        self,
        analysis_id: str,
        proposal_data: Dict[str, Any],
        token_analysis: Dict[str, Any],
        exchange_requirements: List[Any],
        recommendations: List[Any]
    ) -> Optional[str]:
        """Generate exchange listing proposal PDF"""
        try:
            filename = f"proposal_{analysis_id}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for content
            story = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title Page
            story.append(Spacer(1, 2 * inch))
            story.append(Paragraph(
                "Exchange Listing Proposal",
                title_style
            ))
            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph(
                f"<b>{proposal_data['token_name']} ({proposal_data['token_symbol']})</b>",
                ParagraphStyle('TokenName', parent=styles['Normal'], fontSize=18, alignment=TA_CENTER)
            ))
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph(
                f"Generated: {datetime.utcnow().strftime('%B %d, %Y')}",
                ParagraphStyle('Date', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.grey)
            ))
            story.append(Spacer(1, 0.5 * inch))
            
            # Readiness Score Box
            score_data = [
                ["Listing Readiness Score", f"{proposal_data['readiness_score']['total']}/100"],
                ["Grade", proposal_data['readiness_score']['grade']],
                ["Compliance Rate", f"{proposal_data['compliance_rate']}%"]
            ]
            score_table = Table(score_data, colWidths=[3 * inch, 2 * inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
            ]))
            story.append(score_table)
            
            story.append(PageBreak())
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", heading_style))
            story.append(Paragraph(proposal_data['description'], styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))
            
            # Token Information
            story.append(Paragraph("Token Information", heading_style))
            info_data = [
                ["Token Name", proposal_data['token_name']],
                ["Symbol", proposal_data['token_symbol']],
                ["Policy ID", proposal_data['policy_id'][:40] + "..."],
                ["Website", proposal_data['website']],
                ["Total Supply", proposal_data['metrics']['total_supply']],
            ]
            info_table = Table(info_data, colWidths=[2 * inch, 4 * inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e9ecef')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Market Metrics
            story.append(Paragraph("Market Metrics", heading_style))
            metrics_data = [
                ["Metric", "Value"],
                ["Holder Count", proposal_data['metrics']['holders']],
                ["Total Liquidity", proposal_data['metrics']['liquidity']],
                ["24h Volume", proposal_data['metrics']['volume_24h']],
                ["Top 10 Concentration", proposal_data['metrics']['top_10_concentration']],
            ]
            metrics_table = Table(metrics_data, colWidths=[3 * inch, 3 * inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#495057')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Score Breakdown
            story.append(Paragraph("Readiness Score Breakdown", heading_style))
            breakdown = proposal_data['readiness_score']['breakdown']
            score_breakdown_data = [["Category", "Score"]]
            for category, score in breakdown.items():
                score_breakdown_data.append([category, f"{score:.1f}/100"])
            
            breakdown_table = Table(score_breakdown_data, colWidths=[3 * inch, 2 * inch])
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#495057')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(breakdown_table)
            story.append(Spacer(1, 0.3 * inch))
            
            # Unique Value Proposition
            story.append(Paragraph("Unique Value Proposition", heading_style))
            story.append(Paragraph(proposal_data['unique_value_proposition'], styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Market Potential
            story.append(Paragraph("Market Potential", heading_style))
            story.append(Paragraph(proposal_data['market_potential'], styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))
            
            story.append(PageBreak())
            
            # Exchange Requirements
            story.append(Paragraph("Exchange Requirements Analysis", heading_style))
            if exchange_requirements:
                # Group by exchange
                exchanges = {}
                for req in exchange_requirements:
                    if req.exchange not in exchanges:
                        exchanges[req.exchange] = []
                    exchanges[req.exchange].append(req)
                
                for exchange, reqs in exchanges.items():
                    story.append(Paragraph(f"<b>{exchange}</b>", styles['Heading3']))
                    req_data = [["Requirement", "Status", "✓"]]
                    for req in reqs:
                        status_symbol = "✓" if req.meets_requirement else "✗"
                        req_data.append([
                            req.requirement,
                            req.current_status,
                            status_symbol
                        ])
                    
                    req_table = Table(req_data, colWidths=[2.5 * inch, 2.5 * inch, 0.5 * inch])
                    req_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c757d')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                    ]))
                    story.append(req_table)
                    story.append(Spacer(1, 0.2 * inch))
            
            # Recommendations with actionable links
            if recommendations:
                story.append(PageBreak())
                story.append(Paragraph("Improvement Recommendations", heading_style))
                story.append(Paragraph(
                    "Click on the blue links below for guides and resources to help you improve your token metrics.",
                    ParagraphStyle('Intro', parent=styles['Normal'], fontSize=10, textColor=colors.grey, spaceAfter=12)
                ))
                
                for i, rec in enumerate(recommendations, 1):
                    priority_color = {
                        "high": colors.red,
                        "medium": colors.orange,
                        "low": colors.green
                    }.get(rec.priority, colors.grey)
                    
                    story.append(Paragraph(
                        f"<b>{i}. [{rec.priority.upper()}] {rec.category}</b>",
                        ParagraphStyle('RecTitle', parent=styles['Normal'], fontSize=11, textColor=priority_color, spaceAfter=6)
                    ))
                    story.append(Paragraph(f"<b>Issue:</b> {rec.issue}", styles['Normal']))
                    story.append(Paragraph(f"<b>Recommendation:</b> {rec.recommendation}", styles['Normal']))
                    story.append(Paragraph(f"<b>Estimated Impact:</b> {rec.estimated_impact}", styles['Normal']))
                    
                    # Add resource links based on category
                    resource_link = self._get_resource_link(rec.category)
                    if resource_link:
                        story.append(Paragraph(
                            f'<b>→ Resources:</b> <link href="{resource_link["url"]}" color="blue"><u>{resource_link["text"]}</u></link>',
                            ParagraphStyle('Link', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#0066cc'), leftIndent=20)
                        ))
                    
                    story.append(Spacer(1, 0.2 * inch))
            
            # Helpful Resources Section
            story.append(PageBreak())
            story.append(Paragraph("Helpful Resources", heading_style))
            
            resources = [
                ("Cardano Developer Portal", "https://developers.cardano.org", "Official Cardano development resources"),
                ("Blockfrost API Docs", "https://docs.blockfrost.io", "On-chain data and analytics"),
                ("Binance Listing Guide", "https://www.binance.com/en/support/faq/115003827011", "Binance listing requirements"),
                ("KuCoin Listing Process", "https://www.kucoin.com/news/en-digital-asset-listing", "KuCoin application guide"),
                ("Cardano DEX Aggregator", "https://app.minswap.org", "Minswap for liquidity provision"),
                ("Token Holder Analytics", "https://cardanoscan.io", "Analyze holder distribution"),
                ("Cross-Chain Bridge Guide", "https://docs.wanchain.org", "Wanchain bridge documentation"),
            ]
            
            for title, url, desc in resources:
                story.append(Paragraph(
                    f'<b>•</b> <link href="{url}" color="blue"><u>{title}</u></link> - {desc}',
                    ParagraphStyle('Resource', parent=styles['Normal'], fontSize=10, leftIndent=10, spaceAfter=8)
                ))
            
            story.append(Spacer(1, 0.5 * inch))
            
            # Footer
            story.append(Spacer(1, 1 * inch))
            story.append(Paragraph(
                "This analysis is provided for informational purposes only and does not guarantee exchange listing approval.",
                ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
            ))
            story.append(Paragraph(
                f"Generated by Cross-Chain Navigator Agent | {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
                ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
            ))
            
            # Build PDF
            doc.build(story)
            
            return f"/api/pdfs/{filename}"
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None
