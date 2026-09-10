import matplotlib.pyplot as plt
import numpy as np

# Данные из таблицы
matrix_sizes = ['200x200', '400x400', '800x800', '1200x1200', '1600x1600', '2000x2000']
execution_times = [447.13, 3135.84, 22789.5, 84345.2, 204344, 405433]

# Числовые значения для оси X (размер матрицы)
x_values = [200, 400, 800, 1200, 1600, 2000]

# Настройка стиля и размера графика
plt.figure(figsize=(12, 8))
plt.style.use('seaborn-v0_8-darkgrid')

# Построение графика
plt.plot(x_values, execution_times, marker='o', linewidth=2.5, markersize=10, 
         color='#1f77b4', markerfacecolor='#ff7f0e', markeredgecolor='#1f77b4',
         markeredgewidth=2, label='Время выполнения')

# Добавление точек с подписями значений
for x, y in zip(x_values, execution_times):
    plt.annotate(f'{y:.1f} мс', 
                 xy=(x, y), 
                 xytext=(10, 10),
                 textcoords='offset points',
                 fontsize=9,
                 fontweight='bold',
                 color='#333333',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffcc', alpha=0.8))

# Настройка подписей
plt.xlabel('Размер матрицы', fontsize=13, fontweight='bold')
plt.ylabel('Время выполнения (мс)', fontsize=13, fontweight='bold')
plt.title('Зависимость времени выполнения от размера матрицы', 
          fontsize=15, fontweight='bold', pad=20)

# Настройка легенды
plt.legend(fontsize=11, loc='upper left')

# Настройка сетки
plt.grid(True, alpha=0.3, linestyle='--')

# Автоматическая настройка отступов
plt.tight_layout()


plt.savefig('lab1_generated.png', dpi=300, bbox_inches='tight')

# Отображение графика
plt.show()

# Дополнительно: анализ производительности
print("="*60)
print("АНАЛИЗ ВРЕМЕНИ ВЫПОЛНЕНИЯ")
print("="*60)

for i, size in enumerate(matrix_sizes):
    print(f"{size:10s} → {execution_times[i]:>10.1f} мс")

# Анализ роста времени выполнения
print("\n"+"="*60)
print("АНАЛИЗ РОСТА ВРЕМЕНИ ВЫПОЛНЕНИЯ")
print("="*60)

for i in range(1, len(execution_times)):
    ratio = execution_times[i] / execution_times[i-1]
    size_ratio = (x_values[i] / x_values[i-1])**2  # отношение количества элементов
    print(f"{matrix_sizes[i-1]} → {matrix_sizes[i]}:")
    print(f"  Время выросло в {ratio:.2f}x")
    print(f"  Количество элементов выросло в {size_ratio:.2f}x")
    print(f"  Отношение роста времени к росту элементов: {ratio/size_ratio:.2f}x")
    print()

# Аппроксимация сложности алгоритма
print("="*60)
print("АППРОКСИМАЦИЯ СЛОЖНОСТИ АЛГОРИТМА")
print("="*60)

# Логарифмическая аппроксимация: log(T) = a * log(N) + b
log_n = np.log([x**2 for x in x_values])  # N = количество элементов
log_t = np.log(execution_times)

# Линейная регрессия
coeffs = np.polyfit(log_n, log_t, 1)
a, b = coeffs[0], coeffs[1]

print(f"Зависимость: T = {np.exp(b):.2e} * N^{a:.3f}")
print(f"Показатель степени: {a:.3f}")
print(f"Ближайшая сложность: O(N^{a:.2f})")

# Оценка сложности
if a < 1.5:
    complexity = "O(N)"
elif a < 2.5:
    complexity = "O(N²)"
elif a < 3.5:
    complexity = "O(N³)"
else:
    complexity = f"O(N^{a:.1f})"

print(f"Предполагаемая сложность алгоритма: {complexity}")

# Вычисление R² для оценки качества аппроксимации
predicted = np.polyval(coeffs, log_n)
ss_res = np.sum((log_t - predicted) ** 2)
ss_tot = np.sum((log_t - np.mean(log_t)) ** 2)
r_squared = 1 - (ss_res / ss_tot)
print(f"Коэффициент детерминации R²: {r_squared:.4f}")

# Дополнительно: график в логарифмических координатах
plt.figure(figsize=(12, 8))
plt.style.use('seaborn-v0_8-darkgrid')

# Построение графика в логарифмических координатах
n_elements = [x**2 for x in x_values]
plt.loglog(n_elements, execution_times, marker='o', linewidth=2.5, markersize=10,
           color='#2ca02c', markerfacecolor='#d62728', markeredgecolor='#2ca02c',
           markeredgewidth=2, label='Экспериментальные данные')

# Добавление аппроксимирующей линии
n_fit = np.logspace(np.log10(min(n_elements)), np.log10(max(n_elements)), 100)
t_fit = np.exp(b) * n_fit**a
plt.loglog(n_fit, t_fit, '--', linewidth=2, color='#ff7f0e', 
           label=f'Аппроксимация: O(N^{a:.2f})')

plt.xlabel('Количество элементов матрицы (N)', fontsize=13, fontweight='bold')
plt.ylabel('Время выполнения (мс)', fontsize=13, fontweight='bold')
plt.title('Зависимость времени выполнения от количества элементов\n(логарифмические координаты)', 
          fontsize=15, fontweight='bold', pad=20)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
# plt.savefig('lab1_loglog.png', dpi=300, bbox_inches='tight')
plt.show()