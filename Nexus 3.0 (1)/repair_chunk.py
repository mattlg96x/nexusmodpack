import os
import json

# === PATHS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
chunk_path = os.path.join(script_dir, "sliced_json", "chunk_1.json")
output_folder = os.path.join(script_dir, "repaired_json")
os.makedirs(output_folder, exist_ok=True)
repaired_path = os.path.join(output_folder, "chunk_1_repaired.json")

# === LOAD JSON ===
try:
    with open(chunk_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ JSON error: {e}")
    exit()
except Exception as e:
    print(f"❌ Other loading error: {e}")
    exit()

# === CLEAN FUNCTION ===
def clean_json(obj):
    if isinstance(obj, dict):
        return {
            k: clean_json(v)
            for k, v in obj.items()
            if v not in (None, "", [], {}, "null", "Null")
        }
    elif isinstance(obj, list):
        return [clean_json(item) for item in obj if item not in (None, "", [], {}, "null", "Null")]
    else:
        return obj

# === REPAIR AND SAVE ===
cleaned_data = clean_json(data)

with open(repaired_path, 'w', encoding='utf-8') as out:
    json.dump(cleaned_data, out, indent=2)

print(f"✅ Repaired file saved to: {repaired_path}")