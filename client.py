import socket
import pickle
from huffman import Compressor


def compress(original_data, option=2):
    CompressorObject = Compressor(original_data)

    if option == 1:
        compressed_data, code_dict = CompressorObject.fixed_length_helper()
    else:
        compressed_data, code_dict = CompressorObject.variable_length_helper()

    return compressed_data, code_dict


def convert(string):
    l = []
    l[:0] = string
    return l


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 9998

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server\n")

    filename = str(input("Enter input file: "))
    with open(filename, 'r') as file:
        data = file.read()
    data = convert(data)
    print("Successfully read data from file!")

    print("\nChoose the type of Huffman Encoding:")
    print("1) Variable length (Default)")
    print("2) Fixed length")
    option = int(input("Your choice? "))

    compressed_data, code_dict = compress(data, option)

    print("\nSending compressed data and encoding...", end=" ")
    client_socket.send(pickle.dumps([compressed_data, code_dict]))
    print("done!")

    client_socket.close()
