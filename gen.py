import numpy as np

def generate_matrix(size: int, path: str, min_val: int = 0, max_val: int = 100) -> None:
    matrix = np.random.randint(min_val, max_val + 1, size=(size, size))
    np.savetxt(path, matrix, fmt='%d', delimiter=' ')

    print(f"Matrix {size}x{size} saved in '{path}'")

generate_matrix(size=200, path='input/200A.txt')
generate_matrix(size=200, path='input/200B.txt')
generate_matrix(size=400, path='input/400A.txt')
generate_matrix(size=400, path='input/400B.txt')
generate_matrix(size=800, path='input/800A.txt')
generate_matrix(size=800, path='input/800B.txt')
generate_matrix(size=1200, path='input/1200A.txt')
generate_matrix(size=1200, path='input/1200B.txt')
generate_matrix(size=1600, path='input/1600A.txt')
generate_matrix(size=1600, path='input/1600B.txt')
generate_matrix(size=2000, path='input/2000A.txt')
generate_matrix(size=2000, path='input/2000B.txt')