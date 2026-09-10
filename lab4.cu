#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <string>
#include <cuda_runtime.h>

bool readMatrix(const std::string& path, std::vector<std::vector<double>>& data, int size) {
    std::ifstream input(path);
    if (!input.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << path << std::endl;
        return false;
    }

    data.resize(size, std::vector<double>(size));
    for (int row = 0; row < size; ++row) {
        for (int col = 0; col < size; ++col) {
            if (!(input >> data[row][col])) {
                std::cerr << "Ошибка: недостаточно данных в файле " << path << std::endl;
                return false;
            }
        }
    }
    input.close();
    return true;
}

bool writeMatrix(const std::string& path, const std::vector<std::vector<double>>& data, int size) {
    std::ofstream output(path);
    if (!output.is_open()) {
        std::cerr << "Ошибка: не удалось создать файл " << path << std::endl;
        return false;
    }

    for (int row = 0; row < size; ++row) {
        for (int col = 0; col < size; ++col) {
            output << data[row][col] << (col == size - 1 ? "" : " ");
        }
        output << "\n";
    }
    output.close();
    return true;
}

__global__ void matrixMulKernel(const double* first, const double* second, double* result, int dimension) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < dimension && col < dimension) {
        double total = 0.0;
        for (int inner = 0; inner < dimension; ++inner) {
            total += first[row * dimension + inner] * second[inner * dimension + col];
        }
        result[row * dimension + col] = total;
    }
}

void computeProduct(const std::string& firstFile, const std::string& secondFile, const std::string& resultFile, int dimension, int blockX = 16, int blockY = 16) {
    auto startTotal = std::chrono::high_resolution_clock::now();

    std::vector<std::vector<double>> first2D, second2D;
    std::vector<std::vector<double>> result2D(dimension, std::vector<double>(dimension, 0.0));

    if (!readMatrix(firstFile, first2D, dimension) || !readMatrix(secondFile, second2D, dimension)) {
        return;
    }

    std::vector<double> firstFlat(dimension * dimension);
    std::vector<double> secondFlat(dimension * dimension);
    std::vector<double> resultFlat(dimension * dimension, 0.0);

    for (int row = 0; row < dimension; ++row) {
        for (int col = 0; col < dimension; ++col) {
            firstFlat[row * dimension + col] = first2D[row][col];
            secondFlat[row * dimension + col] = second2D[row][col];
        }
    }

    double* deviceFirst, * deviceSecond, * deviceResult;
    size_t bytes = dimension * dimension * sizeof(double);

    cudaMalloc((void**)&deviceFirst, bytes);
    cudaMalloc((void**)&deviceSecond, bytes);
    cudaMalloc((void**)&deviceResult, bytes);

    cudaMemcpy(deviceFirst, firstFlat.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(deviceSecond, secondFlat.data(), bytes, cudaMemcpyHostToDevice);

    dim3 threadsPerBlock(blockX, blockY);
    dim3 numBlocks((dimension + threadsPerBlock.x - 1) / threadsPerBlock.x,
        (dimension + threadsPerBlock.y - 1) / threadsPerBlock.y);

    auto startGPU = std::chrono::high_resolution_clock::now();

    matrixMulKernel << <numBlocks, threadsPerBlock >> > (deviceFirst, deviceSecond, deviceResult, dimension);

    cudaDeviceSynchronize();

    auto endGPU = std::chrono::high_resolution_clock::now();

    cudaMemcpy(resultFlat.data(), deviceResult, bytes, cudaMemcpyDeviceToHost);

    cudaFree(deviceFirst);
    cudaFree(deviceSecond);
    cudaFree(deviceResult);

    for (int row = 0; row < dimension; ++row) {
        for (int col = 0; col < dimension; ++col) {
            result2D[row][col] = resultFlat[row * dimension + col];
        }
    }

    writeMatrix(resultFile, result2D, dimension);

    auto endTotal = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> durationTotal = endTotal - startTotal;
    std::chrono::duration<double, std::milli> durationGPU = endGPU - startGPU;

    std::cout << "Размер: " << dimension << "x" << dimension << " | Конфигурация блока: " << blockX << "x" << blockY << "\n"
        << "  -> Время вычислений (GPU): " << durationGPU.count() << " мс\n"
        << "  -> Общее время (с I/O): " << durationTotal.count() << " мс\n" << std::endl;
}

int main() {
    std::setlocale(LC_ALL, "Russian");

    int dimensions[] = {200, 400, 800, 1200, 1600, 2000};
    for (int dimension : dimensions) {
        computeProduct(
            "input/" + std::to_string(dimension) + "A.txt",
            "input/" + std::to_string(dimension) + "B.txt",
            "output/" + std::to_string(dimension) + "C.txt",
            dimension, 8, 8
        );
    }

    return 0;
}