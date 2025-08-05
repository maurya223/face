# Save this as image_converter.py in the same directory as project.py
from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

image_files = ["monu_fixed.jpg", "rohan_fixed.jpg"]

print(f"Attempting to reprocess images in: {script_dir}")

for img_file in image_files:
    original_path = os.path.join(script_dir, img_file)
    reprocessed_path = os.path.join(script_dir, img_file.replace(".jpg", "_reprocessed.jpg"))

    try:
        if not os.path.exists(original_path):
            print(f"❌ Original file not found: {original_path}. Skipping.")
            continue

        with Image.open(original_path) as img:
            img.convert("RGB").save(reprocessed_path, "JPEG", quality=95)
            print(f"✅ Successfully reprocessed {img_file} to {reprocessed_path}")
    except Exception as e:
        print(f"❌ Error reprocessing {img_file} at {original_path}: {e}")

print("\n--- Image Reprocessing Complete ---")
print("Please check your directory for files ending with '_reprocessed.jpg'.")
print("If successful, update your 'people' dictionary in project.py to use these new files (if you haven't already).")