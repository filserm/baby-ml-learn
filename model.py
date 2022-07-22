import os
from tensorflow.keras import layers

from micmon.dataset import Dataset
from micmon.model import Model

# This is a directory that contains the saved .npz dataset files
datasets_dir = os.path.expanduser('/app/datasets/sound-detect/data')

# This is the output directory where the model will be saved
model_dir = os.path.expanduser('/app/models/sound-detect')

# This is the number of training epochs for each dataset sample
epochs = 2

# Load the datasets from the compressed files.
# 70% of the data points will be included in the training set,
# 30% of the data points will be included in the evaluation set
# and used to evaluate the performance of the model.
datasets = Dataset.scan(datasets_dir, validation_split=0.3)
labels = ['negative', 'positive']
freq_bins = len(datasets[0].samples[0])

# Create a network with 4 layers (one input layer, two intermediate layers and one output layer).
# The first intermediate layer in this example will have twice the number of units as the number
# of input units, while the second intermediate layer will have 75% of the number of
# input units. We also specify the names for the labels and the low and high frequency range
# used when sampling.
model = Model(
    [
        layers.Input(shape=(freq_bins,)),
        layers.Dense(int(2 * freq_bins), activation='relu'),
        layers.Dense(int(0.75 * freq_bins), activation='relu'),
        layers.Dense(len(labels), activation='softmax'),
    ],
    labels=labels,
    low_freq=datasets[0].low_freq,
    high_freq=datasets[0].high_freq
)

# Train the model
for epoch in range(epochs):
    for i, dataset in enumerate(datasets):
        print(f'[epoch {epoch+1}/{epochs}] [audio sample {i+1}/{len(datasets)}]')
        model.fit(dataset)
        evaluation = model.evaluate(dataset)
        print(f'Validation set loss and accuracy: {evaluation}')

# Save the model
model.save(model_dir, overwrite=True)
