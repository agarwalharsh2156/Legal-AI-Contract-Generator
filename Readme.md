# ⚖️ Legal AI Contract Generator

A powerful, AI-driven application for generating professional legal contracts and analyzing contract risks using Google's Gemini AI. Generate NDAs, Service Agreements, and Employment Contracts in minutes with comprehensive legal protections.

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed on your system
- **Google Account** (for free Gemini API access)
- **Internet connection**

### Installation & Setup

#### 1. **Clone or Download the Project**

```bash
cd path/to/your/project
```

#### 2. **Create Virtual Environment** (Recommended)

**On Windows:**
```bash
setup.bat
```

**On macOS/Linux:**
```bash
python3 -m venv legal_ai_env
source legal_ai_env/bin/activate
```

#### 3. **Install Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. **Get Your Free Gemini API Key**

1. Visit **[Google AI Studio](https://aistudio.google.com/)**
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create new secret key"**
4. Copy your API key (starts with `AIza...`)

#### 5. **Configure API Key**

Create a `.env` file in the project root directory:

```
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key from step 4.

#### 6. **Run the Application**

```bash
python run_app.py
```

Or directly with Streamlit:

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

---

## 📋 Features

### 📝 Contract Generation
- **Non-Disclosure Agreements (NDA)** - Mutual confidentiality agreements
- **Service Agreements** - Professional service contracts  
- **Employment Agreements** - Comprehensive employment contracts

### 🔍 Risk Analysis
- AI-powered legal risk assessment
- Rule-based contract analysis
- Identification of missing clauses
- Risk scoring and severity ratings
- Actionable recommendations

### 💾 Export & Download
- Download generated contracts as TXT files
- Save risk analysis reports
- Track generation history
- Usage statistics dashboard

---

## 🎯 Usage Guide

### Generating a Contract

1. **Select Contract Type** from the dropdown menu
2. **Fill Required Fields**:
   - Party/Company information
   - Dates and terms
   - Specific details (services, compensation, etc.)
3. **Click "Generate"** button
4. **Review** the generated contract
5. **Download** as TXT or copy to clipboard

### Analyzing a Contract

1. Go to **"Analyze Contract"** tab
2. Choose analysis option:
   - Paste contract text directly
   - Analyze previously generated contract
   - Upload a file (TXT support)
3. Click **"Analyze"** button
4. Review risk assessment and recommendations
5. Download detailed risk report

### Dashboard

Monitor your usage:
- Total requests and contracts generated
- Daily/monthly usage statistics
- Recent contract history
- System information

---

## 🔑 API Key Setup (Detailed)

### Getting Your Free API Key

1. Go to [aistudio.google.com](https://aistudio.google.com/)
2. Click your profile → "Manage API keys"
3. Click "Create API key" → "Create API key in new project"
4. Copy the generated key

### Storing the API Key

**Option 1: Environment File (Recommended)**

Create `.env` file in project root:
```
GEMINI_API_KEY=AIza_your_actual_key_here
```

**Option 2: Manual Entry**

Run the app and enter your API key in the setup dialog when prompted.

### Verify API Key is Working

The app shows "✅ API Status: Connected" when properly configured.

---

## 💰 Cost Information

### Free Tier Limits
- **15 requests per minute**
- **50 requests per day**
- **$0.00 cost** - Completely free!
- **No credit card required**

### Upgrade (Optional)
- Pay-as-you-go pricing available
- $0.075 per 1M input tokens
- $0.30 per 1M output tokens

---

## 📁 Project Structure

```
Legal AI Contract Generator/
├── app.py                          # Main Streamlit application
├── contract_generator.py           # Contract generation logic
├── risk_analyzer.py                # Risk analysis engine
├── utils.py                        # Utility functions
├── run_app.py                      # Application launcher
├── requirements.txt                # Python dependencies
├── .env                           # API key (create this)
├── .gitignore                     # Git ignore rules
├── setup.bat                      # Windows setup script
├── templates/                     # Contract templates
│   ├── nda_template.txt
│   └── service_template.txt
├── generated_contracts/           # Generated contract files
├── logs/                          # Application logs
└── legal_ai_env/                 # Virtual environment (after setup)
```

---

## 🛠️ Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:**
1. Create `.env` file in project root
2. Add: `GEMINI_API_KEY=your_key_here`
3. Restart the application

### Issue: "ModuleNotFoundError: No module named..."

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "ConnectionError" or "API Error"

**Solution:**
1. Check your internet connection
2. Verify API key is correct
3. Ensure you haven't exceeded rate limits (15 req/min)
4. Try again in a few moments

### Issue: Rate Limit Exceeded

**Solution:**
- The app automatically waits when rate limits are approaching
- Free tier: 15 requests/minute, 50 requests/day
- Wait for next minute or day to continue

### Issue: Streamlit port already in use

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 System Requirements

| Component | Requirement |
|-----------|-------------|
| **Python** | 3.8 or higher |
| **RAM** | 2GB minimum, 4GB recommended |
| **Disk Space** | 500MB for environment + dependencies |
| **Internet** | Required (for API calls) |
| **Browser** | Modern browser (Chrome, Firefox, Safari, Edge) |

---

## 🔒 Security & Privacy

- ✅ API keys stored locally in `.env` (never committed to git)
- ✅ Contracts processed through encrypted connections
- ✅ No data permanently stored on servers
- ✅ `.gitignore` prevents accidental key exposure
- ⚠️ **Always review generated contracts** - Not a substitute for legal advice

---

## 📝 Generated Contract Files

Contracts are automatically saved to `generated_contracts/` folder with naming format:

```
ContractType_Party1_Party2_YYYYMMDD_HHMMSS.txt
```

Example:
```
NDA_TechCorp_Inc_ConsultingFirm_LLC_20250828_181302.txt
```

---

## 📊 Usage Tracking

The application tracks:
- Total contracts generated
- Risk analyses performed
- Daily/monthly request counts
- Stored in `logs/usage.json`

Data is used to:
- Monitor API usage
- Track free tier limits
- Provide usage statistics dashboard

---

## ⚖️ Legal Disclaimer

**IMPORTANT:**
- Generated contracts are **templates** for reference
- **Not a substitute** for legal professional review
- Laws vary by jurisdiction
- **Always consult qualified legal counsel** before executing
- Users assume all responsibility for contract use
- Developers provide no legal warranty or liability

---

## 🆘 Getting Help

### Common Questions

**Q: Is this completely free?**
A: Yes! Uses Google's free Gemini API tier (15 req/min, 50 req/day)

**Q: Can I use generated contracts as-is?**
A: No, always have a lawyer review before execution

**Q: What contract types are supported?**
A: NDA, Service Agreements, Employment Agreements

**Q: How long does generation take?**
A: Typically 15-40 seconds depending on contract complexity

**Q: Can I modify the contracts after generation?**
A: Yes, download and edit in any text editor

### Contact & Support

- Check `.env` setup if experiencing API issues
- Review logs in `logs/` folder for error details
- Verify internet connection for API calls

---

## 🚀 Advanced Usage

### Custom Configuration

Edit environment variables in `.env`:

```bash
GEMINI_API_KEY=your_key
MAX_TOKENS=2000
TEMPERATURE=0.1
```

### Running on Different Port

```bash
streamlit run app.py --server.port 9000
```

### Disable Auto-cleanup

In sidebar settings → uncheck "Auto-cleanup old files"

---

## 📈 Next Steps

1. ✅ Set up project with virtual environment
2. ✅ Get and configure Gemini API key
3. ✅ Run the application
4. ✅ Generate your first contract
5. ✅ Analyze contracts for risks
6. ✅ Download and review results
7. ✅ Consult with legal professionals

---

## 📜 License & Attribution

- Built with **Google Gemini API** (Free Tier)
- Powered by **Streamlit** framework
- Uses **Python** and open-source libraries

---

**⚖️ Legal AI Contract Generator v1.0.0**  
*Professional contract generation, powered by AI*

---

**Last Updated:** December 2024  
**Status:** ✅ Production Ready


This README provides:
- ✅ Clear step-by-step setup instructions
- ✅ API key configuration guide
- ✅ Quick start section
- ✅ Troubleshooting guide
- ✅ System requirements
- ✅ Usage guide with examples
- ✅ Security & privacy information
- ✅ Legal disclaimers
- ✅ Project structure overview
- ✅ FAQ and support information

The instructions work for Windows, macOS, and Linux users!This README provides:
- ✅ Clear step-by-step setup instructions
- ✅ API key configuration guide
- ✅ Quick start section
- ✅ Troubleshooting guide
- ✅ System requirements
- ✅ Usage guide with examples
- ✅ Security & privacy information
- ✅ Legal disclaimers
- ✅ Project structure overview
- ✅ FAQ and support information

The instructions work for Windows, macOS, and Linux users!