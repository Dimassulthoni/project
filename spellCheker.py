import enchant
from Levenshtein import distance

# Membuat objek dictionary untuk bahasa Indonesia
dict_id = enchant.Dict('id_ID')

# Meminta masukan dari pengguna
input_text = input("Masukkan teks yang ingin diperiksa: ")

# Membagi teks menjadi kata-kata
words = input_text.split()

# Mengecek setiap kata dalam kamus
for word in words:
    if not dict_id.check(word):
        # Jika kata tidak ada dalam kamus, menampilkan saran kata yang mirip
        suggestions = dict_id.suggest(word)
        # Menghitung jarak Levenshtein antara kata yang salah dan setiap saran kata
        distances = [distance(word, suggestion) for suggestion in suggestions]
        # Memilih saran kata dengan jarak Levenshtein terkecil
        best_suggestion = suggestions[distances.index(min(distances))]
        # Mengganti kata yang salah dengan saran kata terbaik
        input_text = input_text.replace(word, best_suggestion)

# Menampilkan teks yang telah diperbaiki ejaannya
print("Teks yang telah diperbaiki ejaannya:")
print(input_text)
