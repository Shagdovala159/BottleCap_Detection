import cv2
from tkinter import *
from PIL import ImageTk, Image
import datetime
import subprocess
import RPi.GPIO as GPIO
import time
from time import sleep
from PIL import Image

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
mode = GPIO.getmode()

GPIO.setup(24, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
num = 0
counter = 0
# Create an instance of the tkinter window
win = Tk()

# Define the geometry of the window
win.geometry("640x680")

# Create a Label Widget to display the image
label = Label(win)
label.pack(fill="both", expand="yes")

# Create a Label Widget for the text
text_label = Label(win, font=("Arial", 15), justify="left")

text_label.pack(anchor="w", padx=10, pady=10)

def capture_photo():
    global num
    global counter
    start_time = time.time()
    # Inisialisasi objek kamera
    camera = cv2.VideoCapture(0)

    # Periksa apakah kamera terbuka
    if not camera.isOpened():
        print("Tidak dapat membuka kamera")
        return

    # Baca frame dari kamera
    ret, frame = camera.read()

    # Periksa apakah frame berhasil dibaca
    if not ret:
        print("Tidak dapat membaca frame")
        return

    # Waktu sekarang untuk nama file
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Buat nama file dengan format tgl_waktu.jpg
    filename = f"datatoti/{timestamp}.jpg"
    filedetect = f"results/{timestamp}.txt"
    imgdetect = f"results/{timestamp}.jpg"

    # Simpan frame sebagai file gambar
    cv2.imwrite(filename, frame)

    # Tutup kamera
    camera.release()
    subprocess.run(
        ["python", "TFLite_detection_image.py", "--modeldir=modeltoti", f"--image={filename}", "--save_results",
         "--noshow_results"])
    with open(filedetect, 'r') as file:
        tipe = file.readline().strip()
        words = tipe.split()
    # img = Image.open(imgdetect)
    # img.show()
    if words:
        initipe = words[0]
        print('Objek terdeteksi sebagai: ', initipe)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Waktu: ', elapsed_time)
        if initipe == "CCHITAM":
            print('Clasifikasi : Not Good')
            counter = counter + 1
            num += 1
            GPIO.output(24, False)
            sleep(15)
            GPIO.output(24, True)
            print("total reject:", num)
            Clasifikasi = "Not Good"
        elif initipe == "CCMERAH":
            print('Clasifikasi : Not Good')
            counter = counter + 1
            num += 1
            GPIO.output(24, False)
            sleep(15)
            GPIO.output(24, True)
            print("total reject:", num)
            Clasifikasi = "Not Good"
        else:
            print('Clasifikasi : Good')
            Clasifikasi = "Good"
        # Open the new image
        img = ImageTk.PhotoImage(Image.open(imgdetect))

        # Update the label with the new image
        label.configure(image=img)
        label.image = img  # Keep a reference to prevent garbage collection
        # Update the text label with the corresponding text
        text_label.configure(text="Objek terdeteksi sebagai: " + initipe + "\nWaktu : " + str(elapsed_time) + "detik\nClasifikasi : " + Clasifikasi + "\nCounter :" + str(counter))
        win.update()
    else:
        print('Objek tidak terdeteksi.')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Waktu: ', elapsed_time)


def check_button():
    while True:
        if GPIO.input(18) == 0:
            print('Proses')
            capture_photo()
        else:
            sleep(0.1)

# Panggil fungsi untuk mengambil foto
win.after(0, check_button)
win.mainloop()
