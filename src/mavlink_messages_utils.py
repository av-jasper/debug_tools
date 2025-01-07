import time
from pymavlink import mavutil

def print_command_ack(connection):
    print_specific_message(connection, "COMMAND_ACK" )

# Type is string
def print_specific_message(connection, type ):

    while True:
        # Wait for the next message
        msg = connection.recv_match(type=type, blocking=True)

        
        if msg:
            data = msg.to_dict()
            
            # Print all fields
            for key, value in data.items():
                print(f"{key}: {value}")
        break


def print_messages_for_one_second(connection):
    """
    After sending a message, call this function to receive and print
    any MAVLink messages for up to 1 second.
    """
    start_time = time.time()
    while True:
        # Stop after 1 second
        if time.time() - start_time >= 0.5:
            break

        # Non-blocking read
        msg = connection.recv_match(blocking=False)
        if msg is not None:
            # Convert to dictionary
            data = msg.to_dict()

            # Print the entire message dict
            print("Received message:", msg.get_type())
            for key, value in data.items():
                print(f"  {key}: {value}")

        # Slight sleep to avoid busy-waiting
        time.sleep(0.01)
