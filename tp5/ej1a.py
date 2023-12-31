from tp5.optimizer import Adam
from tp5.nn import MLP
from tp5.layers import Dense
from tp5.activations import ReLU, Sigmoid, Tanh, Identity
from tp5.autoencoder import Autoencoder
from tp5.loss import MSE
from tp4.Hopfield.pattern_loader import *
import matplotlib.pyplot as plt

INPUT_SIZE = 35
LATENT_SIZE = 2
HIDDEN_SIZE = 15
HIDDEN_SIZE2 = 20

# Using ReLU here causes overflow in next hidden layer Sigmoid function
LATENT_FUNCTION = Sigmoid()

NOISE = None

fonts_headers = np.array(
    ["`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
     "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "DEL"]
)


def graph_fonts(original, decoded):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title('Original')
    ax2.set_title('Decoded')
    ax1.imshow(np.array(original).reshape((7, 5)), cmap='gray')
    ax2.imshow(np.array(decoded).reshape((7, 5)), cmap='gray')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    fig.show()


def graph_latent_space(dots):
    for j in range(dots.__len__()):
        plt.scatter(dots[j][0], dots[j][1])
        plt.annotate(fonts_headers[j], xy=dots[j], xytext=(dots[j][0] + 0.01, dots[j][1] + 0.01), fontsize=12)
    plt.show()


if __name__ == "__main__":
    dataset_input = load_pattern_map('characters.txt')

    # set the learning rate and optimizer for training
    optimizer = Adam(0.01)

    amount_correct_characters = 0

    encoder = MLP()
    encoder.addLayer(Dense(inputDim=INPUT_SIZE, outputDim=HIDDEN_SIZE, activation=Sigmoid(), optimizer=optimizer))
    encoder.addLayer(Dense(inputDim=HIDDEN_SIZE, outputDim=LATENT_SIZE, activation=Identity(), optimizer=optimizer))

    decoder = MLP()
    decoder.addLayer(Dense(inputDim=LATENT_SIZE, outputDim=HIDDEN_SIZE, activation=Sigmoid(), optimizer=optimizer))
    decoder.addLayer(Dense(inputDim=HIDDEN_SIZE, outputDim=INPUT_SIZE, activation=Tanh(), optimizer=optimizer))

    autoencoder = Autoencoder(encoder, decoder, noise=NOISE)

    print(autoencoder)

    my_callbacks = {}  # {"loss": loss_callback}

    autoencoder.train(dataset_input=list(dataset_input.values()), loss=MSE(), metrics=["train_loss", "test_loss"],
                      tensorboard=False, epochs=10000,
                      callbacks=my_callbacks)

    dataset_input_list = list(dataset_input.values())

    dots = []
    decoder_outputs = []

    for i in range(len(dataset_input_list)):
        input_reshaped = np.reshape(dataset_input_list[i], (len(dataset_input_list[i]), 1))
        output_history = []
        output = autoencoder.feedforward(input_reshaped, output_history)
        for j in range(len(output)):
            if output[j][0] >= 0:
                output[j][0] = 1
            else:
                output[j][0] = -1

        decoder_outputs.append(output)

        different_pixels = np.where(output.flatten() != dataset_input_list[i])
        amount_different_pixels = len(different_pixels[0])

        if amount_different_pixels <= 1:
            amount_correct_characters += 1

        print(f"Character: {fonts_headers[i]}")
        print(f"Error in pixels: {amount_different_pixels}")

        # First index: 1 because latent space is in index 1
        # Second index: 0 and 1 represent x and y respectively
        # Third index: 0 because is a list of list
        dot = (output_history[1][0][0], output_history[1][1][0])
        dots.append(dot)

    print(f"Recognized characters: {amount_correct_characters}/{len(dataset_input_list)}")

    # 1.a.1)
    # Graph of the neural network
    # autoencoder.plotGraph()

    # 1.a.2)

    # Top 10 because SciView has limit of 29 graphs
    # for j in range(10):
        # graph_fonts(list(dataset_input.values())[j], decoder_outputs[j])

    # 1.a.3)
    graph_latent_space(dots)

    # 1.a.4)
    # Trying a letter similar to 'o', Change letter to have another generated image
    letters = ['o', 'x', '~', "{"]
    for letter in letters:
        index = np.where(fonts_headers == letter)[0][0]

        new_character_coordinates = [dots[index][0] + 0.2, dots[index][1] + 0.2]  # offset of 0.05
        new_character_coordinates_reshaped = np.reshape(new_character_coordinates, (2, 1))
        output = autoencoder.sampling(new_character_coordinates_reshaped)

        for j in range(len(output)):
            if output[j][0] >= 0:
                output[j][0] = 1
            else:
                output[j][0] = -1

        plt.title(f"New character, near to '{letter}'")
        plt.imshow(output.reshape(7, 5), cmap='gray')
        plt.xticks([])
        plt.yticks([])
        plt.show()

