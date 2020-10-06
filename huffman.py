import copy
import heapq
from math import ceil, log
from collections import Counter


class HeapNode:
    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.flag = None

    def __gt__(self, node):
        if node == None or not isinstance(node, HeapNode):
            return -1
        return self.value > node.value

    def __lt__(self, node):
        if node == None or not isinstance(node, HeapNode):
            return -1
        return self.value < node.value


class TreePath:
    def __init__(self):
        self.temp_dict_var = {}

    def paths(self, root):
        path = []
        self.paths_rec(root, path, 0)

    def paths_rec(self, root, path, path_len):
        if root is None:
            return

        if len(path) > path_len:
            path[path_len] = root.flag
        else:
            path.append(root.flag)

        path_len += 1

        if root.left is None and root.right is None:
            self.temp_dict_var[root.key] = copy.deepcopy(
                ''.join(str(char) for char in path[1:]))
        else:
            self.paths_rec(root.left, path, path_len)
            self.paths_rec(root.right, path, path_len)


class Compressor:
    def __init__(self, orignal_data):
        self.orignal_data = orignal_data

    def freq_counter(self):
        return(dict(Counter(self.orignal_data)))

    def fixed_huffman_coding(self, freq_dict, length):
        orignal_data = self.orignal_data
        temp_dict, code_dict = {}, {}

        counter = 0
        for key in freq_dict:
            temp_dict[key] = bin(counter)[2:].zfill(length)
            code_dict[bin(counter)[2:].zfill(length)] = key
            counter += 1

        compressed_data = []
        for value in orignal_data:
            compressed_data.append(temp_dict[value])

        return compressed_data, code_dict

    def variable_huffman_coding(self, freq_dict):
        freq_dict = {key: value for key, value in sorted(
            freq_dict.items(), key=lambda item: item[1])}

        heap = []
        for key in freq_dict:
            node = HeapNode(key, freq_dict[key])
            heapq.heappush(heap, node)

        counter = 0
        while(len(heap) > 1):
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            node1.flag = 0
            node2.flag = 1

            merged = HeapNode(None, node1.value + node2.value)
            merged.flag = (counter % 2)
            counter += 1

            merged.left, merged.right = node1, node2
            heapq.heappush(heap, merged)

        treePath = TreePath()
        treePath.paths(heap[0])

        temp_dict = treePath.temp_dict_var
        compressed_data = []
        for elem in self.orignal_data:
            compressed_data.append(temp_dict[elem])

        code_dict = {}
        for key in temp_dict:
            code_dict[temp_dict[key]] = key

        return compressed_data, code_dict

    def fixed_length_helper(self):
        freq_dict = self.freq_counter()
        max_code_length = ceil(log(len(freq_dict), 2))
        compressed_data, code_dict = self.fixed_huffman_coding(
            freq_dict, max_code_length)

        return compressed_data, code_dict

    def variable_length_helper(self):
        freq_dict = self.freq_counter()
        compressed_data, code_dict = self.variable_huffman_coding(freq_dict)

        return compressed_data, code_dict


class Decompressor:
    def __init__(self, compressed_data, code_dict):
        self.compressed_data = compressed_data
        self.code_dict = code_dict

    def decompressor(self):
        orginal_data = []
        for value in self.compressed_data:
            orginal_data.append(self.code_dict[value])

        return orginal_data
