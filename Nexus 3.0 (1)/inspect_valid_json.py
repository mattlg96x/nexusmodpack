import os
import json

# === Path Setup ===
script_dir = os.path.dirname(os.path.abspath(__file__))
valid_folder = os.path.join(script_dir, "valid_json")

# === List All Files ===
files = [f for f in os.listdir(valid_folder) if f.endswith(".json")]

print(f"\n📦 Found {len(files)} files in valid_json/\n")

for file in sorted(files):
    path = os.path.join(valid_folder, file)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        mods = data if isinstance(data, list) else list(data.values())
        print(f"{file}: {len(mods)} entries")
    except Exception:
        print(f"⚠️ Failed to load {file}")