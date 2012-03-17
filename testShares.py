import random
import Image
import sys
import os
import numpy

def converListToString(List):
	S = ''
	for num in List:
		S = S + str(num)
	return S

def rotateLeft(a,n):
	a = list(a)
	n = n % len(a)
	x = a[n:]
	x.extend(a[:n])
	x = numpy.array(x)
	return x

def rotateRight(a,n):
	a = list(a)
	n = n % len(a)
	x = a[-n:]
	x.extend(a[:-n])
	x = numpy.array(x)
	return x

def convertStringtoArrayNew(S): #This is slightly different from its generateShares.py counterpart
	List = []
	for bit in S:
		List.append(int(bit))
	return numpy.array(List)

def convertStringtoArray(S):
	List = []	
	for number in S:
		NumberInListForm = []
		for bit in number:
			NumberInListForm.append(int(bit))
		List.append(numpy.array(NumberInListForm))
	return numpy.array(List)

def convertArrayToNumber(array): #New function
	#print "Array:", array
	List = []
	for channel in array:
		List.append(channel[0])
	String = converListToString(List)
	#print String
	return int(String, 2)

os.system("rm Reconstructed.png")
if len(sys.argv) < 2:
	print "Insufficient arguments. Please Re-enter."
	exit(0)

size = Image.open("part1.png").size
baseImage = Image.new("RGB", size, None)
for y in range(size[1]):
	for x in range(size[0]):
		baseImage.putpixel((x,y), (0,0,0))

numOfComponents = int(sys.argv[1])
for i in range(numOfComponents):
	imOri = Image.open("part" + str(i+1) + ".png")
	im = imOri.copy()
	#im = im.convert("L")
	for y in range(size[1]):
		for x in range(size[0]):
			pixVal = im.getpixel((x,y))
			pixVal = list(pixVal)
			baseImageVal = baseImage.getpixel((x,y))

			#print "pixVal", pixVal
			#print "baseImageVal", baseImageVal

			for i in range(len(pixVal)):
				pixVal[i] = pixVal[i] | baseImageVal[i]
			
			baseImage.putpixel((x,y), tuple(pixVal))
			#print baseImage.getpixel((x,y))


for y in range(size[1]):
	for x in range(size[0]):
		masked = baseImage.getpixel((x,y))
		masked = list(masked)
		for i in range(len(masked)):
			array = convertStringtoArray(numpy.binary_repr(masked[i], width=8))
			#print "masked:  ", masked
			rotated = rotateRight(array, 5)
			#print "rotated: ", rotated
			#print "rotated", convertArrayToNumber(rotated)
			masked[i] = convertArrayToNumber(rotated)
			#print masked[i]
		baseImage.putpixel((x,y), tuple(masked))

baseImage.save("Reconstructed.png")
baseImage.show()
