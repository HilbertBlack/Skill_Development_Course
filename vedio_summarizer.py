import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

# Function to generate Perlin noise
def generate_noise(width, height, scale=100, octaves=1):
    noise_image = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            noise_value = pnoise2(x / scale, 
                                 y / scale, 
                                 octaves=octaves, 
                                 persistence=0.5, 
                                 lacunarity=2.0, 
                                 repeatx=1024, 
                                 repeaty=1024, 
                                 base=42)
            noise_image[y][x] = (noise_value + 1) / 2  # Normalize to [0, 1]
    return noise_image

# Function to generate and display noise image
def gradio_interface(width=512, height=512, scale=100, octaves=1):
    noise_image = generate_noise(width, height, scale, octaves)
    
    # Plot the noise image using matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(noise_image, cmap='gray', interpolation='nearest')
    ax.axis('off')  # Hide axes for better presentation

    # Save the image as a file and return its path
    plt.tight_layout()
    image_path = "/tmp/generated_noise.png"
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)  # Close the figure to free memory

    return image_path

# Gradio interface
gr.Interface(fn=gradio_interface, 
             inputs=[gr.Slider(minimum=256, maximum=1024, value=512, label="Width"),
                     gr.Slider(minimum=256, maximum=1024, value=512, label="Height"),
                     gr.Slider(minimum=10, maximum=500, value=100, label="Scale"),
                     gr.Slider(minimum=1, maximum=10, value=1, label="Octaves")],
             outputs="image", 
             live=True).launch()

