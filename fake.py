# ES-based training (requires numpy)
import random
import simulation
import play
import math
import copy
import numpy as np

POPULATION = 20       # number of simulations averaged when estimating reward (smaller for speed)
LEARN_RATE = 0.02     # ES step size (tweak)
ES_SAMPLES = 30       # number of perturbations sampled per generation
ES_SIGMA = 0.1        # perturbation stddev

class NeuralNetworkES:
    def __init__(self, size):
        self.size = size
        self.layersW = []
        self.layersB = []
        for i in range(len(size) - 1):
            layerW = [[random.uniform(-1, 1) for _ in range(size[i])] for _ in range(size[i + 1])]
            self.layersW.append(layerW)
            layerB = [random.uniform(-1, 1) for _ in range(size[i + 1])]
            self.layersB.append(layerB)

    # flatten/unflatten helpers
    def get_theta(self):
        parts = []
        shapes = []
        for l in range(len(self.layersW)):
            arr = np.array(self.layersW[l]).ravel()
            parts.append(arr)
            shapes.append(('W', l, np.array(self.layersW[l]).shape))
        for l in range(len(self.layersB)):
            arr = np.array(self.layersB[l]).ravel()
            parts.append(arr)
            shapes.append(('B', l, np.array(self.layersB[l]).shape))
        theta = np.concatenate(parts)
        return theta, shapes

    def set_theta(self, theta, shapes):
        idx = 0
        for s in shapes:
            kind, l, shape = s
            size = shape[0] * (shape[1] if len(shape) > 1 else 1)
            part = theta[idx: idx + size]
            idx += size
            part = part.reshape(shape)
            if kind == 'W':
                self.layersW[l] = part.tolist()
            else:
                self.layersB[l] = part.tolist()

    def evaluate_theta(self, theta, shapes, avg_runs=POPULATION):
        # apply theta, run avg_runs games, return average reward
        old_theta, _ = self.get_theta()
        self.set_theta(theta, shapes)
        total = 0.0
        for _ in range(avg_runs):
            total += simulation.main(self)   # or self.simulateGame()
        avg = total / avg_runs
        # restore old paramization
        self.set_theta(old_theta, shapes)
        return avg

    def learn_es(self, generations=200, samples=ES_SAMPLES, sigma=ES_SIGMA, lr=LEARN_RATE):
        theta, shapes = self.get_theta()
        dim = theta.size

        for gen in range(generations):
            epsilons = np.random.randn(samples, dim)
            rewards = np.zeros(samples)
            for k in range(samples):
                thetap = theta + sigma * epsilons[k]
                rewards[k] = self.evaluate_theta(thetap, shapes)
            # standardize rewards to reduce variance
            A = (rewards - np.mean(rewards))
            if np.std(A) > 0:
                A = A / np.std(A)
            # gradient estimate
            grad = np.dot(A, epsilons) / (samples * sigma)
            theta = theta + lr * grad
            self.set_theta(theta, shapes)

            # logging
            if gen % 5 == 0:
                baseline = self.evaluate_theta(theta, shapes, avg_runs=max(1, POPULATION//5))
                print(f"Gen {gen}, baseline reward ~ {baseline:.3f}")

    def run(self, inputs):
        layer = inputs
        for i in range(len(self.layersW)):
            layer = [self.calculateNode(layer, i, j) for j in range(len(self.layersW[i]))]
        idx = int(np.argmax(layer))
        return ["left", "right", "up", "down"][idx]

    def calculateNode(self, previousLayer, currentLayer, currentNode):
        s = 0.0
        for i in range(len(previousLayer)):
            s += previousLayer[i] * self.layersW[currentLayer][currentNode][i]
        s += self.layersB[currentLayer][currentNode]
        return math.tanh(s)

    def playGame(self):
        play.main(self)

if __name__ == "__main__":
    NN = NeuralNetworkES((4, 4, 4))
    NN.learn_es(generations=1000, samples=25, sigma=0.08, lr=0.03)
    NN.playGame()
