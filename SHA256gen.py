import sys
import os
from hashlib import sha256

#Configure here
ENTROPY_SIZE = 32 #gathered from linux urandom
SEED_THRESHOLD = 1048576 #update seed
OUTPUT_SIZE = 1000000000 #amount of LSBits


OUTPUT_NAME = "sha256_LSB.data"

def savePart(data):
	arq = open(OUTPUT_NAME, 'ab')
	arq.write(data.to_bytes(1, byteorder = 'little'))			
	arq.close()

def runGenerator(limitMBits):

	hashed = os.urandom(ENTROPY_SIZE)
	byteOutput = 0
	countBits = 0
	calls = 0
	for i in range(limitMBits):		
		calls = calls + 1
		hashed = sha256(hashed).digest() #seems to be a string output

		LSB = hashed[-1] & 1
		if (LSB == 1):
			byteOutput = (byteOutput << 1)+1
		else:
			byteOutput = (byteOutput << 1)

		countBits = countBits + 1
		if (countBits == 8):
			#save this in respective file
			savePart(byteOutput)
			byteOutput = 0
			countBits = 0
		
		if calls == SEED_THRESHOLD:			
			hashed = os.urandom(ENTROPY_SIZE)
			calls = 0
	
if __name__ == "__main__":
	print("SHA 256 Generator starting...")
	runGenerator(OUTPUT_SIZE) #1 Gbit

	print("Ended.")