from app.db.models.document import ValidationReport

def generate_html_report(report: ValidationReport) -> str:
    """
    Generates a simple standalone HTML document representing the Validation Report.
    """
    score = report.overall_score
    metrics = report.metrics
    issues = report.issues
    
    issues_html = ""
    for issue in issues:
        severity_color = "red" if issue.get("severity") == "ERROR" else "orange"
        issues_html += f"""
        <div class="issue {issue.get('severity', 'UNKNOWN').lower()}">
            <h3>[{issue.get('category', 'General')}] {issue.get('severity', 'UNKNOWN')}</h3>
            <p><strong>Page:</strong> {issue.get('page', 'N/A')}</p>
            <p><strong>Expected:</strong> {issue.get('expected', '')}</p>
            <p><strong>Actual:</strong> {issue.get('actual', '')}</p>
            <p><strong>Suggestion:</strong> {issue.get('suggestion', '')}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Compliance Report</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 40px; color: #333; }}
            h1 {{ border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }}
            .score-card {{ background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
            .score-card h2 {{ margin-top: 0; }}
            .issue {{ border: 1px solid #eaeaea; border-left: 5px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 4px; }}
            .issue.error {{ border-left-color: #e53e3e; }}
            .issue.warning {{ border-left-color: #dd6b20; }}
            .issue h3 {{ margin-top: 0; color: #1a202c; }}
        </style>
    </head>
    <body>
        <h1>Document Compliance Report</h1>
        <div class="score-card">
            <h2>Overall Score: {score:.1f}%</h2>
            <p><strong>Total Checks:</strong> {metrics.get('total_checks', 0)}</p>
            <p><strong>Passed:</strong> {metrics.get('passed_checks', 0)}</p>
            <p><strong>Failed:</strong> {metrics.get('failed_checks', 0)}</p>
        </div>
        
        <h2>Issues</h2>
        {issues_html if issues else "<p>No issues found! Perfect compliance.</p>"}
    </body>
    </html>
    """
    return html
