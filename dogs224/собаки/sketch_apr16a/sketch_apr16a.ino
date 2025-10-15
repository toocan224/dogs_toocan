const int ledPin = 2;
void setup() {
  Serial.begin(9600);         // Инициализация последовательного соединения
  pinMode(ledPin, OUTPUT);    // Настраиваем пин светодиода как выход
  digitalWrite(ledPin, LOW);  // Гасим светодиод при старте
}

void loop() {
  if (Serial.available() > 0) {          // Если есть данные в порту
    char received = Serial.read();       // Читаем полученный символ
    
    if (received == '1') {               // Если получили '1'
      digitalWrite(ledPin, HIGH);        // Включаем светодиод
      delay(5000);                       // Ждем 5 секунд
      digitalWrite(ledPin, LOW);         // Выключаем светодиод
    }
    // При получении '0' ничего не делаем
  }
}