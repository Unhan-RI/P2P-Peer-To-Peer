import socket
import time

def spam_message(target_host, target_port, message, repeat_count):
    total_bytes_sent = 0
    total_time_taken = 0
    total_latency = 0
    total_response_time = 0
    error_count = 0

    for i in range(repeat_count):
        try:
            # Start time to measure latency (time to establish connection)
            start_time = time.time()

            # Establish connection
            neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neighbor_socket.connect((target_host, target_port))
            latency = time.time() - start_time  # Latency: connection time
            total_latency += latency
            
            print(f"Latency for message {i + 1}: {latency:.6f} seconds")

            # Start time to measure response time (time to send and close connection)
            start_time = time.time()
            
            # Send the message
            message_to_send = f"MESSAGE {message} - Spam {i + 1}".encode()
            bytes_sent = neighbor_socket.send(message_to_send)
            total_bytes_sent += bytes_sent

            # Close connection
            neighbor_socket.close()

            response_time = time.time() - start_time  # Response time: send + close time
            total_response_time += response_time
            total_time_taken += response_time

            print(f"Response time for message {i + 1}: {response_time:.6f} seconds")
            print(f"Bytes sent for message {i + 1}: {bytes_sent} bytes")
            
            time.sleep(0.5)  # Adjust the delay between messages if needed

        except Exception as e:
            print(f"Error sending message to {target_host}:{target_port}: {e}")
            error_count += 1

    # Calculate averages and throughput
    if repeat_count - error_count > 0:
        avg_latency = total_latency / (repeat_count - error_count)
        avg_response_time = total_response_time / (repeat_count - error_count)
    else:
        avg_latency = 0
        avg_response_time = 0

    if total_time_taken > 0:
        throughput = total_bytes_sent / total_time_taken
    else:
        throughput = 0

    print_summary(repeat_count, error_count, avg_latency, avg_response_time, total_bytes_sent, throughput)

def print_summary(repeat_count, error_count, avg_latency, avg_response_time, total_bytes_sent, throughput):
    print("\n===== Test Summary =====")
    print(f"Total messages attempted: {repeat_count}")
    print(f"Total errors encountered: {error_count}")
    print(f"Average latency: {avg_latency:.6f} seconds")
    print(f"Average response time: {avg_response_time:.6f} seconds")
    print(f"Total bytes sent: {total_bytes_sent} bytes")
    print(f"Overall throughput: {throughput:.6f} bytes/second")
    print("========================\n")


if __name__ == "__main__":
    target_host = '10.2.55.83'  # Adjust to your target host
    target_port = 5009         # Adjust to your target port
    message = "This is a spam message"  # Custom message for spamming

    while True:
        choice = input("Select spam count: (1) 5 times, (2) 10 times, (3) 20 times, (type 'exit' to quit): ")
        
        if choice == '1':
            spam_message(target_host, target_port, message, 5)
        elif choice == '2':
            spam_message(target_host, target_port, message, 10)
        elif choice == '3':
            spam_message(target_host, target_port, message, 20)
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid choice. Please select again.")
