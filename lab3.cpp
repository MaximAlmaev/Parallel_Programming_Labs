#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <mpi.h>

bool readMatrix(const std::string& path, std::vector<double>& data, int size) {
    std::ifstream input(path);
    if (!input.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << path << std::endl;
        return false;
    }

    data.resize(size * size);
    for (int row = 0; row < size; ++row) {
        for (int col = 0; col < size; ++col) {
            if (!(input >> data[row * size + col])) {
                std::cerr << "Ошибка: недостаточно данных в файле " << path << std::endl;
                return false;
            }
        }
    }
    input.close();
    return true;
}

bool writeMatrix(const std::string& path, const std::vector<double>& data, int size) {
    std::ofstream output(path);
    if (!output.is_open()) {
        std::cerr << "Ошибка: не удалось создать файл " << path << std::endl;
        return false;
    }

    for (int row = 0; row < size; ++row) {
        for (int col = 0; col < size; ++col) {
            output << data[row * size + col] << (col == size - 1 ? "" : " ");
        }
        output << "\n";
    }
    output.close();
    return true;
}

void computeProduct(const std::string& firstFile, const std::string& secondFile, const std::string& resultFile, int dimension, int rank, int processCount) {
    std::vector<double> first, second, result;
    second.resize(dimension * dimension);

    double startTime;

    if (rank == 0) {
        first.resize(dimension * dimension);
        result.resize(dimension * dimension);
        readMatrix(firstFile, first, dimension);
        readMatrix(secondFile, second, dimension);
        startTime = MPI_Wtime();
    }

    MPI_Bcast(second.data(), dimension * dimension, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    std::vector<int> sendCounts(processCount);
    std::vector<int> displacements(processCount);
    int offset = 0;

    for (int i = 0; i < processCount; ++i) {
        int rows = dimension / processCount + (i < dimension % processCount ? 1 : 0);
        sendCounts[i] = rows * dimension;
        displacements[i] = offset;
        offset += sendCounts[i];
    }

    int localRows = sendCounts[rank] / dimension;
    std::vector<double> localFirst(sendCounts[rank]);
    std::vector<double> localResult(sendCounts[rank], 0.0);

    MPI_Scatterv(rank == 0 ? first.data() : nullptr, sendCounts.data(), displacements.data(), MPI_DOUBLE,
        localFirst.data(), sendCounts[rank], MPI_DOUBLE, 0, MPI_COMM_WORLD);

    for (int row = 0; row < localRows; ++row) {
        for (int col = 0; col < dimension; ++col) {
            double total = 0.0;
            for (int inner = 0; inner < dimension; ++inner) {
                total += localFirst[row * dimension + inner] * second[inner * dimension + col];
            }
            localResult[row * dimension + col] = total;
        }
    }

    MPI_Gatherv(localResult.data(), sendCounts[rank], MPI_DOUBLE,
        rank == 0 ? result.data() : nullptr, sendCounts.data(), displacements.data(), MPI_DOUBLE,
        0, MPI_COMM_WORLD);

    if (rank == 0) {
        double endTime = MPI_Wtime();
        double durationMs = (endTime - startTime) * 1000.0;
        std::cout << "Время перемножения (MPI, потоков: " << processCount << ") матриц " << dimension << "x" << dimension << ": " << durationMs << " мс" << std::endl;
        writeMatrix(resultFile, result, dimension);
    }
}

int main(int argc, char** argv) {
    setlocale(LC_ALL, "Russian");

    MPI_Init(&argc, &argv);

    int rank, processCount;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &processCount);

    if (rank == 0) {
        int dimensions[] = {200, 400, 800, 1200, 1600, 2000};
        for (int dimension : dimensions) {
            computeProduct(
                "input/" + std::to_string(dimension) + "A.txt",
                "input/" + std::to_string(dimension) + "B.txt",
                "output/" + std::to_string(dimension) + "C.txt",
                dimension, rank, processCount
            );
        }
    }

    MPI_Finalize();

    return 0;
}