import math

def generate_primes(limit):
    primes = []
    size = 20000000  # Estimated upper bound for 1 million primes
    sieve = [True] * size
    sieve[0:2] = [False, False]

    for num in range(2, size):
        if sieve[num]:
            primes.append(format(num, 'b'))  # Binary without '0b'
            if len(primes) >= limit:
                break
            for multiple in range(num * 2, size, num):
                sieve[multiple] = False

    return ' '.join(primes)

# Generate binary primes and save to file
output_text = generate_primes(1_000_000)
file_path = "binary_primes.txt"

with open(file_path, "w") as f:
    f.write(output_text)

# Show download link (works in Jupyter/Colab)
try:
    from IPython.display import FileLink, display
    display(FileLink(file_path))
except ImportError:
    print(f"File saved at: {file_path}")
