import os
import sys
from picamera import PiCamera
import time
import boto3
# import RPi.GPIO as GPIO
import pigpio
import time
from numpy import interp

directory = '/home/pi/AWS_Rekognition_RaspberryPi'
PIN_NUM = 12

P = PiCamera()
P.resolution = (2592, 1944)
P.framerate = 15
P.start_preview()
collectionId = 'facecollection'

# aws cli credentials
rek_client = boto3.client('rekognition', region_name = 'eu-west-1')

# rek_client = boto3.client('rekognition',
#                         aws_access_key_id='',
#                         aws_secret_access_key='',
#                         region_name = 'eu-west-1')

def setAngle(angle = 0):
    duty_cycle = int((500 * 50 + (1900 * 50 * angle / 180)))
    return duty_cycle

pi = pigpio.pi()

def main():
    while True:
        time.sleep(2)
        milli = int(round(time.time() * 1000))
        image = '{}/image_{}.jpg'.format(directory,milli)
        P.capture(image, quality=80)
        # 使用二進制讀取圖片檔案
        with open(image, 'rb') as image_binary:
            try:
                match_response = rek_client.search_faces_by_image(CollectionId=collectionId, Image={'Bytes': image_binary.read()}, MaxFaces=1, FaceMatchThreshold=90)
                if match_response['FaceMatches']:
                    print('Hello, ',match_response['FaceMatches'][0]['Face']['ExternalImageId'])
                    for x in range(0, 91, 5):
                        print(x, "degree")
                        dc = setAngle(x)
                        pi.hardware_PWM(PIN_NUM, 50, dc)
                        time.sleep(0.05)
                    for x in range(90, -1, -90):
                        print(x, "xdegree")
                        dc = setAngle(x)
                        pi.hardware_PWM(PIN_NUM, 50, dc)
                        time.sleep(2)
                    print('Similarity: ',match_response['FaceMatches'][0]['Similarity'])
                    print('Confidence: ',match_response['FaceMatches'][0]['Face']['Confidence'])
                else:
                    print('No faces matched')
            except:
                print('No face detected')
        time.sleep(5)       
        print("Remove image name:", image_binary.name)
        os.remove(image_binary.name)

if __name__ == '__main__':
    main()