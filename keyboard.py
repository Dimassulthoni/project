import cv2
import os

def flip_images(folder_path):
    # Mendapatkan daftar file gambar dalam folder
    image_files = [file for file in os.listdir(folder_path) if file.endswith(('.jpg', '.jpeg', '.png'))]

    for file_name in image_files:
        # Baca gambar dari file
        image_path = os.path.join(folder_path, file_name)
        image = cv2.imread(image_path)

        # Melakukan flipping secara horizontal (mirror)
        flipped_image = cv2.flip(image, 1)

        # Mendapatkan nama file dan ekstensinya
        base_name = os.path.splitext(file_name)[0]
        extension = os.path.splitext(file_name)[1]

        # Menyusun path file untuk gambar yang telah di-flip
        flipped_image_path = os.path.join(folder_path, base_name + '_flipped' + extension)

        # Menyimpan gambar yang telah di-flip
        cv2.imwrite(flipped_image_path, flipped_image)

        print(f"Gambar {file_name} telah di-flip dan disimpan sebagai {base_name}_flipped{extension}")

# Path folder yang berisi gambar-gambar yang akan di-flip
folder_path = 'C:/Users/HP/OneDrive/Dokumen/tugas kuliah/SKRIPSI/isyarat/project/Data/P'

flip_images(folder_path)
