import os
import pywintypes
import win32file
import win32con
import csv
import glob
import shutil
import exiftool

inputfolder_name = "input"
exportfolder_name = "export"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def move_file(source_path, destination_dir):
    """
    Moves a file from a source path to a destination directory.

    Args:
        source_path (str): The full path of the file to be moved.
        destination_dir (str): The path of the directory to move the file into.
    """
    # Check if the source file exists
    if not os.path.exists(source_path):
        print(f"Error: Source file not found at '{source_path}'")
        return

    # Check if the destination directory exists and is a directory
    if not os.path.isdir(destination_dir):
        print(f"Error: Destination is not a valid directory at '{destination_dir}'")
        return

    # Construct the full destination path
    # os.path.basename() extracts the filename from the source path
    file_name = os.path.basename(source_path)
    destination_path = os.path.join(destination_dir, file_name)

    # Move the file
    try:
        shutil.move(source_path, destination_path)
        print(f"File '{file_name}' moved successfully to '{destination_dir}'")
    except Exception as e:
        print(f"An error occurred while moving the file: {e}")

def update_metadata_from_csv(folder_name):
    folder_path = os.path.join(script_dir, folder_name, "Photos")
    for csv_filepath in glob.glob(fr"{folder_path}\Photo Details*"):
        """
        Reads a CSV file and updates the metadata of corresponding files.
        """
        if not os.path.exists(csv_filepath):
            print(f"Error: The file '{csv_filepath}' was not found.")
            return

        print(f"Reading {csv_filepath}...")

        # We use a list to store the rows to avoid issues with reading and processing
        # at the same time.
        metadata_updates = []
        try:
            with open(csv_filepath, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Skip the header row
                metadata_updates = list(reader)
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return

        print("CSV file read successfully. Starting metadata updates...")

        # Initialize ExifTool
        with exiftool.ExifTool() as et:
            for row in metadata_updates:
                try:
                    from datetime import datetime
                    # Unpack the row data, assuming the order is consistent
                    img_name, file_checksum, favorite, hidden, deleted, \
                    original_creation_date, view_count, import_date = row

                    # Clean up the dates and remove surrounding quotes
                    original_creation_date = original_creation_date.strip('"')
                    import_date = import_date.strip('"')

                    imgpath = os.path.join(folder_path, img_name)

                    if not os.path.exists(imgpath):
                        print(f"Warning: File '{imgpath}' not found. Skipping.")
                        continue

                    print(f"Updating metadata for '{imgpath}'...")
                    date_object = datetime.strptime(original_creation_date, "%A %B %d,%Y %I:%M %p %Z")

                    handle = win32file.CreateFile(
                        imgpath,
                        win32con.GENERIC_WRITE,
                        0,
                        None,
                        win32con.OPEN_EXISTING,
                        0,
                        None
                    )

                    filetime = pywintypes.Time(date_object)
                    win32file.SetFileTime(handle, filetime, None, None) # Set CreationTime only (leave others as None if you don’t want to change them)
                    handle.close()

                    destination_folder = os.path.join(script_dir, exportfolder_name)
                    move_file(imgpath, destination_folder)

                    # # Takes a long time to apply!
                    # # Construct the ExifTool command.
                    # # The -overwrite_original flag is important to modify in place.
                    # # You can add more tags as needed.
                    # # Note: ExifTool writes dates in a specific format.
                    # command = [
                    #     f"-overwrite_original",
                    #     f"-xmp-photoshop:Source={file_checksum}",
                    #     f"-xmp:Favorite={favorite}",
                    #     f"-xmp:Hidden={hidden}",
                    #     f"-xmp:Deleted={deleted}",
                    #     f"-xmp:Created={original_creation_date}",
                    #     f"-xmp-photoshop:CreationDate={original_creation_date}",
                    #     f"-xmp:ViewCount={view_count}",
                    #     f"-xmp:ImportDate={import_date}",
                    #     imgpath
                    # ]
                    
                    # et.execute(*command)
                    # print(f"Successfully updated metadata with exiftool for '{imgpath}'.")

                except IndexError:
                    print(f"Skipping row due to incorrect format: {row}")
                except Exception as e:
                    print(f"An error occurred while processing '{row[0]}': {e}")

        print("Metadata update process completed.")

if __name__ == "__main__":
    try:
        os.makedirs((os.path.join(script_dir, exportfolder_name)), exist_ok=True)
        print(f"Directory '{exportfolder_name}' created successfully (or already exists).")
    except OSError as e:
        print(f"Error creating directory: {e}")
    
    try:
        os.makedirs((os.path.join(script_dir, inputfolder_name)), exist_ok=True)
        print(f"Directory '{inputfolder_name}' created successfully (or already exists).")
    except OSError as e:
        print(f"Error creating directory: {e}")
    
    # Find all directories that match the pattern "iCloud* in the input folder"
    for folder in glob.glob(os.path.join("input", "iCloud*/")):
        folder_name = folder.rstrip(os.path.sep)
        update_metadata_from_csv(folder_name)