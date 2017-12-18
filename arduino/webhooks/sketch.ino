  #include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

int lcd_key     = 0;
int adc_key_in  = 0;

#define btnSELECT 4
#define btnNONE   5

int read_LCD_buttons(){
    adc_key_in = analogRead(0);

    if (adc_key_in > 1000) return btnNONE; 
    
    if (adc_key_in >= 650 && adc_key_in < 850)  return btnSELECT;  
    return btnNONE;
}

void setup(){
   lcd.begin(16, 2);
   lcd.setCursor(0,0);
   lcd.print("Press Select");
   Serial.begin(9600);
}
 
void loop(){
   lcd.setCursor(0,1);
   lcd_key = read_LCD_buttons();
   if (Serial.available() > 0) {
    int val = int(Serial.read());
    if (val == 1) {
      lcd.print("SUCCESS     ");
    }
   }
   switch (lcd_key){
       case btnSELECT:{
             lcd.print("TRIGGERED       ");
             Serial.println("Hello World");
             break;
       }
       case btnNONE:
            break;
   }
   delay(100);
}
