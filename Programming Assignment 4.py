#!/usr/bin/env python
# coding: utf-8

# In[1]:


with open('C:\\Users\\aidan\\FA_23\\Applied Algorithms\\huffman_book.txt', 'r', encoding='utf-8') as file:
    content = file.read()


# In[3]:


CharNum = 128
ALLOWED_CHARS = "".join([chr(i) for i in range(CharNum)])


# In[4]:


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def compute_frequencies(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

def build_huffman_tree(freq):
    from queue import PriorityQueue
    pq = PriorityQueue()
    for char, freq in freq.items():
        pq.put(Node(char, freq))
    while pq.qsize() > 1:
        left = pq.get()
        right = pq.get()
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        pq.put(merged)
    return pq.get()

def get_codes_from_tree(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
    get_codes_from_tree(node.left, current_code + "0", codes)
    get_codes_from_tree(node.right, current_code + "1", codes)

def huffman_codes(freq):
    root = build_huffman_tree(freq)
    codes = {}
    get_codes_from_tree(root, "", codes)
    return codes


# In[5]:


def bits_diff(text):
    huffman_coding = huffman_codes(compute_frequencies(text))
    huffman_bits = sum([len(huffman_coding[char]) for char in text])
    fixed_length_bits = 7 * len(text)
    return fixed_length_bits - huffman_bits


# In[6]:


diff = bits_diff(content)
print(f"Bits saved using Huffman encoding compared to 7-bit fixed length: {diff}")


# In[11]:


huffman_dict = huffman_codes(compute_frequencies(content))
for char, code in huffman_dict.items():
    # This will display the character and its corresponding Huffman code
    print(f"'{char}': {code}")


# In[12]:


import unittest

class TestHuffmanEncoding(unittest.TestCase):

    def test_compute_frequencies(self):
        text = "aabbc"
        expected = {'a': 2, 'b': 2, 'c': 1}
        self.assertEqual(compute_frequencies(text), expected)

    def test_huffman_codes_simple(self):
        freq = {'a': 2, 'b': 2, 'c': 1}
        codes = huffman_codes(freq)
        # Note: Exact Huffman codes can vary based on implementation and tree structure.
        # This checks the basic correctness: 'a' and 'b' should have shorter codes than 'c'.
        self.assertTrue(len(codes['a']) <= len(codes['c']))
        self.assertTrue(len(codes['b']) <= len(codes['c']))

    def test_bits_diff(self):
        text = "aabbc"
        diff = bits_diff(text)
        # For this simple text, Huffman encoding shouldn't be more efficient than fixed-length encoding.
        self.assertGreaterEqual(diff, 0)

    def test_huffman_codes_with_all_chars(self):
        # Considering all characters are equally frequent, 
        # Huffman code should not be more efficient than fixed-length encoding.
        text = "".join([chr(i) for i in range(CharNum)])
        freq = {char: 1 for char in text}
        codes = huffman_codes(freq)
        total_bits = sum([len(code) for code in codes.values()])
        self.assertEqual(total_bits, 7 * CharNum)

if __name__ == '__main__':
    unittest.main()


# In[13]:





# In[ ]:




