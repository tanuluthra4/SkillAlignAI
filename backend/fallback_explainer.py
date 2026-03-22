def generate_fallback_summary(rejection_report):
    lines = []

    for item in rejection_report: 
        reason = item.get("reason", "")
        severity = item.get("severity", "")
        details = item.get("details", "")

        if isinstance(details, str):
            details = [details]

        if details: 
            detail_text = ", ".join(details)
            lines.append(f"[{severity}] {reason}: {detail_text}.")
        else:
            lines.append(f"[{severity}] {reason}.")

    return "\n".join(lines)