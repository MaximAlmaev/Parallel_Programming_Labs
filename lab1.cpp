#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <string>

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

void computeProduct(const std::string& firstFile, const std::string& secondFile, const std::string& resultFile, int dimension) {
    auto startTime = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<double>> first, second;
    std::vector<std::vector<double>> result(dimension, std::vector<double>(dimension, 0.0));
    readMatrix(firstFile, first, dimension);
    readMatrix(secondFile, second, dimension);

    for (int row = 0; row < dimension; ++row) {
        for (int col = 0; col < dimension; ++col) {
            result[row][col] = 0.0;
            for (int inner = 0; inner < dimension; ++inner) {
                result[row][col] += first[row][inner] * second[inner][col];
            }
        }
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = endTime - startTime;
    std::cout << "Время перемножения матриц размера " << dimension << "x" << dimension << ": " << elapsed.count() << " мс" << std::endl;
    writeMatrix(resultFile, result, dimension);
}

int main() {
    std::setlocale(LC_ALL, "Russian");

    computeProduct("input/200A.txt", "input/200B.txt", "output/200C.txt", 200);
    computeProduct("input/400A.txt", "input/400B.txt", "output/400C.txt", 400);
    computeProduct("input/800A.txt", "input/800B.txt", "output/800C.txt", 800);
    computeProduct("input/1200A.txt", "input/1200B.txt", "output/1200C.txt", 1200);
    computeProduct("input/1600A.txt", "input/1600B.txt", "output/1600C.txt", 1600);
    computeProduct("input/2000A.txt", "input/2000B.txt", "output/2000C.txt", 2000);

    return 0;
}