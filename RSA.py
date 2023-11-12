import keygenerator as kg
DEFAULT_BLOCK_SIZE_1024 = 128 #for the 1024 bits encryption
BYTE_SIZE_1024 = 256 #for the 1024 bits encryption

def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE_1024):
    messageBytes = message.encode('ascii')

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE_1024 ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE_1024):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE_1024 ** i)
                blockInt = blockInt % (BYTE_SIZE_1024 ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE_1024):
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE_1024):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


message = "hello world"
# Generate a key pair
public_key, private_key = kg.keygenerated(2048)

# Encrypt the message
encrypted_message = encryptMessage(message, public_key)

# Decrypt the message
decrypted_message = decryptMessage(encrypted_message, len(message), private_key)

print("Original Message:", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", decrypted_message)
