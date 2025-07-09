import os
import json

# === PATH SETUP ===
script_dir = os.path.dirname(os.path.abspath(__file__))
sliced_folder = os.path.join(script_dir, "sliced_json")
repaired_folder = os.path.join(script_dir, "repaired_json")
valid_folder = os.path.join(script_dir, "valid_json")

# Create folders if they don't exist
os.makedirs(repaired_folder, exist_ok=True)
os.makedirs(valid_folder, exist_ok=True)

# === TRACKERS ===
chunk_stats = {}

# === CLEAN + AUDIT FUNCTION ===
def clean_chunk(data):
    cleaned = []
    skipped = 0

    mods = data if isinstance(data, list) else list(data.values())
    for entry in mods:
        if not isinstance(entry, dict):
            skipped += 1
            continue

        mod_name = entry.get("name") or entry.get("fileName")
        if not mod_name:
            skipped += 1
            continue

        cleaned.append(entry)

    return cleaned, skipped

# === PROCESS CHUNKS ===
chunk_files = [f for f in os.listdir(sliced_folder) if f.endswith(".json")]

print(f"🔧 Repairing {len(chunk_files)} chunks...\n")

for file in chunk_files:
    input_path = os.path.join(sliced_folder, file)
    repaired_path = os.path.join(repaired_folder, file)
    valid_path = os.path.join(valid_folder, file)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
    except Exception:
        print(f"❌ Failed to load {file}")
        continue

    cleaned, skipped = clean_chunk(raw)
    total = len(raw) if isinstance(raw, list) else len(raw.values())

    # Save repaired file (all entries preserved)
    with open(repaired_path, 'w', encoding='utf-8') as out1:
        json.dump(raw, out1, indent=2)

    # Save valid mods only
    with open(valid_path, 'w', encoding='utf-8') as out2:
        json.dump(cleaned, out2, indent=2)

    # 🔍 Log per-chunk stats
    print(f"📂 {file}: {len(cleaned)} valid mods, {skipped} skipped (out of {total})")

    chunk_stats[file] = {
        "total": total,
        "usable": len(cleaned),
        "skipped": skipped
    }

# === PRINT SUMMARY REPORT ===
print("\n📋 Final Chunk Summary:\n")
for file, stats in sorted(chunk_stats.items()):
    print(f"{file}: {stats['usable']} usable mods, {stats['skipped']} skipped (out of {stats['total']})")

print("\n✅ All chunks processed and saved.")
print("📁 Repaired files → repaired_json/")
print("📦 Valid entries → valid_json/")