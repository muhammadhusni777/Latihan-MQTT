######  PROGRAM MEMANGGIL WINDOWS PYQT5 ##########################

####### memanggil library PyQt5 ##################################
#----------------------------------------------------------------#
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtQml import * 
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *  
import sys
import paho.mqtt.client as paho

broker="127.0.0.1"
#broker="mqtt.ardumeka.com"#"broker.emqx.io"
#port = 11219
port = 1883
topic_test = ""
#----------------------------------------------------------------#


########## mengisi class table dengan instruksi pyqt5#############
#----------------------------------------------------------------#
class table(QObject):    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)    
        self.engine.load(QUrl("main.qml"))
        sys.exit(self.app.exec_())
    
    @pyqtSlot(str)
    def button1(self, message):
        global button1_status
        print(message)
        button1_status = message
        client.publish("Steering_DP 1",str(message))
        
    
    @pyqtSlot(result=str)
    def test_message(self):  return topic_test
#----------------------------------------------------------------#


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    t = str(message.topic)

    if(msg[0] == 'c'):
        val =  1
    else:
        val = (msg)
    
    if (t == "system"):
        global topic_test
        topic_test = (msg)
        print(topic_test)
        



########## memanggil class table di mainloop######################
#----------------------------------------------------------------#    
if __name__ == "__main__":
    client= paho.Client("PC_1")
    client.on_message=on_message

    print("connecting to broker ",broker)
    client.connect(broker,port)#connect
    print(broker," connected")
    
    client.loop_start()
    print("Subscribing")

    client.subscribe("system")
    
    main = table()
    
#----------------------------------------------------------------#