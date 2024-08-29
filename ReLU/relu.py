import numpy as np

def relu_array(arr):
    return np.maximum(0,arr)    

def relu(x):
    return max(0,x)


class SimpleNeuralLayer:
    def __init__(self,input_size,output_size) :
        self.weights=np.random.randn(input_size,output_size)
        self.biass=np.zeros(output_size)
    def forward(self,inputs):
        z=np.dot(inputs,self.weights)+self.biass
        return relu_array(z)

layer = SimpleNeuralLayer(3, 2)
inputs = np.array([1, 2, -1])
output = layer.forward(inputs)
print(output)
