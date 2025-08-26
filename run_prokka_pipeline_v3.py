import os
import subprocess
import glob
import argparse
from multiprocessing import Pool
from functools import partial
import logging

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Hardcoded Configuration ---
# The directory containing your .fna genome files.
INPUT_DIRECTORY = "/data/Share/zhanxy_data/BP_research/BP_975_25_fna"
# The main directory where all annotation output folders will be stored.
OUTPUT_DIRECTORY = "BP_975_25_annonation_prokka"


def run_prokka_for_single_file(fna_file_path: str, main_output_dir: str):
    """
    Executes the Prokka annotation command for a single .fna file, with a check
    to skip if already completed.
    """
    try:
        base_name = os.path.splitext(os.path.basename(fna_file_path))[0]
        annotation_output_dir = os.path.join(main_output_dir, base_name)

        # Resumability Check
        success_flag_file = glob.glob(os.path.join(annotation_output_dir, '*.gff'))
        if os.path.isdir(annotation_output_dir) and success_flag_file:
            logging.info(f"Skipping {base_name}: Annotation already found.")
            return (fna_file_path, True, "Skipped (already complete)")

        logging.info(f"Starting Prokka annotation for: {base_name}")

        command = [
            'prokka',
            '--outdir', annotation_output_dir,
            '--prefix', base_name,
            '--force',
            '--cpus', '32',
            fna_file_path
        ]

        process_result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        logging.info(f"Successfully completed annotation for: {base_name}")
        return (fna_file_path, True, "Success")

    except FileNotFoundError:
        error_message = "Error: 'prokka' command not found. Is Prokka installed and in your system's PATH?"
        logging.error(error_message)
        return (fna_file_path, False, error_message)

    except subprocess.CalledProcessError as e:
        error_message = f"Prokka failed for {base_name}. Stderr:\n{e.stderr}"
        logging.error(error_message)
        return (fna_file_path, False, e.stderr)
        
    except Exception as e:
        error_message = f"An unexpected error occurred for {base_name}: {str(e)}"
        logging.error(error_message)
        return (fna_file_path, False, str(e))

def main():
    """Main function to parse arguments and orchestrate the pipeline."""
    parser = argparse.ArgumentParser(
        description="Run Prokka annotation with hardcoded paths (v3 - Resumable).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--processes',
        type=int,
        default=10,
        help='Number of parallel Prokka processes to run. Default is 10.'
    )
    args = parser.parse_args()

    # --- Use Hardcoded Paths ---
    input_dir = INPUT_DIRECTORY
    output_dir = OUTPUT_DIRECTORY

    logging.info(f"Input directory: {input_dir}")
    logging.info(f"Output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    fna_files = glob.glob(os.path.join(input_dir, '*.fna'))
    if not fna_files:
        logging.warning(f"No .fna files found in {input_dir}. Please check the path. Exiting.")
        return

    logging.info(f"Found {len(fna_files)} .fna files to process.")

    logging.info(f"Starting parallel annotation with {args.processes} processes...")
    worker_func = partial(run_prokka_for_single_file, main_output_dir=output_dir)
    
    with Pool(processes=args.processes) as pool:
        results = pool.map(worker_func, fna_files)

    logging.info("All Prokka processes have completed. Reporting summary...")
    success_count = 0
    skipped_count = 0
    failed_files = []
    for fna_file, success, message in results:
        if success:
            if message == "Skipped (already complete)":
                skipped_count += 1
            else:
                success_count += 1
        else:
            failed_files.append((fna_file, message))
    
    total_processed = success_count + skipped_count + len(failed_files)
    logging.info(f"Summary: {success_count} new annotations, {skipped_count} skipped, {len(failed_files)} failed out of {total_processed} total files.")
    if failed_files:
        logging.error("The following files failed annotation:")
        for fna_file, error_msg in failed_files:
            logging.error(f"- {os.path.basename(fna_file)}")

if __name__ == '__main__':
    main()