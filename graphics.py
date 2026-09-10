import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
matrix_sizes = ['200x200', '400x400', '800x800', '1200x1200', '1600x1600', '2000x2000']
cores_1 = [65.5, 568.4, 4619.9, 14707.3, 37450.4, 86650.7]
cores_2 = [39.6, 320.1, 2580.7, 8078.4, 18647.2, 47899.1]
cores_4 = [22.6, 180.8, 1296.3, 3897.3, 9532.6, 26144.4]
cores_8 = [21.8, 177.9, 1246.9, 3678.3, 9452.5, 24878.4]

# Числовые значения для оси X (размер матрицы)
x_values = [200, 400, 800, 1200, 1600, 2000]

# Настройка стиля и размера графика
plt.figure(figsize=(12, 8))
plt.style.use('seaborn-v0_8-darkgrid')

# Построение графиков
plt.plot(x_values, cores_1, marker='o', linewidth=2, markersize=8, label='1 ядро')
plt.plot(x_values, cores_2, marker='s', linewidth=2, markersize=8, label='2 ядра')
plt.plot(x_values, cores_4, marker='^', linewidth=2, markersize=8, label='4 ядра')
plt.plot(x_values, cores_8, marker='D', linewidth=2, markersize=8, label='8 ядер')

# Настройка подписей
plt.xlabel('Размер матрицы', fontsize=12, fontweight='bold')
plt.ylabel('Время выполнения (мс)', fontsize=12, fontweight='bold')
plt.title('Зависимость времени выполнения от размера матрицы\nпри различном количестве ядер', 
          fontsize=14, fontweight='bold')

# Настройка легенды
plt.legend(title='Количество ядер', fontsize=10, title_fontsize=11)

# Настройка сетки
plt.grid(True, alpha=0.3)

# Автоматическая настройка отступов
plt.tight_layout()

plt.savefig('lab3_generated.png', dpi=300, bbox_inches='tight')

# Отображение графика
plt.show()

# Дополнительно: анализ производительности
print("="*70)
print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ПРИ ИСПОЛЬЗОВАНИИ РАЗЛИЧНОГО КОЛИЧЕСТВА ЯДЕР")
print("="*70)

for i, size in enumerate(matrix_sizes):
    print(f"\nРазмер матрицы {size}:")
    print(f"  1 ядро:   {cores_1[i]:.1f} мс")
    print(f"  2 ядра:   {cores_2[i]:.1f} мс (ускорение в {cores_1[i]/cores_2[i]:.2f} раз)")
    print(f"  4 ядра:   {cores_4[i]:.1f} мс (ускорение в {cores_1[i]/cores_4[i]:.2f} раз)")
    print(f"  8 ядер:   {cores_8[i]:.1f} мс (ускорение в {cores_1[i]/cores_8[i]:.2f} раз)")

# Вычисление эффективности параллелизации (закон Амдала)
print("\n"+"="*70)
print("ЭФФЕКТИВНОСТЬ ПАРАЛЛЕЛИЗАЦИИ (ускорение / количество ядер)")
print("="*70)

for i, size in enumerate(matrix_sizes):
    print(f"\nРазмер матрицы {size}:")
    eff_2 = cores_1[i]/(cores_2[i]*2)
    eff_4 = cores_1[i]/(cores_4[i]*4)
    eff_8 = cores_1[i]/(cores_8[i]*8)
    print(f"  2 ядра:   {eff_2:.2f} ({cores_1[i]/cores_2[i]:.2f}x / 2)")
    print(f"  4 ядра:   {eff_4:.2f} ({cores_1[i]/cores_4[i]:.2f}x / 4)")
    print(f"  8 ядер:   {eff_8:.2f} ({cores_1[i]/cores_8[i]:.2f}x / 8)")

# Определение оптимального количества ядер для каждого размера
print("\n"+"="*70)
print("ОПТИМАЛЬНОЕ КОЛИЧЕСТВО ЯДЕР ПО КРИТЕРИЮ ВРЕМЕНИ")
print("="*70)

for i, size in enumerate(matrix_sizes):
    times = [cores_1[i], cores_2[i], cores_4[i], cores_8[i]]
    cores = [1, 2, 4, 8]
    best_core = cores[np.argmin(times)]
    best_time = min(times)
    print(f"{size}: {best_core} ядра/ядер ({best_time:.1f} мс)")

# Вывод максимального ускорения
print("\n"+"="*70)
print("МАКСИМАЛЬНОЕ УСКОРЕНИЕ")
print("="*70)
max_speedup_8 = max([cores_1[i]/cores_8[i] for i in range(len(matrix_sizes))])
max_speedup_4 = max([cores_1[i]/cores_4[i] for i in range(len(matrix_sizes))])
max_speedup_2 = max([cores_1[i]/cores_2[i] for i in range(len(matrix_sizes))])
print(f"Наибольшее ускорение при 2 ядрах: {max_speedup_2:.2f}x")
print(f"Наибольшее ускорение при 4 ядрах: {max_speedup_4:.2f}x")
print(f"Наибольшее ускорение при 8 ядрах: {max_speedup_8:.2f}x")