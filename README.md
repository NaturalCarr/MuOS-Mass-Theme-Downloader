# Muxthm Downloader

This script downloads `.muxthm` files from the latest release of the specified GitHub repository. It ensures that file names are sanitized by replacing periods (`.`) with spaces (` `) except for the file extension.

## Features
- Fetches the latest release information from GitHub.
- Downloads `.muxthm` files to a specified directory.
- Displays real-time download progress and status.
- Handles errors with retry logic and logs them to a file.
- Sanitizes file names for better readability.

## Recent Updates
- **File Name Sanitization**: Periods in file names are now replaced with spaces, except for the file extension (e.g., `Birds.-.Orioles.x.Sakura` becomes `Birds - Orioles x Sakura`).

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

1. Ensure Python 3 is installed.
2. Run the script:
   ```bash
   python getall_muxthms.py
   ```
3. Downloaded files will be saved in the `muxthm_downloads` directory.

## Output

- Downloaded files will be saved in the `muxthm_downloads` directory (or the directory specified in `OUTPUT_DIR`).
- Errors will be logged in `muxthm_download_errors.log`.

## Example Output

```
Fetching latest release info...
Current Release: https://github.com/MustardOS/theme/releases/tag/v1.2.3
Download Directory: /path/to/muxthm_downloads
Found 3 .muxthm files to download.

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
