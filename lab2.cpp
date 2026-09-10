#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <string>
#include <clocale>
#include <omp.h>

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

void computeProduct(const std::string& firstFile, const std::string& secondFile, const std::string& resultFile, int dimension, int threadCount) {
    auto startTime = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<double>> first, second;
    std::vector<std::vector<double>> result(dimension, std::vector<double>(dimension, 0.0));

    if (!readMatrix(firstFile, first, dimension) || !readMatrix(secondFile, second, dimension)) {
        return;
    }

#pragma omp parallel for num_threads(threadCount) schedule(static)
    for (int row = 0; row < dimension; ++row) {
        for (int col = 0; col < dimension; ++col) {
            double total = 0.0;
            for (int inner = 0; inner < dimension; ++inner) {
                total += first[row][inner] * second[inner][col];
            }
            result[row][col] = total;
        }
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = endTime - startTime;
    std::cout << "Время перемножения матриц размера " << dimension << "x" << dimension << " для " << threadCount << " потока(ов): " << elapsed.count() << " мс" << std::endl;
    writeMatrix(resultFile, result, dimension);
}

int main() {
    std::setlocale(LC_ALL, "Russian");

    int sizes[] = {200, 400, 800, 1200, 1600, 2000};
    for (int threadCount = 1; threadCount < 10; threadCount *= 2) {
        for (int size : sizes) {
            computeProduct(
                "input/" + std::to_string(size) + "A.txt",
                "input/" + std::to_string(size) + "B.txt",
                "output/" + std::to_string(size) + "C.txt",
                size, threadCount
            );
        }
    }

    return 0;
}