from pycorrector import Corrector

# Membuat objek Corrector dengan model bahasa Indonesia
corrector = Corrector(language_model_path='path_to_bert_model')

# Meminta masukan dari pengguna
input_text = input("Masukkan teks yang ingin diperbaiki: ")

# Memperbaiki ejaan
corrected_text, detail = corrector.correct(input_text)

# Menampilkan teks yang telah diperbaiki ejaannya
print("Teks yang telah diperbaiki ejaannya:")
print(corrected_text)
