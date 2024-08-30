import serial
import bluetooth

# Configure serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Replace with your serial port
    baudrate=115200,
    timeout=1
)

# Bluetooth server setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

# Make the device discoverable
bluetooth.advertise_service(
    server_sock, "SerialData",
    service_id="00001101-0000-1000-8000-00805F9B34FB",
    service_classes=["00001101-0000-1000-8000-00805F9B34FB", bluetooth.SERIAL_PORT_CLASS],
    profiles=[bluetooth.SERIAL_PORT_PROFILE]
)

print(f"Waiting for connection on RFCOMM channel {port}...")

# Wait for a connection from a Bluetooth client
client_sock, client_info = server_sock.accept()
print(f"Accepted connection from {client_info}")

try:
    while True:
        # Read data from the serial port
        data = ser.readline()
        if data:
            # Send data to the connected Bluetooth device
            client_sock.send(data)
            print(f"Sent: {data.decode('utf-8').strip()}")

except OSError:
    pass

finally:
    print("Disconnected.")
    client_sock.close()
    server_sock.close()
    ser.close()
    print("All connections closed.")
