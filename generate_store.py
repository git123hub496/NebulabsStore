import os
import json
import re

def generate_catalog():
    # Base URL pointing to your raw GitHub repository files
    base_url = "https://githubusercontent.com"
    apps = []

    # Loop through every directory to discover apps
    for folder in os.listdir("."):
        if os.path.isdir(folder) and not folder.startswith("."):
            app_id = f"com.nebulabs.{folder.lower()}"
            
            # 1. Read app description
            desc_path = os.path.join(folder, "description.txt")
            description = ""
            if os.path.exists(desc_path):
                with open(desc_path, "r", encoding="utf-8") as f:
                    description = f.read().strip()

            # 2. Map standard file assets
            icon_url = f"{base_url}/{folder}/icon.png" if os.path.exists(os.path.join(folder, "icon.png")) else ""

            # 3. Locate the APK and parse version from its name
            version = 0
            download_url = ""
            
            for file in os.listdir(folder):
                if file.endswith(".apk"):
                    download_url = f"{base_url}/{folder}/{file}"
                    match = re.search(r"(\d+)\.apk", file)
                    if match:
                        version = int(match.group(1))
                    break

            # Only append if an actual app package exists in the folder
            if download_url:
                app_entry = {
                    "app_id": app_id,
                    "app_name": folder,
                    "version": version,
                    "description": description,
                    "icon_url": icon_url,
                    "download_url": download_url
                }
                apps.append(app_entry)

    # Save to your structured catalog output file
    with open("apps.json", "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4)

if __name__ == "__main__":
    generate_catalog()
