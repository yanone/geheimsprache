from fontTools.ttLib import TTFont
import random, copy, os, time, base64

# Measure creation time
start = time.time()

# Read original TTF/OTF font file
f = TTFont('font.ttf')

# Find font's longest CMAP table
cmap = f['cmap']
longestCMAPtable = None
for t in cmap.tables:
	if not longestCMAPtable or len(t.cmap) > len(longestCMAPtable.cmap):
		longestCMAPtable = t


# Read it into a normal list for shuffling
# This is not excatly elegant, but it works. Improve it.
originalCMAP = []
for u in longestCMAPtable.cmap:
	originalCMAP.append((u, longestCMAPtable.cmap[u]))

# Make copy and shuffle that copy
newCMAP = copy.copy(originalCMAP)
random.shuffle(newCMAP)

# These funtions are ugly, but work well. Improve them.
def newNameToUnicode(unicode):
	for i in range(len(originalCMAP)):
		if originalCMAP[i][0] == unicode:
			return newCMAP[i][1]

def newUnicodeToUnicode(unicode):
	for i in range(len(originalCMAP)):
		if newCMAP[i][0] == unicode:
			return originalCMAP[i][0]

def newUnicodeToName(name):
	for i in range(len(newCMAP)):
		if newCMAP[i][1] == name:
			return originalCMAP[i][0]

def translateText(text):
	new = u''
	for g in text:
		if newUnicodeToUnicode(ord(g)):
			new += unichr(newUnicodeToUnicode(ord(g)))
	return new


# Go through all entries in all cmap tables and assign the new randomized glyph names to the unicodes
for t in cmap.tables:
	for u in t.cmap.keys():
		if newNameToUnicode(u):
			t.cmap[u] = newNameToUnicode(u)


# Save new font file to disk
# Maybe it's a good idea to use unique file names here
f.save('new.ttf')

# Stop measuring time
end = time.time()

# Read font file into base64 string for delivery within CSS
fontBase64 = base64.b64encode(open('new.ttf').read())
# Delete the temporary file
os.remove('new.ttf')

# Time it took to create the web font
duration = end - start

# Output this text alongside the new throw-away web font
securetext = translateText('Putin is a wussy.')