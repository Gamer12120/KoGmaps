import subprocess
import sys
import argparse
from pathlib import Path

# replace with wherever you have the executable
FIXER_PATH = "/home/teero/software/twmap/target/release/twmap-fix"

def process_map(map_path):
    """
    Handles the logic for fixing a single map file.
    Returns True if success, False otherwise.
    """
    temp_output = map_path.with_suffix(".map.fixed")
    try:
        result = subprocess.run(
            [FIXER_PATH, str(map_path), str(temp_output)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and temp_output.exists():
            temp_output.replace(map_path)
            print(f"OK: {map_path}")
            return True
        else:
            print(f"FAIL: {map_path}")
            if result.stdout: print(f"  Stdout: {result.stdout.strip()}")
            if result.stderr: print(f"  Stderr: {result.stderr.strip()}")
            if temp_output.exists(): temp_output.unlink()
            return False

    except Exception as e:
        print(f"EXCEPTION processing {map_path}: {e}")
        if temp_output.exists(): temp_output.unlink()
        return False

def fix_maps(target_path):
    """
    Determines if target is a file or directory and processes accordingly.
    """
    path = Path(target_path)
    if not path.exists():
        print(f"Error: Path '{target_path}' does not exist.")
        return

    if path.is_file():
        map_files = [path]
    elif path.is_dir():
        map_files = list(path.rglob("*.map"))
    else:
        print(f"Error: '{target_path}' is not a valid file or directory.")
        return

    if not map_files:
        print("No .map files found to process.")
        return

    print(f"Found {len(map_files)} target(s). Starting fix process...")

    success_count = sum(1 for f in map_files if process_map(f))
    fail_count = len(map_files) - success_count

    print("\n--- Summary ---")
    print(f"Successfully fixed: {success_count}")
    print(f"Failed:             {fail_count}")
    print(f"Total processed:    {len(map_files)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively fix .map files or process a single file.")
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Path to a .map file or a directory containing them (default: current directory)"
    )

    args = parser.parse_args()
    fix_maps(args.path)
