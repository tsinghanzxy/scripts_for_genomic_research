import os
import re
import sys

def find_dependencies(directory):
    """
    Analyzes Python files in a directory to find imported libraries.

    Args:
        directory (str): The path to the directory to search.

    Returns:
        set: A set of unique library names found.
    """
    dependencies = set()
    import_pattern = re.compile(r"^(?:import|from)\s+([a-zA-Z0-9_]+)")

    if not os.path.isdir(directory):
        print(f"Error: Directory not found at '{directory}'")
        return dependencies

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            match = import_pattern.match(line.strip())
                            if match:
                                # Exclude standard libraries by checking against a basic list
                                # This list is not exhaustive but covers common cases.
                                lib_name = match.group(1)
                                if lib_name not in sys.stdlib_module_names:
                                    dependencies.add(lib_name)
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

    return dependencies

def main():
    """
    Main function to execute the dependency analysis.
    """
    # --- IMPORTANT ---
    # Please change this path to the actual directory you want to analyze.
    scripts_directory = r"/mnt/hgfs/G/others/常用生物信息学脚本Linux命令/Scripts"
    # --- IMPORTANT ---

    print(f"Analyzing Python scripts in: {scripts_directory}\n")
    
    # A basic list of Python standard libraries to exclude.
    # This helps in filtering out built-in modules.
    if sys.version_info.major == 3:
        import stdlib_list
        sys.stdlib_module_names = stdlib_list.stdlib_list("3.10") # Adjust version if needed
    else:
        # Fallback for older python or if stdlib_list is not installed
        sys.stdlib_module_names = {'os', 'sys', 're', 'collections', 'math', 'datetime', 'json', 'argparse', 'subprocess'}


    found_libs = find_dependencies(scripts_directory)

    if not found_libs:
        print("No third-party libraries found or directory is empty.")
        return

    print("Found the following potential third-party libraries:")
    for lib in sorted(found_libs):
        print(f"- {lib}")

    print("\nTo install them, please run the following command in your terminal:")
    print("-" * 50)
    print(f"pip install {' '.join(sorted(found_libs))}")
    print("-" * 50)
    
    print("\nNote: You might need to install the 'stdlib-list' package first for better accuracy by running: pip install stdlib-list")


if __name__ == "__main__":
    main()
