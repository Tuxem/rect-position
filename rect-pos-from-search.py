import logging
import pdb
import os

import click
import fitz  # PyMuPDF



def find_text_bbox(pdf_path, target_text):
    """
    Finds the bounding box of the target text in a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
        target_text (str): Text to search for.

    Returns:
        tuple: Bounding box coordinates (x1, y1, x2, y2) or None if not found.
    """

    doc = fitz.open(pdf_path)

    for page in doc:
        text = page.get_text()
        if target_text in text:
            text_instances = page.search_for(target_text)
            return text_instances[0] if text_instances else None

    return None


def read_pdf(pdf_path):
    """
    Reads the first textbox on the first page of a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
    """

    with fitz.open(pdf_path) as doc:
        page = doc[0]
        match = page.get_textbox(fitz.Rect(90, 442, 350, 445))
        pdb.set_trace()


def process_pdf_folder(folder_path, target_text):
    """
    Searches for the target text in all PDF files within a folder.

    Args:
        folder_path (str): Path to the PDF folder.
        target_text (str): Text to search for.
    """

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            rect = find_text_bbox(pdf_path, target_text)
            if rect:
                logging.info(f"Found '{target_text}' in {filename} at position: ({rect[0]}, {rect[1]}, {rect[2]}, {rect[3]})")


@click.command()
@click.option(
    "-p",
    "--pdf-path",
    type=click.Path(exists=True, readable=True),
    default=os.getcwd(),
    help="Path to the PDF file or folder",
)
@click.option("-t", "--target-text", required=True, help="Text to search for")
def main(pdf_path, target_text):
    """
    Finds text in PDF files or folders.

    Args:
        pdf_path (str): Path to the PDF file or folder.
        target_text (str): Text to search for.
    """

    logging.basicConfig(level=logging.INFO)

    if os.path.isfile(pdf_path):
        # Process single PDF file
        rect = find_text_bbox(pdf_path, target_text)
        if rect:
            logging.info("Bounding box (Rect) of '{}' found:".format(target_text))
            logging.info("Position: ({}, {}, {}, {})".format(rect[0], rect[1], rect[2], rect[3]))
        else:
            logging.info("Text '{}' not found in the PDF.".format(target_text))

        # Loop for interaction
        while True:
            choice = input("Choose an option: interact / redo a search / quit: ").strip().lower()

            if choice == "interact":
                read_pdf(pdf_path)
            elif choice == "redo a search":
                new_target_text = input("Enter the new target text: ")
                rect = find_text_bbox(pdf_path, new_target_text)
                if rect:
                    logging.info("Bounding box (Rect) of '{}' found:".format(new_target_text))
                    logging.info("Position: ({}, {}, {}, {})".format(rect[0], rect[1], rect[2], rect[3]))
                else:
                    logging.info("Text '{}' not found in the PDF.".format(new_target_text))
            elif choice == "quit":
                logging.info("Exiting the script.")
                break
            else:
                logging.warning("Invalid choice. Please try again.")

    elif os.path.isdir(pdf_path):
        # Process PDF folder
        process_pdf_folder(pdf_path, target_text)
    else:
        logging.error("Invalid path provided. Please specify a PDF file or folder.")


if __name__ == "__main__":
    main()
