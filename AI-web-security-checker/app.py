"""
AI Website Security Checker - Main Application
A beginner-friendly tool to check websites for common security issues.

This is a Streamlit web application that performs ethical security scans.
It only checks for publicly visible security misconfigurations - NO hacking.
"""

import streamlit as st
from security_checks import perform_security_scan
from ai_helper import generate_ai_prompt, generate_ai_explanation, is_api_configured, clear_ai_cache
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SecureSight AI",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session storage for AI responses
if "ai_responses" not in st.session_state:
    st.session_state["ai_responses"] = {}

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    .main-title {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .severity-high {
        color: #d62728;
        font-weight: bold;
    }
    .severity-medium {
        color: #ff7f0e;
        font-weight: bold;
    }
    .severity-low {
        color: #2ca02c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown("<h1 class='main-title'>🔒SecureSight AI: Website Security Checker</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Check websites for common security issues (Ethical & Safe)</p>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - INFORMATION & ETHICS WARNING
# ============================================================================

with st.sidebar:
    st.header("ℹ️ About This Tool")
    
    st.markdown("""
    ### What This Tool Does:
    ✅ Checks for HTTPS encryption
    ✅ Scans for missing security headers
    ✅ Detects exposed server information
    ✅ Generates AI explanations
    
    ### What This Tool Does NOT Do:
    ❌ No hacking or penetration testing
    ❌ No password cracking
    ❌ No unauthorized access
    ❌ No network attacks
    
    ### Ethical Use Only:
    🟢 Test on YOUR OWN websites
    🟢 Use authorized test sites like:
    - http://testphp.vulnweb.com
    🔴 NEVER scan websites you don't own without permission
    """)
    
    st.divider()
    
    st.header("📚 How to Use")
    st.markdown("""
    1. Enter a website URL
    2. Click "Scan Website"
    3. Review security issues found
    4. Read AI explanations for each issue
    5. Use AI prompts to learn more
    """)

    st.divider()
    st.header("🔗 AI Configuration")
    api_ok, api_msg = is_api_configured()
    if api_ok:
        st.success("Gemini API configured")
        if st.button("Clear AI cache"):
            cleared = clear_ai_cache()
            if cleared:
                st.info("AI response cache cleared.")
            else:
                st.warning("Failed to clear cache.")
    else:
        st.warning(f"AI not ready: {api_msg}")

# ============================================================================
# MAIN INPUT SECTION
# ============================================================================

st.subheader("🌐 Enter Website URL")

# Create two columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input(
        "Website URL",
        placeholder="https://example.com or testphp.vulnweb.com",
        label_visibility="collapsed"
    )

with col2:
    scan_button = st.button("🔍 Scan Website", use_container_width=True)

# ============================================================================
# SCAN EXECUTION & RESULTS
# ============================================================================

if scan_button:
    # Validate that URL is provided
    if not url_input.strip():
        st.error("❌ Please enter a website URL")
    else:
        # Show spinning loader while scanning
        with st.spinner("🔄 Scanning website... This may take a few seconds"):
            # Perform the security scan
            results = perform_security_scan(url_input)
        
        # ====================================================================
        # SCAN RESULTS DISPLAY
        # ====================================================================
        
        # Show status message
        if results["success"]:
            st.success(f"✅ {results['message']}")
            st.info(f"**HTTP Status Code:** {results['status_code']}")
        else:
            st.error(f"❌ {results['message']}")
        
        # Display summary statistics
        st.divider()
        st.subheader(f"📊 Scan Summary: Found {results['total_issues']} Issues")
        
        # ====================================================================
        # ISSUES DISPLAY
        # ====================================================================
        
        if results["issues"]:
            # Count issues by severity
            high_count = sum(1 for i in results["issues"] if i["severity"] == "High")
            medium_count = sum(1 for i in results["issues"] if i["severity"] == "Medium")
            low_count = sum(1 for i in results["issues"] if i["severity"] == "Low")
            
            # Display severity breakdown
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("🔴 High Severity", high_count)
            with metric_col2:
                st.metric("🟠 Medium Severity", medium_count)
            with metric_col3:
                st.metric("🟡 Low Severity", low_count)
            
            st.divider()
            
            # Display each issue in an expandable section
            st.subheader("🔍 Detailed Findings")
            
            for idx, issue in enumerate(results["issues"], 1):
                # Prepare key and expand if a cached AI response exists
                gen_key = f"gen_{idx}"
                is_expanded = gen_key in st.session_state.get("ai_responses", {})

                # Use expander for each issue; keep expanded if AI response present
                with st.expander(
                    f"Issue #{idx}: {issue['title']} - {issue['severity']} Severity",
                    expanded=is_expanded
                ):
                    # Display issue details in columns
                    detail_col1, detail_col2 = st.columns([1, 1])
                    
                    with detail_col1:
                        st.write("**📝 What is this?**")
                        st.write(issue["details"])
                        st.divider()
                        st.write("**⚠️ Severity:**")
                        severity_color = {"High": "🔴", "Medium": "🟠", "Low": "🟡"}
                        st.write(f"{severity_color.get(issue['severity'], '⚪')} {issue['severity']}")
                    
                    with detail_col2:
                        st.write("**🔧 How to Fix It**")
                        st.info(issue["fix"])
                        st.write("")
                    
                    # Divider between sections
                    st.divider()
                    
                    # AI Explanation Section
                    st.write("**🤖 Learn More with AI**")
                    st.markdown("Click the button below to get a detailed, step-by-step AI explanation of this issue.")
                    
                    # Live AI generation (works with GEMINI_API_KEY)
                    # Button to generate explanation
                    if st.button("✨ Generate AI Explanation", key=gen_key, use_container_width=True):
                        st.write("")  # Add spacing
                        
                        # Show loading message
                        loading_placeholder = st.empty()
                        loading_placeholder.info("🤔 **Gemini AI is thinking... Please wait...**")
                        
                        try:
                            # Call AI API
                            ai_text = generate_ai_explanation(issue)
                            
                            # Clear loading message
                            loading_placeholder.empty()
                            
                            # Persist into session state so it survives reruns
                            st.session_state["ai_responses"][gen_key] = ai_text
                            
                            # Display the result
                            st.divider()
                            
                            if "Error" in ai_text or "not found" in ai_text.lower() or "error" in ai_text.lower():
                                # Show error message
                                st.error("⚠️ Could not generate explanation")
                                st.warning(ai_text)
                            else:
                                # Show success message with AI response
                                st.success("✅ AI Explanation Generated Successfully!")
                                st.markdown(ai_text)
                                
                        except Exception as e:
                            loading_placeholder.empty()
                            st.error(f"Error: {str(e)}")
                            st.warning("Please try again or check your API key")

                    # If an AI response was previously generated, show it from session state
                    if gen_key in st.session_state.get("ai_responses", {}):
                        existing = st.session_state["ai_responses"][gen_key]
                        if existing:
                            st.divider()
                            if "Error" in existing or "not found" in existing.lower() or "error" in existing.lower():
                                st.error("⚠️ Previous AI attempt failed:")
                                st.warning(existing)
                            else:
                                st.success("✅ AI Explanation (cached)")
                                st.markdown(existing)
        
        else:
            st.success("""
            🎉 **Great News!**
            
            No major security issues were detected in this scan.
            However, this tool only checks for common header and HTTPS issues.
            For a complete security audit, consider:
            - Professional penetration testing
            - Security code review
            - Full vulnerability scanning tools
            """)

# ============================================================================
# FOOTER / ADDITIONAL INFORMATION
# ============================================================================

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    ### 📖 Learn Web Security
    - OWASP Top 10
    - Mozilla Security Guidelines
    - Security Headers checklist
    """)

with footer_col2:
    st.markdown("""
    ### 🧪 Test Sites (Safe Practice)
    - testphp.vulnweb.com
    - WebGoat (OWASP)
    - Damn Vulnerable Web App
    """)

with footer_col3:
    st.markdown("""
    ### ⚖️ Legal Reminder
    Only scan websites you own or have explicit permission to test.
    Unauthorized security testing is illegal!
    """)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 12px;'>"
    "AI Website Security Checker | Built for Learning | Ethical & Legal Use Only"
    "</p>",
    unsafe_allow_html=True
)
