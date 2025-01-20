import csv
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode

# Function to generate QR code for a given ID
def generate_qr_code(url, qr_size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img.resize((qr_size, qr_size))

# Function to create one page with 12 rectangles (2 columns, 6 rows)
def create_a4_page(entries, page_number, output_folder, font_path, font_size, padding, qr_size):
    # A4 size in pixels at 300 DPI (2480x3508)
    page_width = 2480
    page_height = 3508
    rectangle_width = page_width // 2  # 2 columns
    rectangle_height = page_height // 6  # 6 rows

    # Create a new white image (A4 page)
    page = Image.new('RGB', (page_width, page_height), color='white')
    draw = ImageDraw.Draw(page)
    
    # Load the font from the given font path
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Error loading font from {font_path}. Using default font.")
        font = ImageFont.load_default()  # Fallback to default if the specified font isn't available

    # Iterate over the first 12 entries (or fewer if there are less than 12)
    for i, entry in enumerate(entries[:12]):
        # Calculate the position of the rectangle (2 columns, 6 rows)
        x = (i % 2) * rectangle_width
        y = (i // 2) * rectangle_height

        # Draw rectangle
        draw.rectangle([x, y, x + rectangle_width, y + rectangle_height], outline="black", width=2)

        # Name text position (on the left, centered vertically)
        name_text = f"{entry['NOME']} {entry['COGNOME']}"
        
        # Get the bounding box of the text to calculate width and height
        text_bbox = draw.textbbox((0, 0), name_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        text_x = x + padding
        text_y = y + (rectangle_height - text_height) // 2  # Center the name vertically
        draw.text((text_x, text_y), name_text, font=font, fill="black")

        # URL for QR code
        url = f"https://firyfoxy.github.io/prigionieriById/#{entry['#']}"
        qr_code = generate_qr_code(url, qr_size)

        # Calculate QR code position (next to the name)
        qr_x = x + rectangle_width - qr_size - padding
        qr_y = y + (rectangle_height - qr_size) // 2  # Vertically center the QR code

        # Paste the QR code onto the page
        page.paste(qr_code, (qr_x, qr_y))

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the image as a PNG file in the specified folder
    output_file = os.path.join(output_folder, f"a4_page_{page_number}.png")
    page.save(output_file)
    print(f"A4 page {page_number} saved as {output_file}")

# Function to read the CSV file and extract entries
def read_csv(file_path):
    entries = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            entries.append(row)
    return entries

# Main execution
if __name__ == "__main__":
    csv_file_path = './output.csv'  # Path to your CSV file
    output_folder = 'generated_pages'  # Folder to save the output images
    font_size = 50  # Adjust the font size here
    font_path = "./font/Lato-Regular.ttf"

    # Ask for padding and QR code size
    padding = 50
    qr_size = 400

    entries = read_csv(csv_file_path)
    
    # Calculate number of pages needed (12 entries per page)
    total_pages = (len(entries) + 11) // 12  # Ceiling division to get total pages

    # Create a page for each set of 12 entries
    for page_number in range(1, total_pages + 1):
        start_index = (page_number - 1) * 12
        end_index = min(start_index + 12, len(entries))
        create_a4_page(entries[start_index:end_index], page_number, output_folder, font_path, font_size, padding, qr_size)

