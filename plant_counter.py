import re

class Plant(object):

    def __init__(self, count, countType, tag, container):
        self.count = count
        self.countType = countType
        self.tag = tag
        self.container = container

    def __str__(self):
        return '{}, {}, {}:{}'.format(self.tag, self.container, self.countType, self.count)

class Plant_Counter():

    def __init__(self):
        print('init-ed')
        self.plantList = []

    def makePlantList(self, input):
        grandTotal = 0
        plants = []
        for line in input:
            parts = re.split('\s{2,}', line.strip())
            if len(parts) >= 3:
                count = parts[0].split()
                countType = 'quantity'
                if len(count) > 1:
                    countType = count[1]
                countNum = int(count[0].replace('(', ''))
                newPlant = Plant(countNum, countType, parts[1], parts[2])
                plants.append(newPlant)
        self.plantList = plants

    def getCountText(self):
        output = ''
        output += self.getGrandTotals(self.plantList)
        output += self.getTotalsByTag(self.plantList)
        output += self.getTotalsByContainer(self.plantList)
        return output

    def getGrandTotals(self, plants):
        totals = {}
        for plant in plants:
            if plant.countType in totals:
                currCount = totals[plant.countType]
                totals[plant.countType] = currCount + plant.count
            else:
                totals[plant.countType] = plant.count
        output = 'Grand Totals'
        for cType in totals.keys():
            output += f'\n\t{cType:8}\t{totals[cType]:8}'
        return output

    def getTotalsByTag(self, plants):
        totals = {}
        for plant in plants:
            if plant.countType not in totals:
                totals[plant.countType] = {}
            if plant.tag in totals[plant.countType]:
                currCount = totals[plant.countType][plant.tag]
                totals[plant.countType][plant.tag] = currCount + plant.count
            else:
                totals[plant.countType][plant.tag] = plant.count
        output = '\n\nTotals by type:\n---------------------------'
        for cType in totals.keys():
            tempKeys = list(totals[cType].keys())
            tempKeys.sort()
            for key in tempKeys:
                output += f'\n\t{key:10}\t{cType:15}\t{totals[cType][key]:10}'
        return output

    def getTotalsByContainer(self, plants):
        totals = {}
        for plant in plants:
            if plant.countType not in totals:
                totals[plant.countType] = {}
            if plant.container in totals[plant.countType]:
                currCount = totals[plant.countType][plant.container]
                totals[plant.countType][plant.container] = currCount + plant.count
            else:
                totals[plant.countType][plant.container] = plant.count
        output = '\n\nTotals by container:\n---------------------------'
        for cType in totals.keys():
            tempKeys = list(totals[cType].keys())
            tempKeys.sort()
            for key in tempKeys:
                output += f'\n\t{key:20}\t{cType:15}\t{totals[cType][key]:10}'
        return output