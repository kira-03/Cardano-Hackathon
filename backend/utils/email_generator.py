"""
Email Generator - Exchange-specific email templates and generation
"""
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class EmailGenerator:
    """
    Generate professional emails for exchange listing applications
    """
    
    def __init__(self):
        self.templates = {
            "binance": self._binance_template,
            "coinbase": self._coinbase_template,
            "kraken": self._kraken_template,
            "kucoin": self._kucoin_template,
            "gateio": self._gateio_template
        }
    
    async def generate_exchange_email(
        self,
        exchange: str,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate email content for specific exchange"""
        
        exchange_lower = exchange.lower()
        template_func = self.templates.get(exchange_lower)
        
        if not template_func:
            logger.warning(f"No template for exchange: {exchange}")
            return self._generic_template(exchange, project_metadata, data_collection, readiness_report)
        
        return template_func(project_metadata, data_collection, readiness_report)
    
    def _binance_template(
        self,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Binance-specific email template"""
        
        holder_count = data_collection.get("holder_distribution", {}).get("total_holders", 0)
        liquidity = data_collection.get("dex_liquidity", {}).get("total_liquidity_usd", 0)
        
        subject = f"Listing Application: {project_metadata.name} ({project_metadata.symbol})"
        
        body_html = f"""
<html>
<body>
<p>Dear Binance Listing Team,</p>

<p>I am writing to submit <strong>{project_metadata.name} ({project_metadata.symbol})</strong> for consideration on the Binance exchange.</p>

<h3>Project Overview</h3>
<p>{project_metadata.name} is a Cardano native token with strong fundamentals and growing community engagement. Our project represents innovation in the Cardano ecosystem with clear utility and value proposition.</p>

<h3>Key Metrics</h3>
<ul>
    <li><strong>Token Holders:</strong> {holder_count:,}</li>
    <li><strong>Liquidity (DEX):</strong> ${liquidity:,.0f} USD</li>
    <li><strong>Blockchain:</strong> Cardano</li>
    <li><strong>Website:</strong> <a href="{project_metadata.website}">{project_metadata.website}</a></li>
</ul>

<h3>Readiness Assessment</h3>
<p>Our internal readiness assessment shows strong alignment with Binance listing criteria. We have prepared comprehensive documentation including technical specifications, tokenomics, and security audits.</p>

<h3>Why Binance?</h3>
<p>Listing on Binance would provide our community with access to world-class trading infrastructure and significantly expand our market reach. We are committed to maintaining the highest standards of transparency and compliance.</p>

<h3>Next Steps</h3>
<p>We have attached our complete listing proposal (PDF) which includes:</p>
<ul>
    <li>Executive Summary</li>
    <li>Detailed Token Metrics</li>
    <li>Holder Distribution Analysis</li>
    <li>Liquidity Snapshot</li>
    <li>Risk Assessment</li>
    <li>Roadmap and Milestones</li>
</ul>

<p>We are available for further discussion and look forward to the opportunity to list {project_metadata.symbol} on Binance.</p>

<p>Best regards,<br>
{project_metadata.contact_email}</p>

<p><em>Note: As per Binance requirements, founder verification documents are available upon request.</em></p>
</body>
</html>
"""
        
        body_text = f"""
Dear Binance Listing Team,

I am writing to submit {project_metadata.name} ({project_metadata.symbol}) for consideration on the Binance exchange.

Project Overview:
{project_metadata.name} is a Cardano native token with strong fundamentals and growing community engagement.

Key Metrics:
- Token Holders: {holder_count:,}
- Liquidity (DEX): ${liquidity:,.0f} USD
- Blockchain: Cardano
- Website: {project_metadata.website}

We have prepared comprehensive documentation and look forward to discussing this opportunity further.

Best regards,
{project_metadata.contact_email}
"""
        
        return {
            "exchange": "Binance",
            "subject": subject,
            "body_html": body_html,
            "body_text": body_text,
            "attachments": ["proposal.pdf"],
            "to": "listing@binance.com",
            "priority": "high"
        }
    
    def _coinbase_template(
        self,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coinbase-specific email template"""
        
        subject = f"Asset Listing Request: {project_metadata.name} ({project_metadata.symbol})"
        
        body_html = f"""
<html>
<body>
<p>Dear Coinbase Asset Listing Team,</p>

<p>We are submitting <strong>{project_metadata.name} ({project_metadata.symbol})</strong> for consideration via the Coinbase Asset Hub.</p>

<h3>Compliance & Legal</h3>
<p>Our token is a utility token on the Cardano blockchain, designed with regulatory compliance in mind. We maintain transparent operations and are committed to meeting all applicable regulatory requirements.</p>

<h3>Digital Asset Framework Assessment</h3>
<p>We have completed a comprehensive self-assessment against the Coinbase Digital Asset Framework, with particular attention to:</p>
<ul>
    <li>Decentralization and governance</li>
    <li>Security and technical implementation</li>
    <li>Market maturity and adoption</li>
    <li>Regulatory compliance posture</li>
</ul>

<h3>Project Information</h3>
<ul>
    <li><strong>Website:</strong> <a href="{project_metadata.website}">{project_metadata.website}</a></li>
    <li><strong>Whitepaper:</strong> <a href="{project_metadata.whitepaper_url or '#'}">Available</a></li>
    <li><strong>GitHub:</strong> <a href="{project_metadata.github_url or '#'}">Open Source</a></li>
</ul>

<p>We look forward to your review and are available for any additional information required.</p>

<p>Sincerely,<br>
{project_metadata.contact_email}</p>
</body>
</html>
"""
        
        body_text = f"""
Dear Coinbase Asset Listing Team,

We are submitting {project_metadata.name} ({project_metadata.symbol}) for consideration via the Coinbase Asset Hub.

Our token is a utility token on Cardano, designed with regulatory compliance in mind.

Project Information:
- Website: {project_metadata.website}
- Whitepaper: {project_metadata.whitepaper_url or 'Available'}
- GitHub: {project_metadata.github_url or 'Open Source'}

We look forward to your review.

Sincerely,
{project_metadata.contact_email}
"""
        
        return {
            "exchange": "Coinbase",
            "subject": subject,
            "body_html": body_html,
            "body_text": body_text,
            "attachments": ["proposal.pdf"],
            "to": "asset-hub@coinbase.com",
            "priority": "high"
        }
    
    def _kraken_template(
        self,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Kraken-specific email template"""
        
        subject = f"Get Listed Application: {project_metadata.name}"
        
        body_html = f"""
<html>
<body>
<p>Dear Kraken Listing Team,</p>

<p>We would like to submit <strong>{project_metadata.name} ({project_metadata.symbol})</strong> for your Get Listed program.</p>

<h3>Security & Compliance</h3>
<p>Security is our top priority. Our smart contracts follow best practices and we maintain rigorous security standards throughout our development process.</p>

<h3>Market Demand</h3>
<p>Our growing community and increasing trading volumes demonstrate strong market demand for {project_metadata.symbol}. We believe Kraken's platform would be an excellent match for our user base.</p>

<p>Website: <a href="{project_metadata.website}">{project_metadata.website}</a></p>

<p>Please find attached our comprehensive listing proposal.</p>

<p>Best regards,<br>
{project_metadata.contact_email}</p>
</body>
</html>
"""
        
        body_text = f"""
Dear Kraken Listing Team,

We would like to submit {project_metadata.name} ({project_metadata.symbol}) for your Get Listed program.

Security is our top priority and our smart contracts follow best practices.

Website: {project_metadata.website}

Please find attached our comprehensive listing proposal.

Best regards,
{project_metadata.contact_email}
"""
        
        return {
            "exchange": "Kraken",
            "subject": subject,
            "body_html": body_html,
            "body_text": body_text,
            "attachments": ["proposal.pdf"],
            "to": "listings@kraken.com",
            "priority": "medium"
        }
    
    def _kucoin_template(
        self,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """KuCoin-specific email template"""
        
        subject = f"Listing Application: {project_metadata.symbol} on KuCoin"
        
        body_html = f"""
<html>
<body>
<p>Dear KuCoin Listing Team,</p>

<p><strong>{project_metadata.name} ({project_metadata.symbol})</strong> is seeking listing on KuCoin exchange.</p>

<h3>Project Innovation</h3>
<p>Our project brings unique value to the Cardano ecosystem with innovative features and strong community support.</p>

<h3>Contact Information</h3>
<ul>
    <li>Website: <a href="{project_metadata.website}">{project_metadata.website}</a></li>
    <li>Email: {project_metadata.contact_email}</li>
</ul>

<p>Full proposal attached. We look forward to partnering with KuCoin.</p>

<p>Thank you,<br>
{project_metadata.name} Team</p>
</body>
</html>
"""
        
        body_text = f"""
Dear KuCoin Listing Team,

{project_metadata.name} ({project_metadata.symbol}) is seeking listing on KuCoin exchange.

Our project brings unique value to the Cardano ecosystem.

Website: {project_metadata.website}
Email: {project_metadata.contact_email}

Full proposal attached.

Thank you,
{project_metadata.name} Team
"""
        
        return {
            "exchange": "KuCoin",
            "subject": subject,
            "body_html": body_html,
            "body_text": body_text,
            "attachments": ["proposal.pdf"],
            "to": "listing@kucoin.com",
            "priority": "medium"
        }
    
    def _gateio_template(
        self,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gate.io-specific email template"""
        
        subject = f"{project_metadata.symbol} Listing Request"
        
        body_html = f"""
<html>
<body>
<p>Dear Gate.io Team,</p>

<p>We request listing for <strong>{project_metadata.name} ({project_metadata.symbol})</strong>.</p>

<p><strong>Project:</strong> {project_metadata.name}<br>
<strong>Symbol:</strong> {project_metadata.symbol}<br>
<strong>Website:</strong> <a href="{project_metadata.website}">{project_metadata.website}</a></p>

<p>Proposal document attached.</p>

<p>Regards,<br>
{project_metadata.contact_email}</p>
</body>
</html>
"""
        
        body_text = f"""
Dear Gate.io Team,

We request listing for {project_metadata.name} ({project_metadata.symbol}).

Project: {project_metadata.name}
Symbol: {project_metadata.symbol}
Website: {project_metadata.website}

Proposal document attached.

Regards,
{project_metadata.contact_email}
"""
        
        return {
            "exchange": "Gate.io",
            "subject": subject,
            "body_html": body_html,
            "body_text": body_text,
            "attachments": ["proposal.pdf"],
            "to": "listing@gate.io",
            "priority": "low"
        }
    
    def _generic_template(
        self,
        exchange: str,
        project_metadata: Any,
        data_collection: Dict[str, Any],
        readiness_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generic exchange email template"""
        
        subject = f"Listing Application: {project_metadata.name}"
        
        body_html = f"""
<html>
<body>
<p>Dear {exchange} Team,</p>

<p>We would like to apply for listing <strong>{project_metadata.name} ({project_metadata.symbol})</strong> on your exchange.</p>

<p>Website: <a href="{project_metadata.website}">{project_metadata.website}</a></p>

<p>Please find our complete proposal attached.</p>

<p>Best regards,<br>
{project_metadata.contact_email}</p>
</body>
</html>
"""
        
        body_text = f"""
Dear {exchange} Team,

We would like to apply for listing {project_metadata.name} ({project_metadata.symbol}) on your exchange.

Website: {project_metadata.website}

Please find our complete proposal attached.

Best regards,
{project_metadata.contact_email}
"""
        
        return {
            "exchange": exchange,
            "subject": subject,
            "body_html": body_html,
            "body_text": body_text,
            "attachments": ["proposal.pdf"],
            "to": f"listing@{exchange.lower()}.com",
            "priority": "medium"
        }
