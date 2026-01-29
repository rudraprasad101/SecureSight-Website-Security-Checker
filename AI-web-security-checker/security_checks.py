"""
Security Checks Module
Performs basic security checks on websites without any illegal hacking.
Safe and ethical checks only - suitable for authorized test sites.
"""

import requests
from typing import List, Dict
import logging

# Setup logging for error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_https(url: str) -> Dict:
    """
    Check if the website uses HTTPS (secure connection).
    HTTPS is the encrypted version of HTTP - required for security.
    
    Args:
        url: Website URL to check
        
    Returns:
        Dictionary with issue details
    """
    if not url.startswith("https://"):
        return {
            "title": "Missing HTTPS",
            "severity": "High",
            "details": "Website does not use HTTPS encryption. This means data sent between your browser and the website is not encrypted.",
            "fix": "Configure SSL/TLS certificate and redirect HTTP traffic to HTTPS. Most hosting providers offer free SSL certificates."
        }
    return None


def check_security_headers(url: str) -> List[Dict]:
    """
    Check for missing security headers that protect against common attacks.
    
    Args:
        url: Website URL to check
        
    Returns:
        List of missing security headers issues
    """
    issues = []
    
    # Important security headers to check
    security_headers = {
        "Content-Security-Policy": "Prevents XSS (code injection) attacks by controlling what resources can load",
        "Strict-Transport-Security": "Forces browser to always use HTTPS connection",
        "X-Frame-Options": "Prevents clickjacking attacks (embedding site in malicious frames)",
        "X-Content-Type-Options": "Prevents browser from guessing file types (blocks MIME-type attacks)",
        "Referrer-Policy": "Controls what information is sent when visiting other sites",
        "Permissions-Policy": "Controls which browser features (camera, microphone) can be used"
    }
    
    try:
        # Send request to fetch headers (timeout after 10 seconds)
        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        
        # Check each security header
        for header, description in security_headers.items():
            if header not in headers:
                issues.append({
                    "title": f"Missing {header}",
                    "severity": "Medium",
                    "details": f"The {header} header is missing. {description}",
                    "fix": f"Add the '{header}' header to your web server configuration or application code."
                })
    except Exception as e:
        # Log error but don't crash - return empty list
        logger.error(f"Error checking security headers: {str(e)}")
    
    return issues


def check_server_header(url: str) -> Dict:
    """
    Check if the server header is exposed (reveals server software version).
    Exposed server info helps attackers target known vulnerabilities.
    
    Args:
        url: Website URL to check
        
    Returns:
        Dictionary with server exposure issue (or None if safe)
    """
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        
        # Check for Server header exposure
        if "Server" in headers:
            server_info = headers["Server"]
            return {
                "title": "Server Information Exposed",
                "severity": "Medium",
                "details": f"Server header reveals: '{server_info}'. This helps attackers identify vulnerabilities specific to this server version.",
                "fix": "Remove or obfuscate the Server header by configuring your web server to hide this information."
            }
    except Exception as e:
        logger.error(f"Error checking server header: {str(e)}")
    
    return None


def perform_security_scan(url: str) -> Dict:
    """
    Main function that performs all security checks on a website.
    Returns all issues found in a structured format.
    
    Args:
        url: Website URL to scan
        
    Returns:
        Dictionary containing status, issues, and metadata
    """
    issues = []
    
    # Ensure URL has proper format
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    try:
        # First, test if website is reachable
        response = requests.head(url, timeout=10, allow_redirects=True)
        status_code = response.status_code
        
        # Perform all security checks
        # 1. HTTPS check
        https_issue = check_https(url)
        if https_issue:
            issues.append(https_issue)
        
        # 2. Security headers check
        header_issues = check_security_headers(url)
        issues.extend(header_issues)
        
        # 3. Server exposure check
        server_issue = check_server_header(url)
        if server_issue:
            issues.append(server_issue)
        
        return {
            "success": True,
            "status_code": status_code,
            "issues": issues,
            "total_issues": len(issues),
            "message": f"Scan complete! Found {len(issues)} security issues."
        }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Error: Website took too long to respond (timeout). Please check the URL.",
            "issues": [],
            "total_issues": 0,
            "status_code": None
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "Error: Cannot connect to website. Please check the URL or internet connection.",
            "issues": [],
            "total_issues": 0,
            "status_code": None
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during scan: {str(e)}",
            "issues": [],
            "total_issues": 0,
            "status_code": None
        }
