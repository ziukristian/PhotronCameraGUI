import socket
from time import sleep


class Firefly_LW_2024:

    def __init__(self, sock = None):

        #create port
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        #connect to lan port, parameters: IP address, port number
        self.sock.connect(('192.168.1.231', 49946))
        print ("FireFly LAN port connected")

        #send message to laser (server) to establish link
        # messages are sent to laser in json format, see FireFly3 documentation
        #********make sure that the computer trying to talk to the M2 laser has IP address:192.168.1.187
        #********the M2 laser IP address is: 192.168.1.231
        startmessage_string = '{"message":{"transmission_id":[1],"op":"start_link","parameters":{"ip_address":"192.168.1.187"}}}'
        startmessage = bytes(startmessage_string,'UTF-8')
        self.sock.sendall(startmessage)

        startanswer = self.sock.recv(1024)
        condition_str = "ok"
        condition = bytes(condition_str,'UTF-8')
        if condition in startanswer:
            print ("Connected to FireFly3")
        else:
            print ("Could not connect to FireFly3. Respose to start link: ", startanswer)


    def ping(self):
        #send text message, reply should invert the case of sent message, see FireFly3 documentation
        while True:
            cmd = raw_input("Enter ping message (maximum 20 characters) or type exit to end: ")
            if cmd == 'exit':
                break
            else:
                pingmessage = '{"message": {"transmission_id": [1], "op": "ping", "parameters": {"text_in": "'+cmd+'"}}}'
                self.sock.sendall(pingmessage)
                pinganswer = self.sock.recv(1024)
                printanswer = pinganswer.replace('"}}}','') #this is just to make the respone cleaner and readable
                print ('Response : ', printanswer[78:])

    def temperature(self):
        temperaturemessage = '{"message":{"transmission_id":[1],"op":"temperature_status"}}'
        self.sock.sendall(temperaturemessage)
        temperatureanswer = self.sock.recv(1024)
        print (temperatureanswer) #Need to reduce answer from the laser

    def wavelength_status(self):
        wavelengthstatusmessage_str = '{"message": {"transmission_id": [2], "op": "wavelength_status", "parameters": {"beam": "idler","units": "cm-1"}}}' # Asking the laser about its wavelength
        wavelengthstatusmessage = bytes(wavelengthstatusmessage_str,'UTF-8')
        self.sock.sendall(wavelengthstatusmessage)
        wavelengthstatusanswer = self.sock.recv(1024)
        #print (wavelengthstatusanswer)
        return wavelengthstatusanswer

    def go_to_wavelength(self,target):
        gotowavelengthmessage_str = '{"message": {"transmission_id": [3], "op": "go_to_wavelength", "parameters": {"target_wavelength": ['+str(target)+'],"beam": "idler","units": "cm-1"}}}' #Should change wavelength
        gotowavelengthmessage = bytes(gotowavelengthmessage_str,'UTF-8')
        self.sock.sendall(gotowavelengthmessage)
        sleep(0.5)  # time to change wavelength
        gotowavelengthanswer = self.sock.recv(1024)
        #print(gotowavelengthanswer)


#class Firefly_LW_2024:
    #pass


if __name__ == '__main__':
    Firefly = Firefly_LW_2024()#(sock=None)
    #Firefly3.ping()
    #Firefly3.temperature()
    Firefly.wavelength_status()
    #Firefly3.go_to_wavelength(3305)
    #Firefly.wavelength_status()
    #Firefly3.disconnect()
'''
    len_lambda = 161 #edit here, number of steps for wavelength scan - if >5nm steps, change sleep time in Firefly3a library
    lambda1, lambda2 = 2900, 3700 #edit here, wavelength range for spectrum in nm
    lambda_pattern = np.linspace(lambda1,lambda2,len_lambda)
    scan_shape = np.shape(lambda_pattern)
    data = np.zeros(scan_shape)

    Firefly3.go_to_wavelength(lambda1)
    sleep(5.0)  # to allow Firefly to change wavelength

    for index in np.ndindex(scan_shape):
        Firefly3.go_to_wavelength(lambda_pattern[index])
        Firefly3.wavelength_status()

'''
