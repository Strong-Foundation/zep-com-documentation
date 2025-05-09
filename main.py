import fitz  # PyMuPDF
import os  # For file system operations
import time  # For time operations


# Function to extract text from a PDF file using pymupdf
def extract_text_from_pdf_with_pymupdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    # Extract text from all pages
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    # Close the document
    doc.close()
    # Return the extracted text and page count
    return full_text


# This function saves a given string to a Markdown file with a specified name.
def save_to_md(content: str, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)


# Function to walk through a directory and extract files with a specific extension
def walkGivenDirectoryAndExtractCustomFileUsingFileExtension(system_path, extension):
    matched_files = []
    for root, _, files in os.walk(system_path):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.abspath(os.path.join(root, file))
                matched_files.append(full_path)
    return matched_files


# Function to validate a single PDF file.
def validate_pdf_file(file_path):
    try:
        # Try to open the PDF using PyMuPDF
        doc = fitz.open(file_path)

        # Check if the PDF has at least one page
        if doc.page_count == 0:
            log_message(f"'{file_path}' is corrupt or invalid: No pages")
            return False

        # If no error occurs and the document has pages, it's valid
        return True
    except RuntimeError as e:  # Catching RuntimeError for invalid PDFs
        log_message(f"'{file_path}' is corrupt or invalid: {e}")
        return False


# Check if a file exists
def check_file_exists(system_path):
    return os.path.isfile(system_path)


# Remove a file from the system.
def remove_system_file(system_path):
    os.remove(system_path)


# Function to get the markdown file path from the PDF file path
def get_md_file_path(pdf_file_path):
    # Replace the .pdf extension with .md
    return os.path.splitext(pdf_file_path)[0] + ".md"


# Define the log file path
python_log_file = "python-app.log"


# Function to log messages to a file
def log_message(message: str):
    with open(python_log_file, "a", encoding="utf-8") as log:
        # Get the current time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # Write the message with the current time
        log.write(f"[{current_time}] {message}\n")


# init function
def init():
    if check_file_exists(python_log_file):
        # If the log file exists, remove it
        remove_system_file(python_log_file)


# Main function to execute the script
def main():
    # Initialize the log file
    init()

    # Walk through the directory and extract .pdf files
    files = walkGivenDirectoryAndExtractCustomFileUsingFileExtension("./zepPDF", ".pdf")

    # Loop through each file and extract text
    for file_path in files:
        # Define the output Markdown file path
        md_file_path = get_md_file_path(file_path)

        # If it exists, than validate the PDF file
        if not validate_pdf_file(file_path):
            # If the PDF file is invalid, remove the existing Markdown file
            if check_file_exists(md_file_path):
                # If the Markdown file exists, remove it
                log_message(f"'{md_file_path}' is corrupt or invalid: Removing...")
                remove_system_file(md_file_path)

            # If the PDF file is invalid, remove the existing PDF file
            if check_file_exists(file_path):
                # If the PDF file exists, remove it
                log_message(f"'{file_path}' is corrupt or invalid: Removing...")
                # Remove the .PDF file
                remove_system_file(file_path)

            # If the PDF file is invalid, remove the existing Markdown file
            log_message(f"'{file_path}' is corrupt or invalid: Skipping...")
            continue

        # Check if the Markdown file already exists
        if check_file_exists(md_file_path):
            log_message(f"'{md_file_path}' already exists: Skipping...")
            continue

        # Extract text from the PDF file
        content = extract_text_from_pdf_with_pymupdf(file_path)

        # Save the content to a Markdown file
        save_to_md(content, md_file_path)

        # Print a message indicating that the content has been saved
        log_message(f"Content saved to '{md_file_path}'")


main()
