import os
import json
from collections import Counter, defaultdict

# === PATHS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, "valid_json")  # ← Updated folder here

# === TRACKERS ===
usable_per_chunk = {}
skipped_per_chunk = {}
duplicates = Counter()
mod_chunk_map = defaultdict(set)

chunk_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

print(f"\n🔍 Analyzing {len(chunk_files)} valid chunks...\n")

for chunk_file in chunk_files:
    chunk_path = os.path.join(input_folder, chunk_file)
    try:
        with open(chunk_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        continue

    mods = data if isinstance(data, list) else list(data.values())
    usable = 0
    skipped = 0

    for mod in mods:
        if not isinstance(mod, dict):
            skipped += 1
           