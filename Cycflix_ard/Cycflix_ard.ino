/*
 * 
 * Exercise_bike.ino
 * This code is used to read an analog voltage from A7
 * to measure the varying frequnecy square coming from a 
 * stationary bike. This speed is sent over Serial to a python 
 * script which controls netflix, the the speed is too slow, netflix will
 * be paused.
 * Create By Ronan Byrne,
 * Last Updated 08/07/2017
 * Blog: https://roboroblog.wordpress.com/
 * Instructables Post: https://www.instructables.com/id/Cycflix-Exercise-Powered-Entertainment/ 
 * Youtube Video: https://youtu.be/-nc0irLB-iY
 */

volatile unsigned long temp_time = 0; // Temperarally save current time
volatile unsigned long time1 = 0;     // time of last rising edge
volatile unsigned long time_d = 0;    // time between rising edges
volatile float Speed = 0;             // Cycling speed
volatile uint8_t count = 0;           // Count used for reseting speed
volatile bool voltage_low;            // Bool to check if voltage high or low
volatile uint16_t voltage_b = 0;      // Analog voltage in bits
  
void setup()
{
  noInterrupts();
  //set timer1 interrupt at 2Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 7812;// = (16*10^6) / (2*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  pinMode(A7,INPUT);
  interrupts();

  Serial.begin(115200); // Set baudrate at max speed(115200)
  establishContact();// Wait for a response from the PC
  if (analogRead(A7) >= 150)
  {
    voltage_low = 0;
  }
  else
  {
    voltage_low = 1;
  }
}

// Add loop code
void loop() 
{
  voltage_b = analogRead(A7);
  // Check for rising edge, calculate speed
  if (voltage_low && (voltage_b >= 150))
  {
    temp_time = millis();
    time_d = temp_time-time1;
    time1 = temp_time;
    voltage_low = 0;
    Speed = time_d*-0.0384+60.372;
    count = 0;
  }
  // Check for falling edge
  else if (!voltage_low && (voltage_b < 30))
  {
    voltage_low = 1;
  }
}

void establishContact() {
  // Send "B" until a response is heard
  while (Serial.available() == 0) {
    Serial.println("B");
    delay(300);
  }
  Serial.flush();
}

// Timer Interrupt
ISR(TIMER1_COMPA_vect){
  count ++;
  // If speed hasn't been updated in 10 counts, reset
  if(count == 10)
  {
    Speed = 0;  
  }
  // Send Speed if requested
  if (Serial.available() > 0)
  {
    Serial.println(Speed);
  }
}
