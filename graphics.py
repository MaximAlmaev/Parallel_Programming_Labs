import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
matrix_sizes = ['200x200', '400x400', '800x800', '1200x1200', '1600x1600', '2000x2000']
cores_1 = [100.4, 641.6, 5407.3, 16492.2, 38892.1, 78574.6]
cores_2 = [62.4, 376.3, 2246.4, 7339.2, 18598.3, 35654.8]
cores_4 = [26.3, 207.7, 1299.4, 3746.4, 9826.5, 19345.2]
cores_8 = [17.5, 100.4, 676.4, 2206.5, 5372.7, 9769.5]
cores_16 = [6.4, 55.5, 392.2, 1221.4, 3123.8, 5106.1]
cores_32 = [6.8, 19.3, 131.4, 421.5, 1067.3, 1791.5]

# Числовые значения для оси X (размер матрицы)
x_values = [200, 400, 800, 1200, 1600, 2000]

# Настройка стиля и размера графика
plt.figure(figsize=(14, 9))
plt.style.use('seaborn-v0_8-darkgrid')

# Построение графиков с разными маркерами и цветами
plt.plot(x_values, cores_1, marker='o', linewidth=2.5, markersize=9, label='1 ядро', color='#1f77b4')
plt.plot(x_values, cores_2, marker='s', linewidth=2.5, markersize=9, label='2 ядра', color='#ff7f0e')
plt.plot(x_values, cores_4, marker='^', linewidth=2.5, markersize=9, label='4 ядра', color='#2ca02c')
plt.plot(x_values, cores_8, marker='D', linewidth=2.5, markersize=9, label='8 ядер', color='#d62728')
plt.plot(x_values, cores_16, marker='*', linewidth=2.5, markersize=12, label='16 ядер', color='#9467bd')
plt.plot(x_values, cores_32, marker='X', linewidth=2.5, markersize=10, label='32 ядра', color='#8c564b')

# Настройка подписей
plt.xlabel('Размер матрицы', fontsize=13, fontweight='bold')
plt.ylabel('Время выполнения (мс)', fontsize=13, fontweight='bold')
plt.title('Зависимость времени выполнения от размера матрицы\nпри различном количестве ядер (OpenMP)', 
          fontsize=15, fontweight='bold', pad=20)

# Настройка легенды
plt.legend(title='Количество ядер', fontsize=11, title_fontsize=12, 
           loc='upper left', framealpha=0.95)

# Настройка сетки
plt.grid(True, alpha=0.3, linestyle='--')


# Автоматическая настройка отступов
plt.tight_layout()

plt.savefig('lab5_generated.png', dpi=300, bbox_inches='tight')

# Отображение графика
plt.show()

# Дополнительно: подробный анализ производительности
print("="*80)
print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ПРИ РАЗЛИЧНОМ КОЛИЧЕСТВЕ ЯДЕР")
print("="*80)

for i, size in enumerate(matrix_sizes):
    print(f"\n{'='*40}")
    print(f"Размер матрицы {size}")
    print(f"{'='*40}")
    print(f"  1 ядро:   {cores_1[i]:.1f} мс")
    print(f"  2 ядра:   {cores_2[i]:.1f} мс (ускорение в {cores_1[i]/cores_2[i]:.2f}x)")
    print(f"  4 ядра:   {cores_4[i]:.1f} мс (ускорение в {cores_1[i]/cores_4[i]:.2f}x)")
    print(f"  8 ядер:   {cores_8[i]:.1f} мс (ускорение в {cores_1[i]/cores_8[i]:.2f}x)")
    print(f"  16 ядер:  {cores_16[i]:.1f} мс (ускорение в {cores_1[i]/cores_16[i]:.2f}x)")
    print(f"  32 ядра:  {cores_32[i]:.1f} мс (ускорение в {cores_1[i]/cores_32[i]:.2f}x)")

# Эффективность параллелизации (закон Амдала)
print("\n"+"="*80)
print("ЭФФЕКТИВНОСТЬ ПАРАЛЛЕЛИЗАЦИИ (ускорение / количество ядер)")
print("="*80)

for i, size in enumerate(matrix_sizes):
    print(f"\nРазмер матрицы {size}:")
    cores_list = [2, 4, 8, 16, 32]
    speedups = [cores_1[i]/cores_2[i], cores_1[i]/cores_4[i], 
                cores_1[i]/cores_8[i], cores_1[i]/cores_16[i], 
                cores_1[i]/cores_32[i]]
    
    for j, (c, s) in enumerate(zip(cores_list, speedups)):
        efficiency = s / c
        print(f"  {c:2d} ядер: {efficiency:.2f} ({s:.2f}x / {c})")

# Оптимальное количество ядер для каждого размера
print("\n"+"="*80)
print("ОПТИМАЛЬНОЕ КОЛИЧЕСТВО ЯДЕР (по времени выполнения)")
print("="*80)

for i, size in enumerate(matrix_sizes):
    times = [cores_1[i], cores_2[i], cores_4[i], cores_8[i], cores_16[i], cores_32[i]]
    cores = [1, 2, 4, 8, 16, 32]
    best_idx = np.argmin(times)
    print(f"{size:10s} → {cores[best_idx]:2d} ядер  ({times[best_idx]:.1f} мс)")

# Максимальное ускорение
print("\n"+"="*80)
print("МАКСИМАЛЬНОЕ ДОСТИГНУТОЕ УСКОРЕНИЕ")
print("="*80)

max_speedups = []
cores_labels = ['2', '4', '8', '16', '32']
for j, label in enumerate(cores_labels):
    speedups = []
    for i in range(len(matrix_sizes)):
        if j == 0:
            speedup = cores_1[i]/cores_2[i]
        elif j == 1:
            speedup = cores_1[i]/cores_4[i]
        elif j == 2:
            speedup = cores_1[i]/cores_8[i]
        elif j == 3:
            speedup = cores_1[i]/cores_16[i]
        else:
            speedup = cores_1[i]/cores_32[i]
        speedups.append(speedup)
    
    max_sp = max(speedups)
    max_idx = np.argmax(speedups)
    print(f"{label:>2} ядра: {max_sp:.2f}x (при {matrix_sizes[max_idx]})")
    max_speedups.append(max_sp)

# Вывод общей статистики
print("\n"+"="*80)
print("ОБЩАЯ СТАТИСТИКА")
print("="*80)
print(f"Среднее ускорение при 2 ядрах:  {np.mean([cores_1[i]/cores_2[i] for i in range(6)]):.2f}x")
print(f"Среднее ускорение при 4 ядрах:  {np.mean([cores_1[i]/cores_4[i] for i in range(6)]):.2f}x")
print(f"Среднее ускорение при 8 ядрах:  {np.mean([cores_1[i]/cores_8[i] for i in range(6)]):.2f}x")
print(f"Среднее ускорение при 16 ядрах: {np.mean([cores_1[i]/cores_16[i] for i in range(6)]):.2f}x")
print(f"Среднее ускорение при 32 ядрах: {np.mean([cores_1[i]/cores_32[i] for i in range(6)]):.2f}x")

# Анализ масштабируемости
print("\n"+"="*80)
print("АНАЛИЗ МАСШТАБИРУЕМОСТИ (рост производительности при удвоении ядер)")
print("="*80)

for i, size in enumerate(matrix_sizes):
    print(f"\n{size}:")
    print(f"  2→4 ядра: {cores_2[i]/cores_4[i]:.2f}x")
    print(f"  4→8 ядер: {cores_4[i]/cores_8[i]:.2f}x")
    print(f"  8→16 ядер: {cores_8[i]/cores_16[i]:.2f}x")
    print(f"  16→32 ядер: {cores_16[i]/cores_32[i]:.2f}x")