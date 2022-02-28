
#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import psycopg2
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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

def yetkiliSes():
      Buzz.start(10) 
      Buzz.ChangeFrequency(150)
      time.sleep(0.12)
      Buzz.ChangeFrequency(250)
      time.sleep(0.12)
      Buzz.ChangeFrequency(350)
      time.sleep(0.12)
      Buzz.stop(350)
      
def yetkisizSes():
      Buzz.start(10) 
      Buzz.ChangeFrequency(350)
      time.sleep(0.15)
      Buzz.ChangeFrequency(150) 
      time.sleep(0.25)
      Buzz.stop(350)


try:
  while True:
    ekranTemizle()
    ekranYaz('   Lutfen Kartinizi\n      Okutunuz')
    id, text = reader.read()
    card_id = id
    cursor = db.cursor()
    cursor.execute("SELECT  * FROM users WHERE rfid="+str(card_id))
    result = cursor.fetchone()
    
    ekranTemizle()
    if result is not None:
        
        cursor.execute("SELECT  lastlogin FROM attendance WHERE account_id= "+str(result[0]) +" AND date_part('day',lastlogin)=date_part('day',CURRENT_DATE);")
        result2 = cursor.fetchone()
        
        if result2 is not None:
            ekranYaz(result[1] + " "+ result[2]+"\nZATEN KAYITLI")
            yetkiliSes()
            time.sleep(2)
        else:
            add_attendance= "INSERT INTO attendance (account_id, course_id) VALUES (%s, %s);"
            cursor.execute(add_attendance , (result[0],1))
            db.commit()
            ekranYaz(result[1] + " "+ result[2]+"\nYOKLAMANIZ ALINDI")
            yetkiliSes()
            time.sleep(2)

    else :
        
        ekranYaz("   Yetkiniz Yoktur")
        yetkisizSes()
        time.sleep(2)
        
        
finally:
  GPIO.cleanup()
