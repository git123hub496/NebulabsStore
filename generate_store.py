import os
import json
import re

def generate_catalog():
    # Base URL pointing to your raw GitHub repository files
    base_url = "https://githubusercontent.com"
    apps = []

    # Loop through every directory to discover apps
    for folder in os.listdir("."):
        if os.path.isdir(folder) and not folder.startswith(".") and folder != "dist":
            app_id = f"com.nebulabs.{folder.lower().replace(' ', '')}"
            
            # 1. Read app description
            desc_path = os.path.join(folder, "description.txt")
            description = ""
            if os.path.exists(desc_path):
                with open(desc_path, "r", encoding="utf-8") as f:
                    description = f.read().strip()

            # 2. Map standard file assets
            # URL encodes spaces as %20 so web links don't break
            web_folder_name = folder.replace(" ", "%20")
            icon_url = f"{base_url}/{web_folder_name}/icon.png" if os.path.exists(os.path.join(folder, "icon.png")) else ""

            # 3. Locate the APK and parse version from its name
            version = 0
            download_url = ""
            
            for file in os.listdir(folder):
                if file.endswith(".apk"):
                    web_file_name = file.replace(" ", "%20")
                    download_url = f"{base_url}/{web_folder_name}/{web_file_name}"
                    match = re.search(r"(\d+)\.apk", file)
                    if match:
                        version = int(match.group(1))
                    break

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

    # NEW: Automatically creates a folder named 'dist' if it does not exist yet
    output_folder = "dist"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Saves the unified catalog file cleanly inside your new folder
    output_path = os.path.join(output_folder, "apps.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4)

if __name__ == "__main__":
    generate_catalog()
