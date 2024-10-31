import os
import subprocess
import glob
import shutil

def convert_pptx_to_png(input_folder, output_folder):
    """
    Converts each .pptx file in the input_folder to PNG images for each slide.
    The images are saved in the output_folder with filenames like 'filename_slide1.png'.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all .pptx files in the input folder
    pptx_files = glob.glob(os.path.join(input_folder, '*.pptx'))

    if not pptx_files:
        print(f"No .pptx files found in {input_folder}.")
        return

    for pptx_path in pptx_files:
        # Extract the base filename without extension
        base_name = os.path.splitext(os.path.basename(pptx_path))[0]
        
        # Create a temporary directory for conversion
        temp_dir = os.path.join(output_folder, f"{base_name}_temp")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Step 1: Convert pptx to pdf using LibreOffice
            print(f"Converting '{pptx_path}' to PDF...")
            subprocess.run([
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', temp_dir,
                pptx_path
            ], check=True)

            pdf_path = os.path.join(temp_dir, f"{base_name}.pdf")
            if not os.path.isfile(pdf_path):
                print(f"Failed to create PDF for '{pptx_path}'. Skipping...")
                continue

            # Step 2: Convert pdf to png using pdftoppm
            print(f"Converting '{pdf_path}' to PNG images...")
            subprocess.run([
                'pdftoppm',
                '-png',
                '-r', '300',  # Resolution (optional)
                pdf_path,
                os.path.join(temp_dir, base_name)
            ], check=True)

            # The above command creates files like 'base_name-1.png', 'base_name-2.png', etc.
            png_pattern = os.path.join(temp_dir, f"{base_name}-*.png")
            png_files = sorted(glob.glob(png_pattern))

            if not png_files:
                print(f"No PNG files were generated for '{pptx_path}'.")
                continue

            for index, png_path in enumerate(png_files, start=1):
                # Define the new filename
                new_filename = f"{base_name}_slide{index}.png"
                new_path = os.path.join(output_folder, new_filename)
                
                # Move and rename the file
                shutil.move(png_path, new_path)
                print(f"Created '{new_path}'")

        except subprocess.CalledProcessError as e:
            print(f"Failed to convert '{pptx_path}'. Error: {e}")

        finally:
            # Remove the temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    print("Conversion process completed.")

if __name__ == "__main__":
    INPUT_FOLDER = 'data'     # Replace with your input folder path
    OUTPUT_FOLDER = 'slides'  # Replace with your desired output folder path
    
    convert_pptx_to_png(INPUT_FOLDER, OUTPUT_FOLDER)
