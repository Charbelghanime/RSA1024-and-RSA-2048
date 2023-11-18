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



def encryptMessage(message, public_key, blockSize=DEFAULT_BLOCK_SIZE, encrypted_blocks_file='encrypted_blocks.txt'):
    encryptedBlocks = []

    # Extract public key components (n, e)
    n, e = public_key

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
def generate_random_message(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
def generate_signature(message, private_key, signature_file='signature.txt'):
    # Extract private key components (n, d)
    n, d = private_key

    # Hash the message using SHA-256
    hashed_message = int(SHA256.new(message.encode()).hexdigest(), 16)

    # Sign the hashed message using the private key
    signature = pow(hashed_message, d, n)

    # Save the signature to a file
    with open(signature_file, 'w') as signature_file:
        signature_file.write(str(signature))

    return signature

def verify_signature(message, public_key, signature_file='signature.txt'):
    # Extract public key components (n, e)
    n, e = public_key

    # Hash the message using SHA-256
    hashed_message = int(SHA256.new(message.encode()).hexdigest(), 16)

    # Read the signature from the file
    with open(signature_file, 'r') as signature_file:
        signature = int(signature_file.read().strip())

    # Verify the signature using the public key
    decrypted_signature = pow(signature, e, n)
    return decrypted_signature == hashed_message
def main():
    y = int(input("Enter the key size: "))
    public_key, private_key = kg.keygenerated(y)

    # Save public and private keys to files
    public_key_file = 'public_key.txt'
    private_key_file = 'private_key_d.txt'

    with open(public_key_file, 'w') as public_key_file:
        public_key_file.write(f"{public_key[0]}\n{public_key[1]}")

    with open(private_key_file, 'w') as private_key_file:
        private_key_file.write(f"{private_key[0]}\n{private_key[1]}")

    # Generate a random message
    random_message = generate_random_message(50)
    print("Original Message:", random_message)

    # Generate a digital signature for the message and save it to a file
    signature = generate_signature(random_message, private_key)
    print("Digital Signature:", signature)

    # Verify the signature from the file
    verification_result = verify_signature(random_message, public_key)
    print("Signature Verification Result:", verification_result)

    # Encrypt the message using the correct public key
    encrypted_blocks_file = encryptMessage(random_message, public_key)

    # Decrypt the message
    decrypted_message = decryptMessage('private_key_n.txt', 'private_key_d.txt', encrypted_blocks_file, len(random_message), private_key)
    print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()
