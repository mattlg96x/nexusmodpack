import os

# === Dummy Mod Entry ===
mod = {
    "name": "TestMod",
    "version": "1.0.0",
    "sourceChunk": "chunk_1.json",
    "categoryIds": [100, 200],
    "downloadUrl": "https://example.com/mod.jar"
}

html_lines = [
    "<html><head><title>Test Dashboard</title><style>body{font-family:sans-serif;}",
    "table{border-collapse:collapse;width:100%;}th,td{border:1px solid #ccc;padding:6px;}th{background:#eee;}</style></head><body>",
    "<h1>🧪 Dashboard Sanity Check</h1><table><tr><th>Name</th><th>Version</th><th>Chunk</th><th>Category</th><th>Download</th></tr>"
]

html_lines.append("<tr>")
html_lines.append(f"<td>{mod['name']}</td><td>{mod['version']}</td><td>{mod['sourceChunk']}</td><td>{', '.join(map(str, mod['categoryIds']))}</td>")
html_lines.append(f"<td><a href='{mod['downloadUrl']}'>Link</a></td>")
html_lines.append("</tr></table></body></html>")

# === SAVE HTML FILE ===
test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_test.html")
with open(test_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(html_lines))

print(f"✅ Test dashboard saved to: {test_path}")