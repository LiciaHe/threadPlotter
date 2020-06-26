'''
Converting an image into a fixed grid layout
'''
import PIL
from scipy.spatial import Delaunay
import numpy as np
from threadPlotter.PunchNeedle import threadColorManagement as TCM
class GridImgConverter:
    def getIntensities(self,pixelization_length, pixels, i, j):
        total_red_intensity = total_green_intensity = total_blue_intensity = 0
        averaging_pixel_number = pixelization_length * pixelization_length
        #
        for k in range(0, pixelization_length):
            for l in range(0, pixelization_length):
                # print(pixels[i * pixelization_length + k, j * pixelization_length + l])
                total_red_intensity += pixels[i * pixelization_length + k, j * pixelization_length + l][0]
                total_green_intensity += pixels[i * pixelization_length + k, j * pixelization_length + l][1]
                total_blue_intensity += pixels[i * pixelization_length + k, j * pixelization_length + l][2]
        #
        average_red_intensity = int(total_red_intensity / averaging_pixel_number)
        average_green_intensity = int(total_green_intensity / averaging_pixel_number)
        average_blue_intensity = int(total_blue_intensity / averaging_pixel_number)
        return average_red_intensity, average_green_intensity, average_blue_intensity
    def getIntensities_noAvg(self,pixelization_length, pixels, i, j):
        total_red_intensity = total_green_intensity = total_blue_intensity = 0
        averaging_pixel_number = pixelization_length * pixelization_length
        #
        for k in range(0, pixelization_length):
            for l in range(0, pixelization_length):
                # print(pixels[i * pixelization_length + k, j * pixelization_length + l])
                total_red_intensity += pixels[i * pixelization_length + k, j * pixelization_length + l][0]
                total_green_intensity += pixels[i * pixelization_length + k, j * pixelization_length + l][1]
                total_blue_intensity += pixels[i * pixelization_length + k, j * pixelization_length + l][2]
        #
        average_red_intensity = int(total_red_intensity / averaging_pixel_number)
        average_green_intensity = int(total_green_intensity / averaging_pixel_number)
        average_blue_intensity = int(total_blue_intensity / averaging_pixel_number)
        return pixels[i * pixelization_length , j * pixelization_length ][0],pixels[i * pixelization_length , j * pixelization_length ][1],pixels[i * pixelization_length , j * pixelization_length ][2]

    def halftone(self,x_units,y_units,pixelization_length,pixels):
        dotLocations = []
        dotColors = []

        for i in range(0, x_units):
            col=[]
            self.gridImg.append(col)
            for j in range(0, y_units):
                average_red_intensity, average_green_intensity, average_blue_intensity = self.getIntensities(
                    pixelization_length, pixels, i, j)
                x0 = i * pixelization_length
                y0 = j * pixelization_length
                x1 = i * pixelization_length + pixelization_length - 1
                y1 = j * pixelization_length + pixelization_length - 1
                cx = (x0 + x1) / 2.0
                cy = (y0 + y1) / 2.0
                dotLocations.append((cx, cy))
                dotColors.append((average_red_intensity, average_green_intensity, average_blue_intensity))
                col.append(((cx,cy),(average_red_intensity, average_green_intensity, average_blue_intensity)))
        return dotLocations,dotColors

    def halftone_noAvg(self, x_units, y_units, pixelization_length, pixels):
        dotLocations = []
        dotColors = []

        for i in range(0, x_units):
            col = []
            self.gridImg.append(col)
            for j in range(0, y_units):
                r,g,b= self.getIntensities_noAvg(
                    pixelization_length, pixels, i, j)
                x0 = i * pixelization_length
                y0 = j * pixelization_length
                x1 = i * pixelization_length + pixelization_length - 1
                y1 = j * pixelization_length + pixelization_length - 1
                cx = (x0 + x1) / 2.0
                cy = (y0 + y1) / 2.0
                dotLocations.append((cx, cy))

                dotColors.append((r,g,b))
                col.append(((cx,cy),(r,g,b)))

        return dotLocations, dotColors
    def __init__(self,imgLoc,imgName,colorCount=5,imgSize=(960,960), pixelization_length =4,grayScale=False,removeSmallCollections=True,quantize=True,idealColors=-1):
        '''
        convert
        :param saveLoc:
        :param imgName:
        :param imgSize:
        :param gridSize:
        '''
        img = PIL.Image.open(imgLoc + imgName)
        img=img.resize([int(xy) for xy in imgSize])
        img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        if quantize:
            img= img.quantize(colorCount)
        self.quantize=quantize
        if grayScale:
            img=img.convert('LA')
        img=img.convert('RGB')
        self.img=img
        # img = img.convert('P', palette=Image.ADAPTIVE, colors=colorCount)
        self.gridImg = []
        pixels = img.load()
        x_units = int(img.size[0] / pixelization_length)
        y_units = int(img.size[1] / pixelization_length)
        self.pixelization_length=pixelization_length
        dotLocations, dotColors=self.halftone_noAvg(x_units,y_units,pixelization_length,pixels)
        self.x_units=x_units
        self.y_units=y_units
        self.pathCollection={}

        if not self.quantize:
            #replacing close colors
            lim=80
            dotColors,colors=self.replaceColors(lim,dotColors)
            while idealColors>0 and len(colors)>idealColors:
                lim+=20
                dotColors, colors = self.replaceColors(lim, dotColors)


        for i,c in enumerate(dotColors):
            rgb="rgb("+",".join([str(int(xy)) for xy in c])+")"

            dots=[pt for j,pt in enumerate(dotLocations) if dotColors[j]==c]
            # dots.sort(key=lambda x:(x[1],x[0]))
            self.pathCollection[rgb]=dots
        if removeSmallCollections:
            keys=list(self.pathCollection.keys())
            for c in keys:
                if len(self.pathCollection[c])<30:
                    del self.pathCollection[c]
        print("finished calculation",colorCount,self.pathCollection.keys())
    def saveImg(self,loc):
        self.img.save(loc  + "convertedImg.png")
    def replaceColors(self,lim,dotColors):
        colorCollection = set(dotColors)
        colors = []
        for color in colorCollection:
            rgb = TCM.rgbToString(color)
            colors.sort(key=lambda c: TCM.calculateColorDifference(color, c))
            if len(colors) > 0 and TCM.calculateColorDifference(color, colors[0]) < lim:
                closeColor = colors[0]
                # replaceColors[rgb] = closeColor
                # replacing
                for i, c in enumerate(dotColors):
                    if c == color:
                        dotColors[i] = closeColor
                for col in self.gridImg:
                    for j, (pt, c) in enumerate(col):
                        if c == color:
                            col[j] = (pt, closeColor)
            else:
                colors.append(color)
        return dotColors,colors
    def exportOrderedGrid(self):
        centerByColorAndRow={}
        for color in self.pathCollection:
            centers=self.pathCollection[color]
            maxY=max([pt[1] for pt in centers])
            centerByColorAndRow[color] = [[] for i in range(int(maxY/self.pixelization_length)+1)]
            # print(lastPtY,)
            #assign to list
            for pt in centers:
                idx=int(pt[1]/self.pixelization_length)
                centerByColorAndRow[color][idx].append(pt)
            #sort
            for i,lst in enumerate(centerByColorAndRow[color]):
                reverseLst=i%2==1
                lst.sort(key=lambda pt:pt[0],reverse=reverseLst)
        print("finished sorting")
        return centerByColorAndRow

    def exportOrderedGridListVersion(self):
        '''
        reconstruct ordered grid
        :return:
        '''
        exportGrid=[]
        for i, col in enumerate(self.gridImg):
            rowCopy=[]
            for j,ptRgb in enumerate(col):
                rowCopy.append(ptRgb)
            if i%2==0:
                rowCopy=rowCopy[::-1]
            exportGrid.append(rowCopy)
        return exportGrid

    def exportDelaunayPath(self):
        pathsByColor={}
        for color in self.pathCollection:
            points=np.array(self.pathCollection[color])

            tri = Delaunay(points)
            triPts = points[tri.simplices]
            orderedPts = []
            traveled = set()
            for i, triangle in enumerate(triPts):
                waitlist = []
                for j in range(3):
                    ptStr = ",".join([str(xy) for xy in triangle[j]])
                    if i != len(triPts) - 1 and triangle[j] in triPts[i + 1]:
                        waitlist.append(triangle[j])
                    elif ptStr not in traveled:
                        orderedPts.append(list(triangle[j]))
                        traveled.add(ptStr)
                for pt in waitlist:
                    ptStr = ",".join([str(xy) for xy in pt])
                    if ptStr not in traveled:
                        orderedPts.append(list(pt))
                        traveled.add(ptStr)
            pathsByColor[color]=orderedPts
        return pathsByColor















