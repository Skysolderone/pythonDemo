import math

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Custom neural network layer
def neural_layer(input_list, weights, bias):
    return [sigmoid(x * w + bias) for x, w in zip(input_list, weights)]

input_list = [0.5, -1.2, 3.0, -0.7]
weights = [0.8, -0.5, 1.2, 0.3]
bias = 0.1
output_list = neural_layer(input_list, weights, bias)

for i, y in enumerate(output_list):
    print(f"Layer output for input[{i}] = {y}")