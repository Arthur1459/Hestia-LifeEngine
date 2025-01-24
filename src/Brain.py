import config as cf
import vars as vr
import utils as u
import tools as t
from tools import sigmoid
import numpy as np

class NeuralNetwork:
    def __init__(self, nb_inputs, nb_out, nb_neurons_by_layer=()):
        self.id = u.getNewId()

        self.nb_inputs = nb_inputs
        self.nb_outputs = nb_out

        self.layers = []
        for nb_neurons in nb_neurons_by_layer:
            self.layers.append(Layer(nb_neurons,  self.nb_inputs if len(self.layers) == 0 else self.layers[-1].size_out()))
        self.layers.append(Layer(self.nb_outputs, self.nb_inputs if len(self.layers) == 0 else self.layers[-1].size_out()))

    def predict(self, inputs):
        if len(inputs) != self.nb_inputs:
            raise ValueError("Wrong inputs ! (size issue)")

        row_information = np.array(inputs)
        information = row_information / t.norm(row_information)
        for layer in self.layers:
            information = layer.apply(information)

        if len(information) != self.nb_outputs:
            raise ValueError("Wrong output layer ! (size issue)")

        return information

    def Mutate(self, spread=0.1):
        for layer in self.layers: layer.Mutate(spread=spread)

class Layer:
    def __init__(self, nb_neurons, nb_inputs):
        self.id = u.getNewId()

        self.nb_neurons = nb_neurons
        self.neurons = [Neuron(nb_inputs) for i in range(nb_neurons)]

    def apply(self, inputs):
        return np.array([neuron.activate(inputs) for neuron in self.neurons])
    def size_out(self):
        return len(self.neurons)
    def Mutate(self, spread):
        for neuron in self.neurons: neuron.Mutate(spread=spread)

class Neuron:
    def __init__(self, nb_inputs, func=sigmoid):
        self.id = u.getNewId()

        self.function = func
        self.weights = np.array([t.random() - 0.5 for _ in range(nb_inputs)])

    def activate(self, information):
        if len(information) != len(self.weights):
            raise ValueError(f"informations != nb weights : {len(information) != {len(self.weights)}}")
        return sum(self.weights * information)

    def Mutate(self, spread):
        self.weights = t.normal(self.weights, spread, len(self.weights))

def PrintNeuralNetwork(network: NeuralNetwork):
    print("Network Print : ")
    print(f" inputs : {network.nb_inputs}", end="")
    for i in range(len(network.layers)):
        print(f" -> layer[{i}] : {network.layers[i].size_out()}", end="")
    print(" = output ")

def test():
    input = [1, 4, 2, 7, 2]
    network = NeuralNetwork(5, 4, (4,))
    PrintNeuralNetwork(network)
    print(network.predict(input))
    network.Mutate()
    print(network.predict(input))

test()
