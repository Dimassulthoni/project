import tkinter as tk
import cv2
from PIL import Image, ImageTk

# Membuat objek Tkinter
window = tk.Tk()

# Variabel status untuk melacak status webcam
webcam_open = False

# Membuat objek VideoCapture
cap = cv2.VideoCapture(0)

# Fungsi untuk membuka atau menutup webcam
def toggle_webcam():
    global webcam_open

    if not webcam_open:
        # Mengubah teks tombol menjadi "Close Webcam"
        button.config(text="Close Webcam")
        webcam_open = True

        # Mengambil dan menampilkan frame webcam
        capture_frame()

    else:
        # Mengubah teks tombol menjadi "Open Webcam"
        button.config(text="Open Webcam")
        webcam_open = False

# Fungsi untuk mengambil dan menampilkan frame webcam
def capture_frame():
    ret, frame = cap.read()

    if ret:
        # Konversi frame OpenCV menjadi format yang dapat ditampilkan di Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        # Menampilkan frame di Tkinter
        label.configure(image=img_tk)
        label.image = img_tk

    if webcam_open:
        # Mengambil dan menampilkan frame berikutnya setelah 10 ms
        window.after(10, capture_frame)

# Membuat tombol untuk membuka atau menutup webcam
button = tk.Button(window, text="Open Webcam", command=toggle_webcam)
button.pack()

# Membuat label untuk menampilkan frame webcam
label = tk.Label(window)
label.pack()

# Menjalankan aplikasi
window.mainloop()

# Menutup webcam dan menghapus objek VideoCapture setelah aplikasi ditutup
cap.release()
cv2.destroyAllWindows()
