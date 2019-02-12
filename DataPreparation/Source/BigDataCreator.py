import random
import os
from _ast import Try

class BigDataCreator:
        
    def Create(self):
        blockData = self.ReadBlockData('../InitialData/DataBlock.csv')
        blockMedian = self.ReadBlockMedian('../InitialData/BlockMedian.txt')
        fle = self.CreateOutputFile()
        
        header = 'Time,Machine name,Batch,LT left temp,LT right temp,LT dwell,LT UPH,RT left temp,RT right temp,RT dwell,RT UPH\n'
        self.WriteLine(fle, header)
        
        for median in blockMedian:
            self.CreateNextSetOfData(fle, blockData, median)
                
    def CreateNextSetOfData(self, fle, blockData, median):
        nUpperMedian = 5
        nLowerMedian = -5
        for blockPart in blockData:
            ltLeft = blockPart[0] + median + random.randint(nLowerMedian,nUpperMedian)
            ltRigh = blockPart[1] + median + random.randint(nLowerMedian,nUpperMedian)
            rtLeft = blockPart[2] + median + random.randint(nLowerMedian,nUpperMedian)
            rtRigh = blockPart[3] + median + random.randint(nLowerMedian,nUpperMedian)
            time = '09:57:59.714'
            line = '{0},T7X0,N/A,{1},{2},N/A,N/A,{3},{4},200,N/A\n'.format(time, ltLeft, ltRigh, rtLeft, rtRigh)
            self.WriteLine(fle, line)

    def CreateOutputFile(self):
        flePath = "../FinalData/DataToTeach.csv"
        self.CreateOutputDirectory(flePath)
        return open(flePath, "w+") 
    
    def CreateOutputDirectory(self, flePath):
        directory = os.path.dirname(flePath)
        if not os.path.exists(directory):
            os.mkdir(directory)
        
    def WriteLine(self, fle, line):
        #print (line)
        fle.write(line)

    def ReadBlockData(self, fileName):
        blockData = []
        file = open(fileName, 'r')
        for line in file:
            parts = line.split('\t')
            blockPart = []
            for part in parts:
                blockPart.append(float(part))
            blockData.append(blockPart)
        return blockData

    def ReadBlockMedian(self, fileName):
        data = []
        file = open(fileName, 'r')
        for line in file:
            data.append(float(line))
        return data

creator = BigDataCreator()
creator.Create()
