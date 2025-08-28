"""
Main Streamlit Application for Legal AI Contract Generator
"""

import streamlit as st
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, date
import time

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import our modules
from contract_generator import ContractGenerator
from risk_analyzer import ContractRiskAnalyzer
from utils import (
    get_project_info, create_project_structure, cleanup_old_contracts,
    usage_tracker, logger, validate_api_key
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class LegalAIApp:
    """Main Legal AI Streamlit Application"""
    
    def __init__(self):
        """Initialize the Legal AI application"""
        
        # Create necessary directories
        create_project_structure()
        
        # Configure Streamlit page
        st.set_page_config(
            page_title="Legal AI Contract Generator",
            page_icon="⚖️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize session state
        self._initialize_session_state()
        
        # Clean up old files (optional)
        if st.session_state.get('cleanup_enabled', True):
            cleanup_old_contracts(days_old=7)  # Clean files older than 7 days
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.api_key_validated = False
            st.session_state.contract_generator = None
            st.session_state.risk_analyzer = None
            st.session_state.generation_history = []
            st.session_state.analysis_history = []
            st.session_state.current_contract = None
            st.session_state.cleanup_enabled = True
    
    def run(self):
        """Run the main Streamlit application"""
        
        # Display header
        self._display_header()
        
        # Check API key configuration
        if not self._validate_api_configuration():
            self._display_api_setup()
            return
        
        # Initialize AI components
        if not st.session_state.api_key_validated:
            try:
                st.session_state.contract_generator = ContractGenerator()
                st.session_state.risk_analyzer = ContractRiskAnalyzer()
                st.session_state.api_key_validated = True
                st.success("✅ AI components initialized successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to initialize AI components: {str(e)}")
                return
        
        # Display sidebar
        self._display_sidebar()
        
        # Main application interface
        self._display_main_interface()
    
    def _display_header(self):
        """Display application header"""
        
        project_info = get_project_info()
        
        st.title("⚖️ Legal AI Contract Generator")
        st.markdown(f"*{project_info['description']}*")
        
        # Status bar
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Version", project_info['version'])
        
        with col2:
            api_status = "✅ Connected" if st.session_state.api_key_validated else "❌ Not Connected"
            st.metric("API Status", api_status)
        
        with col3:
            stats = usage_tracker.get_usage_stats()
            st.metric("Contracts Generated", stats['contracts_generated'])
        
        with col4:
            st.metric("Analyses Performed", stats['analyses_performed'])
        
        st.markdown("---")
    
    def _validate_api_configuration(self) -> bool:
        """Validate API key configuration"""
        
        api_key = os.getenv("GEMINI_API_KEY")
        return api_key and validate_api_key(api_key)
    
    def _display_api_setup(self):
        """Display API key setup interface"""
        
        st.warning("🔑 API Key Configuration Required")
        
        with st.expander("🔧 Setup Instructions", expanded=True):
            st.markdown("""
            **To get started, you need a Google Gemini API key:**
            
            1. Visit [Google AI Studio](https://aistudio.google.com/)
            2. Sign in with your Google account
            3. Click "Get API Key" and create a new key
            4. Copy your API key (starts with `AIza...`)
            5. Add it to your `.env` file: `GEMINI_API_KEY=your_key_here`
            6. Refresh this page
            
            **Your API key is completely FREE with generous limits:**
            - 15 requests per minute
            - 50 requests per day
            - No billing required for basic usage
            """)
        
        # Allow manual API key entry for testing
        with st.form("api_key_form"):
            st.subheader("🧪 Manual API Key Entry (for testing)")
            manual_key = st.text_input(
                "Enter your Gemini API Key:",
                type="password",
                placeholder="AIza..."
            )
            
            if st.form_submit_button("Test API Key"):
                if manual_key and validate_api_key(manual_key):
                    # Temporarily set the API key for this session
                    os.environ["GEMINI_API_KEY"] = manual_key
                    st.success("✅ API key validated! Initializing...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid API key format")
    
    def _display_sidebar(self):
        """Display application sidebar"""
        
        with st.sidebar:
            st.markdown("### 📊 Dashboard")
            
            # Usage statistics
            stats = usage_tracker.get_usage_stats()
            st.metric("Today's Requests", stats['today_requests'])
            st.metric("Monthly Requests", stats['month_requests'])
            
            # Rate limit info
            st.markdown("### ⚡ API Limits")
            st.info("""
            **FREE Tier Limits:**
            - 15 requests/minute
            - 50 requests/day
            - No billing required
            """)
            
            # Generation history
            if st.session_state.generation_history:
                st.markdown("### 📜 Recent Contracts")
                for i, contract in enumerate(st.session_state.generation_history[-3:], 1):
                    contract_type = contract.get('contract_type', 'Unknown')
                    timestamp = contract.get('generated_at', '')[:16]  # Show date and time
                    st.text(f"{i}. {contract_type} - {timestamp}")
            
            # Settings
            st.markdown("### ⚙️ Settings")
            st.session_state.cleanup_enabled = st.checkbox(
                "Auto-cleanup old files",
                value=st.session_state.cleanup_enabled,
                help="Automatically remove files older than 7 days"
            )
            
            # Help section
            with st.expander("❓ Help & Support"):
                st.markdown("""
                **Quick Tips:**
                - Fill all required fields
                - Use clear, specific language
                - Review generated contracts carefully
                - Consult legal professionals for important agreements
                
                **Supported Contract Types:**
                - Non-Disclosure Agreements (NDA)
                - Service Agreements
                - Employment Agreements
                """)
    
    def _display_main_interface(self):
        """Display main application interface"""
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Generate Contract", 
            "🔍 Analyze Contract", 
            "📊 Dashboard",
            "ℹ️ About"
        ])
        
        with tab1:
            self._display_contract_generation()
        
        with tab2:
            self._display_contract_analysis()
        
        with tab3:
            self._display_dashboard()
        
        with tab4:
            self._display_about()
    
    def _display_contract_generation(self):
        """Display contract generation interface"""
        
        st.header("📝 Generate Professional Legal Contract")
        
        # Contract type selection
        contract_types = st.session_state.contract_generator.get_supported_contract_types()
        
        contract_type = st.selectbox(
            "Select Contract Type:",
            options=list(contract_types.keys()),
            format_func=lambda x: f"{contract_types[x]['name']} - {contract_types[x]['description']}"
        )
        
        # Display contract type info
        type_info = contract_types[contract_type]
        with st.expander("📋 Contract Information"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Estimated Length", type_info['estimated_length'])
            with col2:
                st.metric("Generation Time", type_info['generation_time'])
            
            st.markdown(f"**Required Fields:** {', '.join(type_info['required_fields'])}")
        
        # Contract generation forms
        if contract_type == "NDA":
            self._display_nda_form()
        elif contract_type == "SERVICE":
            self._display_service_form()
        elif contract_type == "EMPLOYMENT":
            self._display_employment_form()
    
    def _display_nda_form(self):
        """Display NDA generation form"""
        
        st.subheader("🤝 Non-Disclosure Agreement Details")
        
        with st.form("nda_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                party1 = st.text_input(
                    "Party 1 (Disclosing Party):",
                    placeholder="e.g., TechCorp Inc.",
                    help="Company or individual sharing confidential information"
                )
                
                party2 = st.text_input(
                    "Party 2 (Receiving Party):",
                    placeholder="e.g., ConsultingFirm LLC",
                    help="Company or individual receiving confidential information"
                )
                
                effective_date = st.date_input(
                    "Effective Date:",
                    value=datetime.now().date(),
                    help="When the agreement becomes effective"
                )
            
            with col2:
                term = st.text_input(
                    "Agreement Term:",
                    value="2 years",
                    placeholder="e.g., 2 years, 18 months",
                    help="How long the confidentiality obligations last"
                )
                
                jurisdiction = st.text_input(
                    "Governing Jurisdiction:",
                    value="California",
                    placeholder="e.g., California, New York",
                    help="Which state/country's laws govern the agreement"
                )
            
            # Advanced options
            with st.expander("🔧 Advanced Options"):
                include_non_compete = st.checkbox("Include Non-Compete Clauses")
                include_non_solicitation = st.checkbox("Include Non-Solicitation Clauses")
                custom_clauses = st.text_area(
                    "Additional Custom Clauses:",
                    placeholder="Enter any specific clauses or requirements..."
                )
            
            # Generate button
            generate_btn = st.form_submit_button(
                "🚀 Generate NDA Contract",
                type="primary",
                use_container_width=True
            )
            
            if generate_btn:
                params = {
                    'party1': party1,
                    'party2': party2,
                    'date': effective_date.strftime("%B %d, %Y"),
                    'term': term,
                    'jurisdiction': jurisdiction
                }
                
                # Add advanced options to params if selected
                if custom_clauses:
                    params['custom_clauses'] = custom_clauses
                
                self._generate_contract("NDA", params)
    
    def _display_service_form(self):
        """Display Service Agreement generation form"""
        
        st.subheader("🤝 Service Agreement Details")
        
        with st.form("service_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                client = st.text_input(
                    "Client Name:",
                    placeholder="e.g., TechStartup Inc.",
                    help="Company or individual purchasing services"
                )
                
                provider = st.text_input(
                    "Service Provider:",
                    placeholder="e.g., DevServices LLC",
                    help="Company or individual providing services"
                )
                
                services = st.text_area(
                    "Services Description:",
                    placeholder="Describe the services in detail...",
                    help="Detailed description of services to be provided",
                    height=100
                )
            
            with col2:
                payment = st.text_input(
                    "Compensation:",
                    placeholder="e.g., $5,000 per month",
                    help="How much and how often payment is made"
                )
                
                duration = st.text_input(
                    "Contract Duration:",
                    placeholder="e.g., 6 months",
                    help="How long the service agreement lasts"
                )
                
                effective_date = st.date_input(
                    "Effective Date:",
                    value=datetime.now().date()
                )
                
                jurisdiction = st.text_input(
                    "Governing Jurisdiction:",
                    value="New York",
                    placeholder="e.g., New York, Delaware"
                )
            
            # Generate button
            generate_btn = st.form_submit_button(
                "🚀 Generate Service Agreement",
                type="primary",
                use_container_width=True
            )
            
            if generate_btn:
                params = {
                    'client': client,
                    'provider': provider,
                    'services': services,
                    'payment': payment,
                    'duration': duration,
                    'date': effective_date.strftime("%B %d, %Y"),
                    'jurisdiction': jurisdiction
                }
                
                self._generate_contract("SERVICE", params)
    
    def _display_employment_form(self):
        """Display Employment Agreement generation form"""
        
        st.subheader("👔 Employment Agreement Details")
        
        with st.form("employment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                employer = st.text_input(
                    "Employer Name:",
                    placeholder="e.g., Innovation Corp"
                )
                
                employee = st.text_input(
                    "Employee Name:",
                    placeholder="e.g., John Smith"
                )
                
                position = st.text_input(
                    "Job Position:",
                    placeholder="e.g., Senior Software Developer"
                )
            
            with col2:
                salary = st.text_input(
                    "Annual Salary:",
                    placeholder="e.g., $85,000"
                )
                
                start_date = st.date_input(
                    "Start Date:",
                    value=datetime.now().date()
                )
                
                jurisdiction = st.text_input(
                    "Governing Jurisdiction:",
                    value="California",
                    placeholder="e.g., California, Texas"
                )
            
            generate_btn = st.form_submit_button(
                "🚀 Generate Employment Agreement",
                type="primary",
                use_container_width=True
            )
            
            if generate_btn:
                params = {
                    'employer': employer,
                    'employee': employee,
                    'position': position,
                    'salary': salary,
                    'start_date': start_date.strftime("%B %d, %Y"),
                    'jurisdiction': jurisdiction
                }
                
                self._generate_contract("EMPLOYMENT", params)
    
    def _generate_contract(self, contract_type: str, params: Dict[str, Any]):
        """Generate contract using AI"""
        
        # Validate parameters
        if not all(params.values()):
            st.error("⚠️ Please fill in all required fields")
            return
        
        # Show generation progress
        with st.spinner(f"🤖 Gemini AI is drafting your {contract_type} contract..."):
            try:
                # Generate contract
                if contract_type == "NDA":
                    result = st.session_state.contract_generator.generate_nda_contract(params)
                elif contract_type == "SERVICE":
                    result = st.session_state.contract_generator.generate_service_agreement(params)
                elif contract_type == "EMPLOYMENT":
                    result = st.session_state.contract_generator.generate_employment_agreement(params)
                
                if result.get("success"):
                    st.session_state.current_contract = result
                    st.session_state.generation_history.append(result)
                    self._display_generated_contract(result)
                else:
                    st.error(f"❌ Contract generation failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                logger.error(f"Contract generation error: {str(e)}")
    
    def _display_generated_contract(self, result: Dict[str, Any]):
        """Display generated contract results"""
    
        st.success(f"✅ {result['contract_type']} Contract Generated Successfully!")
    
    # Contract statistics
        metadata = result.get('metadata', {})
        col1, col2, col3, col4 = st.columns(4)
    
        with col1:
            st.metric("Words", f"{metadata.get('word_count', 0):,}")
        with col2:
            st.metric("Characters", f"{metadata.get('character_count', 0):,}")
        with col3:
            st.metric("Estimated Pages", metadata.get('estimated_pages', 0))
        with col4:
            st.metric("Generation Time", f"{result.get('generation_time', 0):.1f}s")
    
        # Display contract text
        st.markdown("### 📄 Generated Contract")
    
        contract_text = result.get('contract_text', '')
        st.text_area(
            "Contract Text:",
            value=contract_text,
            height=400,
            help="Review the generated contract carefully before use"
        )
    
    # Action buttons (MOVED OUTSIDE FORM - NO st.form() here)
        st.markdown("### 📥 Download & Actions")
        col1, col2, col3 = st.columns(3)
    
        with col1:
            # Download button - NOW WORKS!
            st.download_button(
                "📥 Download as TXT",
                data=contract_text,
                file_name=f"{result['contract_type']}_Contract_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"download_{result['contract_type']}_{datetime.now().strftime('%Y%m%d_%H%M')}"
            )
    
        with col2:
            # Analyze button
            if st.button("🔍 Analyze This Contract", use_container_width=True, 
                         key=f"analyze_{result['contract_type']}_{datetime.now().strftime('%Y%m%d_%H%M')}"):
                self._analyze_current_contract()
    
        with col3:
            # Copy to clipboard helper
            if st.button("📋 Show for Copy", use_container_width=True,
                         key=f"copy_{result['contract_type']}_{datetime.now().strftime('%Y%m%d_%H%M')}"):
                st.code(contract_text, language="text")

    
    def _display_contract_analysis(self):
        """Display contract analysis interface"""
        
        st.header("🔍 Legal Contract Risk Analysis")
        
        # Analysis input options
        analysis_option = st.radio(
            "Choose Analysis Option:",
            ["Analyze Text Input", "Analyze Generated Contract", "Upload Contract File"],
            help="Select how you want to provide the contract for analysis"
        )
        
        if analysis_option == "Analyze Text Input":
            self._display_text_analysis()
        elif analysis_option == "Analyze Generated Contract":
            self._display_generated_contract_analysis()
        elif analysis_option == "Upload Contract File":
            self._display_file_analysis()
    
    def _display_text_analysis(self):
        """Display text input analysis interface"""
        
        st.subheader("📝 Paste Contract Text")
        
        contract_text = st.text_area(
            "Contract Text:",
            height=300,
            placeholder="Paste the complete contract text here for analysis...",
            help="Enter the full contract text you want to analyze for legal risks"
        )
        
        if st.button("🔍 Analyze Contract", type="primary", use_container_width=True):
            if contract_text.strip():
                self._perform_contract_analysis(contract_text)
            else:
                st.warning("⚠️ Please enter contract text to analyze")
    
    def _display_generated_contract_analysis(self):
        """Display analysis interface for previously generated contracts"""
        
        if not st.session_state.current_contract:
            st.info("📝 Generate a contract first, then come back to analyze it")
            return
        
        current = st.session_state.current_contract
        st.subheader(f"📊 Analyze Generated {current['contract_type']} Contract")
        
        # Show contract preview
        contract_text = current.get('contract_text', '')
        st.text_area(
            "Contract Preview:",
            value=contract_text[:500] + "..." if len(contract_text) > 500 else contract_text,
            height=150,
            disabled=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Word Count", current.get('metadata', {}).get('word_count', 0))
        with col2:
            st.metric("Generated", current.get('generated_at', '')[:16])
        
        if st.button("🔍 Analyze This Contract", type="primary", use_container_width=True):
            self._perform_contract_analysis(contract_text)
    
    def _display_file_analysis(self):
        """Display file upload analysis interface"""
        
        st.subheader("📁 Upload Contract File")
        
        uploaded_file = st.file_uploader(
            "Choose contract file:",
            type=['txt', 'pdf', 'docx'],
            help="Upload a contract file for analysis"
        )
        
        if uploaded_file is not None:
            try:
                # Handle different file types
                if uploaded_file.type == "text/plain":
                    content = str(uploaded_file.read(), "utf-8")
                elif uploaded_file.type == "application/pdf":
                    st.warning("📄 PDF analysis not yet implemented. Please copy and paste text instead.")
                    return
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    st.warning("📄 DOCX analysis not yet implemented. Please copy and paste text instead.")
                    return
                else:
                    st.error("❌ Unsupported file type")
                    return
                
                st.success(f"✅ File loaded: {len(content.split())} words")
                
                # Show preview
                st.text_area("File Content Preview:", value=content[:500] + "...", height=150, disabled=True)
                
                if st.button("🔍 Analyze Uploaded Contract", type="primary"):
                    self._perform_contract_analysis(content)
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    def _analyze_current_contract(self):
        """Analyze the currently generated contract"""
        
        if st.session_state.current_contract:
            contract_text = st.session_state.current_contract.get('contract_text', '')
            self._perform_contract_analysis(contract_text)
        else:
            st.error("❌ No contract to analyze")
    
    def _perform_contract_analysis(self, contract_text: str):
        """Perform comprehensive contract analysis"""
        
        with st.spinner("🤖 AI is analyzing your contract for legal risks..."):
            try:
                # Perform analysis
                analysis_result = st.session_state.risk_analyzer.analyze_contract_comprehensive(contract_text)
                
                if analysis_result.get("success"):
                    st.session_state.analysis_history.append({
                        'analysis': analysis_result,
                        'analyzed_at': datetime.now().isoformat(),
                        'contract_length': len(contract_text.split())
                    })
                    
                    self._display_analysis_results(analysis_result)
                else:
                    st.error(f"❌ Analysis failed: {analysis_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Analysis error: {str(e)}")
                logger.error(f"Contract analysis error: {str(e)}")
    
    def _display_analysis_results(self, analysis_result: Dict[str, Any]):
        """Display contract analysis results"""
    
        st.success("✅ Contract Analysis Complete!")
    
        # Overall risk assessment
        risk_assessment = analysis_result.get("overall_risk_assessment", {})
    
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            risk_level = risk_assessment.get("risk_level", "Unknown")
            color = {"LOW": "green", "MEDIUM": "orange", "HIGH": "red"}.get(risk_level, "gray")
            st.markdown(f"**Risk Level:** <span style='color:{color}'>{risk_level}</span>", unsafe_allow_html=True)
    
        with col2:
            st.metric("Risk Score", f"{risk_assessment.get('risk_score', 0):.2f}/1.00")
    
        with col3:
            st.metric("Issues Found", risk_assessment.get('total_issues', 0))
    
        with col4:
            st.metric("Analysis Type", "Comprehensive")
    
        # Detailed analysis tabs
        analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs(["🤖 AI Analysis", "📋 Risk Summary", "📊 Detailed Report"])
    
        with analysis_tab1:
            st.subheader("🧠 AI Legal Analysis")
            ai_analysis = analysis_result.get("ai_analysis", {})
            if ai_analysis:
                st.info(ai_analysis.get("detailed_analysis", "No detailed analysis available"))
            else:
                st.warning("AI analysis not available")
    
        with analysis_tab2:
            st.subheader("⚠️ Risk Summary")
            self._display_risk_summary(analysis_result)
    
        with analysis_tab3:
            st.subheader("📊 Comprehensive Report")
            report = st.session_state.risk_analyzer.generate_risk_report(analysis_result)
            st.text_area("Full Risk Report:", value=report, height=400)
        
        # Download button OUTSIDE any form
            st.download_button(
            "📥 Download Risk Report",
                data=report,
                file_name=f"Risk_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                key=f"download_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )

    
    def _display_risk_summary(self, analysis_result: Dict[str, Any]):
        """Display risk summary"""
        
        rule_analysis = analysis_result.get("rule_based_analysis", {})
        risks_by_severity = rule_analysis.get("risks_by_severity", {})
        
        for severity in ["HIGH", "MEDIUM", "LOW"]:
            risks = risks_by_severity.get(severity, [])
            if risks:
                color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[severity]
                
                with st.expander(f"{color} {severity} Priority Issues ({len(risks)})", expanded=(severity=="HIGH")):
                    for i, risk in enumerate(risks, 1):
                        st.markdown(f"**{i}. {risk['description']}**")
                        st.markdown(f"*Recommendation:* {risk['recommendation']}")
                        st.markdown(f"*Category:* {risk.get('category', 'General')}")
                        if i < len(risks):  # Don't add divider after last item
                            st.markdown("---")
        
        # Recommendations
        recommendations = analysis_result.get("recommendations", {})
        immediate = recommendations.get("immediate_actions", [])
        
        if immediate:
            st.subheader("🚨 Immediate Actions Required")
            for action in immediate:
                st.warning(f"⚠️ {action}")
    
    def _display_dashboard(self):
        """Display application dashboard"""
    
        st.header("📊 Legal AI Dashboard")
    
    # Usage statistics
        stats = usage_tracker.get_usage_stats()
    
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Requests", stats['total_requests'])
        with col2:
            st.metric("Contracts Generated", stats['contracts_generated'])
        with col3:
            st.metric("Risk Analyses", stats['analyses_performed'])
        with col4:
            st.metric("Today's Usage", stats['today_requests'])
    
    # Generation history
        if st.session_state.generation_history:
            st.subheader("📜 Generation History")
        
            for i, contract in enumerate(reversed(st.session_state.generation_history[-10:]), 1):
                with st.expander(f"{contract['contract_type']} - {contract['generated_at'][:19]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Words", contract.get('metadata', {}).get('word_count', 0))
                        st.metric("Generation Time", f"{contract.get('generation_time', 0):.1f}s")
                    with col2:
                    # View button
                        if st.button(f"📋 View Contract", key=f"view_contract_{i}"):
                            st.text_area(
                                f"Contract Preview:", 
                                value=contract['contract_text'][:1000] + "...", 
                                height=200,
                                key=f"preview_{i}"
                            )
                    
                    # Download button (OUTSIDE form)
                        st.download_button(
                            f"📥 Download",
                            data=contract['contract_text'],
                            file_name=f"{contract['contract_type']}_{contract['generated_at'][:10]}.txt",
                            mime="text/plain",
                            key=f"download_history_{i}"
                        )
    
    # System information (rest remains the same)
        st.subheader("🔧 System Information")
    
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **AI Model:** Google Gemini 1.5 Flash  
            **API Cost:** $0.00 (Free Tier)  
            **Rate Limit:** 15 requests/minute  
            **Daily Limit:** 50 requests/day
            """)
    
        with col2:
            project_info = get_project_info()
            st.info(f"""
            **Version:** {project_info['version']}  
            **Tech Stack:** {project_info['tech_stack']}  
            **Created:** {project_info['created']}  
            **Status:** Operational ✅
            """)

    
    def _display_about(self):
        """Display about information"""
        
        st.header("ℹ️ About Legal AI Contract Generator")
        
        project_info = get_project_info()
        
        st.markdown(f"""
        ## {project_info['name']}
        
        **Version:** {project_info['version']}  
        **Description:** {project_info['description']}  
        **Technology Stack:** {project_info['tech_stack']}
        
        ### 🚀 Features
        
        - **AI-Powered Contract Generation:** Create professional legal contracts using Google Gemini AI
        - **Comprehensive Risk Analysis:** Advanced AI and rule-based contract risk assessment
        - **Multiple Contract Types:** Support for NDAs, Service Agreements, and Employment Contracts
        - **Free to Use:** Completely free with Google Gemini's generous free tier
        - **Professional Quality:** Generate contracts with all standard legal protections
        - **Download & Export:** Save contracts in multiple formats
        - **Usage Tracking:** Monitor your API usage and generation history
        
        ### 📋 Supported Contract Types
        
        1. **Non-Disclosure Agreements (NDA)**
           - Mutual confidentiality agreements
           - Comprehensive confidentiality protections
           - Standard legal remedies and enforcement
        
        2. **Service Agreements**
           - Professional service contracts
           - Clear scope, payment, and termination terms
           - Intellectual property and liability protections
        
        3. **Employment Agreements**
           - Comprehensive employment contracts
           - Salary, benefits, and termination procedures
           - Confidentiality and non-compete provisions
        
        ### ⚖️ Legal Disclaimer
        
        **IMPORTANT:** This application generates contract templates using AI technology. 
        
        - All generated contracts should be reviewed by qualified legal professionals
        - The application is for informational and educational purposes only
        - No attorney-client relationship is created by using this service
        - Laws vary by jurisdiction - consult local legal counsel
        - The developers assume no liability for the use of generated contracts
        
        ### 🔒 Privacy & Security
        
        - Your contract data is processed securely through Google's Gemini API
        - Generated contracts are temporarily saved locally for your session
        - No contract content is permanently stored or shared
        - API keys and sensitive data are handled securely
        
        ### 📞 Support
        
        For questions, issues, or feature requests:
        - Review the documentation and help sections
        - Check the FAQ in the sidebar
        - Ensure your API key is properly configured
        - Verify all required fields are completed
        
        ### 🙏 Acknowledgments
        
        Built with:
        - **Google Gemini AI** for contract generation and analysis
        - **Streamlit** for the web interface
        - **Python** for backend processing
        - Open source libraries and tools
        
        ---
        
        **© 2025 Legal AI Contract Generator - Built for Educational and Professional Use**
        """)

def main():
    """Main application entry point"""
    
    try:
        app = LegalAIApp()
        app.run()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
