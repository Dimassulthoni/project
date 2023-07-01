import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import sounddevice as sd


def get_audio_devices():
        audio_devices = sd.query_devices()
        return [device['name'] for device in audio_devices if device['max_input_channels'] > 0]

def get_video_devices():
    video_devices = []
    i = 0
    while True:
        cap = cv2.VideoCapture(i)
        if not cap.read()[0]:
            break
        else:
            video_devices.append(f'Camera {i}')
            cap.release()
        i += 1
    return video_devices

class WebcamApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("BISIS")
        
        # Mendapatkan daftar perangkat audio dan video
        self.audio_devices = get_audio_devices()
        self.video_devices = get_video_devices()
        
        self.frame = tk.Frame(window)
        self.frame.pack(anchor=tk.NW)
        
        # Membuat dropdown button untuk perangkat audio
        tk.Label(self.frame, text='camera').grid(column=0)
        self.audio_device_combobox = ttk.Combobox(self.frame, values=self.audio_devices, state='readonly')
        self.audio_device_combobox.current(0)  # Mengatur indeks nilai default
        self.audio_device_combobox.bind("<<ComboboxSelected>>", self.select_audio_device)
        self.audio_device_combobox.grid(column=1, row=0)

        # Membuat dropdown button untuk perangkat video
        self.video_device_combobox = ttk.Combobox(self.frame, values=self.video_devices, state='readonly')
        self.video_device_combobox.current(0)  # Mengatur indeks nilai default
        self.video_device_combobox.bind("<<ComboboxSelected>>", self.select_video_device)
        self.video_device_combobox.grid(column=3, row=0)
        
        tk.Button(self.frame, text= "Mulai").grid(column=4, row= 0)

        # Membuat objek VideoCapture
        self.video_capture = cv2.VideoCapture(video_source)
        
        # Membuat elemen Canvas untuk menampilkan gambar webcam
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()
        
        
        # Fungsi untuk membaca frame webcam
        self.update()
        
    def select_audio_device(self):
        selected_device = self.audio_device_var.get()
        print(f'Selected audio device: {selected_device}')

    def select_video_device(self):
        selected_device = self.video_device_var.get()
        print(f'Selected video device: {selected_device}')
        
    def update(self):
        # Membaca frame webcam
        ret, frame = self.video_capture.read()
        
        if ret:
            # Mengkonversi frame menjadi format RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Mengubah frame menjadi objek gambar PIL
            image = Image.fromarray(frame_rgb)
            resized_image = image.resize((640, 480))
            
            self.photo = ImageTk.PhotoImage(resized_image)
        
            # Menampilkan gambar di elemen Canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        # Mengupdate tampilan setiap 15 milidetik
        self.window.after(15, self.update)
        

    
# Membuat objek Tkinter
window = tk.Tk()

lebar = 1280
tinggi = 720

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()

x = int((screenwidth/2)-(lebar/2))
y = int((screenheight/2)-(tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{x}+{y}")
window.resizable(0,0)

# Membuat objek aplikasi WebcamApp
app = WebcamApp(window)
# Menjalankan aplikasi
window.mainloop()

