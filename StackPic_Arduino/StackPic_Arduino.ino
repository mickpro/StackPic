#define STEP 2
#define DIR 3
#define M1 4

#define FORWARD 1
#define BACKWARD -1

// May need a little bit of adjustment (should be ok...)
#define DELAY_SEND 10
#define DELAY_LOOP 10

void setup()
{
  // Start serial communication
  Serial.begin(9600);

  // Pin declaration
  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(M1, OUTPUT);

  // Divides steps per 32
  digitalWrite(M1, HIGH);
  // Default direction
  digitalWrite(DIR, LOW);
}

void loop()
{
  while (Serial.available())
  {
    switch(Serial.read())
    {
      case '+':
        step(FORWARD);
        Serial.print("AVANT TOUTE");
        break;
      case '-':
        step(BACKWARD);
        Serial.print("SPRES TOUTE");
        break;
      // May need to add commands... (not supposed)
      default:
        break;
    }
    delay(DELAY_LOOP);
  }
}

void step(char direction)
{
  // Set the direction
  // May need to be switched
  if (direction < 0)
    digitalWrite(DIR, LOW);
  else
    digitalWrite(DIR, HIGH);

  // Pulse to step
  digitalWrite(13, HIGH);
  delay(DELAY_SEND);
  digitalWrite(13, LOW);
}
