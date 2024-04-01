import pdb
import fitz  # PyMuPDF



def find_checkboxes(page):
    widgets = page.widgets()

    # Iterate over each widget
    for widget in widgets:
        # Check if the widget is a checkbox
        if widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
            # Print the field name of the checkbox
            print(f'Checkbox field name: {widget.field_name} position: {widget.rect}')


def find_text_box(pdf_path, target_text, show_checkboxes=False):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Create an empty list to store all the rect positions
    all_rects = []
    
    # Iterate over pages
    for page in doc:
        # Get the text on the page
        text = page.get_text()
        # Check if the target text is in this page
        if target_text in text:
            # Get the rect positions of the text fragments containing the target text
            text_instances = page.search_for(target_text)
            # Add all the rect positions to the list
            all_rects.extend(text_instances)

        if show_checkboxes:
            find_checkboxes(page)                
    
    # Return all the rect positions
    return all_rects


def read_pdf(pdf_path):
    # Open the PDF
    with fitz.open(pdf_path) as doc:
        page = doc[0]
        match = page.get_textbox(fitz.Rect(90, 442, 350, 445))
        pdb.set_trace()

    


if __name__ == "__main__":
    # Ask the user for PDF file path
    default_pdf_path = r"./FeuilletDeclaration.pdf"
    pdf_path = input("Enter the path to the PDF file (leave empty for default): ").strip() or default_pdf_path

    
    # Ask the user for target text
    target_text = input("Enter the target text: ")
    
    # Find the bounding boxes of the target text
    rects = find_text_box(pdf_path, target_text)

    if rects:
        print("Bounding boxes (Rect) of '{}' found:".format(target_text))
        for i, rect in enumerate(rects):
            print("Bounding box {} position: ({}, {}, {}, {})".format(i+1, rect[0], rect[1], rect[2], rect[3]))
    else:
        print("Text '{}' not found in the PDF.".format(target_text))

    # Loop for interaction
    while True:
        # Ask the user for their choice
        choice = input("Choose an option: interact / redo a search / quit: ").strip().lower()

        if choice == "interact":
            read_pdf(pdf_path)
        elif choice.startswith("redo"):
            # Ask the user for another target text
            target_text = input("Enter the new target text: ")
            # Find the bounding boxes of the target text
            rects = find_text_box(pdf_path, target_text)

            if rects:
                print("Bounding boxes (Rect) of '{}' found:".format(target_text))
                for i, rect in enumerate(rects):
                    print("Bounding box {} position: ({}, {}, {}, {})".format(i+1, rect[0], rect[1], rect[2], rect[3]))
            else:
                print("Text '{}' not found in the PDF.".format(target_text))
        elif choice == "quit":
            print("Exiting the script.")
            break
        else:
            print("Invalid choice. Please try again.")
