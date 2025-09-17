# icloud-photo-metadata-fixer
A Python script to process and clean up exported Apple iCloud Photos.

It automatically:
- Reads iCloud CSV metadata files (Photo Details…)
- Restores original creation dates on photos
- Updates file timestamps using Windows APIs
- Moves corrected files into a clean export folder
- (Optional) Supports metadata updates with ExifTool

This tool is useful when unzipping large multi-part iCloud Photo archives and wanting a properly organized, timestamp-corrected export.

# Steps:
1. Download and install the latest python from official python site: https://www.python.org/
2. Install the following modules via CMD `pip install -U pyexiftool pypiwin32`
2. Unzip all apple photos. Move all the unzipped folders to the input folder. The unzipped folders must start with the name "iCloud". Full name of a directory could be like "iCloud Photos Part 1 of 166", or something familiar.
3. Run script in at script location with `python .\icloud_metadata_inserter.py` (if it doesnt work: `& C:/Users/Admin/AppData/Local/Programs/Python/Python313/python.exe c:/REPOS/icloud-photo-metadata-fixer/icloud_metadata_inserter.py` alt: use visual code to run it.)
4. All corrected photo's with metadata will be moved to the export folder. All files that failed the metadata insert, stay at the original location.