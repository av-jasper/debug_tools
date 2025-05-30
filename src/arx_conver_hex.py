# Convert the provided hex array into a byte string and decode it.

hex_list = [
    'fd', '2e', '0', '0', '17', '1', '1', 'b3', '1', '0', '1', '0', '0', '0', '0',
    '0', '0', '0', '9', '1', '0', '4e', '6f', '20', '6d', '6f', '64', '65', '0',
    'b', 'd1', '60', '0', '0', '53', '4', 'e6', '2b', '6c', '7d', '0', '0', '0',
    '10', '80', '0', '0', '0', '0', '0', '88', '14', '0', 'f0', '6b', '7d', '84', 'db'
]

# Convert hex strings to bytes
data_bytes = bytes(int(x, 16) for x in hex_list)

# Decode to string using Latin-1 to preserve all byte values
decoded_str = data_bytes.decode('latin-1')

print("Decoded String:")
print(decoded_str)
print("\nString Representation (with escape sequences):")
print(repr(decoded_str))
print("\nIndividual Characters:")
print([c for c in decoded_str])
