import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
matrix_sizes = ['200x200', '400x400', '800x800', '1200x1200', '1600x1600', '2000x2000']
threads_1 = [178.8, 1437.5, 11034.3, 38432.7, 112105.4, 220012.3]
threads_2 = [102.5, 768.5, 6400.4, 20479.7, 55450.2, 115644.5]
threads_4 = [60.2, 400.5, 2891.4, 10043.4, 28027.6, 54351.8]
threads_8 = [61.7, 443.3, 2820.7, 9930.5, 28894.2, 54560.6]

# Числовые значения для оси X (размер матрицы)
x_values = [200, 400, 800, 1200, 1600, 2000]

# Настройка стиля и размера графика
plt.figure(figsize=(12, 8))
plt.style.use('seaborn-v0_8-darkgrid')

# Построение графиков
plt.plot(x_values, threads_1, marker='o', linewidth=2, markersize=8, label='1 поток')
plt.plot(x_values, threads_2, marker='s', linewidth=2, markersize=8, label='2 потока')
plt.plot(x_values, threads_4, marker='^', linewidth=2, markersize=8, label='4 потока')
plt.plot(x_values, threads_8, marker='D', linewidth=2, markersize=8, label='8 потоков')

# Настройка подписей
plt.xlabel('Размер матрицы', fontsize=12, fontweight='bold')
plt.ylabel('Время выполнения (мс)', fontsize=12, fontweight='bold')
plt.title('Зависимость времени выполнения от размера матрицы\nпри различном количестве потоков', 
          fontsize=14, fontweight='bold')

# Настройка легенды
plt.legend(title='Количество потоков', fontsize=10, title_fontsize=11)

# Настройка сетки
plt.grid(True, alpha=0.3)

# Автоматическая настройка отступов
plt.tight_layout()

# Сохранение графика в файл (опционально)
plt.savefig('lab2_generated.png', dpi=300, bbox_inches='tight')

# Отображение графика
plt.show()

# Дополнительно: анализ производительности
print("="*60)
print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
print("="*60)

for i, size in enumerate(matrix_sizes):
    print(f"\nРазмер матрицы {size}:")
    print(f"  1 поток:  {threads_1[i]:.1f} мс")
    print(f"  2 потока: {threads_2[i]:.1f} мс (ускорение в {threads_1[i]/threads_2[i]:.2f} раз)")
    print(f"  4 потока: {threads_4[i]:.1f} мс (ускорение в {threads_1[i]/threads_4[i]:.2f} раз)")
    print(f"  8 потоков: {threads_8[i]:.1f} мс (ускорение в {threads_1[i]/threads_8[i]:.2f} раз)")

# Вычисление эффективности параллелизации
print("\n"+"="*60)
print("ЭФФЕКТИВНОСТЬ ПАРАЛЛЕЛИЗАЦИИ (ускорение / количество потоков)")
print("="*60)

for i, size in enumerate(matrix_sizes):
    print(f"\nРазмер матрицы {size}:")
    print(f"  2 потока: {threads_1[i]/(threads_2[i]*2):.2f} ({threads_1[i]/threads_2[i]:.2f}x / 2)")
    print(f"  4 потока: {threads_1[i]/(threads_4[i]*4):.2f} ({threads_1[i]/threads_4[i]:.2f}x / 4)")
    print(f"  8 потоков: {threads_1[i]/(threads_8[i]*8):.2f} ({threads_1[i]/threads_8[i]:.2f}x / 8)")