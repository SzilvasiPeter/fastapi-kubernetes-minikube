from pathlib import Path
from datetime import date

import sys
import glob
import shutil

mnt_path = Path("/mnt/fastapi_app")
log_folder = mnt_path / "logs" if mnt_path.exists() else Path("logs")
archive_folder = mnt_path / "archives" if mnt_path.exists() else Path("archives")

if not log_folder.exists():
    sys.exit()

# Archive all log folders
archive_folder.mkdir(parents=True, exist_ok=True)
shutil.make_archive(f"{archive_folder}/archived_{date.today()}", "gztar", log_folder)

# Get the old log folders
old_folders = glob.glob(f"{log_folder}/*")[5:]

# Delete the old log folders
for folder in old_folders:
    shutil.rmtree(folder)
