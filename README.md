# FIM (File Integrity Monitor)

## Overview
FIM is a Python script designed for real-time tracking of file changes within specified directories. It provides a robust file integrity monitoring solution to enhance security and ensure the integrity of critical files.

## Features
- **Real-time Monitoring:** Track changes to files in specified directories.
- **Multiple Paths:** Monitor multiple paths concurrently for comprehensive coverage.
- **Configurability:** Easily configure monitoring settings using the `config.ini` file.
- **Ignored Files/Folders:** Specify files and folders to be ignored during monitoring.
- **Allowed Extensions:** Define file extensions to include or exclude from monitoring.
- **File Size Management:** Set a maximum file size for efficient resource utilization.
- **Logging:** Log events with different levels (INFO, WARNING, ERROR) to a specified file.
- **Security Measures:** Ensure integrity with hash-based integrity checks on the monitor script.

## Getting Started

### Prerequisites
- Python 3.x
- hashlib library

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/s4crifice/fim.git
   ```

2. Run the hash.py program to calculate the MD5 hash of the main.py script:
   ```bash
   python hash.py
   ```
3. Update the monitor_integrity_hash in config.ini with the calculated MD5 hash.

4. Customize the config.ini file to meet your monitoring requirements.

### Configuration
**Monitoring Settings**:
  - folder_paths: Comma-separated list of paths to monitor.
  - hash_algorithm: Hashing algorithm to use (e.g., md5, sha256).
  - scan_interval: Time interval (in seconds) between scans.
  - ignore_list: Comma-separated list of files/folders to ignore.
  - max_file_size: Maximum file size to monitor (in bytes).
  - allowed_extensions: Comma-separated list of allowed file extensions.
    
**Logging Settings**:
  - log_file: Log file name/path.
  - log_level: Logging level (INFO, WARNING, ERROR).

**Security Settings**:
  - monitor_integrity_hash: MD5 hash of the main.py script.
    
### Usage
Run the main.py script to initiate the monitoring process:
```bash
python main.py
```

### Example Configuration
```ini
[Monitoring]
folder_paths = C:\Users\your_username\Documents\Project
hash_algorithm = md5
scan_interval = 1
ignore_list = test.file
max_file_size = 10485760
allowed_extensions = .txt, .log

[Logging]
log_file = monitor.log
log_level = INFO

[Security]
monitor_integrity_hash = 829ee92738a92f8e49186c849df6c965
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.
