#include <Stepper.h>

#define STEP 200 	// steppermotor step size
#define HALF_ROT 100	// half rotation
/* initialize my_stepper */
Stepper my_stepper1 = Stepper(STEP, 8, 9);
Stepper my_stepper2 = Stepper(STEP, 10, 11);

void setup()
{
	my_stepper1.setSpeed(60);	// set speed of
	my_stepper2.setSpeed(60);	// steppers in RPM

	int step1_pos = 0;
	int step2_pos = 0;
}

void loop()
{

}


/* This function will close dam
   by alternating the steps taken 
   by each steppermotor */
void close_routine()
{
	int s;	// step counter

	for (s=0; s < HALF_ROT; ++s){
		my_stepper1.step(1);
		delay(200);
		my_stepper2.step(1);
		delay(200);
	}
}


/* This function opens the dam
   by alternating the steps taken
   by each steppermotor */
void open_routine()
{
	int s;	// step counter

	for (s=HALF_ROT; s > 0; --s){
		my_stepper1.step(1);
		delay(200);
		my_stepper2.step(2);
		delay(200);
	}
}
