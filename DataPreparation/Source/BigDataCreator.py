
class BigDataCreator:

    def Create(self):
        blockData = self.ReadBlockData('../InitialData/DataBlock.csv')
        blockMedian = self.ReadBlockMedian('../InitialData/BlockMedian.txt')

        header = 'Time,Machine name,Batch,LT left temp,LT right temp,LT dwell,LT UPH,RT left temp,RT right temp,RT dwell,RT UPH'
        self.WriteLine(header)

        for median in blockMedian:
            for blockPart in blockData:
                ltLeft = blockPart[0] + median
                ltRigh = blockPart[1] + median
                rtLeft = blockPart[2] + median
                rtRigh = blockPart[3] + median
                time = '09:57:59.714'
                line = '{0},T7X0,N/A,{1},{2},N/A,N/A,{3},{4},200,N/A'.format(time, ltLeft, ltRigh, rtLeft, rtRigh)
                self.WriteLine(line)

    def WriteLine(self, line):
        print (line)

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
