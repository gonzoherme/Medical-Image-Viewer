import math, copy
from cmu_112_graphics import *


#################################################
# Helper functions
#################################################
def rgbString(red, green, blue):
     return f'#{red:02x}{green:02x}{blue:02x}'

#################################################
# Helper functions for lists
#################################################

def print2dList(data):
    # Simple print of 2D list data
    # New line for each row, spaces between columns
    size1, size0 = len(data), len(data[0])
    for i in range(size1):
        for j in range(size0):
            value = data[i][j]
            print(value, end=' ')
        # New line after row
        print()

def print3dList(data):
    # Simple print of 2D list data
    # New line for each row, spaces between columns
    # Extra new line between slices
    size2, size1, size0 = len(data), len(data[0]), len(data[0][0])
    for i in range(size2):
        for j in range(size1):
            for k in range(size0):
                value = data[i][j][k]
                print(value, end=' ')
            # New line after row
            print()
        # Extra new line
        print()

def list1DTo3D(list1D, size0, size1, size2):
    # Create a 3D list with size0 rows, size1 columns, and size2 slices and
    # fill sequentially with values from list1D
    
    n = len(list1D)
    if n != size0*size1*size2:
        dimStr = f"({size0}, {size1}, {size2})"
        print(f"Length of list ({n}) doesn't match 3D dimensions {dimStr}.")
        return None
    
    list3D = []
    index1D = 0
    for i in range(size2):
        slice = []
        for j in range(size1):
            row = []
            for k in range(size0):
                value = list1D[index1D]
                index1D += 1
                row.append(value)
            slice.append(row)
        list3D.append(slice)

    return list3D

def createDecimalImage(size0, size1):
    # Create a 2D list with size0 rows and size1 columns and
    # fill with rowIndex + colIndex*10
    im = []
    for i in range(size1):
        row = []
        for j in range(size0):
            val = j + i*10
            row.append(val)
        im.append(row)

    return im

def createDecimalVolume(size0, size1, size2):
    # Create a 3D list with size0 rows, size1 columns, and size2 slices and
    # fill with rowIndex + colIndex*10 + sliceIndex*100
    vol = []
    for i in range(size2):
        slice = []
        for j in range(size1):
            row = []
            for k in range(size0):
                val = k + j*10 + i*100
                row.append(val)
            slice.append(row)
        vol.append(slice)

    return vol

def flattenImage(imList2D):
    # Converts 2D list image to 1D list
    imList1D = []
    for row in imList2D:
        imList1D += row
    return imList1D

def loadMedicalImageVolume():
    filename = "head_ct_50_50_50.csv"
    rowsPerImage = 50

    vol = []
    with open(filename) as f:
        lineIndex = 0
        for line in f.readlines():
            if lineIndex % rowsPerImage == 0:
                slice = []

            # Split by commas and convert strings to int
            row = []
            for val in line.split(','):
                row.append(int(val))
            slice.append(row)

            if lineIndex % rowsPerImage == 0:
                vol.append(slice)

            lineIndex += 1
            
    return vol

#################################################
# Main Functions
#################################################



def getXtranslation(row, dx, backgroundValue):
    if dx > 0:
        for _ in range(dx):
            x = row.pop()
            row = [x] + row

        # replace for backgroundValue
        for index in range(len(row)):
            if index < dx:
                row[index] = backgroundValue

    elif dx < 0:
        for _ in range(-dx):
            x = row.pop(0)
            row.append(x)

        # replace background Value
        for index in range(len(row)):
            if index >= -dx:
                row[index] = backgroundValue
    
    return row



def panImage(im, dx, dy, backgroundValue):
    IM = copy.deepcopy(im)
    # edge case
    if dx == 0 and dy == 0:
        return IM
    
    # case of dx or dy larger than all values
    if (abs(dx) >= len(IM[0])) or (abs(dy) >= len(IM)):
        for row in range(len(IM)):
            for col in  range(len(IM[0])):
                IM[row][col] = backgroundValue

        return IM

    # We do DX first
    for rowIndex in range(len(IM)):
        newRow = getXtranslation(IM[rowIndex], dx, backgroundValue)
        IM[rowIndex] = newRow

    # Now we do DY
    if dy > 0:
        originalIm = copy.deepcopy(IM)
        for rowIndex in range(len(IM)):
            for colIndex in  range(len(IM[0])):
                # if column passed
                if rowIndex - abs(dy) < 0:
                    IM[rowIndex][colIndex] = backgroundValue

                # else
                else:
                    y = originalIm[rowIndex-abs(dy)][colIndex]
                    IM[rowIndex][colIndex] = y

    elif dy < 0:
        for rowIndex in range(len(IM)):
            for colIndex in  range(len(IM[0])):
                # if column passed
                if rowIndex + abs(dy) > len(IM)-1:
                    IM[rowIndex][colIndex] = backgroundValue

                # else
                else:
                   IM[rowIndex][colIndex] = IM[rowIndex+abs(dy)][colIndex]
            
            
    return IM




def volSlicer(vol, sliceIndex, sliceAxis):
    VOL = copy.deepcopy(vol)
    retrieved = []
    sliceColumn = []
    # Case 1: slice 1
    if sliceAxis == 0:
    # Loop through every slice, every row, every column
        for eachSlice in range(len(vol)):
            for rowIndex in range(len(vol[0])):
                for colIndex in range(len(vol[0][0])):

                    if colIndex == sliceIndex:
                        sliceColumn.append(vol[eachSlice][rowIndex][colIndex])

                    if len(sliceColumn) == len(vol[0]):
                        retrieved.append(sliceColumn)
                        sliceColumn = []



    # Case 2: slice 2
    elif sliceAxis == 1:
        for slices in vol:
            retrieved.append(slices[sliceIndex])

    # Case 3: slice 3
    elif sliceAxis == 2:
        retrieved.extend(vol[sliceIndex])

    return retrieved



def maximumIntensityProjection(vol, maxAxis):
    retrieved = []
    bestRow= []
    # Case 1:
    if maxAxis == 0:
        for slices in vol:
            for row in slices:                    
                bestRow.append(max(row))
                
            retrieved.append(bestRow)
            bestRow = []
        return retrieved
        

    # Case 2: slice 2
    elif maxAxis == 1:
        bestRow = []
        for sliceIndex in range(len(vol)):

            # we create a grid to edit later
            bestRow.append([0]*len(vol[0][0]))

            for rowIndex in range(len(vol[0])):
                for colIndex in range(len(vol[0][0])):                    
                    if (vol[sliceIndex][rowIndex][colIndex] >
                        bestRow[sliceIndex][colIndex]):
                        y = vol[sliceIndex][rowIndex][colIndex]
                        bestRow[sliceIndex][colIndex] = y
        return bestRow

    
    # Case 3: slice 3
    elif maxAxis == 2:
        # create a grid to edit later
        grid = []
        for _ in vol[0]:
            grid.append([0]*len(vol[0][0]))

        for sliceIndex in range(len(vol)):
            for rowIndex in range(len(vol[0])):
                for colIndex in range(len(vol[0][0])):
                    if (vol[sliceIndex][rowIndex][colIndex]
                        > grid[rowIndex][colIndex]):
                        y = vol[sliceIndex][rowIndex][colIndex]
                        grid[rowIndex][colIndex] = y
        return grid








    

#################################################
# 3D Medical Image Viewer
#################################################

def appStarted(app):
    # Load the medical image volume as a 3D list
    # This app.vol should never change
    app.vol = loadMedicalImageVolume()

    # DO NOT CHANGE these app settings
    app.imageDisplayWidth = 400
    app.imageDisplayHeight = 400

    # TODO: Add any other app startup code you need here
    app.sliceAxis = 2
    app.sliceIndex = len(app.vol)//2
    app.dx = 0
    app.dy = 0
    app.isMIP = False


    # Keep this here to initialize your first image
    # updateImage will also be called everytime you chnge app settings that 
    # affect your image
    updateImage(app)

def updateImage(app):
    # Call volSlicer, maximumIntensityProjection, and panImage as necessary to
    # converty the app.vol into a 2D list image named im.
    # Store your resulting image as im (which is then passed to imageToTk
    # at the bottom of this funciton).

    # TODO: YOUR CODE HERE
    # You'll want to change the line below (and add others)
    im = app.vol[len(app.vol)//2]

    #3D list
    #3D to 2D
    if app.isMIP:
        im = maximumIntensityProjection(app.vol, app.sliceAxis)
    else:
        app.sliceIndex = app.sliceIndex % len(app.vol)
        im = volSlicer(app.vol, app.sliceIndex, app.sliceAxis)
        
        
    im = panImage(im, app.dx, app.dy, 99)
    # Convert your 2D list im to an image that can be display by Tkinter
    # IMPORTANT: Keep this line at the bottom of updateImage
    #and don't change it
    app.imTk = imageToTk(im, app.imageDisplayWidth, app.imageDisplayHeight)

def imageToTk(im, displayWidth, displayHeight):
    # DO NOT CHANGE this function
    # You don't need to understand this function
    # In short, in converts your 2D image list into an image that can be
    # displayed directly with Tkinter
    imHeight, imWidth = len(im), len(im[0])
    imPIL = Image.new('L', (imWidth, imHeight))
    imPIL.putdata(flattenImage(im))
    imPIL = imPIL.resize((displayWidth, displayHeight), Image.NEAREST)
    return ImageTk.PhotoImage(imPIL)

# Add 112 graphics controller functions here
# IMPORTANT: Be sure to call updateImage anytime you change anything in app
# that affects your image
# We started you with a blank keyPressed function.
# You can add other controller methods here as well if you'd like

def keyPressed(app, event):
    # Change app settings based on key press events
    # TODO: YOUR CODE HERE
    if event.key == 's':
        app.sliceIndex += 1
    elif event.key == 'd':
        app.sliceIndex -= 1

    elif event.key == 'a':
        app.sliceAxis = (app.sliceAxis + 1) % 3
    elif event.key == 'm':
        app.isMIP = not app.isMIP # false->true; true->false

    # DIRECTION KEYS
    # elif event.key == 'Up':
    #     app.dy -= 1
    # elif event.key == 'Down':
    #     app.dy += 1
    # elif event.key == 'Left':
    #     app.dx -= 1
    # elif event.key == 'Right':
    #     app.dx += 1

    # Make sure to call this anytime you change anything in app that affects
    # your image
    updateImage(app)

def drawInstructions(app, canvas, x0, y0, x1, y1):
    canvas.create_rectangle(x0, y0, x1, y1, fill='lightblue', outline='')
    # Add your code to display instuctions text
    # (feel free to modify/delete the rectangle line above)
    # TODO: YOUR CODE HERE

    textX = x0 + 30
    lineHeight = (y1 - y0)//15

    textY = lineHeight * 2
    canvas.create_text(textX, textY,
                       text = "INSTRUCTIONS", anchor = 'nw', font = 'Cambria 20 bold underline')    
    
    textY += 1.5*lineHeight
    canvas.create_text(textX, textY,
                       text = "A: cycle through slice axis", anchor = 'nw', font = 'Cambria 15 bold')    

    textY += lineHeight
    canvas.create_text(textX, textY,
                       text = "S: increase slice index", anchor = 'nw', font = 'Cambria 15 bold')

    textY += lineHeight
    canvas.create_text(textX, textY,
                       text = "D: decrease slice index", anchor = 'nw', font = 'Cambria 15 bold')

    textY += lineHeight
    canvas.create_text(textX, textY,
                       text = "M: toggle between MIP and slice view", anchor = 'nw', font = 'Cambria 15 bold')

    # DIRECTION INSTRUCTIONS
    # textY += lineHeight
    # canvas.create_text(textX, textY,
    #                    text = "Arrow keys: pan left, right, up, down", anchor = 'nw',font = 'Cambria 15 bold')
    
    
    
    

def redrawAll(app, canvas):
    # DO NOT CHANGE anything in this function

    drawInstructions(app, canvas, 400, 0, 800, 400)
    
    if app.imTk is not None:
        canvas.create_image(0, 0, image=app.imTk, anchor='nw')

def startViewer():
    # DO NOT CHANGE anything in this function
    runApp(width=800, height=400)



    
def main():
    startViewer()

if __name__ == '__main__':
    main()

    
main()
