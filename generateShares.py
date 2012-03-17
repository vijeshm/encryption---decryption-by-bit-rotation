import random
import Image
import sys
import os
import numpy

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

def initNewImage(im):
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			im.putpixel((y,x), (255,255,255))

def convertStringtoArray(S):
	List = []	
	for number in S:
		NumberInListForm = []
		for bit in number:
			NumberInListForm.append(int(bit))
		List.append(numpy.array(NumberInListForm))
	return numpy.array(List)

def converListToString(List):
	S = ''
	for num in List:
		S = S + str(num)
	return S

def convertArrayToNumber(array):
	DecimalValues = []
	for channel in array:
		List = list(channel)
		String = converListToString(List)
	 	DecimalValues.append(int(String, 2))
	return tuple(DecimalValues)

os.system("rm part*.png")
if len(sys.argv) < 3:
	print "Insufficient arguments. Please Re-enter."
	exit(0)

numOfComponents = int(sys.argv[2])
imOri = Image.open(sys.argv[1])
im = imOri.copy()
#im = im.convert("L")
size = im.size

#a.tolist()
#numpy.bitwise_and(numpy.array([1,0,1]), numpy.array([1,0,0]))
#numpy.binary_repr(100)

components = []
for i in range(numOfComponents):
	imTemp = Image.new("RGB", size, None)
	#initNewImage(imTemp)

	components.append(imTemp)

prog = 0
total = size[0] * size[1]
for y in range(size[1]):
	for x in range(size[0]):
		pixVal = im.getpixel((x,y))
		binRep = []
		for channel in pixVal:
			binRep.append(numpy.binary_repr(channel, width=8))
		#print binRep
		binRep = convertStringtoArray(binRep)
		#print binRep

		binArr = []
		for i in range(len(components)):
			channelValues = []
			for channel in binRep:
				masked = numpy.random.randint(2,size=8) & channel
				rotated = rotateLeft(masked, 5)
				channelValues.append(rotated)
			binArr.append(channelValues)
		
		for i in range(len(binArr)):
			binArr[i] = convertArrayToNumber(binArr[i])

		for i in range(len(components)):
			components[i].putpixel((x,y), binArr[i])

		#left/right shift

		prog += 1
		sys.stdout.write(50*"\b")
		sys.stdout.write("progress: " + str( float(prog) / total * 100) + "%")
		sys.stdout.flush()
print "\n"

count = 1
for component in components:
	component.save("part" + str(count) + ".png","PNG")
	print "Written into part" + str(count) + ".png"
	count += 1
