import os

def scan_mods(mods_folder, output_path):
    print(f"[INFO] Targeting mods folder: {mods_folder}")

    if not os.path.exists(mods_folder):
        print(f"[ERROR] Mods folder not found: {mods_folder}")
        return

    all_files = os.listdir(mods_folder)
    print(f"[INFO] Found {len(all_files)} items in the mods folder:")

    mod_files = []
    for f in all_files:
        full_path = os.path.join(mods_folder, f)
        if os.path.isfile(full_path):
            if f.lower().endswith(".jar"):
                mod_files.append(f)
                print(f"[OK]   {f}")
            else:
                print(f"[SKIP] {f} (not a .jar)")
        else:
            print(f"[SKIP] {f} (not a file)")

    if not mod_files:
        print("[WARNING] No .jar files found. Nothing exported.")
        return

    mod_files.sort()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as out:
            out.write("\n".join(mod_files))
        print(f"[DONE] Exported {len(mod_files)} mods to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write output file: {e}")

if __name__ == "__main__":
    # ✅ Your actual mods folder (absolute path)
    mods_dir = r"C:\Users\gerar\curseforge\minecraft\Instances\Nexus 3.0 (1)\mods"

    # ✅ Output path (creates 'mod-export/' in the same folder as this script)
    export_file = os.path.join(os.path.dirname(__file__), "mod-export", "modlist_from_folder.txt")

    scan_mods(mods_dir, export_file)