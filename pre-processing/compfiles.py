import os

def get_all_files(directory):
    """Recursively get all file paths in a directory."""
    file_set = set()
    for root, _, files in os.walk(directory):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), directory)
            file_set.add(rel_path)
    return file_set

def compare_directories(dir1, dir2):
    """Compare two directories and find different filenames."""
    files1 = get_all_files(dir1)
    files2 = get_all_files(dir2)
    
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1
    
    if only_in_dir1:
        print(f"Files only in {dir1}:")
        for file in only_in_dir1:
            if not ".ds_store" in  file.lower():
                print(f"  {file}")
    
    if only_in_dir2:
        print(f"Files only in {dir2}:")
        for file in only_in_dir2:
            print(f"  {file}")
    
    if not only_in_dir1 and not only_in_dir2:
        print("Both directories have the same files.")

# Example usage
dir1 = "C:/Users/Lovelace/Downloads/TrashNet (Full Size)"
dir2 = "C:/Users/Lovelace/Downloads/datasets/TrashNet (Corrected)"
compare_directories(dir1, dir2)