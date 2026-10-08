"""
Report Formatting & Export Utilities
Author: Gyatchut (gyatchut@gmail.com)
License: Apache-2.0
"""

import json
from datetime import datetime
from typing import Dict, Any

class ReportExporter:
    @staticmethod
    def format_audit_summary(
        target_name: str,
        audit_type: str,
        content: str,
        model_name: str = "gemma-4-26b-a4b-it"
    ) -> Dict[str, Any]:
        """Creates a structured JSON summary object of an audit."""
        return {
            "project": "GemmaLens",
            "target": target_name,
            "audit_type": audit_type,
            "model": model_name,
            "timestamp": datetime.now().isoformat(),
            "raw_findings": content,
            "version": "1.0.0"
        }

    @staticmethod
    def to_markdown_report(summary: Dict[str, Any]) -> str:
        """Converts structured summary into a formatted markdown audit sheet."""
        return f"""# GemmaLens Audit Report: {summary['target']}

- **Audit Category:** {summary['audit_type']}
- **Model Engine:** {summary['model']}
- **Generated At:** {summary['timestamp']}

---

## Detailed Findings

{summary['raw_findings']}

---
*Report generated automatically by GemmaLens under Apache-2.0.*
"""
