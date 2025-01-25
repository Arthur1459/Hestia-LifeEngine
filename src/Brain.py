import config as cf
import vars as vr
import utils as u
import tools as t
from tools import sigmoid
import numpy as np

class NeuralNetwork:
    def __init__(self, nb_inputs=1, nb_out=1, nb_neurons_by_layer=(), copy_from=None):
        self.id = u.getNewId()

        if copy_from is None:
            self.nb_inputs = nb_inputs
            self.nb_outputs = nb_out

            self.layers = []
            for nb_neurons in nb_neurons_by_layer:
                self.layers.append(Layer(nb_neurons,  self.nb_inputs if len(self.layers) == 0 else self.layers[-1].size_out()))
            self.layers.append(Layer(self.nb_outputs, self.nb_inputs if len(self.layers) == 0 else self.layers[-1].size_out()))
        else:
            self.nb_inputs = copy_from.nb_inputs
            self.nb_outputs = copy_from.nb_outputs
            self.layers = [layer.getCopy() for layer in copy_from.layers]

    def predict(self, inputs):
        if len(inputs) != self.nb_inputs:
            raise ValueError("Wrong inputs ! (size issue)")

        row_information = np.array(inputs)
        information = row_information * t.inv(t.norm(row_information))
        for layer in self.layers:
            information = layer.apply(information)

        if len(information) != self.nb_outputs:
            raise ValueError("Wrong output layer ! (size issue)")

        return information

    def Mutate(self, spread=0.1):
        for layer in self.layers: layer.Mutate(spread=spread)

    def NewInput(self):
        self.nb_inputs += 1
        self.layers[0].NewInput()
    def NewNeuron(self, at_layer=0, amount=1):
        if at_layer == -1:
            at_layer = len(self.layers) - 1
        for _ in range(amount):
            self.layers[at_layer].NewNeuron()
            if at_layer == len(self.layers) - 1:
                self.nb_outputs += 1
            else:
                self.layers[at_layer + 1].NewInput()
    def NewLayer(self, nb_neurons=1, layer_at=None):
        if layer_at is None : layer_at = len(self.layers) - 1 # New Layer in last just Before the out-layer)
        nb_inputs = self.layers[layer_at - 1].size_out() if layer_at - 1 >= 0 else self.nb_inputs
        self.layers.insert(layer_at, Layer(nb_neurons, nb_inputs))
        self.layers[layer_at + 1].controlInputs(nb_neurons)

class Layer:
    def __init__(self, nb_neurons, nb_inputs, neuron_weights=None):
        self.id = u.getNewId()

        self.nb_neurons = nb_neurons
        self.nb_inputs = nb_inputs
        self.neurons = [Neuron(nb_inputs, weights=(None if neuron_weights is None else neuron_weights[i])) for i in range(nb_neurons)]

    def apply(self, inputs):
        return np.array([neuron.activate(inputs) for neuron in self.neurons])
    def size_out(self):
        return len(self.neurons)
    def size_in(self):
        return len(self.neurons[0].weights)
    def Mutate(self, spread):
        for neuron in self.neurons: neuron.Mutate(spread=spread)
    def NewInput(self):
        self.nb_inputs += 1
        for neuron in self.neurons:
            neuron.AddWeight()
    def NewNeuron(self):
        self.nb_neurons += 1
        self.neurons.append(Neuron(self.nb_inputs))
    def getCopy(self):
        return Layer(self.nb_neurons, len(self.neurons), neuron_weights=[neuron.weights[:] for neuron in self.neurons])
    def controlInputs(self, nb_input):
        if nb_input < self.size_in():
            for neuron in self.neurons:
                neuron.weights = np.array([neuron.weights[i] for i in range(0, nb_input)])
        elif nb_input > self.size_in():
            for i in range(nb_input - self.nb_inputs - 1):
                for neuron in self.neurons:
                    neuron.AddWeight()
        self.nb_inputs = self.size_in()

class Neuron:
    def __init__(self, nb_inputs, func=sigmoid, weights=None):
        self.id = u.getNewId()

        self.function = func
        self.weights = np.array([t.random() - 0.5 for _ in range(nb_inputs)]) if weights is None else weights

    def activate(self, information):
        if len(information) != len(self.weights):
            raise ValueError(f"informations != nb weights : {len(information)} != {len(self.weights)}")
        return sum(self.weights * information)

    def Mutate(self, spread):
        self.weights = t.normal(self.weights, spread, len(self.weights))
    def AddWeight(self):
        self.weights = np.array(list(self.weights) + [t.random() - 0.5])

def PrintNeuralNetwork(network: NeuralNetwork):
    print("Network Print : ")
    print(f" inputs : {network.nb_inputs}", end="")
    for i in range(len(network.layers)):
        print(f" -> in ({network.layers[i].size_in()}) layer[{i}] out ({network.layers[i].size_out()})", end="")
    print(" = output ")

def test():

    network_1 = NeuralNetwork(3, 1, (2,))
    network_2 = NeuralNetwork(copy_from=network_1)

    PrintNeuralNetwork(network_2)

    network_2.NewLayer(5)

    PrintNeuralNetwork(network_2)
#test()