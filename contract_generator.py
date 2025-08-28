"""
Legal Contract Generator using Google Gemini API
"""

import google.generativeai as genai
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from utils import (
    RateLimiter, validate_contract_params, save_contract, 
    extract_contract_metadata, logger, usage_tracker
)

# Load environment variables
load_dotenv()

class ContractGenerator:
    """Main contract generation class using Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the contract generator"""
        
        # Configure Gemini API
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(max_requests_per_minute=15)
        
        # Configuration
        self.max_tokens = int(os.getenv("MAX_TOKENS", 2000))
        self.temperature = float(os.getenv("TEMPERATURE", 0.1))
        
        logger.info("ContractGenerator initialized with Gemini 1.5 Flash")
    
    def generate_nda_contract(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Generate a comprehensive NDA contract"""
        
        prompt = f"""
        Draft a comprehensive, legally sound mutual non-disclosure agreement with these exact specifications:

        PARTIES AND DETAILS:
        - Party 1 (Disclosing Party): {params['party1']}
        - Party 2 (Receiving Party): {params['party2']}
        - Effective Date: {params['date']}
        - Agreement Term: {params['term']}
        - Governing Jurisdiction: {params['jurisdiction']}

        REQUIREMENTS:
        Create a professional, enforceable NDA that includes:

        1. TITLE AND PREAMBLE
        - Clear agreement title
        - Proper legal preamble with parties identification

        2. DEFINITIONS SECTION
        - Comprehensive definition of "Confidential Information"
        - Definition of "Receiving Party" and "Disclosing Party"
        - Definition of "Purpose"

        3. CONFIDENTIALITY OBLIGATIONS
        - Duty to maintain confidentiality
        - Standard of care (reasonable care)
        - Non-disclosure commitments
        - Restrictions on use

        4. PERMITTED DISCLOSURES
        - Publicly available information
        - Information independently developed
        - Information rightfully received from third parties
        - Required disclosures by law or court order

        5. RETURN OF MATERIALS
        - Obligation to return or destroy confidential materials
        - Certification of destruction/return

        6. TERM AND TERMINATION
        - Effective period: {params['term']}
        - Survival of obligations post-termination
        - Termination procedures

        7. REMEDIES
        - Acknowledgment that breach may cause irreparable harm
        - Right to seek injunctive relief
        - Monetary damages and attorney fees

        8. GENERAL PROVISIONS
        - Governing law: {params['jurisdiction']}
        - Jurisdiction for disputes
        - Entire agreement clause
        - Amendment procedures
        - Severability clause
        - Counterpart execution

        9. SIGNATURE BLOCKS
        - Proper signature blocks for both parties
        - Date and title fields

        FORMAT REQUIREMENTS:
        - Use numbered sections and subsections
        - Professional legal formatting
        - Clear, enforceable language
        - Minimum 2000 words for comprehensiveness
        - Include all standard legal protections

        Generate a complete, professional NDA ready for execution.
        """
        
        return self._generate_contract("NDA", prompt, params)
    
    def generate_service_agreement(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Generate a comprehensive service agreement"""
        
        prompt = f"""
        Draft a comprehensive, professional service agreement with these specifications:

        CONTRACT DETAILS:
        - Client: {params['client']}
        - Service Provider: {params['provider']}
        - Services: {params['services']}
        - Compensation: {params['payment']}
        - Contract Duration: {params['duration']}
        - Effective Date: {params['date']}
        - Governing Jurisdiction: {params['jurisdiction']}

        REQUIRED SECTIONS:

        1. TITLE AND PARTIES
        - Clear service agreement title
        - Identification of client and service provider

        2. SCOPE OF SERVICES
        - Detailed description: {params['services']}
        - Service specifications and deliverables
        - Performance standards and metrics
        - Timeline and milestones

        3. COMPENSATION AND PAYMENT
        - Payment terms: {params['payment']}
        - Payment schedule and methods
        - Late payment penalties
        - Expense reimbursement policies
        - Invoice requirements

        4. TERM AND TERMINATION
        - Contract duration: {params['duration']}
        - Termination for cause procedures
        - Termination for convenience (30-day notice)
        - Post-termination obligations
        - Final payment procedures

        5. INTELLECTUAL PROPERTY
        - Work product ownership
        - Pre-existing IP rights
        - License grants
        - Third-party IP indemnification

        6. CONFIDENTIALITY
        - Protection of confidential information
        - Non-disclosure obligations
        - Return of confidential materials

        7. WARRANTIES AND REPRESENTATIONS
        - Service provider warranties
        - Client warranties
        - Disclaimer of other warranties

        8. LIMITATION OF LIABILITY
        - Liability caps and limitations
        - Exclusion of consequential damages
        - Indemnification obligations

        9. FORCE MAJEURE
        - Definition of force majeure events
        - Procedures for force majeure situations
        - Suspension and termination rights

        10. GENERAL PROVISIONS
        - Governing law: {params['jurisdiction']}
        - Dispute resolution procedures
        - Independent contractor relationship
        - Entire agreement clause
        - Amendment procedures
        - Severability clause
        - Assignment restrictions

        11. SIGNATURE BLOCKS
        - Client and provider signature sections
        - Date and title fields

        FORMAT REQUIREMENTS:
        - Professional legal formatting with numbered sections
        - Clear, enforceable language
        - Comprehensive coverage (minimum 2500 words)
        - Industry-standard clauses and protections

        Create a complete, legally sound service agreement ready for execution.
        """
        
        return self._generate_contract("SERVICE", prompt, params)
    
    def generate_employment_agreement(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Generate a comprehensive employment agreement"""
        
        prompt = f"""
        Draft a comprehensive employment agreement with these specifications:

        EMPLOYMENT DETAILS:
        - Employer: {params['employer']}
        - Employee: {params['employee']}
        - Position: {params['position']}
        - Annual Salary: {params['salary']}
        - Start Date: {params['start_date']}
        - Governing Jurisdiction: {params['jurisdiction']}

        REQUIRED SECTIONS:

        1. PARTIES AND POSITION
        - Employer and employee identification
        - Job title: {params['position']}
        - Start date: {params['start_date']}

        2. DUTIES AND RESPONSIBILITIES
        - Primary job functions for {params['position']}
        - Reporting relationships
        - Performance expectations
        - Professional conduct standards

        3. COMPENSATION AND BENEFITS
        - Annual salary: {params['salary']}
        - Payment schedule (bi-weekly/monthly)
        - Overtime policies
        - Benefits eligibility
        - Paid time off policies

        4. TERM OF EMPLOYMENT
        - At-will employment status
        - Notice requirements for resignation
        - Employment duration terms

        5. CONFIDENTIALITY AND NON-DISCLOSURE
        - Protection of employer confidential information
        - Non-disclosure obligations
        - Return of company property

        6. INTELLECTUAL PROPERTY
        - Work-for-hire provisions
        - Assignment of inventions
        - Company ownership of work product

        7. NON-COMPETE AND NON-SOLICITATION (if applicable)
        - Non-competition restrictions
        - Customer non-solicitation
        - Employee non-solicitation
        - Geographic and temporal limitations

        8. TERMINATION
        - Termination for cause definitions
        - Termination procedures
        - Final pay and benefit continuation
        - Return of company property

        9. GENERAL PROVISIONS
        - Governing law: {params['jurisdiction']}
        - Entire agreement clause
        - Amendment procedures
        - Severability clause

        10. SIGNATURE BLOCKS
        - Employer and employee signatures
        - Date fields

        Create a legally compliant, comprehensive employment agreement.
        """
        
        return self._generate_contract("EMPLOYMENT", prompt, params)
    
    def _generate_contract(self, contract_type: str, prompt: str, params: Dict[str, str]) -> Dict[str, Any]:
        """Internal method to generate contract using Gemini API"""
        
        # Validate parameters
        validation_result = validate_contract_params(contract_type, params)
        if "error" in validation_result:
            return validation_result
        
        # Apply rate limiting
        self.rate_limiter.wait_if_needed()
        
        try:
            # Track usage
            usage_tracker.track_request("contract_generation")
            
            # Generate contract
            start_time = time.time()
            response = self.model.generate_content(prompt)
            generation_time = time.time() - start_time
            
            # Extract and process response
            contract_text = response.text.strip()
            metadata = extract_contract_metadata(contract_text)
            
            # Save contract to file
            parties = self._extract_parties(params)
            file_path = save_contract(contract_text, contract_type, parties)
            
            result = {
                "success": True,
                "contract_text": contract_text,
                "contract_type": contract_type,
                "metadata": metadata,
                "parameters": params,
                "file_path": file_path,
                "generation_time": round(generation_time, 2),
                "model_used": "Google Gemini 1.5 Flash (FREE)",
                "generated_at": datetime.now().isoformat(),
                "api_usage": {
                    "tokens_estimated": len(contract_text) // 4,  # Rough estimate
                    "cost_estimate": "$0.00 (Free Tier)"
                }
            }
            
            logger.info(f"Successfully generated {contract_type} contract with {metadata['word_count']} words")
            return result
            
        except Exception as e:
            error_msg = f"Contract generation failed: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "contract_type": contract_type,
                "parameters": params,
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_parties(self, params: Dict[str, str]) -> List[str]:
        """Extract party names for file naming"""
        parties = []
        
        # Different contract types have different party field names
        if "party1" in params and "party2" in params:
            parties = [params["party1"], params["party2"]]
        elif "client" in params and "provider" in params:
            parties = [params["client"], params["provider"]]
        elif "employer" in params and "employee" in params:
            parties = [params["employer"], params["employee"]]
        
        return parties
    
    def get_supported_contract_types(self) -> Dict[str, Dict[str, Any]]:
        """Get list of supported contract types and their requirements"""
        return {
            "NDA": {
                "name": "Non-Disclosure Agreement",
                "description": "Mutual confidentiality agreement between two parties",
                "required_fields": ["party1", "party2", "date", "term", "jurisdiction"],
                "estimated_length": "2000-3000 words",
                "generation_time": "15-30 seconds"
            },
            "SERVICE": {
                "name": "Service Agreement",
                "description": "Professional services contract between client and provider",
                "required_fields": ["client", "provider", "services", "payment", "duration", "jurisdiction", "date"],
                "estimated_length": "2500-4000 words",
                "generation_time": "20-40 seconds"
            },
            "EMPLOYMENT": {
                "name": "Employment Agreement",
                "description": "Employment contract between employer and employee",
                "required_fields": ["employer", "employee", "position", "salary", "start_date", "jurisdiction"],
                "estimated_length": "2000-3500 words",
                "generation_time": "15-35 seconds"
            }
        }
    
    def validate_generation_request(self, contract_type: str, params: Dict[str, str]) -> Dict[str, Any]:
        """Validate a contract generation request before processing"""
        
        supported_types = self.get_supported_contract_types()
        
        if contract_type.upper() not in supported_types:
            return {
                "valid": False,
                "error": f"Unsupported contract type: {contract_type}",
                "supported_types": list(supported_types.keys())
            }
        
        return validate_contract_params(contract_type, params)
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get generation statistics"""
        stats = usage_tracker.get_usage_stats()
        
        return {
            "total_contracts_generated": stats["contracts_generated"],
            "total_requests": stats["total_requests"],
            "today_requests": stats["today_requests"],
            "month_requests": stats["month_requests"],
            "supported_contract_types": len(self.get_supported_contract_types()),
            "model_used": "Google Gemini 1.5 Flash",
            "api_cost": "$0.00 (Free Tier)",
            "rate_limit": "15 requests/minute"
        }
