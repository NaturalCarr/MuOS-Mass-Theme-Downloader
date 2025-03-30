# Muxthm Downloader

This script automates the process of downloading `.muxthm` files from the latest release of a specified GitHub repository. It ensures efficient downloading with retry mechanisms, progress tracking, and error logging.

## Features

- Fetches the latest release information from a GitHub repository.
- Downloads `.muxthm` files from the release assets.
- Displays real-time progress updates for downloads.
- Logs errors to a file for troubleshooting.
- Automatically retries failed downloads after a delay.

## Requirements

- Python 3.x
- Internet connection
- Permissions to create directories and write files in the script's directory.

## Configuration

The script includes the following configurable parameters:

- **REPO**: The GitHub repository to fetch releases from (e.g., `MustardOS/theme`).
- **OUTPUT_DIR**: The directory where downloaded files will be saved.
- **RETRY_DELAY**: The delay (in seconds) before retrying a failed download.
- **LOG_FILE**: The file where errors will be logged.

## Usage

1. Clone or download this repository to your local machine.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script using the following command:
   ```bash
   python getall_muxthms.py
   ```
4. The script will:
   - Fetch the latest release information.
   - Identify `.muxthm` files in the release assets.
   - Download the files to the specified output directory.
   - Display progress and log any errors.

## Output

- Downloaded files will be saved in the `muxthm_downloads` directory (or the directory specified in `OUTPUT_DIR`).
- Errors will be logged in `muxthm_download_errors.log`.

## Example Output

```
Fetching latest release info...
Current Release: https://github.com/MustardOS/theme/releases/tag/v1.2.3
Download Directory: /path/to/muxthm_downloads
Found 3 .muxthm files to download.

Downloading: theme1.muxthm [1.2 MB/1.2 MB]
Completed: 1/3 files, 1.2 MB/3.6 MB

Downloading: theme2.muxthm [1.1 MB/1.1 MB]
Completed: 2/3 files, 2.3 MB/3.6 MB

Downloading: theme3.muxthm [1.3 MB/1.3 MB]
Completed: 3/3 files, 3.6 MB/3.6 MB

All .muxthm downloads from latest release complete.
```

## Error Handling

If a download fails, the script will:
- Log the error in `muxthm_download_errors.log`.
- Retry the download after the specified delay.

## License

This script is provided "as is" without warranty of any kind. Feel free to modify and use it as needed.
