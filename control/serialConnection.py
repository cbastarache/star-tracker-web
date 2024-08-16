import serial
import serial.tools
import time
import serial.tools.list_ports

class SerialTerminal:
    def __init__(self):
        self.getPorts()

    def __del__(self):
        self.close()

    def getPorts(self):
        self.ports = serial.tools.list_ports.comports()

        self.port_ids = []
        for p in self.ports:
            self.port_ids += [p.name]
        return self.port_ids

    def openPort(self, port):
        print("connecting to port", port)
        self.ser = serial.Serial(port)
        self.ser.flush()
        time.sleep(0.5)

    def write(self, cmd):
        self.ser.write(cmd.encode())
        time.sleep(0.1)

    def read(self):
        msg = b''
        while self.ser.in_waiting > 0:
            msg += self.ser.read(1)
        self.msg = msg.decode("utf-8")
        # callback(self.msg)
        return self.msg

    def close(self):
        self.ser.close()

    def nullCallback(msg):
        print(msg)

        
if __name__ == "__main__":
    ser = SerialTerminal()
