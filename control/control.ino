#include <Stepper.h>

#define MOTOR_REV 32 	// steppermotor internal step size
#define FULL_ROT 2048	// stepper makes full rotation in 2048 steps

/* initialize my_stepper */
Stepper my_stepper1(MOTOR_REV, 8, 10, 9, 11);
Stepper my_stepper2(MOTOR_REV, 4, 6, 5, 7);

int serial_data;

void setup()
{
	my_stepper1.setSpeed(400);	// set speed of
	my_stepper2.setSpeed(400);	// steppers in RPM

	Serial.begin(9600);		// wait for client serial conn
}

void loop()
{
	if (Serial.available() > 0){
		serial_data = Serial.read();

		switch(serial_data){
			case 'A':
				Serial.println("CLOSE");
				close_routine();
				break;
			case 'B':
				Serial.println("OPEN");
				open_routine();
				break;
		}
	}
}


/* This function will close dam
   by alternating the steps taken 
   by each steppermotor */
void close_routine()
{
	int s;	// step counter

	/* 1/8 rotation inward */
	for (s=0; s < FULL_ROT / 8; ++s){
		my_stepper1.step(1);
		delay(30);
		my_stepper2.step(-1);
		delay(30);
	}
}


/* This function opens the dam
   by alternating the steps taken
   by each steppermotor */
void open_routine()
{
	int s;	// step counter

	/* 1/8 rotation outward */
	for (s=0; s < FULL_ROT / 8; ++s){
		my_stepper1.step(-1);
		delay(30);
		my_stepper2.step(1);
		delay(30);
	}
}
