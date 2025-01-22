from PIL import Image
import os

try:
    archive_list = os.listdir("images")
    if not archive_list:
        print("No images found in the directory, please fill it.")
    wish = str(input("Do you want to convert all of the images in the directory? (y/n):"))
    if wish.lower() == "y":
        img_type = str(input("What is the type that you want to convert all of you images?\n"))
        os.makedirs(img_type, exist_ok=True)
        for archive in archive_list:
            file_name, _ = os.path.splitext(archive)
            Open_Img = Image.open(f"images/{archive}").convert("RGB")
            Open_Img.save(f"{img_type}/{file_name}.{img_type}")
    elif wish.lower() == "n":
        img_name = str(input("Write the archive name that you want to convert:\n"))
        if img_name not in archive_list:
            print("The archive name does not exist, please put him and try again.")
        img_type = str(input("What is the type that you want to convert you image?\n"))
        os.makedirs(img_type, exist_ok=True)
        file_name, _ = os.path.splitext(img_name)
        Open_Img = Image.open(f"images/{img_name}").convert("RGB")
        Open_Img.save(f"{img_type}/{file_name}.{img_type}")
    else:
        print("Invalid option, please just say y/n.")

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")