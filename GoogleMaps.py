'''
IO Experiment 4
SMS coordinates to Address using Python 2.7 and Google Maps

Caberio
Cacalda
Decano
Gonzales

'''

# necessary imports
import sys
import os
import serial
import time
from Tkinter import *
from googlemaps import GoogleMaps

#objects and variables
gmaps = GoogleMaps(api_key = "AIzaSyD4qJM8Ai8dl3hTxvf_CiCimDWbFHdHey8")
SerialPort = serial.Serial("COM29",115200)
buf = ''
SerialPort.write('AT+CMGF=1\r\n')
time.sleep(1)
r1= SerialPort.read(SerialPort.inWaiting())
print r1
x = "OK" in r1


#mainloop
if x == True:
    print "Step1"
    buf = buf+r1
    print buf
    y = "OK" in buf
    if y == True:
        print "Step2"
        SerialPort.write('AT+CMGR=0\r\n')
        time.sleep(1)
        r2 = SerialPort.read(SerialPort.inWaiting())
        buf = buf+r2
        print buf
        buf1 = buf.split()

        lat = buf1[4]
        lng = buf1[5]
        u = buf1[3]
        splitsender = u.split(',')

        sender = splitsender[1]
        print 'Latitude = '+lat
        print 'Longitude = ' +lng
        print "Sender = "+sender
        LAT = float(lat)
        LNG = float(lng)
        destination = gmaps.latlng_to_address(LAT, LNG)
        print "The corresponding address is:\n"+destination


        #texting to sender
        SerialPort.write('AT+CMGS='+sender+'\r\n')
        time.sleep(1)
        print SerialPort.read(SerialPort.inWaiting())
        time.sleep(1)
        SerialPort.write(destination+'\x1A')
        print SerialPort.read(SerialPort.inWaiting())
        time.sleep(1)
        print 'Confirmation Message Sent'
        SerialPort.write('AT+CMGD=0\r\n')    

        #GUI
        app = Tk()
        app.title('IO Experiment 4: Coordinates to Address')
        app.geometry('350x300+350+400')
  	labeltext = StringVar()
        labeltext.set("Latitude: "+lat + "\nLongitude: "+lng+"\nSender: "+sender+"\nLocation: " +destination)
        label1 = Label(app, textvariable = labeltext, height =20)
        label1.pack()
        app.mainloop()


