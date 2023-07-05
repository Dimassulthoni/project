import tkinter as tk
import cv2
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Webcam App")

        # Membuat label untuk menampilkan output webcam
        self.label1 = tk.Label(self.window)
        self.label1.pack(padx=10, pady=10, side=tk.LEFT)

        self.label2 = tk.Label(self.window)
        self.label2.pack(padx=10, pady=10, side=tk.LEFT)

        # Membuka video source (webcam)
        self.video = cv2.VideoCapture(video_source)

        self.update()

    def update(self):
        # Membaca frame dari video source
        ret, frame = self.video.read()

        if ret:
            # Konversi frame ke format yang dapat ditampilkan di tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)

            # Menampilkan frame di tkinter
            self.label1.configure(image=image)
            self.label1.image = image

            # Menampilkan duplikat frame di sebelahnya
            self.label2.configure(image=image)
            self.label2.image = image

        # Memanggil metode update secara rekursif setiap 10 milidetik (atau sesuai kebutuhan)
        self.window.after(10, self.update)

    def run(self):
        self.window.mainloop()

# Membuat instance aplikasi dan menjalankannya
root = tk.Tk()
app = WebcamApp(root)
app.run()
