"""
Word Document Generator for Exchange Listing Proposals
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from datetime import datetime
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ListingProposalGenerator:
    """Generate professional Word documents for exchange listing proposals"""
    
    def __init__(self):
        self.output_dir = "outputs/proposals"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_proposal(self, analysis_id: str, proposal_data: Dict[str, Any]) -> str:
        """
        Generate a professional exchange listing proposal as a Word document
        
        Args:
            analysis_id: Unique identifier for this analysis
            proposal_data: Complete proposal data from exchange preparation agent
            
        Returns:
            Path to generated .docx file
        """
        try:
            logger.info(f"📄 Generating exchange listing proposal for {analysis_id}")
            
            # Create document
            doc = Document()
            
            # Set document margins
            sections = doc.sections
            for section in sections:
                section.top_margin = Inches(1)
                section.bottom_margin = Inches(1)
                section.left_margin = Inches(1)
                section.right_margin = Inches(1)
            
            # Add title
            self._add_title(doc, proposal_data)
            
            # Add executive summary
            self._add_executive_summary(doc, proposal_data)
            
            # Add token overview
            self._add_token_overview(doc, proposal_data)
            
            # Add metrics section
            self._add_metrics_section(doc, proposal_data)
            
            # Add readiness assessment
            self._add_readiness_assessment(doc, proposal_data)
            
            # Add compliance checklist
            self._add_compliance_checklist(doc, proposal_data)
            
            # Add market potential
            self._add_market_section(doc, proposal_data)
            
            # Add contact information
            self._add_contact_section(doc, proposal_data)
            
            # Save document
            filename = f"listing_proposal_{analysis_id[:8]}.docx"
            filepath = os.path.join(self.output_dir, filename)
            doc.save(filepath)
            
            logger.info(f"✅ Proposal generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Error generating proposal: {e}", exc_info=True)
            return None
    
    def _add_title(self, doc: Document, data: Dict[str, Any]):
        """Add document title and header"""
        # Main title
        title = doc.add_heading('Exchange Listing Proposal', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Token name
        token_title = doc.add_heading(f'{data.get("token_name", "Unknown")} ({data.get("token_symbol", "N/A")})', 1)
        token_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Date
        date_para = doc.add_paragraph()
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        date_run = date_para.add_run(f'Generated: {datetime.utcnow().strftime("%B %d, %Y")}')
        date_run.font.size = Pt(10)
        date_run.font.color.rgb = RGBColor(128, 128, 128)
        
        doc.add_paragraph()  # Spacing
    
    def _add_executive_summary(self, doc: Document, data: Dict[str, Any]):
        """Add executive summary section"""
        doc.add_heading('Executive Summary', 1)
        
        # Grade badge
        grade = data.get("readiness_score", {}).get("grade", "N/A")
        score = data.get("readiness_score", {}).get("total", 0)
        compliance = data.get("compliance_rate", 0)
        
        summary_para = doc.add_paragraph()
        summary_para.add_run(f'Listing Readiness Grade: ').bold = True
        grade_run = summary_para.add_run(f'{grade} ({score:.1f}/100)')
        grade_run.font.size = Pt(14)
        grade_run.font.color.rgb = RGBColor(0, 102, 204)
        grade_run.bold = True
        
        compliance_para = doc.add_paragraph()
        compliance_para.add_run(f'Exchange Requirements Met: ').bold = True
        compliance_run = compliance_para.add_run(f'{compliance:.1f}%')
        compliance_run.font.color.rgb = RGBColor(34, 139, 34) if compliance >= 70 else RGBColor(204, 51, 0)
        compliance_run.bold = True
        
        # UVP
        uvp = data.get("unique_value_proposition", "")
        if uvp:
            doc.add_paragraph()
            uvp_heading = doc.add_paragraph()
            uvp_heading.add_run('Unique Value Proposition').bold = True
            doc.add_paragraph(uvp, style='Intense Quote')
        
        doc.add_page_break()
    
    def _add_token_overview(self, doc: Document, data: Dict[str, Any]):
        """Add token overview section"""
        doc.add_heading('1. Token Overview', 1)
        
        # Basic info table
        table = doc.add_table(rows=5, cols=2)
        table.style = 'Light Grid Accent 1'
        
        # Headers
        cells = table.rows[0].cells
        cells[0].text = 'Property'
        cells[1].text = 'Value'
        self._set_cell_bold(cells[0])
        self._set_cell_bold(cells[1])
        
        # Data
        table.rows[1].cells[0].text = 'Token Name'
        table.rows[1].cells[1].text = data.get("token_name", "N/A")
        
        table.rows[2].cells[0].text = 'Symbol'
        table.rows[2].cells[1].text = data.get("token_symbol", "N/A")
        
        table.rows[3].cells[0].text = 'Blockchain'
        table.rows[3].cells[1].text = 'Cardano'
        
        table.rows[4].cells[0].text = 'Policy ID'
        policy_text = data.get("policy_id", "N/A")
        if len(policy_text) > 50:
            policy_text = f"{policy_text[:25]}...{policy_text[-15:]}"
        table.rows[4].cells[1].text = policy_text
        
        # Description
        doc.add_paragraph()
        desc_heading = doc.add_paragraph()
        desc_heading.add_run('Description').bold = True
        doc.add_paragraph(data.get("description", "No description available"))
        
        # Social links
        social = data.get("social_links", {})
        if any(social.values()):
            doc.add_paragraph()
            social_heading = doc.add_paragraph()
            social_heading.add_run('Official Links').bold = True
            
            link_list = []
            if data.get("website") and data.get("website") != "N/A":
                link_list.append(f'Website: {data.get("website")}')
            if social.get("twitter") and social.get("twitter") != "N/A":
                link_list.append(f'Twitter: {social.get("twitter")}')
            if social.get("telegram") and social.get("telegram") != "N/A":
                link_list.append(f'Telegram: {social.get("telegram")}')
            if social.get("discord") and social.get("discord") != "N/A":
                link_list.append(f'Discord: {social.get("discord")}')
            
            for link in link_list:
                p = doc.add_paragraph(link, style='List Bullet')
        
        doc.add_page_break()
    
    def _add_metrics_section(self, doc: Document, data: Dict[str, Any]):
        """Add key metrics section"""
        doc.add_heading('2. Key Metrics', 1)
        
        metrics = data.get("metrics", {})
        
        # Create metrics table
        table = doc.add_table(rows=6, cols=2)
        table.style = 'Light Grid Accent 1'
        
        # Headers
        cells = table.rows[0].cells
        cells[0].text = 'Metric'
        cells[1].text = 'Value'
        self._set_cell_bold(cells[0])
        self._set_cell_bold(cells[1])
        
        # Data
        table.rows[1].cells[0].text = 'Total Supply'
        table.rows[1].cells[1].text = str(metrics.get("total_supply", "N/A"))
        
        table.rows[2].cells[0].text = 'Total Holders'
        table.rows[2].cells[1].text = f'{metrics.get("holders", "N/A"):,}' if isinstance(metrics.get("holders"), int) else str(metrics.get("holders", "N/A"))
        
        table.rows[3].cells[0].text = 'Liquidity (USD)'
        table.rows[3].cells[1].text = str(metrics.get("liquidity", "N/A"))
        
        table.rows[4].cells[0].text = '24h Trading Volume'
        table.rows[4].cells[1].text = str(metrics.get("volume_24h", "N/A"))
        
        table.rows[5].cells[0].text = 'Top 10 Holders Concentration'
        table.rows[5].cells[1].text = str(metrics.get("top_10_concentration", "N/A"))
        
        doc.add_page_break()
    
    def _add_readiness_assessment(self, doc: Document, data: Dict[str, Any]):
        """Add readiness assessment section"""
        doc.add_heading('3. Listing Readiness Assessment', 1)
        
        readiness = data.get("readiness_score", {})
        breakdown = readiness.get("breakdown", {})
        
        # Overall score
        para = doc.add_paragraph()
        para.add_run('Overall Readiness: ').bold = True
        score_run = para.add_run(f'{readiness.get("grade", "N/A")} Grade ({readiness.get("total", 0):.1f}/100)')
        score_run.font.size = Pt(12)
        score_run.font.color.rgb = RGBColor(0, 102, 204)
        
        doc.add_paragraph()
        
        # Score breakdown
        if breakdown:
            doc.add_paragraph('Score Breakdown:', style='Heading 3')
            
            for category, score in breakdown.items():
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(f'{category}: ').bold = True
                score_text = f'{score:.1f}/100'
                score_run = p.add_run(score_text)
                
                # Color code based on score
                if score >= 80:
                    score_run.font.color.rgb = RGBColor(34, 139, 34)  # Green
                elif score >= 60:
                    score_run.font.color.rgb = RGBColor(255, 140, 0)  # Orange
                else:
                    score_run.font.color.rgb = RGBColor(204, 51, 0)  # Red
        
        doc.add_page_break()
    
    def _add_compliance_checklist(self, doc: Document, data: Dict[str, Any]):
        """Add exchange requirements compliance checklist"""
        doc.add_heading('4. Exchange Requirements Compliance', 1)
        
        requirements = data.get("requirements", [])
        
        if not requirements:
            doc.add_paragraph("No specific requirements data available.")
            return
        
        # Group by exchange
        exchanges = {}
        for req in requirements:
            exchange = req.get("exchange", "Unknown")
            if exchange not in exchanges:
                exchanges[exchange] = []
            exchanges[exchange].append(req)
        
        # Add each exchange's requirements
        for exchange, reqs in exchanges.items():
            doc.add_paragraph(f'{exchange} Requirements:', style='Heading 3')
            
            for req in reqs:
                p = doc.add_paragraph(style='List Bullet')
                
                # Checkbox
                checkbox = '☑' if req.get("meets_requirement") else '☐'
                p.add_run(f'{checkbox} ').bold = True
                
                # Requirement text
                p.add_run(req.get("requirement", "N/A"))
                
                # Status
                status_text = f' ({req.get("current_status", "N/A")})'
                status_run = p.add_run(status_text)
                status_run.font.size = Pt(9)
                status_run.font.color.rgb = RGBColor(128, 128, 128)
            
            doc.add_paragraph()  # Spacing between exchanges
        
        doc.add_page_break()
    
    def _add_market_section(self, doc: Document, data: Dict[str, Any]):
        """Add market potential section"""
        doc.add_heading('5. Market Potential & Growth Strategy', 1)
        
        market_potential = data.get("market_potential", "")
        if market_potential:
            doc.add_paragraph(market_potential)
        
        # Recommended exchanges
        recommended = data.get("recommended_exchanges", [])
        if recommended:
            doc.add_paragraph()
            doc.add_paragraph('Recommended Target Exchanges:', style='Heading 3')
            for exchange in recommended:
                doc.add_paragraph(exchange, style='List Bullet')
        
        doc.add_page_break()
    
    def _add_contact_section(self, doc: Document, data: Dict[str, Any]):
        """Add contact information section"""
        doc.add_heading('6. Contact Information', 1)
        
        doc.add_paragraph('For additional information or questions regarding this listing proposal, please contact:')
        doc.add_paragraph()
        
        # Contact table
        table = doc.add_table(rows=3, cols=2)
        table.style = 'Light List Accent 1'
        
        table.rows[0].cells[0].text = 'Project Website'
        table.rows[0].cells[1].text = data.get("website", "N/A")
        
        social = data.get("social_links", {})
        table.rows[1].cells[0].text = 'Twitter'
        table.rows[1].cells[1].text = social.get("twitter", "N/A")
        
        table.rows[2].cells[0].text = 'Telegram'
        table.rows[2].cells[1].text = social.get("telegram", "N/A")
        
        # Footer
        doc.add_paragraph()
        footer = doc.add_paragraph()
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer_run = footer.add_run('This document was generated by Cross-Chain Navigator AI')
        footer_run.font.size = Pt(8)
        footer_run.font.color.rgb = RGBColor(128, 128, 128)
    
    def _set_cell_bold(self, cell):
        """Make cell text bold"""
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
