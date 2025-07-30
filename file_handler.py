from pathlib import Path

def write_to_file_and_create_dir(file_path_str, content):
    """
    Writes content to a specified file, creating parent directories if they don't exist.

    Args:
        file_path_str (str): The path to the file, including its name.
        content (str): The string content to write to the file.
    """
    file_path = Path(file_path_str)
    
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content to the file
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(content)