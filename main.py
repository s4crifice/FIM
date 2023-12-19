import os
import hashlib
import time
import configparser
import logging

def calculate_checksum(file_path, algorithm='md5', block_size=65536):
    # Calculate the checksum of a file using the specified algorithm
    hasher = hashlib.new(algorithm)

    with open(file_path, 'rb') as file:
        buffer = file.read(block_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(block_size)

    return hasher.hexdigest()

def list_files_with_modification_time(paths, config):
    # Create a dictionary to store file information (hash and modification time)
    file_info_dict = {}

    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                # Ignore files based on the ignore list in the configuration
                if any(ignore_path in file_path for ignore_path in config.get('Monitoring', 'ignore_list').split(',')):
                    continue

                # Ignore files with disallowed extensions
                allowed_extensions = [ext.strip() for ext in config.get('Monitoring', 'allowed_extensions').split(',')]
                if not any(file_path.endswith(extension) for extension in allowed_extensions):
                    continue

                # Ignore files larger than the specified max size
                max_file_size = int(config.get('Monitoring', 'max_file_size'))
                if os.path.getsize(file_path) > max_file_size:
                    continue

                # Calculate the hash and get the modification time of the file
                hash_c = calculate_checksum(file_path, config.get('Monitoring', 'hash_algorithm'))
                mod_time = os.path.getmtime(file_path)

                if file_path in file_info_dict:
                    file_info_dict[file_path].append((hash_c, mod_time))
                else:
                    file_info_dict[file_path] = [(hash_c, mod_time)]

    return file_info_dict

def setup_logging(log_file, log_level):
    # Set up logging configuration
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    logging.basicConfig(filename=log_file, level=numeric_level, format='%(asctime)s [%(levelname)s] %(message)s')

def load_config(config_file='config.ini'):
    # Load the configuration from the specified file and perform validation
    config = configparser.ConfigParser()
    config.read(config_file)

    validate_config(config)

    return config

def validate_config(config):
    # Validate folder paths, allowed extensions, log level, hash algorithm, and monitor integrity
    folder_paths = config.get('Monitoring', 'folder_paths').split(',')
    for path in folder_paths:
        if not os.path.exists(path.strip()):
            raise ValueError(f"Invalid folder path: {path.strip()}")

    allowed_extensions = [ext.strip() for ext in config.get('Monitoring', 'allowed_extensions').split(',')]
    for ext in allowed_extensions:
        if not ext.startswith('.'):
            raise ValueError(f"Invalid extension: {ext}")

    log_level = config.get('Logging', 'log_level').upper()
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        raise ValueError(f"Invalid log level: {log_level}")

    hash_algorithm = config.get('Monitoring', 'hash_algorithm').lower()
    if hash_algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Invalid hash algorithm: {hash_algorithm}")

    monitor_integrity_hash = calculate_checksum(__file__)
    if monitor_integrity_hash != config.get('Security', 'monitor_integrity_hash'):
        raise ValueError('Integrity check failed. Exiting...')

def main():
    # Main monitoring loop
    config = load_config()

    paths = [p.strip() for p in config.get('Monitoring', 'folder_paths').split(',')]

    log_file = config.get('Logging', 'log_file')
    log_level = config.get('Logging', 'log_level')
    setup_logging(log_file, log_level)

    file_info_dict = list_files_with_modification_time(paths, config)

    while True:
        monitor = list_files_with_modification_time(paths, config)

        existing_files = set(file_info_dict.keys())
        current_files = set(file_path for file_path in monitor.keys())

        deleted_files = existing_files - current_files
        added_files = current_files - existing_files

        for deleted_file in deleted_files:
            logging.info(f'{deleted_file} - deleted')
            del file_info_dict[deleted_file]

        for added_file in added_files:
            logging.info(f'{added_file} - added')
            file_info_dict[added_file] = monitor[added_file]

        for file_path in existing_files.intersection(current_files):
            monitor_paths = set(monitor.keys())

            if file_path not in monitor_paths:
                logging.info(f'{file_path} - moved or renamed')

            for hash_value, mod_time in monitor[file_path]:
                if mod_time != file_info_dict[file_path][-1][1]:
                    logging.info(f'{file_path} - file has been changed (modification time)')
                    file_info_dict[file_path].append((hash_value, mod_time))
                elif hash_value != file_info_dict[file_path][-1][0]:
                    logging.info(f'{file_path} - file has been changed (checksum)')
                    file_info_dict[file_path].append((hash_value, mod_time))

        time.sleep(int(config.get('Monitoring', 'scan_interval')))

if __name__ == "__main__":
    main()