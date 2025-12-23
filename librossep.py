import requests
import os
from PIL import Image
from fpdf import FPDF
from tqdm import tqdm
import re
import sys

def download_conaliteg_book():
    """
    Prompts for a CONALITEG book URL, downloads all images for the book
    based on the extracted code, and compiles them into a single PDF.
    """

    # --- 1. USER INPUT AND BOOK CODE EXTRACTION ---

    # Ask the user for the URL
    book_code_url = input("Please paste the URL of the CONALITEG book's HTML page (e.g., https://historico.conaliteg.gob.mx/H1972P6MA094.htm): \n> ").strip()

    if not book_code_url:
        print("❌ No URL provided. Exiting.")
        sys.exit()

    # Use a regular expression to find the unique book identifier
    # This pattern HxxxxPxxAxxx is robust for the CONALITEG historical format
    match = re.search(r'([A-Z]\d{4}[A-Z]\d[A-Z]{2}\d{3})', book_code_url)

    if match:
        book_code = match.group(1)
        print(f"\n✅ Extracted Book Code: {book_code}")
    else:
        print(f"❌ Could not extract a valid book code from the URL: {book_code_url}")
        print("Please ensure the URL ends with a code like H1972P6MA094.htm.")
        sys.exit()

    # Define URL pattern using the extracted code
    image_url_pattern = f"https://historico.conaliteg.gob.mx/c/{book_code}/{{page_num:03d}}.jpg"

    # Output directory and PDF file name are dynamic
    output_dir = f"conaliteg_images_{book_code}"
    pdf_output_file = f"conaliteg_book_{book_code}.pdf"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"📁 Images will be saved to: {output_dir}")
    print(f"📄 PDF will be named: {pdf_output_file}")

    # Determine the range of pages to download
    # Start at page 0 for covers/initial pages, search up to 300 pages max
    start_page = 0
    end_page = 300
    page_range = range(start_page, end_page + 1)

    # --- Part 2: DOWNLOAD IMAGES ---

    print(f"\n## Starting Image Download ({start_page:03d} to {end_page:03d} maximum pages)...")
    image_paths = []

    # Prepare headers for a robust request and set a timeout
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

    # Wrap the page range iteration with tqdm for a progress bar
    for page_num in tqdm(page_range, desc="Downloading Pages", unit="page"):
        image_url = image_url_pattern.format(page_num=page_num)
        image_path = os.path.join(output_dir, f"page_{page_num:03d}.jpg")

        try:
            response = requests.get(image_url, stream=True, headers=headers, timeout=15)
            response.raise_for_status()

            with open(image_path, 'wb') as f:
                # Iterate over content in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            image_paths.append(image_path)

        except requests.exceptions.HTTPError as e:
            # 404 signals the end of a sequence, which is expected
            if response.status_code == 404:
                tqdm.write(f"✅ Page {page_num:03d} not found (404). Assuming end of book and stopping.")
            else:
                tqdm.write(f"Error downloading image for page {page_num:03d}: {e}")
            break # Stop on any HTTP error, especially 404
        except requests.exceptions.RequestException as e:
            tqdm.write(f"Network Error for page {page_num:03d}: {e}. Stopping download.")
            break

    # --- Part 3: CONVERT IMAGES TO PDF ---

    print("\n" + "---" * 10)
    if not image_paths:
        print("❌ No images were successfully downloaded. Cannot create PDF.")
        # Clean up the empty directory if no images were saved
        if os.path.exists(output_dir):
            try:
                os.rmdir(output_dir)
                print(f"Cleaned up empty directory: {output_dir}")
            except OSError:
                pass
    else:
        print("## Starting PDF Conversion...")

        # FPDF setup: Portrait ('P'), mm units, A4 size
        pdf = FPDF('P', 'mm', 'A4')
        A4_WIDTH_MM = 210
        A4_HEIGHT_MM = 297

        # Wrap the image paths iteration with tqdm for a second progress bar
        for img_path in tqdm(image_paths, desc="Creating PDF", unit="image"):
            try:
                # Get dimensions using Pillow
                with Image.open(img_path) as img:
                    width, height = img.size

                # Calculate the proportional height and width to fit the image on the A4 page
                w_mm = A4_WIDTH_MM
                h_mm = w_mm * height / width

                if h_mm > A4_HEIGHT_MM:
                    # If calculated height is too large, fit to A4 height instead
                    h_mm = A4_HEIGHT_MM
                    w_mm = h_mm * width / height

                # Add a new page.
                pdf.add_page()
                # Center the image on the page
                x_center = (A4_WIDTH_MM - w_mm) / 2
                y_center = (A4_HEIGHT_MM - h_mm) / 2
                pdf.image(img_path, x=x_center, y=y_center, w=w_mm, h=h_mm)

            except Exception as e:
                tqdm.write(f"Could not add image {img_path} to PDF: {e}")

        # --- FIX APPLIED HERE ---
        # Removed the destination argument ("F") to avoid the TypeError,
        # as FPDF.output() defaults to saving to file when a name is given.
        pdf.output(pdf_output_file) 
        
        print(f"\n" + "---" * 10)
        print(f"🎉 Success! Created **{pdf_output_file}** with **{len(image_paths)}** pages.")

if __name__ == "__main__":
    download_conaliteg_book()
