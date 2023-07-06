import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import font
import sounddevice as sd
import math
from cvzone.HandTrackingModule import HandDetector
from gtts import gTTS
import pygame


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
        tk.Label(self.frame, text='Audio').grid(column=0)
        self.audio_device_combobox = ttk.Combobox(self.frame, values=self.audio_devices, state='readonly')
        self.audio_device_combobox.current(0)  # Mengatur indeks nilai default
        self.audio_device_combobox.bind("<<ComboboxSelected>>", self.select_audio_device)
        self.audio_device_combobox.grid(column=1, row=0)

        # Membuat dropdown button untuk perangkat video
        tk.Label(self.frame, text='Video').grid(column=3, row=0)
        self.video_device_combobox = ttk.Combobox(self.frame, values=self.video_devices, state='readonly')
        self.video_device_combobox.current(0)  # Mengatur indeks nilai default
        self.video_device_combobox.bind("<<ComboboxSelected>>", self.select_video_device)
        self.video_device_combobox.grid(column=4, row=0)
        
        self.button = tk.Button(self.frame, text= "Open Webcam").grid(column=5, row= 0)
         # Membuat objek VideoCapture
        self.video_capture = cv2.VideoCapture(video_source)
        
         # Menginisialisasi HandDetector
        self.hand_detector = HandDetector(maxHands=2, detectionCon=0.8)
        
        # Membuat elemen Canvas untuk menampilkan gambar webcam
        self.frame_cv = tk.Frame (window)
        self.frame_cv.pack(anchor=tk.NW)
        
        # Membuat label untuk menampilkan output webcam
        self.label1 = tk.Label(self.frame_cv)
        self.label1.pack(padx=10, pady=10, side=tk.LEFT)

        self.label2 = tk.Label(self.frame_cv)
        self.label2.pack(padx=10, pady=10, side=tk.LEFT)
        
        # Fungsi untuk membaca frame webcam
        self.update()
        
        
        #textfield
        self.frame_tf = tk.Frame(window)
        self.frame_tf.pack(anchor=tk.SW, side=tk.LEFT)
        self.text_field = tk.Entry(self.frame_tf)
        self.text_field.configure(font=font.Font(size=20), width=70)
        self.text_field.grid(column=0, padx=10, pady=5)
        
        #button_tts
        tk.Button(self.frame_tf, text= "TTS", width=10, height=2, command= self.tts).grid(column=1, row= 0, padx=10, pady=5)
        
    def tts(self):
        bahasa = 'id'
        suara = gTTS(text=self.text_field.get(), lang=bahasa, slow= False)
        suara.save("sample.mp3")
        pygame.mixer.init()
        sound = pygame.mixer.Sound("sample.mp3")
        sound.play()
        
    def update(self):
    # Membaca frame dari video source
        ret, frame = self.video_capture.read()

        if ret:
            # Duplikasi frame
            frame1 = frame.copy()
            frame2 = frame.copy()
            
            offset = 20
            imgSize = 450

            # Mendeteksi tangan dalam salah satu frame
            hands = self.detect_hand(frame1)
            if hands:
                # Mengambil tangan pertama
                if len(hands) == 1:
                    hand1 = hands[0]
                    x, y, w, h = hand1['bbox']
                    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                    imgCrop = frame[y - offset:y + h + offset, x - offset:x + w + offset]
                    imgCropShape = imgCrop.shape
                    aspectRatio = h / w
                    if aspectRatio > 1:
                        k = imgSize / h
                        wCal = math.ceil(k * w)
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize
                        frame2 = imgWhite

                    else:
                        k = imgSize / w
                        hCal = math.ceil(k * h)
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize
                        frame2 = imgWhite
                    # Menandai tangan dengan kotak bounding box
                    cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    
                else :
                    hand2 = hands[1]
                    x, y, w, h = hand2['bbox']
                    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                    imgCrop = frame[y - offset:y + h + offset, x - offset:x + w + offset]
                    # Calculate bounding box for both hands
                    x_min, y_min, x_max, y_max = 10000, 10000, -1, -1
                    for hand in hands:
                        x_min = min(x_min, hand['bbox'][0])
                        y_min = min(y_min, hand['bbox'][1])
                        x_max = max(x_max, hand['bbox'][0] + hand['bbox'][2])
                        y_max = max(y_max, hand['bbox'][1] + hand['bbox'][3])
                        imgCrop = frame[y_min - offset :y_max + offset, x_min - offset:x_max + offset]
                        imgCropShape = imgCrop.shape
                        aspectRatio = h / w
                        if aspectRatio > 1:
                            k = imgSize / h
                            wCal = math.ceil(k * w)
                            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                            imgResizeShape = imgResize.shape
                            wGap = math.ceil((imgSize - wCal) / 2)
                            imgWhite[:, wGap:wCal + wGap] = imgResize
                            frame2 = imgWhite

                        else:
                            k = imgSize / w
                            hCal = math.ceil(k * h)
                            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                            imgResizeShape = imgResize.shape
                            hGap = math.ceil((imgSize - hCal) / 2)
                            imgWhite[hGap:hCal + hGap, :] = imgResize
                            frame2 = imgWhite
                            
        
                            
            # Konversi frame ke format PIL Image
            pil_image1 = Image.fromarray(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
            pil_image2 = Image.fromarray(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))

            # Konversi PIL Image ke format ImageTk
            image1 = ImageTk.PhotoImage(pil_image1)
            image2 = ImageTk.PhotoImage(pil_image2)

            # Menampilkan frame di tkinter
            self.label1.configure(image=image1)
            self.label1.image = image1

            self.label2.configure(image=image2)
            self.label2.image = image2

        # Memanggil metode update secara rekursif setiap 10 milidetik (atau sesuai kebutuhan)
        self.window.after(10, self.update)
        
    def detect_hand(self, frame):
        # Mendeteksi tangan menggunakan HandDetector
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hands, _ = self.hand_detector.findHands(frame)
        return hands
                      
    def select_audio_device(self):
        selected_device = self.audio_device_var.get()
        print(f'Selected audio device: {selected_device}')

    def select_video_device(self):
        selected_device = self.video_device_var.get()
        print(f'Selected video device: {selected_device}')
        

    
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

