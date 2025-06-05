import subprocess
import os

def convert_audio_files():
    """
    Converts audio files from a user-specified source folder and format
    to MP3 format in a user-specified destination folder using FFmpeg.
    """

    while True:
        source_folder_input = input("Enter the full path to the folder containing your audio files (e.g., /Users/YourName/Music/MyFlacs): ")
        source_folder = os.path.normpath(source_folder_input)
        if os.path.isdir(source_folder):
            break
        else:
            print("Error: The specified source folder does not exist. Please enter a valid path.")

    while True:
        source_format = input("Enter the current format of your audio files (e.g., FLAC, WAV, OGG): ").strip().lower()
        if source_format:
            break
        else:
            print("Error: Please enter a file format.")

    while True:
        destination_folder_input = input("Enter the full path to the folder where you want to save the converted MP3s (e.g., /Users/YourName/Music/MyMp3s): ")
        destination_folder = os.path.normpath(destination_folder_input)
        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        if os.path.isdir(destination_folder): # Check if it was created or already exists
            break
        else:
            print("Error: Could not create the destination folder. Please check the path and your permissions.")

    print(f"\nStarting conversion from '{source_folder}' ({source_format.upper()}) to '{destination_folder}' (MP3)...")

    converted_count = 0
    skipped_count = 0
    error_count = 0

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(f".{source_format}"):
            source_filepath = os.path.join(source_folder, filename)
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            mp3_filepath = os.path.join(destination_folder, mp3_filename)

            print(f"Converting '{filename}' to MP3...")

            try:
                # FFmpeg command to convert audio to MP3
                # -i: input file
                # -ab 320k: audio bitrate (320 kbps for high quality)
                # -map_metadata 0: copy metadata from input to output
                command = [
                    "ffmpeg",
                    "-i", source_filepath,
                    "-ab", "320k",
                    "-map_metadata", "0",
                    mp3_filepath
                ]
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Successfully converted '{filename}' to '{mp3_filename}'")
                converted_count += 1
            except subprocess.CalledProcessError as e:
                print(f"Error converting '{filename}':")
                print(f"  Standard Output: {e.stdout.decode()}")
                print(f"  Standard Error: {e.stderr.decode()}")
                error_count += 1
            except FileNotFoundError:
                print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your system's PATH.")
                return # Exit if FFmpeg is not found
            except Exception as e:
                print(f"An unexpected error occurred during conversion of '{filename}': {e}")
                error_count += 1
        else:
            print(f"Skipping '{filename}' (not a '{source_format}' file).")
            skipped_count += 1

    print("\nConversion process complete.")
    print(f"Summary:")
    print(f"  Converted: {converted_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")

if __name__ == "__main__":
    convert_audio_files()