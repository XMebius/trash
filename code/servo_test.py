from servo import PCA9685
import time

# Create an instance of PCA9685
pca = PCA9685(address=0x40, debug=True)

# Set PWM frequency (for example, 50 Hz)
pca.setPWMFreq(50)

# Set servo angle for channel 0 (for example, 45 degrees)
pca.setServoAngle(channel=0,angle= 50)
#pca.setServoAngle(channel=0,angle= -90)
time.sleep(2)
pca.setServoAngle(channel=1,angle= 30)

#time.sleep(2)

#pca.setServoAngle(channel=0,angle= 30)
#time.sleep(2)

#pca.setServoAngle(channel=0,angle= 90)
#pca.setServoAngle(channel=1,angle= 30)
