import socket
import pickle
from huffman import Decompressor


def decompress(compressed_data, code_dict):
    DecompressorObject = Decompressor(compressed_data, code_dict)
    decompressed_data = DecompressorObject.decompressor()

    return decompressed_data


def recvall(socket):
    BUFF_SIZE = 4096

    fragments = b''
    while True:
        chunk = socket.recv(BUFF_SIZE)
        if not chunk:
            break
        fragments += chunk

    return fragments


def convert(list):
    return ''.join(list)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 9998

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server running...")

    client_socket, addr = server_socket.accept()
    print("Got a connection from %s" % str(addr))

    print("\nReceiving compressed data and encoding...", end=" ")
    recv_data = pickle.loads(recvall(client_socket))
    print("done!")

    client_socket.close()

    uncompressed_data = convert(decompress(recv_data[0], recv_data[1]))

    filename = str(input("\nEnter output file: "))
    with open(filename, 'w') as file:
        file.write(uncompressed_data)
    print("Successfully wrote data to file!")
