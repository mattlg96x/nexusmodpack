import os
import json

# === PATH SETUP ===
script_dir = os.path.dirname(os.path.abspath(__file__))
chunk_path = os.path.join(script_dir, "sliced_json", "chunk_1.json")  # <-- FIXED HERE
report_path = os.path.join(script_dir, "structure_report.txt")

def analyze_json_structure(data, depth=0, key_summary=None):
    if key_summary is None:
        key_summary = {}

    if isinstance(data, dict):
        for key, value in data.items():
            key_summary.setdefault(key, {"count": 0, "types": set(), "empty": 0, "max_depth": depth})
            key_summary[key]["count"] += 1
            key_summary[key]["types"].add(type(value).__name__)
            if value in (None, "", [], {}):
                key_summary[key]["empty"] += 1
            key_summary[key]["max_depth"] = max(key_summary[key]["max_depth"], depth)
            analyze_json_structure(value, depth + 1, key_summary)

    elif isinstance(data, list):
        for item in data:
            analyze_json_structure(item, depth + 1, key_summary)

    return key_summary

# === LOAD JSON CHUNK ===
try:
    with open(chunk_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except Exception as e:
    print(f"❌ Failed to load JSON chunk: {e}")
    exit()

# === ANALYZE STRUCTURE ===
summary = analyze_json_structure(json_data)

# === WRITE REPORT ===
with open(report_path, 'w', encoding='utf-8') as report:
    report.write("🧬 JSON Structure Report\n")
    report.write("=========================\n\n")
    for key, info in summary.items():
        line = (
            f"- Key: '{key}'\n"
            f"  • Count: {info['count']}\n"
            f"  • Types: {', '.join(info['types'])}\n"
            f"  • Empty Values: {info['empty']}\n"
            f"  • Max Nesting Depth: {info['max_depth']}\n"
        )
        report.write(line + "\n")

print(f"✅ Structure report saved to: {report_path}")