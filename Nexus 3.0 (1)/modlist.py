import json
import argparse
import os

def extract_mods(modpack_path, format="txt"):
    input_path = os.path.join(modpack_path, "manifest.json")
    export_dir = os.path.join(modpack_path, "mod-export")
    os.makedirs(export_dir, exist_ok=True)
    output_path = os.path.join(export_dir, f"modlist.{format}")

    # Load manifest
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: Could not find manifest.json at {input_path}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Failed to parse JSON at {input_path}")
        return

    # Extract mod identifiers
    mods = []
    if "files" in data:
        for mod in data["files"]:
            mod_id = mod.get("projectID") or mod.get("fileID") or mod.get("name") or "Unknown Mod"
            mods.append(str(mod_id))
    elif "mods" in data:
        for mod in data["mods"]:
            mod_id = mod.get("modId") or mod.get("name") or "Unknown Mod"
            mods.append(mod_id)
    elif isinstance(data, list):
        for mod in data:
            mod_id = mod.get("modId") or mod.get("name") or "Unknown Mod"
            mods.append(mod_id)
    else:
        print("❌ Error: Unsupported JSON structure—no 'files' or 'mods' key found.")
        return

    # Write to file
    try:
        with open(output_path, "w", encoding="utf-8") as out:
            if format == "txt":
                out.write("\n".join(mods))
            elif format == "md":
                out.write("# Mod List\n\n" + "\n".join(f"- {mod}" for mod in mods))
            elif format == "json":
                json.dump(mods, out, indent=2)
            else:
                print("❌ Error: Invalid output format.")
                return
        print(f"✅ Exported {len(mods)} mods to: {output_path}")
    except Exception as e:
        print(f"❌ Error while writing output: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and export mod list from a Minecraft modpack manifest.")
    parser.add_argument(
        "-p", "--path",
        required=True,
        help="Path to your modpack folder (where manifest.json is located)"
    )
    parser.add_argument(
        "--format",
        default="txt",
        choices=["txt", "md", "json"],
        help="Output format: txt (default), md, or json"
    )
    args = parser.parse_args()
    extract_mods(args.path, args.format)
    