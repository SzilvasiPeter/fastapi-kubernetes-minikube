from pathlib import Path
from datetime import date

import sys
import glob
import shutil

log_path = Path("/var/log/fastapi_app")
log_folder = log_path / "logs" if log_path.exists() else Path("logs")

if not log_folder.exists():
    sys.exit()

# Archive all log folders
shutil.make_archive(f"archived_{date.today()}", "gztar", log_folder)

# Get the old log folders
old_folders = glob.glob(log_folder.as_posix() + "/*")[5:]

# Delete the old log folders
for folder in old_folders:
    shutil.rmtree(folder)
