import random
import simulation
import play
import math
import pandas as pd
import os

POPULATION = 1000
LEARN_RATE = 0.0005

save_csv_path = "save.csv"

class NeuralNetwork:
    def __init__(self, size, weights=None, biases=None):
        self.size = size

        if weights is None:
            layersW = []
            rewardsW = []
            for i in range(len(size) - 1):
                layerW = []
                rewardW = []
                for t in range(size[i + 1]):
                    subLayerW = []
                    subRewardW = []
                    for w in range(size[i]):
                        weight = random.uniform(0, 1)
                        subLayerW.append(weight)
                        subRewardW.append(0)
                    layerW.append(subLayerW)
                    rewardW.append(subRewardW)
                layersW.append(layerW)
                rewardsW.append(rewardW)
        else:
            layersW = weights
            rewardsW = [[[0 for _ in range(size[i])] for _ in range(size[i+1])] 
                        for i in range(len(size)-1)]

        
        if biases is None:
            layersB = []
            rewardsB = []
            for i in range(len(size) - 1):
                layerB = []
                rewardB = []
                for t in range(size[i + 1]):
                    bias = random.uniform(0,1)
                    layerB.append(bias)
                    rewardB.append(0)
                layersB.append(layerB)
                rewardsB.append(rewardB)
        else:
            layersB = biases
            rewardsB = [[0 for _ in range(size[i+1])] for i in range(len(size)-1)]
        
        self.layersW = layersW
        self.layersB = layersB
        self.rewardW = rewardsW
        self.rewardB = rewardsB
    
    def run(self, inputs):
        layer = inputs
        for i in range(len(self.layersW)):
            layer = self.calculateLayer(layer, i)
        index = layer.index(max(layer))
        if(index == 0):
            return "left"
        elif(index == 1):
            return "right"
        elif(index == 2):
            return "up"
        elif(index == 3):
            return "down"

    def calculateLayer(self, previousLayer, currentLayer):
        newLayer = []
        for i in range(len(self.layersW[currentLayer])):
            newLayer.append(self.calculateNode(previousLayer, currentLayer, i))
        return newLayer

    
    def calculateNode(self, previousLayer, currentLayer, currentNode):
        newNode = 0
        for i in range(len(previousLayer)):
            newNode += previousLayer[i] * self.layersW[currentLayer][currentNode][i]
        newNode += self.layersB[currentLayer][currentNode]
        newNode = activationFunctionHT(newNode)
        return newNode

    def simulateGame(self):
        score = simulation.main(self)
        return score
    
    def playGame(self):
        play.main(self)

    def train(self):
        pass
    
    def learn(self):
        rand = random.randint(1,2)
        if(rand == 1):
            h = random.uniform(-0.2, 0.2)
        else:
            h = random.uniform(-0.05,0.05)
        originalReward = self.Reward()
        for i in range(len(self.size) - 1):
            for t in range(self.size[i + 1]):
                for w in range(self.size[i]):
                    self.layersW[i][t][w] += h
                    deltaReward = self.Reward() - originalReward
                    self.layersW[i][t][w] -= h
                    self.rewardW[i][t][w] = deltaReward / h
        for i in range(len(self.size) - 1):
            for t in range(self.size[i + 1]):
                self.layersB[i][t] += h
                deltaReward = self.Reward() - originalReward
                self.layersB[i][t] -= h
                if(deltaReward >= 0):
                    self.rewardB[i][t] = deltaReward / h
                else:
                    self.rewardB[i][t] = 0
        self.ApplyReward()

    def Reward(self):
        reward = 0
        for i in range(POPULATION):
            reward += self.simulateGame()
        reward = reward / POPULATION
        return reward

    def ApplyReward(self):
        for i in range(len(self.size) - 1):
            for t in range(self.size[i + 1]):
                for w in range(self.size[i]):
                    self.layersW[i][t][w] += self.rewardW[i][t][w] * LEARN_RATE
        for i in range(len(self.size) - 1):
            for t in range(self.size[i + 1]):
                self.layersB[i][t] += self.rewardB[i][t] * LEARN_RATE

    def train(self):
        generations = 1000
        for i in range(generations):
            self.learn()
            print(f"weights: {self.layersW}")
            print(f"biases: {self.layersB}")
            print(i)
            if(i % 5 == 0):
                self.playGame()
                self.findAverage()
    
    def findAverage(self):
        global bestNetwork
        average = 0
        for i in range(10):
            average += self.Reward()
        average = average/10
        print(f"Average: {average}")
        if(average >= bestNetwork[0]):
            bestNetwork[0] = average
            bestNetwork[1] = self.copy()
            bestNetwork[1].save()
        elif(average <= bestNetwork[0] - 0.1):
            self = bestNetwork[1].copy()
    
    def save(self):
        network = bestNetwork[1].copyData()
        data = {
            "average": bestNetwork[0],
            "network": network
        }
        df = pd.DataFrame([data])
        df.to_csv(
            save_csv_path,
            mode="a",
            header=not os.path.exists(save_csv_path),
            index=False
        )
        print("saved")

    def copy(self):
        # Deep copy weights and biases
        new_weights = [
            [list(node) for node in layer]  # copy each neuron's weight list
            for layer in self.layersW
        ]
        new_biases = [
            list(layer) for layer in self.layersB
        ]
        
        # Create a new NeuralNetwork with same size and copied params
        return NeuralNetwork(self.size, weights=new_weights, biases=new_biases)

    def copyData(self):
        new_weights = [
            [list(node) for node in layer]
            for layer in self.layersW
        ]
        new_biases = [
            list(layer) for layer in self.layersB
        ]
        return [new_weights, new_biases]



def activationFunctionHT(weight):
    return math.tanh(weight)

bestNetwork = [0, NeuralNetwork((4,4,4,4))]
if __name__ == "__main__":
    NN = NeuralNetwork((4,4,4,4))
    average = 0
    for i in range(10):
        average += NN.Reward()
    average = average/10
    print(f"Average: {average}")
    print(NN.layersB)
    print(NN.layersW)
    NN.train()
    NN.playGame()