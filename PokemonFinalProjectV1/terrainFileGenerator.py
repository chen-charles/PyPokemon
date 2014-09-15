__author__ = 'Charles-Jianye Chen'
import rgine as rgine

def generate(width, height, ordered=True):
	terrain = rgine.Terrain("w", width, height, 32, 32)
	if ordered:
			i = 0
			for y in range(height):
					for x in range(width):
						terrain.setIdentifier(x, y, i)
						i += 1
			fname = "%dx%d_ordered" % (width, height)
			terrain.writeTerrain(fname)
	else:
		fname = "%dx%d" % (width, height)
		terrain.writeTerrain(fname)
	return fname

if __name__ == "__main__":
	t = input("-> Ordered? (T/F) ").lower()
	width = int(input("-> Width? "))
	height = int(input("-> Height? "))
	if t == "t":
		generate(width, height, True)
	else:
		generate(width, height, False)
	input("Done! ")

