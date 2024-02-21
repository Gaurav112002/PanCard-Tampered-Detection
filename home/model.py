from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import fitz
import os

def predict(image):
    _, file_extension = os.path.splitext(image.name.lower())
    # print(f'Name: {_}\nExtension: {file_extension}')

    if (file_extension == '.pdf'):
        pdf_file_path = default_storage.save('temp.pdf', ContentFile(image.read()))

        pdf_document = fitz.open(pdf_file_path)
        for page_number in range(pdf_document.page_count):
            # Get the page
            page = pdf_document[page_number]
            # Get the image list on the page
            image_list = page.get_images(full=True)

            # Iterate over each image on the page
            for image_index, img in enumerate(image_list):
                # Get the image data
                img_index = img[0]
                base_image = pdf_document.extract_image(img_index)
                image_bytes = base_image["image"]

                # Convert the image to PNG using Pillow
                image = Image.open(BytesIO(image_bytes)).resize((250, 160))

                # Save the processed image
                output_path = os.path.join('static', f'uploaded_img.png')
                image.save(output_path, 'PNG')

        # Close the PDF document
        pdf_document.close()
        # Delete the temporary PDF file
        default_storage.delete(pdf_file_path)
    else:
        uploaded_img = Image.open(image).resize((250, 160))
        # original_img = Image.open("static/pan-card.jpg").resize((250, 160))

        uploaded_img.save("static/uploaded_img.png")
        # original_img.save("static/original_img.png")

    # we can also use this for converting image in array format
    uploaded_img = cv2.imread("static/uploaded_img.png")
    original_img = cv2.imread("static/original_img.png")

    # Converting image in numpy array for processing
    # uploaded_img = np.array(uploaded_img)
    # original_img = np.array(original_img)

    uploaded_gray = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)
    original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
    diff = (diff * 255).astype('uint8')
    # print("SSIM: {}".format(score))

    thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(original_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.rectangle(uploaded_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    obj_img = Image.fromarray(uploaded_img)
    obj_img.save("static/obj_img1.png")

    difference = Image.fromarray(diff)
    difference.save("static/diff_img1.png")
        
    return round(score,2)
