#!/usr/bin/env python3
"""
Image Organizer by Date

This script organizes images into folders by date (year-month).
It extracts date information from filenames or uses file modification dates.

Usage:
1. Place this script in any directory
2. Run: python organize_images_by_date.py /path/to/your/images
   (Replace /path/to/your/images with the actual path to your image folder)

The script will:
- Create a new "organized" folder in the same directory as your images
- Sort all images into year-month folders (e.g., 2023-05 for May 2023)
- Keep the original files intact

"""

import os
import re
import sys
import shutil
from datetime import datetime

def organize_images(source_dir):
    """
    Organize images from source_dir into folders by date.

    Args:
        source_dir: Directory containing images to organize
    """
    # Ensure source directory exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return False

    # Create target directory
    parent_dir = os.path.dirname(os.path.abspath(source_dir))
    target_dir = os.path.join(parent_dir, "organized")
    os.makedirs(target_dir, exist_ok=True)

    # Regular expression to match date patterns in filenames
    date_patterns = [
        # YYYYMMDD_HHMMSS format (common in smartphone photos)
        r'^(\d{4})(\d{2})(\d{2})_',
        # IMG-YYYYMMDD-WA format
        r'IMG-(\d{4})(\d{2})(\d{2})-',
        # Other potential date formats can be added here
    ]

    # Dictionary to track which files have been processed
    processed_files = {}

    # Create a folder for files without clear date information
    unknown_date_dir = os.path.join(target_dir, "unknown_date")
    os.makedirs(unknown_date_dir, exist_ok=True)

    # Process each file in the source directory
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Skip if not a file
            if not os.path.isfile(file_path):
                continue

            # Skip if not an image file (based on common extensions)
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
            if not any(filename.lower().endswith(ext) for ext in image_extensions):
                continue

            # Try to extract date from filename using patterns
            date_found = False

            for pattern in date_patterns:
                match = re.search(pattern, filename)
                if match:
                    year, month, day = match.groups()

                    # Create year/month directory if it doesn't exist
                    year_month_dir = os.path.join(target_dir, f"{year}-{month}")
                    os.makedirs(year_month_dir, exist_ok=True)

                    # Copy file to the appropriate directory
                    dest_path = os.path.join(year_month_dir, filename)
                    shutil.copy2(file_path, dest_path)

                    print(f"Copied {filename} to {year_month_dir}")
                    processed_files[filename] = f"{year}-{month}"
                    date_found = True
                    break

            # If no date pattern found in filename, use file modification time
            if not date_found:
                try:
                    # Get file modification time
                    mtime = os.path.getmtime(file_path)
                    dt = datetime.fromtimestamp(mtime)
                    year = dt.strftime("%Y")
                    month = dt.strftime("%m")

                    # Create year/month directory if it doesn't exist
                    year_month_dir = os.path.join(target_dir, f"{year}-{month}")
                    os.makedirs(year_month_dir, exist_ok=True)

                    # Copy file to the appropriate directory
                    dest_path = os.path.join(year_month_dir, filename)
                    shutil.copy2(file_path, dest_path)

                    print(f"Copied {filename} to {year_month_dir} (using file modification time)")
                    processed_files[filename] = f"{year}-{month}"
                except Exception as e:
                    # If all else fails, put in unknown_date directory
                    dest_path = os.path.join(unknown_date_dir, filename)
                    shutil.copy2(file_path, dest_path)
                    print(f"Copied {filename} to unknown_date directory (error: {e})")
                    processed_files[filename] = "unknown_date"

    # Print summary
    print("\nSummary of organization:")
    year_month_counts = {}
    for filename, year_month in processed_files.items():
        year_month_counts[year_month] = year_month_counts.get(year_month, 0) + 1

    for year_month, count in sorted(year_month_counts.items()):
        print(f"{year_month}: {count} files")

    print(f"\nTotal files processed: {len(processed_files)}")
    print(f"\nOrganized files are in: {target_dir}")

    return True

def main():
    # Check if source directory is provided
    if len(sys.argv) < 2:
        print("Usage: python organize_images_by_date.py /path/to/your/images")
        print("Please provide the path to your image directory.")
        return

    source_dir = sys.argv[1]
    print(f"Organizing images in: {source_dir}")
    organize_images(source_dir)

if __name__ == "__main__":
    main()
