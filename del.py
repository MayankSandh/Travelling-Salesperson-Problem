import numpy as np

# Define the elements to choose from
elements = np.array([1, 2, 3, 4])

# Define the weights corresponding to each element
weights = np.array([0.1, 0.2, 0.3, 0.4])

# Number of samples to draw
num_samples = 100

# Perform weighted probability selection
samples = np.random.choice(elements,  p=weights)

print(samples)
