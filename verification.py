import numpy as np

def verify_multiplication(file_a, file_b, file_c):
    try:
        A = np.loadtxt(file_a)
        B = np.loadtxt(file_b)
        C_loaded = np.loadtxt(file_c)

        C_calculated = np.dot(A, B)

        if np.allclose(C_calculated, C_loaded):
            print("Verification passed: the multiplication result is correct.")
        else:
            print("Verification failed: the calculated matrix does not match the resulting matrix.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Data reading error or dimension mismatch: {e}")

verify_multiplication('input/200A.txt', 'input/200B.txt', 'output/200C.txt')
verify_multiplication('input/400A.txt', 'input/400B.txt', 'output/400C.txt')
verify_multiplication('input/800A.txt', 'input/800B.txt', 'output/800C.txt')
verify_multiplication('input/1200A.txt', 'input/1200B.txt', 'output/1200C.txt')
verify_multiplication('input/1600A.txt', 'input/1600B.txt', 'output/1600C.txt')
verify_multiplication('input/2000A.txt', 'input/2000B.txt', 'output/2000C.txt')