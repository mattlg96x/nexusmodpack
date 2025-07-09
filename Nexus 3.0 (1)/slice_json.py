import os
import json

# === PATH SETUP ===
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "minecraftinstance.json")
output_folder = os.path.join(script_dir, "sliced_json")
report_path = os.path.join(script_dir, "validation_report.txt")
chunk_size = 1000  # number of lines per chunk

# === DISPLAY ===
print("🔍 Working directory:", script_dir)
print("📄 Target JSON file:", file_path)

# === FOLDER PREP ===
os.makedirs(output_folder, exist_ok=True)

# === READ FULL FILE ===
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    print("❌ File not found. Double-check the filename and path.")
    exit()

# === START REPORT FILE ===
with open(report_path, 'w', encoding='utf-8') as report:
    report.write("📋 Chunk Validation Report\n")
    report.write("==========================\n\n")

    # === CHUNKING + VALIDATION ===
    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        chunk_name = f"chunk_{i // chunk_size + 1}.json"
        chunk_path = os.path.join(output_folder, chunk_name)

        # Save the chunk
        with open(chunk_path, 'w', encoding='utf-8') as out:
            out.writelines(chunk)

        # Validate it
        try:
            with open(chunk_path, 'r', encoding='utf-8') as chunk_file:
                json.load(chunk_file)
            status = f"✅ {chunk_name} is valid"
        except json.JSONDecodeError as e:
            status = f"⚠️ {chunk_name} is invalid: {str(e).splitlines()[0]}"

        print(status)
        report.write(status + "\n")

print(f"\n📊 Validation complete! See: {report_path}")