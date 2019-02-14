import random
import os
import datetime
from _ast import Or, If
#from _datetime import datetime
from lib2to3.tests.data.infinite_recursion import int_least16_t

class DataConfig(object):
    def __init__(self, optimalData, trendFactor, leastValue, mostValue, periodReq):
        self.optimalData = optimalData
        self.trendFactor = trendFactor
        self.leastValue = leastValue
        self.mostValue= mostValue
        self.periodReq = periodReq
        
    def getOptimalData(self, nIndex):
        if len(self.optimalData) <= nIndex :
            return 0.0
        return float(self.optimalData[nIndex])
    
    def getTrendFactorData(self, nIndex):
        if len(self.trendFactor) <= nIndex:
            return "NIL"
        return self.trendFactor[nIndex]
    
    def getLeastValue(self, nIndex):
        if len(self.leastValue) <= nIndex:
            return 0
        return float(self.leastValue[nIndex])
    
    def getMostValue(self, nIndex):
        if len(self.mostValue) <= nIndex:
            return 0
        return float(self.mostValue[nIndex])
    
    def getPeriodData(self, nIndex):
        if len(self.periodReq) <= nIndex:
            return 0
        return int(self.periodReq[nIndex])

class BigDataCreator:
        
    def Create1(self):
        blockData = self.ReadBlockData('../InitialData/DataBlock.csv')
        blockMedian = self.ReadBlockMedian('../InitialData/BlockMedian.txt')
        
        fle = self.CreateOutputFile()
        
        header = 'Time,Machine name,Batch,LT left temp,LT right temp,LT dwell,LT UPH,RT left temp,RT right temp,RT dwell,RT UPH\n'
        self.WriteLine(fle, header)
        
        for median in blockMedian:
            self.CreateNextSetOfData1(fle, blockData, median)
                
    def CreateNextSetOfData1(self, fle, blockData, median):
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
    
    # - - - - - - - - - - - - - - - - - - - - - - - -
                
    def CreateNextSetOfData2(self, fle, optimalData, trendFactor, leastValue, mostValue, periodReq):
        nUpperMedian = 5
        nLowerMedian = -5
        ntrendVar = 0;
        haltProduction = False
        nextStepFreq = 0
        if trendFactor == "UP":
            nextStepFreq = int(periodReq / (mostValue - optimalData))
        elif trendFactor == "DN":
            nextStepFreq = int(periodReq / (optimalData - leastValue))
        
        for timePeriod in range(periodReq):
            if 0 == timePeriod % nextStepFreq:
                if trendFactor == "UP":
                    ntrendVar += 1;
                elif trendFactor == "DN":
                    ntrendVar -= 1;
            ltLeft  = optimalData + ntrendVar + random.randint(nLowerMedian,nUpperMedian)
            ltRight  = optimalData + ntrendVar + random.randint(nLowerMedian,nUpperMedian)
            rtLeft  = optimalData + ntrendVar + random.randint(nLowerMedian,nUpperMedian)
            rtRight = optimalData + ntrendVar + random.randint(nLowerMedian,nUpperMedian)
                    
            if timePeriod >= periodReq:
                if ( ltLeft < leastValue or ltRight < leastValue or \
                     rtLeft < leastValue or rtRight < leastValue or \
                     ltLeft > mostValue or ltRight > mostValue or \
                     rtLeft > mostValue or rtRight < mostValue ):
                    haltProduction = True
                else:
                    nSetIdxWrong = random.randint(0, 3)
                    if trendFactor == "UP":
                        if 0 == nSetIdxWrong:
                            ltLeft = mostValue + 5
                        elif 1 == nSetIdxWrong:
                            ltRight = mostValue + 5
                        elif 2 == nSetIdxWrong:
                            rtLeft = mostValue + 5
                        elif 3 == nSetIdxWrong:
                            rtRight = mostValue + 5
                    elif trendFactor == "DN":
                        if 0 == nSetIdxWrong:
                            ltLeft = leastValue - 5
                        elif 1 == nSetIdxWrong:
                            ltRight = leastValue - 5
                        elif 2 == nSetIdxWrong:
                            rtLeft = leastValue - 5
                        elif 3 == nSetIdxWrong:
                            rtRight = leastValue - 5

                    haltProduction = True
            else:        
                if ltLeft < leastValue:
                    ltLeft = leastValue + random.randint(nLowerMedian,nUpperMedian)
                if ltRight < leastValue:
                    ltRight = leastValue + random.randint(nLowerMedian,nUpperMedian)
                if rtLeft < leastValue:
                    rtLeft = leastValue + random.randint(nLowerMedian,nUpperMedian)
                if rtRight < leastValue:
                    rtRight = leastValue + random.randint(nLowerMedian,nUpperMedian)
                if ltLeft > mostValue:
                    ltLeft = mostValue - random.randint(nLowerMedian,nUpperMedian)
                if ltRight > mostValue:
                    ltRight = mostValue - random.randint(nLowerMedian,nUpperMedian)
                if rtLeft > mostValue:
                    rtLeft = mostValue - random.randint(nLowerMedian,nUpperMedian)
                if rtRight > mostValue:
                    rtRight = mostValue - random.randint(nLowerMedian,nUpperMedian)
                    
            #time = '09:57:59.714'
            self.startTimeValue += datetime.timedelta(seconds=30)
            time = self.startTimeValue
            line = '{0},{1},{2},{3},{4}\n'.format(time, ltLeft, ltRight, rtLeft, rtRight)
            self.WriteLine(fle, line)
            
            if haltProduction == True:
                break

    def CreateNextSetOfData(self, fle, optimalData, trendFactor, leastValue, mostValue, periodReq):
        nUpperMedian = 5
        nLowerMedian = -5
        ntrendVar = 0;
        haltProduction = False
        nextStepFreq = 0

        trendDataSet = line.split('\t')
        trendGenFactors = []
        for part in trendDataSet
            trendGenFactors.append(float(part))
        blockData.append(blockPart)


        if trendFactor == "UP":
            nextStepFreq = int(periodReq / (mostValue - optimalData))
        elif trendFactor == "DN":
            nextStepFreq = int(periodReq / (optimalData - leastValue))

        for timePeriod in range(periodReq):
            if 0 == timePeriod % nextStepFreq:
                if trendFactor == "UP":
                    ntrendVar += 1;
                elif trendFactor == "DN":
                    ntrendVar -= 1;
            ltLeft = optimalData + ntrendVar + random.randint(nLowerMedian, nUpperMedian)
            ltRight = optimalData + ntrendVar + random.randint(nLowerMedian, nUpperMedian)
            rtLeft = optimalData + ntrendVar + random.randint(nLowerMedian, nUpperMedian)
            rtRight = optimalData + ntrendVar + random.randint(nLowerMedian, nUpperMedian)

            if timePeriod >= periodReq:
                if (ltLeft < leastValue or ltRight < leastValue or \
                        rtLeft < leastValue or rtRight < leastValue or \
                        ltLeft > mostValue or ltRight > mostValue or \
                        rtLeft > mostValue or rtRight < mostValue):
                    haltProduction = True
                else:
                    nSetIdxWrong = random.randint(0, 3)
                    if trendFactor == "UP":
                        if 0 == nSetIdxWrong:
                            ltLeft = mostValue + 5
                        elif 1 == nSetIdxWrong:
                            ltRight = mostValue + 5
                        elif 2 == nSetIdxWrong:
                            rtLeft = mostValue + 5
                        elif 3 == nSetIdxWrong:
                            rtRight = mostValue + 5
                    elif trendFactor == "DN":
                        if 0 == nSetIdxWrong:
                            ltLeft = leastValue - 5
                        elif 1 == nSetIdxWrong:
                            ltRight = leastValue - 5
                        elif 2 == nSetIdxWrong:
                            rtLeft = leastValue - 5
                        elif 3 == nSetIdxWrong:
                            rtRight = leastValue - 5

                    haltProduction = True
            else:
                if ltLeft < leastValue:
                    ltLeft = leastValue + random.randint(nLowerMedian, nUpperMedian)
                if ltRight < leastValue:
                    ltRight = leastValue + random.randint(nLowerMedian, nUpperMedian)
                if rtLeft < leastValue:
                    rtLeft = leastValue + random.randint(nLowerMedian, nUpperMedian)
                if rtRight < leastValue:
                    rtRight = leastValue + random.randint(nLowerMedian, nUpperMedian)
                if ltLeft > mostValue:
                    ltLeft = mostValue - random.randint(nLowerMedian, nUpperMedian)
                if ltRight > mostValue:
                    ltRight = mostValue - random.randint(nLowerMedian, nUpperMedian)
                if rtLeft > mostValue:
                    rtLeft = mostValue - random.randint(nLowerMedian, nUpperMedian)
                if rtRight > mostValue:
                    rtRight = mostValue - random.randint(nLowerMedian, nUpperMedian)

            # time = '09:57:59.714'
            self.startTimeValue += datetime.timedelta(seconds=30)
            time = self.startTimeValue
            line = '{0},{1},{2},{3},{4}\n'.format(time, ltLeft, ltRight, rtLeft, rtRight)
            self.WriteLine(fle, line)

            if haltProduction == True:
                break

    def getFrequencyPerMonth(self):
        return 2 * 60 * 24 * 30 

    def ReadDataConfig(self, fileName):
        optimalData = []
        trendFactor = []
        leastValue  = []
        mostValue   = []
        periodReq   = []
        file = open(fileName, 'r')
        for line in file:
            parts = line.split(':')
            optimalData.append(parts[0])
            trendFactor.append(parts[1])
            leastValue.append(parts[2])
            mostValue.append(parts[3])
            periodReq.append(parts[4])
            #data.append(float(line))
        return DataConfig(optimalData, trendFactor, leastValue, mostValue, periodReq)
    
    def Create(self):
        
        dataCnfg = self.ReadDataConfig('../InitialData/DataConfig.txt')
        fle = self.CreateOutputFile()
        
        self.startTimeValue = datetime.datetime(2018, 1, 17, 21, 47, 13, 90244)
        
        nIdxData = 0
        optimumData = dataCnfg.getOptimalData(nIdxData)        
        while 0.0 < optimumData:
            trendFactor = dataCnfg.getTrendFactorData(nIdxData)
            periodReq = int(dataCnfg.getPeriodData(nIdxData)) *  self.getFrequencyPerMonth()
            leastVal = dataCnfg.getLeastValue(nIdxData)
            mostVal= dataCnfg.getMostValue(nIdxData)
            self.CreateNextSetOfData(fle, optimumData, trendFactor, leastVal, mostVal, periodReq)
            nIdxData += 1
            optimumData = float(dataCnfg.getOptimalData(nIdxData))

#starttimeValue = datetime.datetime(100,1,1,11,34,59) #datetime.datetime(2018, 1, 17, 21, 47, 13, 90244)
creator = BigDataCreator()
creator.Create()
