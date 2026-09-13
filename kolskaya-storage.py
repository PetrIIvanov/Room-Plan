import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Размеры комнаты (в см)
room_width = 247   # по горизонтали (X)
room_height = 153  # по вертикали (Y)

# Дверь на левой стене
door_gap_top = 44      # от верха стены до верха проёма
door_gap_bottom = 34   # от низа стены до низа проёма
door_width = room_height - door_gap_top - door_gap_bottom  # 75 см
door_leaf = 67         # ширина полотна двери

# Короб труб в левом верхнем углу
box_x = 18   # выступает в комнату
box_y = 27   # вдоль стены

# Создание фигуры
fig, ax = plt.subplots(figsize=(12, 8))

# Рисуем стены комнаты (толстые линии)
wall_thickness = 2

# Нижняя стена
ax.plot([0, room_width], [0, 0], 'k-', linewidth=wall_thickness)
# Правая стена
ax.plot([room_width, room_width], [0, room_height], 'k-', linewidth=wall_thickness)
# Верхняя стена
ax.plot([room_width, 0], [room_height, room_height], 'k-', linewidth=wall_thickness)
# Левая стена (с проёмом для двери)
ax.plot([0, 0], [0, door_gap_bottom], 'k-', linewidth=wall_thickness)
ax.plot([0, 0], [door_gap_bottom + door_width, room_height], 'k-', linewidth=wall_thickness)

# Дверной проём (пунктир показывает границы)
ax.plot([0, 0], [door_gap_bottom, door_gap_bottom + door_width], 'k--', linewidth=1, alpha=0.5)

# Полотно двери в закрытом состоянии
ax.plot([0, door_leaf], [door_gap_bottom + door_width, door_gap_bottom + door_width], 
        'b-', linewidth=3, label='Дверь (закрыта)')

# Дуга открывания двери
theta = np.linspace(0, np.pi/2, 50)
arc_x = door_leaf * np.cos(theta)
arc_y = door_gap_bottom + door_width - door_leaf * np.sin(theta)
ax.plot(arc_x, arc_y, 'b--', linewidth=1, alpha=0.6)

# Короб труб в левом верхнем углу
box = patches.Rectangle((0, room_height - box_y), box_x, box_y, 
                        linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.7)
ax.add_patch(box)
ax.text(box_x/2, room_height - box_y/2, 'Трубы\n27×18', 
        ha='center', va='center', fontsize=9, color='darkred')

# Размерные линии
offset = 15  # отступ для размерных линий

# Ширина комнаты (внизу)
ax.annotate('', xy=(0, -offset), xytext=(room_width, -offset),
            arrowprops=dict(arrowstyle='<->', lw=1.5))
ax.text(room_width/2, -offset - 8, f'{room_width} см', 
        ha='center', va='top', fontsize=11, fontweight='bold')

# Высота комнаты (справа)
ax.annotate('', xy=(room_width + offset, 0), xytext=(room_width + offset, room_height),
            arrowprops=dict(arrowstyle='<->', lw=1.5))
ax.text(room_width + offset + 10, room_height/2, f'{room_height} см', 
        ha='left', va='center', fontsize=11, fontweight='bold', rotation=270)

# Размеры двери
# От верха до двери
ax.plot([-8, -8], [room_height, door_gap_bottom + door_width], 'g-', linewidth=1)
ax.plot([-10, -6], [room_height, room_height], 'g-', linewidth=1)
ax.plot([-10, -6], [door_gap_bottom + door_width, door_gap_bottom + door_width], 'g-', linewidth=1)
ax.text(-12, (room_height + door_gap_bottom + door_width)/2, f'{door_gap_top} см', 
        ha='right', va='center', fontsize=9, color='green')

# Ширина проёма
ax.plot([-8, -8], [door_gap_bottom, door_gap_bottom + door_width], 'g-', linewidth=1)
ax.plot([-10, -6], [door_gap_bottom, door_gap_bottom], 'g-', linewidth=1)
ax.text(-12, door_gap_bottom + door_width/2, f'{door_width} см\n(проём)', 
        ha='right', va='center', fontsize=9, color='green')

# От низа до двери
ax.plot([-8, -8], [0, door_gap_bottom], 'g-', linewidth=1)
ax.plot([-10, -6], [0, 0], 'g-', linewidth=1)
ax.text(-12, door_gap_bottom/2, f'{door_gap_bottom} см', 
        ha='right', va='center', fontsize=9, color='green')

# Настройки графика
ax.set_xlim(-30, room_width + 40)
ax.set_ylim(-30, room_height + 20)
ax.set_aspect('equal')
ax.grid(True, alpha=0.2, linestyle='--')
ax.set_xlabel('X (см)', fontsize=10)
ax.set_ylabel('Y (см)', fontsize=10)
ax.set_title('План комнаты 247×153 см\nВысота потолка: 222 см', 
             fontsize=14, fontweight='bold', pad=20)

# Легенда
ax.legend(loc='upper right', fontsize=10)

# Добавляем информацию в правом нижнем углу
info_text = f'Площадь: {room_width * room_height / 10000:.2f} м²\n'
info_text += f'Дверь: {door_width} см (проём)\n'
info_text += f'Полотно: {door_leaf} см\n'
info_text += f'До противоп. стены: {room_width - door_leaf} см'
ax.text(room_width - 5, 10, info_text, 
        ha='right', va='bottom', fontsize=9, 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('room_plan.png', dpi=150, bbox_inches='tight')
print("План комнаты сохранён в файл 'room_plan.png'")
plt.show()