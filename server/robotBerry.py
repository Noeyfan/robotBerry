#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 19 NOV 2015

import time
import SocketServer
import struct
import sys, glob # for listing serial ports
import Tkinter as Tk

try:
  import serial
except ImportError:
  tkMessageBox.showerror('Import error', 'Please install pyserial.')
  raise

connection = None

class TetheredDriveApp(SocketServer.BaseRequestHandler):
  def handle(self):
    self.onConnect()
    self.data = self.request.recv(1024).strip()
    self.callbackKey(self.data)
    self.request.sendall("precessed")

  # sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
  def sendCommandASCII(self, command):
    cmd = ""
    for v in command.split():
      cmd += chr(int(v))
    self.sendCommandRaw(cmd)

  # sendCommandRaw takes a string interpreted as a byte array
  def sendCommandRaw(self, command):
    global connection
    try:
      if connection is not None:
	connection.write(command)
      else:
	print "Not connected."
    except serial.SerialException:
      print "Lost connection"
      connection = None
    print ' '.join([ str(ord(c)) for c in command ])

  def callbackKey(self, k):
    if k == 'P':   # Passive
      self.sendCommandASCII('128')
    elif k == 'S': # Safe
      self.sendCommandASCII('131')
    elif k == 'F': # Full
      self.sendCommandASCII('132')
    elif k == 'C': # Clean
      self.sendCommandASCII('135')
    elif k == 'D': # Dock
      self.sendCommandASCII('143')
    elif k == 'R': # Reset
      self.sendCommandASCII('7')
    elif k == 'FORWARD':
      self.forward()
    elif k == 'BACK':
      self.back()
    elif k == 'LEFT':
      self.turnLeft()
    elif k == 'RIGHT':
      self.turnRight()

  # iRobot commands
  def stop(self):
    self.sendCommandASCII('145 0 0 0 0')

  # TODO Rotation is not accurate
  def turnLeft(self):
    self.sendCommandASCII('145 0 150 255 106')
    time.sleep(1.3)
    self.stop()

  def turnRight(self):
    self.sendCommandASCII('145 255 106 0 150')
    time.sleep(1.3);
    self.stop()

  def forward(self):
    self.sendCommandASCII('145 0 200 0 200')
    time.sleep(2);
    self.sendCommandASCII('145 0 0 0 0')

  def back(self):
    self.sendCommandASCII('145 255 56 255 56')
    time.sleep(2);
    self.sendCommandASCII('145 0 0 0 0')

  def beep(self):
    self.sendCommandASCII('140 3 1 64 16 141 3')

  def dock(self):
    self.sendCommandASCII('143')

  def onConnect(self):
    global connection
    if connection is not None:
      print "Already Connect"
      return

    try:
      # ports are all avaliable ports, should select the USB-SERIAL
      ports = self.getSerialPorts()
      # TODO, ports[1] is for Darwin 10.11
      port = ports[1]
      print port
    except EnvironmentError:
      print "Port Error"

    if port is not None:
      print "Trying " + str(port) + "... "
    try:
      connection = serial.Serial(port, baudrate=115200, timeout=1)
      print "Connected!"
    except:
      print "Failed."

  def getSerialPorts(self):
    if sys.platform.startswith('win'):
      ports = ['COM' + str(i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
      # this is to exclude your current terminal "/dev/tty"
      ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
      ports = glob.glob('/dev/tty.*')

    else:
      raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
      try:
       s = serial.Serial(port)
       s.close()
       result.append(port)
      except (OSError, serial.SerialException):
	pass
    return result

if __name__ == "__main__":
  HOST, PORT = "localhost", 9999
  server = SocketServer.TCPServer((HOST, PORT), TetheredDriveApp)
  server.serve_forever()
