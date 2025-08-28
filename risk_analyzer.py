"""
Legal Contract Risk Analysis Module
"""

import google.generativeai as genai
import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from utils import RateLimiter, logger, usage_tracker

# Load environment variables
load_dotenv()

class ContractRiskAnalyzer:
    """Advanced contract risk analysis using AI and rule-based methods"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the risk analyzer"""
        
        # Configure Gemini API
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(max_requests_per_minute=15)
        
        # Load risk assessment rules
        self.risk_rules = self._load_risk_rules()
        
        logger.info("ContractRiskAnalyzer initialized")
    
    def _load_risk_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load risk assessment rules and patterns"""
        return {
            # Critical risk factors (High impact)
            "missing_liability_cap": {
                "patterns": [r"liability.*limit", r"limitation.*liability", r"cap.*damages"],
                "severity": "HIGH",
                "weight": 0.9,
                "description": "Missing or inadequate liability limitations",
                "recommendation": "Add clear liability limitation clauses to cap financial exposure"
            },
            
            "missing_termination": {
                "patterns": [r"terminat", r"end.*agreement", r"expir", r"cancel"],
                "severity": "HIGH", 
                "weight": 0.8,
                "description": "Missing or unclear termination provisions",
                "recommendation": "Include clear termination procedures and notice requirements"
            },
            
            "missing_governing_law": {
                "patterns": [r"governing.*law", r"governed.*by", r"jurisdiction", r"applicable.*law"],
                "severity": "MEDIUM",
                "weight": 0.7,
                "description": "Missing governing law and jurisdiction clauses",
                "recommendation": "Specify governing law and jurisdiction for dispute resolution"
            },
            
            "missing_confidentiality": {
                "patterns": [r"confidential", r"proprietary", r"non.?disclos", r"trade.*secret"],
                "severity": "MEDIUM",
                "weight": 0.6,
                "description": "Missing confidentiality and non-disclosure provisions",
                "recommendation": "Add confidentiality clauses to protect sensitive information"
            },
            
            # Payment and financial risks
            "vague_payment_terms": {
                "patterns": [r"\$[\d,]+", r"payment.*schedule", r"compensation", r"fee"],
                "severity": "MEDIUM",
                "weight": 0.5,
                "description": "Vague or missing payment terms",
                "recommendation": "Specify clear payment amounts, schedules, and procedures"
            },
            
            "missing_late_fees": {
                "patterns": [r"late.*fee", r"interest.*overdue", r"penalty.*late"],
                "severity": "LOW",
                "weight": 0.3,
                "description": "Missing late payment penalties",
                "recommendation": "Consider adding late payment fees and interest charges"
            },
            
            # Intellectual property risks
            "missing_ip_clauses": {
                "patterns": [r"intellectual.*property", r"copyright", r"trademark", r"patent", r"work.*product"],
                "severity": "MEDIUM",
                "weight": 0.6,
                "description": "Missing intellectual property provisions",
                "recommendation": "Clarify ownership and rights to intellectual property created"
            },
            
            # Force majeure and unforeseen events
            "missing_force_majeure": {
                "patterns": [r"force.*majeure", r"act.*god", r"unforeseeable", r"beyond.*control"],
                "severity": "LOW",
                "weight": 0.4,
                "description": "Missing force majeure provisions",
                "recommendation": "Consider adding force majeure clauses for unforeseen circumstances"
            },
            
            # Amendment and modification
            "missing_amendment_clause": {
                "patterns": [r"amendment", r"modif", r"chang.*agreement", r"written.*consent"],
                "severity": "LOW",
                "weight": 0.3,
                "description": "Missing amendment and modification procedures",
                "recommendation": "Specify how the agreement can be amended or modified"
            },
            
            # Severability
            "missing_severability": {
                "patterns": [r"severab", r"invalid.*provision", r"unenforceable"],
                "severity": "LOW",
                "weight": 0.2,
                "description": "Missing severability clause",
                "recommendation": "Add severability clause to preserve agreement if one provision is invalid"
            }
        }
    
    def analyze_contract_comprehensive(self, contract_text: str) -> Dict[str, Any]:
        """Perform comprehensive AI-powered risk analysis"""
        
        # Apply rate limiting
        self.rate_limiter.wait_if_needed()
        
        try:
            # Track usage
            usage_tracker.track_request("contract_analysis")
            
            # Create comprehensive analysis prompt
            prompt = self._create_analysis_prompt(contract_text)
            
            # Generate AI analysis
            response = self.model.generate_content(prompt)
            ai_analysis = response.text.strip()
            
            # Perform rule-based analysis
            rule_based_analysis = self.analyze_contract_rules(contract_text)
            
            # Combine analyses
            combined_analysis = self._combine_analyses(ai_analysis, rule_based_analysis, contract_text)
            
            logger.info("Successfully completed comprehensive contract analysis")
            return combined_analysis
            
        except Exception as e:
            error_msg = f"Contract analysis failed: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_contract_rules(self, contract_text: str) -> Dict[str, Any]:
        """Perform rule-based risk analysis"""
        
        risks_identified = []
        total_risk_score = 0
        
        contract_lower = contract_text.lower()
        
        for risk_id, rule in self.risk_rules.items():
            # Check if any pattern matches
            patterns_found = []
            for pattern in rule["patterns"]:
                if re.search(pattern, contract_lower):
                    patterns_found.append(pattern)
            
            # If no patterns found, it's a missing clause (risk)
            if not patterns_found:
                risk = {
                    "risk_id": risk_id,
                    "severity": rule["severity"],
                    "weight": rule["weight"],
                    "description": rule["description"],
                    "recommendation": rule["recommendation"],
                    "category": self._categorize_risk(risk_id)
                }
                risks_identified.append(risk)
                total_risk_score += rule["weight"]
        
        # Calculate risk metrics
        max_possible_risk = sum(rule["weight"] for rule in self.risk_rules.values())
        normalized_risk_score = min(total_risk_score / max_possible_risk, 1.0) if max_possible_risk > 0 else 0
        
        # Determine risk level
        if normalized_risk_score >= 0.7:
            risk_level = "HIGH"
        elif normalized_risk_score >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "success": True,
            "analysis_type": "Rule-Based",
            "overall_risk_score": round(normalized_risk_score, 2),
            "risk_level": risk_level,
            "total_risks": len(risks_identified),
            "risks_by_severity": self._group_risks_by_severity(risks_identified),
            "risks_identified": risks_identified,
            "contract_length": len(contract_text.split()),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _create_analysis_prompt(self, contract_text: str) -> str:
        """Create comprehensive analysis prompt for AI"""
        
        return f"""
        You are an expert legal contract analyst. Perform a comprehensive risk assessment of this contract:

        CONTRACT TEXT:
        {contract_text}

        Provide a detailed legal analysis covering:

        1. OVERALL RISK ASSESSMENT
        - Risk Level: (LOW/MEDIUM/HIGH)
        - Contract Quality Score: (1-10 scale)
        - Legal Enforceability Rating: (1-10 scale)
        - Completeness Assessment: (1-10 scale)

        2. CRITICAL LEGAL ISSUES
        - Identify any provisions that could lead to legal disputes
        - Flag ambiguous or contradictory clauses
        - Highlight missing standard legal protections
        - Note any unusual or problematic terms

        3. CLAUSE-BY-CLAUSE ANALYSIS
        - Essential clauses present and their adequacy
        - Missing standard contract provisions
        - Problematic or vague language that needs clarification
        - Recommendations for improvement

        4. FINANCIAL AND LIABILITY RISKS
        - Payment terms analysis and potential issues
        - Liability exposure and limitations
        - Insurance and indemnification provisions
        - Financial protection adequacy

        5. COMPLIANCE AND LEGAL RISKS
        - Regulatory compliance issues
        - Jurisdictional concerns
        - Industry-specific requirements
        - Potential enforceability problems

        6. OPERATIONAL RISKS
        - Performance obligations clarity
        - Delivery and acceptance terms
        - Change management procedures
        - Dispute resolution mechanisms

        7. INTELLECTUAL PROPERTY ANALYSIS
        - IP ownership and rights allocation
        - Confidentiality and trade secret protection
        - License grants and restrictions
        - Third-party IP considerations

        8. TERMINATION AND EXIT PROVISIONS
        - Termination triggers and procedures
        - Notice requirements
        - Post-termination obligations
        - Asset and information return provisions

        9. RECOMMENDATIONS FOR IMPROVEMENT
        - Priority improvements (High/Medium/Low)
        - Specific language suggestions
        - Additional clauses to consider
        - Risk mitigation strategies

        10. PRECEDENT AND MARKET STANDARDS
        - Comparison to industry standards
        - Market-typical terms assessment
        - Unusual provisions analysis
        - Negotiation recommendations

        Format your analysis as a professional legal memorandum with clear sections and specific, actionable recommendations.
        """
    
    def _combine_analyses(self, ai_analysis: str, rule_analysis: Dict[str, Any], contract_text: str) -> Dict[str, Any]:
        """Combine AI and rule-based analyses"""
        
        # Extract additional insights
        contract_stats = self._extract_contract_statistics(contract_text)
        
        return {
            "success": True,
            "analysis_type": "Comprehensive (AI + Rule-Based)",
            
            # Primary risk assessment
            "overall_risk_assessment": {
                "risk_level": rule_analysis["risk_level"],
                "risk_score": rule_analysis["overall_risk_score"],
                "confidence": "High",
                "total_issues": rule_analysis["total_risks"]
            },
            
            # Detailed AI analysis
            "ai_analysis": {
                "detailed_analysis": ai_analysis,
                "model_used": "Google Gemini 1.5 Flash",
                "analysis_depth": "Comprehensive"
            },
            
            # Rule-based findings
            "rule_based_analysis": {
                "risks_identified": rule_analysis["risks_identified"],
                "risks_by_severity": rule_analysis["risks_by_severity"],
                "missing_clauses": len(rule_analysis["risks_identified"]),
                "critical_gaps": len([r for r in rule_analysis["risks_identified"] if r["severity"] == "HIGH"])
            },
            
            # Contract statistics
            "contract_statistics": contract_stats,
            
            # Recommendations
            "recommendations": {
                "immediate_actions": self._get_high_priority_recommendations(rule_analysis["risks_identified"]),
                "medium_term_improvements": self._get_medium_priority_recommendations(rule_analysis["risks_identified"]),
                "long_term_considerations": self._get_low_priority_recommendations(rule_analysis["risks_identified"])
            },
            
            # Metadata
            "analysis_metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "analysis_time": "< 30 seconds",
                "cost": "$0.00 (Free Tier)",
                "model": "Gemini 1.5 Flash + Rule Engine"
            }
        }
    
    def _extract_contract_statistics(self, contract_text: str) -> Dict[str, Any]:
        """Extract statistical information about the contract"""
        
        words = contract_text.split()
        sentences = len(re.findall(r'[.!?]+', contract_text))
        sections = len(re.findall(r'^\d+\.', contract_text, re.MULTILINE))
        
        return {
            "word_count": len(words),
            "character_count": len(contract_text),
            "sentence_count": sentences,
            "section_count": sections,
            "estimated_pages": max(1, len(words) // 250),  # Rough estimate
            "reading_time_minutes": max(1, len(words) // 200),  # Average reading speed
            "complexity_score": min(10, max(1, len(words) // 200))  # Rough complexity measure
        }
    
    def _categorize_risk(self, risk_id: str) -> str:
        """Categorize risk by type"""
        categories = {
            "liability": ["missing_liability_cap", "vague_payment_terms"],
            "termination": ["missing_termination"],
            "legal": ["missing_governing_law", "missing_amendment_clause", "missing_severability"],
            "confidentiality": ["missing_confidentiality"],
            "financial": ["vague_payment_terms", "missing_late_fees"],
            "intellectual_property": ["missing_ip_clauses"],
            "operational": ["missing_force_majeure"]
        }
        
        for category, risks in categories.items():
            if risk_id in risks:
                return category.replace("_", " ").title()
        
        return "General"
    
    def _group_risks_by_severity(self, risks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group risks by severity level"""
        grouped = {"HIGH": [], "MEDIUM": [], "LOW": []}
        
        for risk in risks:
            severity = risk.get("severity", "LOW")
            if severity in grouped:
                grouped[severity].append(risk)
        
        return grouped
    
    def _get_high_priority_recommendations(self, risks: List[Dict[str, Any]]) -> List[str]:
        """Get high priority recommendations"""
        high_risks = [r for r in risks if r["severity"] == "HIGH"]
        return [risk["recommendation"] for risk in high_risks]
    
    def _get_medium_priority_recommendations(self, risks: List[Dict[str, Any]]) -> List[str]:
        """Get medium priority recommendations"""
        medium_risks = [r for r in risks if r["severity"] == "MEDIUM"]
        return [risk["recommendation"] for risk in medium_risks]
    
    def _get_low_priority_recommendations(self, risks: List[Dict[str, Any]]) -> List[str]:
        """Get low priority recommendations"""
