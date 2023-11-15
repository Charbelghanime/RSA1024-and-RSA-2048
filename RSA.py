import keygenerator as kg
import os
from Crypto.Hash import SHA256,SHA512,SHA384,MD5,SHA1
from Crypto.Signature import pkcs1_15
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme # to used for signature.
DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 128 
hash="SHA-256" #will be used by default
def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    messageBytes = message.encode('ascii')

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)



def encryptMessage(message, public_key_file='public_key.txt', blockSize=DEFAULT_BLOCK_SIZE, encrypted_blocks_file='encrypted_blocks.txt'):
    encryptedBlocks = []

    # Read public key (n, e) from the public_key_file
    with open(public_key_file, 'r') as public_key_file:
        # Skip lines that are not numeric
        n, e = [int(line.strip()) for line in public_key_file.readlines() if line.strip().isdigit()]

    # Ensure that the message is a multiple of the block size
    padded_message = message.ljust((len(message) // blockSize + 1) * blockSize, '\0')

    with open(encrypted_blocks_file, 'w') as encrypted_file:
        for block in getBlocksFromText(padded_message, blockSize):
            encrypted_block = pow(block, e, n)
            encryptedBlocks.append(encrypted_block)
            encrypted_file.write(f"{encrypted_block}\n")

    return encrypted_blocks_file


def decryptMessage(private_key_n_file, private_key_d_file, encrypted_blocks_file, messageLength=None, key=None, blockSize=DEFAULT_BLOCK_SIZE):
    if key is None:
        raise ValueError("Key is required for decryption.")

    decryptedBlocks = []
    n, d = key

    with open(encrypted_blocks_file, 'r') as encrypted_file:
        for line in encrypted_file:
            encrypted_block = int(line.strip())
            decrypted_block = pow(encrypted_block, d, n)
            decryptedBlocks.append(decrypted_block)

    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


# def sign_message(privatekey, message,hashalgo):
#     global hash # since that hash will be used in decryption
#     hash_alg=hash
#     signer=PKCS115_SigScheme(privatekey)#here the private will be signed.
#     if (hash == "SHA-512"):
#       signed = SHA512.new()
#     elif (hash == "SHA-384"):
#       signed = SHA384.new()
#     elif (hash == "SHA-256"):
#       signed = SHA256.new()
#     elif (hash == "SHA-1"):
#       signed = SHA1.new()
#     else:
#       signed = MD5.new()
#     signed.update(message)
#     return signer.sign(signed)
# def verify_signature(message, signature, public_key):
#     verifier = pkcs1_15.new(public_key)
    
#     if hash == "SHA-512":
#         digest = SHA512.new()
#     elif hash == "SHA-384":
#         digest = SHA384.new()
#     elif hash == "SHA-256":
#         digest = SHA256.new()
#     elif hash == "SHA-1":
#         digest = SHA1.new()
#     else:
#         digest = MD5.new()
    
#     digest.update(message)
#     return verifier.verify(digest, signature)



def generate_random_message(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def main():
    # Generate a key pair
    public_key, private_key = kg.keygenerated(1024)

    # Save public key to a file
    public_key_file = 'public_key.txt'

    # Extract the public key from the tuple
    actual_public_key = public_key[0]

    # Generate a random message
    random_message = generate_random_message(50)
    print("Original Message:", random_message)

    # Encrypt the message using the correct public key
    encrypted_blocks_file = encryptMessage(random_message, public_key_file)

    # Decrypt the message
    decrypted_message = decryptMessage('private_key_n.txt', 'private_key_d.txt', encrypted_blocks_file, len(random_message), private_key)
    print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()

# message_to_sign = b'This is a test message.'

# # Choose a hash algorithm
# hash_algorithm = "SHA-256"

# # Sign the message
# signature = sign_message(private_key, message_to_sign, hash_algorithm)
# print("Signature:", signature)

# # Verify the signature
# is_valid_signature = verify_signature(message_to_sign, signature, public_key)
# print("Is Valid Signature:", is_valid_signature)
