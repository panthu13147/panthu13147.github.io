from pathlib import Path

# 1. Define where you want to save it
# (Current Folder -> "scraped_data.txt")
save_path = Path.cwd() / 'scraped_data.txt'

# 2. Preparation (Optional but smart)
# This checks if the file already exists
if not save_path.exists():
    print("Creating new file...")

# 3. Write the data
# This handles opening, writing, and closing automatically.
save_path.write_text("Bitcoin Price: $95,000")