import digitalio
import board
import adafruit_character_lcd.character_lcd as characterlcd
import time
lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D23)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D8)
lcd_d6 = digitalio.DigitalInOut(board.D7)
lcd_d7 = digitalio.DigitalInOut(board.D1)


lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                       lcd_d7, lcd_columns, lcd_rows)


lcd.clear()

lcd.message = "Welcome"

