# Erome Downloader

Erome Downloader is a user-friendly GUI application that simplifies the process of downloading content from erome.com using the gallery-dl tool.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
   - [Option 1: Run from source](#option-1-run-from-source)
   - [Option 2: Download and run the release version](#option-2-download-and-run-the-release-version)
4. [Usage](#usage)
5. [License](#license)
6. [Disclaimer](#disclaimer)

## Features

- Intuitive graphical user interface for easy operation
- Support for downloading from multiple URLs simultaneously
- Custom download directory selection
- Real-time progress tracking with estimated time of arrival (ETA)
- Download history management for easy access to previous downloads
- Ability to pause or stop ongoing downloads
- Option to open the download directory after completion
- Tooltip hints for better user guidance

## Requirements

- Windows 7/8/10/11 or macOS 10.12+
- For running from source:
  - Python 3.6+
  - tkinter (usually comes pre-installed with Python)
  - gallery-dl

## Installation

### Option 1: Run from source

1. Ensure you have Python 3.6+ installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/kehhhh/erome-downloader.git
   cd erome-downloader
   ```

3. Install the required dependencies:
   ```
   pip install gallery-dl
   ```

4. Run the application:
   ```
   python app.py
   ```

### Option 2: Download and run the release version

1. Go to the [Releases](https://github.com/kehhhh/erome-downloader/releases) page of this repository.
2. Run the `App.exe` executable.

## Usage

1. Launch the Erome Downloader application.

2. Enter one or more erome.com URLs in the input field, separated by commas.

3. Click "Select Download Directory" to choose where the files will be saved.

4. Click "⬇ Download" to start the download process.

5. Monitor the progress in the output area and progress bar.

6. Use the "⏹ Stop" button to cancel the download if needed.

7. View your download history by clicking "🕒 Download History".

8. After the download completes, you can click "Open Download Directory" to view the downloaded files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

Erome Downloader is intended for educational and personal use only. Please respect copyright laws and the terms of service of erome.com when using this application. The developers of this tool are not responsible for any misuse or any violations of erome.com's terms of service.
