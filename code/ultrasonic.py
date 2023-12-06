
import csv
import time
import Jetson.GPIO as GPIO
names=["kitchen","others","recycle","harmful"]
distance=[[111,111,111,111],[222,222,222,222],[333,333,333,333],[444,444,444,444]]
count=0
def ultrasonic(): 
    global distance 
    global count
    global names
    while True:
        trig_pin1 = 22  # 发射超声波信号的GPIO引脚
        echo_pin1 = 21  # 接收超声波回波的GPIO引脚
        trig_pin2 = 24  # 发射超声波信号的GPIO引脚
        echo_pin2 = 23  # 接收超声波回波的GPIO引脚
        trig_pin3 = 26  # 发射超声波信号的GPIO引脚
        echo_pin3 = 19  # 接收超声波回波的GPIO引脚
        trig_pin4 = 18  # 发射超声波信号的GPIO引脚
        echo_pin4 = 16  # 接收超声波回波的GPIO引脚
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(trig_pin1, GPIO.OUT)
        GPIO.setup(echo_pin1, GPIO.IN)
        GPIO.setup(trig_pin2, GPIO.OUT)
        GPIO.setup(echo_pin2, GPIO.IN)
        GPIO.setup(trig_pin3, GPIO.OUT)
        GPIO.setup(echo_pin3, GPIO.IN)
        GPIO.setup(trig_pin4, GPIO.OUT)
        GPIO.setup(echo_pin4, GPIO.IN)
        
        pulse_start1=-2
        pulse_end1=-1
        pulse_start2=-2
        pulse_end2=-1
        pulse_start3=-2
        pulse_end3=-1
        pulse_start4=-2
        pulse_end4=-1

        

        GPIO.output(trig_pin1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig_pin1, GPIO.LOW)
        now1_time=time.time()

        while (time.time()-now1_time)<1 :
            if GPIO.input(echo_pin1) == 1 :
                pulse_start1 = time.time()
                break
                
        now2_time=pulse_start1###################
        while (time.time()-now2_time)<1:
            if GPIO.input(echo_pin1) == 0 :
                pulse_end1 = time.time()
                break
        if(pulse_start1>0 and pulse_end1>0):
            pulse_duration1 = pulse_end1 - pulse_start1
            distance[0][count] = pulse_duration1 * 17000  # 声速（cm/s）/ 2
            distance[0][count] = round(distance[0][count], 2)
        else:
            distance[0][count]=100

        GPIO.output(trig_pin2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig_pin2, GPIO.LOW)
        now1_time=time.time()

        while (time.time()-now1_time)<1 :
            if GPIO.input(echo_pin2) == 1 :
                pulse_start2 = time.time()
                break
                
        now2_time=pulse_start2
        while (time.time()-now2_time)<1:
            if GPIO.input(echo_pin2) == 0 :
                pulse_end2 = time.time()
                break
        if(pulse_start2>0 and pulse_end2>0):
            pulse_duration2 = pulse_end2 - pulse_start2
            distance[1][count] = pulse_duration2 * 17000  # 声速（cm/s）/ 2
            distance[1][count] = round(distance[1][count], 2)
        else:
            distance[1][count]=100

        GPIO.output(trig_pin3, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig_pin3, GPIO.LOW)
        now1_time=time.time()

        while (time.time()-now1_time)<1 :
            if GPIO.input(echo_pin3) == 1 :
                pulse_start3 = time.time()
                break
                
        now2_time=pulse_start3
        while (time.time()-now2_time)<1:
            if GPIO.input(echo_pin3) == 0 :
                pulse_end3 = time.time()
                break
        if(pulse_start3>0 and pulse_end3>0):
            pulse_duration3 = pulse_end3 - pulse_start3
            distance[2][count] = pulse_duration3 * 17000  # 声速（cm/s）/ 2
            distance[2][count] = round(distance[2][count], 2)
        else:
            distance[2][count]=100  


        GPIO.output(trig_pin4, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig_pin4, GPIO.LOW)
        now1_time=time.time()

        while (time.time()-now1_time)<1 :
            if GPIO.input(echo_pin4) == 1 :
                pulse_start4 = time.time()
                break
                
        now2_time=pulse_start4
        while (time.time()-now2_time)<1:
            if GPIO.input(echo_pin4) == 0 :
                pulse_end4 = time.time()
                break
        if(pulse_start4>0 and pulse_end4>0):
            pulse_duration4 = pulse_end4 - pulse_start4
            distance[3][count] = pulse_duration4 * 17000 # 声速（cm/s）/ 2
            distance[3][count] = round(distance[3][count], 2)
        else:
            distance[3][count]=100   

        if (count+1)<4:
            count+=1
        else:
            count=0
            distance=[[111,111,111,111],[222,222,222,222],[333,333,333,333],[444,444,444,444]]
            

        time.sleep(1)
        print(distance)

        with open("/home/mebius/workspace/yolov5/expression.csv", 'a', newline='') as csv_file:
            filenames=['Total','Kinds','Numbers','Success']
            writer=csv.DictWriter(csv_file,fieldnames=filenames)
            for i in range(4):
                if all(distance[i][count] <= 8 for count in range(3)):
                    writer.writerow({'Total':f"{names[i]}",'Kinds':" is ",'Numbers':"FULL",'Success':" !!! "})

ultrasonic()


    


