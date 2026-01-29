# 🔒 SecureSight:Web Security Checker

An easy-to-use web application that scans websites for common security issues and provides AI-powered explanations.

## ✨ Features

- **Automated Security Scans**
  - HTTPS encryption status
  - Missing security headers (CSP, HSTS, X-Frame-Options, etc.)
  - Server information exposure

- **AI-Powered Explanations**
  - Google Gemini provides detailed, beginner-friendly explanations
  - Step-by-step remediation guidance
  - Educational context for each finding

- **User-Friendly Interface**
  - Built with Streamlit for simplicity
  - Clean, intuitive design
  - Instant results with caching for performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (get one free from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AI-web-security-checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:8501`

## 📖 Usage

1. Enter a website URL in the input field
2. Click "Scan Website" to run security checks
3. Review the findings with severity levels
4. Click "✨ Generate AI Explanation" on any issue to get detailed guidance
5. Follow the step-by-step instructions to remediate

## 📁 Project Structure

```
ai_helper.py          # Gemini API integration & AI explanations
app.py                # Main Streamlit application
security_checks.py    # Security scanning functions
requirements.txt      # Python dependencies
.env.example          # Environment variable template
README.md             # This file
```

## 🔧 How It Works

1. **Security Scanning**: The app makes HTTP requests to check headers and SSL/TLS configuration
2. **Issue Detection**: Identifies missing security headers and encryption
3. **AI Explanation**: Uses Google Gemini to generate human-readable explanations and fixes
4. **Caching**: Responses are cached to reduce API calls and improve performance

## ⚠️ Important Notes

- **Ethical Use Only**: Only scan websites you own or have permission to test
- **No Hacking**: This tool only checks publicly visible configuration issues
- **Educational**: Designed for learning and security awareness

## 🛠️ Technologies

- **Streamlit** - Web UI framework
- **Google GenAI** - Generative AI integration
- **Requests** - HTTP client
- **Python 3.8+** - Programming language

## 📝 License

This project is provided as-is for educational and authorized security testing purposes.

## ❓ Troubleshooting

**"API key not found"**
- Make sure `.env` file exists and contains `GEMINI_API_KEY`
- Verify the API key is valid from Google AI Studio

**"Website scan fails"**
- Ensure the URL is valid and accessible
- Check your internet connection
- Some sites may block automated requests

**"AI explanation not showing"**
- Verify your Gemini API has quota remaining
- Check for any API errors in the sidebar
- Try clearing the AI cache using the sidebar button

---

**Made with ❤️ for web security awareness**

