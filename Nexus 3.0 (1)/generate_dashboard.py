import os
import json
from collections import defaultdict

# === PATHS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, "valid_json")
md_path = os.path.join(script_dir, "modpack_dashboard.md")
html_path = os.path.join(script_dir, "modpack_dashboard.html")

# === COLLECTIONS ===
all_mods = []
duplicate_tracker = defaultdict(int)
category_map = defaultdict(list)
version_map = defaultdict(list)

# === MOD KEYS TO DISPLAY ===
display_keys = ["name", "version", "fileName", "downloadUrl", "categoryIds"]

chunk_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

# === PROCESS MODS FROM CHUNKS ===
for chunk_file in chunk_files:
    chunk_path = os.path.join(input_folder, chunk_file)
    try:
        with open(chunk_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        continue

    mods = data if isinstance(data, list) else list(data.values())
    for mod in mods:
        if not isinstance(mod, dict):
            continue

        entry = {k: mod.get(k, "") for k in display_keys}
        entry["sourceChunk"] = chunk_file  # ✅ Always attach chunk name

        norm_name = entry.get("name") or entry.get("fileName", "").lower()
        if norm_name:
            duplicate_tracker[norm_name] += 1

        all_mods.append(entry)

        for cat in entry.get("categoryIds", []):
            category_map[str(cat)].append(entry)

        version = entry.get("version", "Unknown")
        version_map[version].append(entry)

# === BUILD DASHBOARD CONTENT ===
md_lines = ["# 📊 Nexus 2.0 Modpack Dashboard", "---"]
html_lines = [
    "<html><head><title>Modpack Dashboard</title><style>body{font-family:sans-serif;}",
    "table{border-collapse:collapse;width:100%;}th,td{border:1px solid #ccc;padding:6px;}th{background:#eee;}</style></head><body>",
    "<h1>📊 Nexus 2.0 Modpack Dashboard</h1><hr>"
]

# === SUMMARY ===
md_lines.append(f"**Total Mods:** {len(all_mods)}")
md_lines.append(f"**Unique Names:** {len(duplicate_tracker)}")
md_lines.append(f"**Duplicates Detected:** {sum(1 for count in duplicate_tracker.values() if count > 1)}")
md_lines.append(f"**Unique Categories:** {len(category_map)}")
md_lines.append(f"**Detected Versions:** {len(version_map)}\n")

html_lines.append(f"<p><strong>Total Mods:</strong> {len(all_mods)}<br>")
html_lines.append(f"<strong>Unique Names:</strong> {len(duplicate_tracker)}<br>")
html_lines.append(f"<strong>Duplicates Detected:</strong> {sum(1 for count in duplicate_tracker.values() if count > 1)}<br>")
html_lines.append(f"<strong>Unique Categories:</strong> {len(category_map)}<br>")
html_lines.append(f"<strong>Detected Versions:</strong> {len(version_map)}</p><hr>")

# === MOD TABLE ===
md_lines.append("## 🔍 Mod List\n")
html_lines.append("<table><tr><th>Name</th><th>Version</th><th>Chunk</th><th>Category</th><th>Download</th><th>Missing</th></tr>")

for mod in all_mods:
    name = mod.get("name") or mod.get("fileName", "Unnamed Mod")
    version = mod.get("version", "Unknown")
    chunk = mod.get("sourceChunk", "—")
    category = ", ".join(map(str, mod.get("categoryIds", []))) or "Uncategorized"
    url = mod.get("downloadUrl", "")
    missing = [k for k in ["name", "version", "downloadUrl"] if not mod.get(k)]
    flag = f"⚠️ Missing: {', '.join(missing)}" if missing else ""

    # === Safe Markdown Construction ===
    line_md = f"- **{name}** | 🏷 `{version}` | 📁 `{category}` | 📄 `{chunk}`"
    if url:
        line_md += f" | 🔗 [Download]({url})"
    if flag:
        line_md += f" | {flag}"
    md_lines.append(line_md)

    # === HTML Row ===
    html_lines.append("<tr>")
    html_lines.append(f"<td>{name}</td><td>{version}</td><td>{chunk}</td><td>{category}</td>")
    html_lines.append(f"<td><a href='{url}'>Link</a></td>" if url else "<td>—</td>")
    html_lines.append(f"<td>{flag}</td></tr>")

html_lines.append("</table></body></html>")

# === SAVE FILES ===
with open(md_path, 'w', encoding='utf-8') as out_md:
    out_md.write("\n".join(md_lines))

with open(html_path, 'w', encoding='utf-8') as out_html:
    out_html.write("\n".join(html_lines))

print(f"✅ Markdown dashboard saved to: {md_path}")
print(f"✅ HTML dashboard saved to: {html_path}")
print(f"🔍 Dashboard includes {len(all_mods)} mods.")