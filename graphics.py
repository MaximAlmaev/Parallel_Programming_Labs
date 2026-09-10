import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
matrix_sizes = ['200x200', '400x400', '800x800', '1200x1200', '1600x1600', '2000x2000']
grid_8x8 = [163.4, 143.4, 205.8, 225.3, 285.3, 346.2]
grid_16x16 = [145.7, 149.6, 181.5, 228.5, 276.3, 333.5]
grid_32x32 = [159.4, 138.7, 194.9, 224.6, 254.3, 318.7]

# Числовые значения для оси X (размер матрицы)
x_values = [200, 400, 800, 1200, 1600, 2000]

# Настройка стиля и размера графика
plt.figure(figsize=(10, 6))
plt.style.use('seaborn-v0_8-darkgrid')

# Построение графиков
plt.plot(x_values, grid_8x8, marker='o', linewidth=2, markersize=8, label='8x8')
plt.plot(x_values, grid_16x16, marker='s', linewidth=2, markersize=8, label='16x16')
plt.plot(x_values, grid_32x32, marker='^', linewidth=2, markersize=8, label='32x32')

# Настройка подписей
plt.xlabel('Размер матрицы', fontsize=12, fontweight='bold')
plt.ylabel('Время выполнения (мс)', fontsize=12, fontweight='bold')
plt.title('Зависимость времени выполнения от размера матрицы\nпри различных конфигурациях сетки', 
          fontsize=14, fontweight='bold')

# Настройка легенды
plt.legend(title='Конфигурация сетки', fontsize=10, title_fontsize=11)

# Настройка сетки
plt.grid(True, alpha=0.3)

# Автоматическая настройка отступов
plt.tight_layout()

plt.savefig('lab4_generated.png', dpi=300, bbox_inches='tight')

# Отображение графика
plt.show()

# Дополнительно: вывод статистики
print("Минимальное время выполнения:")
print(f"8x8: {min(grid_8x8)} мс (при {matrix_sizes[np.argmin(grid_8x8)]})")
print(f"16x16: {min(grid_16x16)} мс (при {matrix_sizes[np.argmin(grid_16x16)]})")
print(f"32x32: {min(grid_32x32)} мс (при {matrix_sizes[np.argmin(grid_32x32)]})")