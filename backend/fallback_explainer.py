def generate_fallback_summary(rejection_report):
    lines = []

    for item in rejection_report: 
        reason = item["reason"]
        severity = item["severity"]
        details = item["details"]

        if details: 
            detail_text = ", ".join(details)
            lines.append(f"[{severity}] {reason}: {detail_text}.")
        else:
            lines.append(f"[{severity}] {reason}.")

    return "\n".join(lines)