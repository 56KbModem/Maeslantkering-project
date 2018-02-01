#include <Stepper.h>

#define MOTOR_REV 32 	// steppermotor internal step size
#define FULL_ROT 2048	// stepper makes full rotation in 2048 steps

/* initialize my_stepper */
Stepper my_stepper1(MOTOR_REV, 8, 10, 9, 11);
Stepper my_stepper2(MOTOR_REV, 4, 6, 5, 7);

int sensor = A0;	// anolog input water sensor

int serial_data;	// incoming serial data

void setup()
{
	my_stepper1.setSpeed(400);	// set speed of
	my_stepper2.setSpeed(400);	// steppers in RPM

	pinMode(sensor, INPUT);		// water sensor is analog input

	Serial.begin(9600);		// wait for client serial conn
}

void loop()
{
	/* initialize measuring place */
	int place = 1;
	char rotterdam[4] = "RD ";
	char dordrecht[4] = "DD ";

	while (1){
		/* take a measurement at a site */
		char measurement[8];
		if (place == 1){
			strcpy(measurement, rotterdam);
		}
		else{
			strcpy(measurement, dordrecht);
		}
		char water_level_str[3];
		int water_level = measure_water_level(sensor);
		
		itoa(water_level, water_level_str, 10);
		strncat(measurement, water_level_str, 3);

		Serial.println(measurement);

		/* read command to open or close*/
		if (Serial.available() > 0){
			serial_data = Serial.read();

			switch(serial_data){
				case 'A':
					Serial.println("CLOSE");
					close_routine();
					Serial.flush();
					break;
				case 'B':
					Serial.println("OPEN");
					open_routine();
					Serial.flush();
					break;
				case 'C':
					if (place == 1){
						place = 0;
					}
					else if (place == 0){
						place = 1;
					}
			}
		}
		delay(1500); // wait 1.5 seconds
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

/* This function measures the water
   level as an analog input, converts
   it to centimeters and returns
   that value as an int*/
int measure_water_level(int sensor)
{
	int water_level = analogRead(sensor);
	water_level = map(water_level, 0, 650, 280, 310); // convert to cm.

	return water_level;
}

