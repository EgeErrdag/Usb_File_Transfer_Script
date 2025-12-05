# USB File Transfer Script

This Python script automatically detects connected USB drives and copies files from a specified source directory to the USB drive. It provides a graphical user interface (GUI) to monitor the progress of file transfers for multiple USB drives simultaneously.

## Features

- **Automatic Detection**: Automatically detects when a removable USB drive is connected.
- **Concurrent Copying**: Handles multiple USB drives at the same time using threading.
- **Progress Tracking**: Shows a progress bar, current file being copied, and estimated time remaining (ETA) for each drive.
- **Status Updates**: Displays status messages (e.g., "Checking...", "Completed", "Error").
- **Smart Copying**: Skips copying if the destination folder already exists on the USB drive.

## Prerequisites

- Python 3.x
- `psutil` library

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/Usb_File_Transfer_Script.git
    cd Usb_File_Transfer_Script
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the script:
    ```bash
    python Multiple_Usb_File_Transfer_Script.py
    ```

2.  If the source path is not configured in the script, a dialog box will appear asking you to select the folder you want to copy to the USB drives.

3.  Insert a USB drive. The script will detect it and start copying the files from the selected source folder to the USB drive.

## Configuration

You can hardcode the source path in the script by modifying the `SOURCE_PATH` variable in `Multiple_Usb_File_Transfer_Script.py`:

```python
SOURCE_PATH = Path(r"C:\Path\To\Your\Source\Folder")
```

If left empty, the script will prompt you to select a folder on startup.

## License

