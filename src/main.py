from vex import *

# GEAR RATIOS
# BLUE 6_1 max rpm 600
# GREEN 18_1 max rpm 200
# RED 36_1 max rpm 100


# Brain should be defined by default
brain = Brain()

# Robot configuration code
claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)

#8L, 3R
left_elevator = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
right_elevator = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)

controller_1 = Controller(PRIMARY)

front_left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
front_right = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
back_left = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
back_right = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)


def controller_L1_Pressed():
    left_elevator.spin(FORWARD)
    right_elevator.spin(FORWARD)
    # elevator_motor.spin(FORWARD)
    while controller_1.buttonL1.pressing():
        wait(5, MSEC)
    left_elevator.stop()
    right_elevator.stop()

def controller_L2_Pressed():
    left_elevator.spin(REVERSE)
    right_elevator.spin(REVERSE)
    while controller_1.buttonL2.pressing():
        wait(5, MSEC)
    left_elevator.stop()
    right_elevator.stop()

def controller_R1_Pressed():
    claw_motor.spin(REVERSE)
    while controller_1.buttonR1.pressing():
        wait(5, MSEC)
    claw_motor.stop()

def controller_R2_Pressed():
    claw_motor.spin(FORWARD)
    while controller_1.buttonR2.pressing():
        wait(5, MSEC)
    claw_motor.stop()


def clamp(x):
    return max(-100, min(100, x))


controller_1.buttonL1.pressed(controller_L1_Pressed)
controller_1.buttonL2.pressed(controller_L2_Pressed)
controller_1.buttonR1.pressed(controller_R1_Pressed)
controller_1.buttonR2.pressed(controller_R2_Pressed)
wait(15, MSEC)

left_elevator.set_stopping(HOLD)
right_elevator.set_stopping(HOLD)

claw_motor.set_stopping(HOLD)

left_elevator.set_velocity(60, PERCENT)
right_elevator.set_velocity(60, PERCENT)

claw_motor.set_velocity(30, PERCENT)

while True:
    forward = controller_1.axis3.position()  # left stick up/down
    strafe = controller_1.axis4.position()   # left stick left/right
    turn = controller_1.axis1.position()     # right stick left/right

    # Deadband to stop drift
    if abs(forward) < 5:
        forward = 0
    if abs(strafe) < 5:
        strafe = 0
    if abs(turn) < 5:
        turn = 0

    front_left.spin(FORWARD,  clamp(forward + strafe + turn), PERCENT)
    front_right.spin(FORWARD, clamp(forward - strafe - turn), PERCENT)
    back_left.spin(FORWARD,   clamp(forward - strafe + turn), PERCENT)
    back_right.spin(FORWARD,  clamp(forward + strafe - turn), PERCENT)
    wait(5, MSEC)