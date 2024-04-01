import pdb
import fitz  # PyMuPDF


def find_text_bbox(pdf_path, target_text):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Iterate over pages
    for page in doc:
        # Get the text on the page
        text = page.get_text()
        # Check if the target text is in this page
        if target_text in text:
            # Get the rect positions of the text fragments containing the target text
            text_instances = page.search_for(target_text)
            # Return the first rect position found
            if text_instances:
                return text_instances[0]
                
        widgets = page.widgets()

        # Iterate over each widget
        for widget in widgets:
            # Check if the widget is a checkbox
            if widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                # Print the field name of the checkbox
                print(f'Checkbox field name: {widget.field_name} position: {widget.rect}')
    
    # Return None if the text is not found
    return None

def read_pdf(pdf_path):
    # Open the PDF
    with fitz.open(pdf_path) as doc:
        page = doc[0]
        match = page.get_textbox(fitz.Rect(90, 442, 350, 445))
        pdb.set_trace()

    


if __name__ == "__main__":
    # Ask the user for PDF file path
    default_pdf_path = r"C:\Users\emeric\dev\guso-autofill\blanked\FeuilletDeclaration.pdf"
    pdf_path = input("Enter the path to the PDF file (leave empty for default): ").strip() or default_pdf_path

    
    # Ask the user for target text
    target_text = input("Enter the target text: ")
    
    # Find the bounding box of the target text
    rect = find_text_bbox(pdf_path, target_text)
    
    if rect:
        print("Bounding box (Rect) of '{}' found:".format(target_text))
        print("Position: ({}, {}, {}, {})".format(rect[0], rect[1], rect[2], rect[3]))
    else:
        print("Text '{}' not found in the PDF.".format(target_text))

    # Loop for interaction
    while True:
        # Ask the user for their choice
        choice = input("Choose an option: interact / redo a search / quit: ").strip().lower()

        if choice == "interact":
            read_pdf(pdf_path)
        elif choice == "redo a search":
            # Ask the user for another target text
            new_target_text = input("Enter the new target text: ")
            rect = find_text_bbox(pdf_path, new_target_text)
            if rect:
                print("Bounding box (Rect) of '{}' found:".format(new_target_text))
                print("Position: ({}, {}, {}, {})".format(rect[0], rect[1], rect[2], rect[3]))
            else:
                print("Text '{}' not found in the PDF.".format(new_target_text))
        elif choice == "quit":
            print("Exiting the script.")
            break
        else:
            print("Invalid choice. Please try again.")
