# icloud-photo-metadata-fixer
A Python script to process and clean up exported Apple iCloud Photos.
It automatically:

- Reads iCloud CSV metadata files (Photo Details…)
- Restores original creation dates on photos
- Updates file timestamps using Windows APIs
- Moves corrected files into a clean export folder
- (Optional) Supports metadata updates with ExifTool

This tool is useful when unzipping large multi-part iCloud Photo archives and wanting a properly organized, timestamp-corrected export.


# Create a dir named icloud
# Unzip all apple photos to folders in the same direcory like dir:iCloud Photos Part 2 of 166, dir:iCloud Photos Part 3 of 166
# place this script in the same dir, and excecute it
# It creates a export file that moves all corrected photos in to
