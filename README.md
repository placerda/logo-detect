# logo-detect

This repository provides tools to convert PowerPoint presentations (`.pptx`) into images for each slide and then detect logos on those slides using Azure OpenAI. The project includes two main scripts:

## Files Overview

### 1. `convert_pptx_to_png.py`
Converts each `.pptx` file in a given input folder to PNG images for each slide. These images are saved in a specified output folder with filenames indicating the slide number. The conversion process involves:
- Converting `.pptx` files to PDF using LibreOffice.
- Converting the PDF into PNG images for each slide using `pdftoppm`.

#### Usage
1. Place your `.pptx` files in the input folder (e.g., `data`).
2. Run the script:
   ```bash
   python convert_pptx_to_png.py
   ```

3. The script will save PNG images for each slide in the output folder (e.g., `slides`). 

#### Configuration
The default directories for input and output are:
```python
INPUT_FOLDER = 'data'      # Path to the input folder with .pptx files
OUTPUT_FOLDER = 'slides'   # Path to the output folder for PNG images
```
You can change `INPUT_FOLDER` and `OUTPUT_FOLDER` to customize where files are read and saved.

### 2. `detect_logos_gpt4o.py`
Processes each PNG image of a slide, sending it to an Azure OpenAI model that detects company logos. The script reads all PNG files in a specified folder, converts each image to base64, and sends it to the OpenAI API. Results are saved in an output file with the detected logos for each slide.

#### Usage
1. Ensure that the PNG images from `convert_pptx_to_png.py` are in the slides directory (e.g., `slides`).
2. Run the script:
   ```bash
   python detect_logos_gpt4o.py
   ```
3. The results will be saved in an output file (`output/logos_output_gpt4o.txt`).

#### Configuration
The default directory for PNG files is:
```python
SLIDES_DIR = 'slides'  # Path to the folder with PNG files for processing
```
You can change `SLIDES_DIR` if your images are saved in a different directory.

#### Environment Variables
Before running `detect_logos_gpt4o.py`, create a `.env` file in the project root with the necessary Azure OpenAI API credentials. The file should contain:

- **`AZURE_OPENAI_API_KEY`**: Your API key for Azure OpenAI.
- **`AZURE_OPENAI_ENDPOINT`**: The endpoint URL for Azure OpenAI.
- **`AZURE_OPENAI_DEPLOYMENT_ID`**: The deployment ID of your model.

An example `.env` file:
```plaintext
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your_endpoint.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_ID=your_deployment_id
```
These values will be used by `detect_logos_gpt4o.py` to authenticate and interact with the Azure OpenAI API.

## Prerequisites

- **Python** (3.11 or later)
- **LibreOffice**: Required for converting `.pptx` to PDF on Linux.
- **poppler-utils**: Required for converting PDF to PNG.
- **Java**: Needed for LibreOffice if not already installed.

## Installation on Linux

1. **Install LibreOffice**:
   ```bash
   sudo apt update
   sudo apt install -y libreoffice-core libreoffice-impress libreoffice-script-provider-python
   sudo apt upgrade -y libreoffice
   ```
   
2. **Install Java (if needed)**:
   ```bash
   sudo apt install -y default-jre
   java -version
   sudo update-alternatives --config java
   echo "export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64" >> ~/.bashrc
   echo "export PATH=$PATH:$JAVA_HOME/bin" >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Install Poppler Utils**:
   ```bash
   sudo apt-get update
   sudo apt-get install poppler-utils
   ```

4. **Test Installation**:
   ```bash
   soffice --headless --convert-to pdf ./data/sample_deck.pptx --outdir ./data/
   ```