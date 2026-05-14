from gpiozero import OutputDevice
from time import sleep

# pins 
step_pin = OutputDevice(6)
dir_pin = OutputDevice(5)
en_pin = OutputDevice(13)


def move_motor(steps, forward = True):
	dir_pin.value = forward
	step_pin.on()
	for i in range(steps):
		step_pin.on()
		sleep(0.005)
		step_pin.off()
		sleep(0.005)
	step_pin.off()
def motor_off():
	step_pin.off()
	en_pin.on()
def motor_on():
	en_pin.off()
def vibromove(time):
	for i in range(time*5):

		move_motor(8,forward=True)
		sleep(0.01)
		move_motor(6,forward= False)
		sleep(0.01)
#try:
#	while True:
#		x = int(input())
#
#		vibromove(x)
#		print("giving a bit of korm")
#
#except KeyboardInterrupt:
#	motor_off()
#	print("program ended")
#except err:
#	motor_off()
#	print(err)
motor_on()
vibromove(10)
motor_off()

