#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import psycopg2
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image,ImageDraw,ImageFont

BuzzerPin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT) 
global Buzz 
Buzz = GPIO.PWM(BuzzerPin, 440) 


RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

db = psycopg2.connect(
    database="your_db_name",
    user="your_database_user_name",
    password="pass",
    host="localhost"
)
cursor = db.cursor()
reader = SimpleMFRC522()

def ekranTemizle():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(image)
    disp.display()

def ekranYaz(yazi):
    draw.text((0, 0),yazi,  font=font, fill=255)
    disp.image(image)
    disp.display()

try:
  while True:
    ekranTemizle()
    ekranYaz('    KAYIT ICIN \nKARTINIZI OKUTUNUZ')
    print("Kartınızı Okutunuz")
    id, text = reader.read() # Kart bilgilerini alma .
    print("Kartınızın id'si :",id)                # id yazdır .
    card_id =id
    cursor.execute("SELECT id FROM users WHERE rfid="+str(card_id)+" ;") # rfid'yi databsede sorgulama.
    cursor.fetchone() 
    if cursor.rowcount >= 1:
        
        ekranTemizle()
        ekranYaz("KART TANIMLI \nGUNCELLE Y|N ?")
        print("Kullanıcı zaten var !")
        overwrite = input("Kullanıcıyı güncelle (Y/N)? ")
        if overwrite[0] == 'Y' or overwrite[0] == 'y':
            
          ekranTemizle()
          ekranYaz('      KULLANICI \n    DEGISTIRILIYOR')
          
          update_name = input("Isim: ")
          update_surname = input("Soyisim: ")
          update_schoolid = int(input("Okul Numarası: "))
          update_code = "UPDATE users SET name = %s ,surname = %s, schoolid= %s WHERE rfid=%s ;"
          cursor.execute(update_code, (update_name,update_surname,update_schoolid,int(card_id)))
          db.commit()
          print("Kullanıcı Güncellendi")
          ekranYaz('      KULLANICI \n    GUNCELLENDI')
          time.sleep(2)
          ekranTemizle()
          
        else:
            continue;
    else:

        
        ekranTemizle()
        ekranYaz('    BILGILERINIZI\n       GIRINIZ')
        
        new_name = input("Isim: ")
        new_surname = input("Soyisim: ")
        new_rfid=int(card_id)
        new_schoolid = int(input("Okul Numarası: "))
        
        add = "INSERT INTO users (name, surname,rfid,schoolid) VALUES (%s, %s,%s,%s);"
        cursor.execute(add , (new_name,new_surname,new_rfid,new_schoolid))

        db.commit()

        ekranTemizle()
        ekranYaz( "    "+new_name + " "+ new_surname +"\n     EKLENDI")
        time.sleep(2)
    
finally:
  GPIO.cleanup()

