  //  TRAFFIC LIGHT SIMULATION   //
  
  int first_red = 10;
  int first_yellow = 8;
  int first_green = 9;
  
  int second_red = 11;
  int second_yellow = 12;
  int second_green = 13;

  int ticket = 0;
  int last_command;
  
void setup() {
  // put your setup code here, to run once:
  pinMode(first_red, OUTPUT);
  pinMode(first_yellow, OUTPUT);
  pinMode(first_green, OUTPUT);
  
  pinMode(second_red, OUTPUT);
  pinMode(second_yellow, OUTPUT);
  pinMode(second_green, OUTPUT);
  digitalWrite(first_red,HIGH);
  digitalWrite(second_red,HIGH);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) //Serial Portta değer gelirse
  {
  ticket = Serial.read();
  switch (ticket) {
    case '1':
      if(digitalRead(first_red) == HIGH){
        if(digitalRead(second_green) == HIGH) {
            second_road_green2red();
          }
        first_road_red2green();
      }
      break;
    case '2':
       if(digitalRead(first_green) == HIGH){
          first_road_green2red();
        }
      break;

    case '3':
        if(digitalRead(second_red) == HIGH ){
          if(digitalRead(first_green) == HIGH) {
            first_road_green2red();
            }
          second_road_red2green();
        }
        break;
        
    case '4':
      if(digitalRead(second_green) == HIGH){
        second_road_green2red();
        }
        break;
        
    default:
      // if nothing else matches, do the default
      // default is optional
    break;
    }
  }
}


void first_road_red2green(){
      digitalWrite(first_yellow, HIGH);
      delay(1500);
      digitalWrite(first_red,LOW);
      digitalWrite(first_yellow, LOW);
      delay(100);
      digitalWrite(first_green,HIGH);
      delay(3000);
 }

  void first_road_green2red(){
      digitalWrite(first_green,LOW);
      delay(500);
      digitalWrite(first_green,HIGH);
      delay(500);
      digitalWrite(first_green,LOW);
      delay(500);
      digitalWrite(first_green,HIGH);
      delay(500);
      digitalWrite(first_green,LOW);
      delay(500);
      digitalWrite(first_green,HIGH);
      delay(500);
      digitalWrite(first_green,LOW);
      
      digitalWrite(first_yellow, HIGH);
      delay(1500);
      
      digitalWrite(first_yellow, LOW);
      digitalWrite(first_red,HIGH);
  }

 void second_road_red2green(){
      digitalWrite(second_yellow, HIGH);
      delay(1500);
      digitalWrite(second_red,LOW);
      digitalWrite(second_yellow, LOW);
      delay(100);
      digitalWrite(second_green,HIGH);
      delay(3000);
 }

 void second_road_green2red(){
        digitalWrite(second_green,LOW);
        delay(500);
        digitalWrite(second_green,HIGH);
        delay(500);
        digitalWrite(second_green,LOW);
        delay(500);
        digitalWrite(second_green,HIGH);
        delay(500);
        digitalWrite(second_green,LOW);
        delay(500);
        digitalWrite(second_green,HIGH);
        delay(500);
        digitalWrite(second_green,LOW);
        
        digitalWrite(second_yellow, HIGH);
        delay(1500);
        
        digitalWrite(second_yellow, LOW);
        digitalWrite(second_red,HIGH);
 }
