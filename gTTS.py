from gtts import gTTS
import os

kata = input("masukan kata: ")
bahasa = 'id'

suara = gTTS(text=kata, lang=bahasa, slow= False)
suara.save("sample.mp3")
os.system("sample.mp3")