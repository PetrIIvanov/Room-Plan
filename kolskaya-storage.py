import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Размеры комнаты (в см)
room_width = 247   # X
room_height = 153  # Y
ceiling_height = 222  # Z

# Дверь на левой стене
door_gap_bottom = 34
door_gap_top = 44
door_width = room_height - door_gap_top - door_gap_bottom  # 75 см
door_leaf = 67

# Короб труб в правом верхнем углу
box_width = 27   # вдоль стены 247
box_height = 18  # вдоль стены 153
box_x = room_width - box_width
box_y = room_height - box_height

# Создание фигуры с двумя проекциями
fig = plt.figure(figsize=(16, 14))

# ============ 2D ПЛАН (сверху) ============
ax2d = fig.add_subplot(211)

# Стены комнаты
wall_thickness = 2
ax2d.plot([0, room_width], [0, 0], 'k-', linewidth=wall_thickness)
ax2d.plot([room_width, room_width], [0, room_height], 'k-', linewidth=wall_thickness)
ax2d.plot([room_width, 0], [room_height, room_height], 'k-', linewidth=wall_thickness)
ax2d.plot([0, 0], [0, door_gap_bottom], 'k-', linewidth=wall_thickness)
ax2d.plot([0, 0], [door_gap_bottom + door_width, room_height], 'k-', linewidth=wall_thickness)

# Дверной проём
ax2d.plot([0, 0], [door_gap_bottom, door_gap_bottom + door_width], 'k--', linewidth=1, alpha=0.5)

# Полотно двери
ax2d.plot([0, 0], [door_gap_bottom, door_gap_bottom + door_width], 'b-', linewidth=4, label='Дверь (закрыта)')

# Дуга открывания
theta = np.linspace(np.pi/2, 0, 50)
arc_x = door_leaf * np.cos(theta)
arc_y = door_gap_bottom + door_leaf * np.sin(theta)
ax2d.plot(arc_x, arc_y, 'b--', linewidth=1.5, alpha=0.6)
ax2d.plot([0, door_leaf], [door_gap_bottom, door_gap_bottom], 'b-', linewidth=2, alpha=0.5, label='Дверь (открыта)')
ax2d.plot(0, door_gap_bottom, 'ro', markersize=8, label='Петли')

# Короб труб
box = patches.Rectangle((box_x, box_y), box_width, box_height, 
                        linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.7)
ax2d.add_patch(box)
ax2d.text(box_x + box_width/2, box_y + box_height/2, 'Трубы\n27×18', 
        ha='center', va='center', fontsize=9, color='darkred')

# Размерные линии
offset = 15
ax2d.annotate('', xy=(0, -offset), xytext=(room_width, -offset),
            arrowprops=dict(arrowstyle='<->', lw=1.5))
ax2d.text(room_width/2, -offset - 8, f'{room_width} см', 
        ha='center', va='top', fontsize=11, fontweight='bold')

ax2d.annotate('', xy=(room_width + offset, 0), xytext=(room_width + offset, room_height),
            arrowprops=dict(arrowstyle='<->', lw=1.5))
ax2d.text(room_width + offset + 10, room_height/2, f'{room_height} см', 
        ha='left', va='center', fontsize=11, fontweight='bold', rotation=270)

# Размеры двери
ax2d.plot([-8, -8], [room_height, door_gap_bottom + door_width], 'g-', linewidth=1)
ax2d.plot([-10, -6], [room_height, room_height], 'g-', linewidth=1)
ax2d.plot([-10, -6], [door_gap_bottom + door_width, door_gap_bottom + door_width], 'g-', linewidth=1)
ax2d.text(-12, (room_height + door_gap_bottom + door_width)/2, f'{door_gap_top} см', 
        ha='right', va='center', fontsize=9, color='green')

ax2d.plot([-8, -8], [door_gap_bottom, door_gap_bottom + door_width], 'g-', linewidth=1)
ax2d.plot([-10, -6], [door_gap_bottom, door_gap_bottom], 'g-', linewidth=1)
ax2d.text(-12, door_gap_bottom + door_width/2, f'{door_width} см\n(проём)', 
        ha='right', va='center', fontsize=9, color='green')

ax2d.plot([-8, -8], [0, door_gap_bottom], 'g-', linewidth=1)
ax2d.plot([-10, -6], [0, 0], 'g-', linewidth=1)
ax2d.text(-12, door_gap_bottom/2, f'{door_gap_bottom} см', 
        ha='right', va='center', fontsize=9, color='green')

# Размеры короба
ax2d.annotate('', xy=(box_x, room_height + 8), xytext=(room_width, room_height + 8),
            arrowprops=dict(arrowstyle='<->', lw=1))
ax2d.text((box_x + room_width)/2, room_height + 12, f'{box_width} см', 
        ha='center', va='bottom', fontsize=9, color='red')

ax2d.annotate('', xy=(room_width + 8, box_y), xytext=(room_width + 8, room_height),
            arrowprops=dict(arrowstyle='<->', lw=1))
ax2d.text(room_width + 12, (box_y + room_height)/2, f'{box_height} см', 
        ha='left', va='center', fontsize=9, color='red', rotation=270)

ax2d.set_xlim(-30, room_width + 40)
ax2d.set_ylim(-30, room_height + 25)
ax2d.set_aspect('equal')
ax2d.grid(True, alpha=0.2, linestyle='--')
ax2d.set_xlabel('X (см)', fontsize=10)
ax2d.set_ylabel('Y (см)', fontsize=10)
ax2d.set_title('2D План комнаты (вид сверху)', fontsize=13, fontweight='bold')
ax2d.legend(loc='upper right', fontsize=10)

info_text = f'Площадь: {room_width * room_height / 10000:.2f} м²\n'
info_text += f'Высота: {ceiling_height} см\n'
info_text += f'Объём: {room_width * room_height * ceiling_height / 1000000:.2f} м³'
ax2d.text(room_width - 5, 10, info_text, 
        ha='right', va='bottom', fontsize=9, 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# ============ 3D ПРОЕКЦИЯ (снизу) ============
ax3d = fig.add_subplot(212, projection='3d')

# Пол
floor = [[0, 0, 0], [room_width, 0, 0], [room_width, room_height, 0], [0, room_height, 0]]
ax3d.add_collection3d(Poly3DCollection([floor], facecolors='lightgray', alpha=0.3, edgecolors='black', linewidth=1))

# Потолок
ceiling = [[0, 0, ceiling_height], [room_width, 0, ceiling_height], 
           [room_width, room_height, ceiling_height], [0, room_height, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([ceiling], facecolors='white', alpha=0.2, edgecolors='black', linewidth=1))

# Правая стена (сплошная)
right_wall = [[room_width, 0, 0], [room_width, room_height, 0], 
              [room_width, room_height, ceiling_height], [room_width, 0, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([right_wall], facecolors='lightblue', alpha=0.4, edgecolors='black', linewidth=1))

# Верхняя стена (сплошная)
top_wall = [[0, room_height, 0], [room_width, room_height, 0], 
            [room_width, room_height, ceiling_height], [0, room_height, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([top_wall], facecolors='lightgreen', alpha=0.4, edgecolors='black', linewidth=1))

# Нижняя стена (сплошная)
bottom_wall = [[0, 0, 0], [room_width, 0, 0], 
               [room_width, 0, ceiling_height], [0, 0, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([bottom_wall], facecolors='lightyellow', alpha=0.4, edgecolors='black', linewidth=1))

# Левая стена с дверным проёмом (две части)
# Часть 1: от пола до низа двери
left_wall_bottom = [[0, 0, 0], [0, door_gap_bottom, 0], 
                    [0, door_gap_bottom, ceiling_height], [0, 0, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([left_wall_bottom], facecolors='lightpink', alpha=0.4, edgecolors='black', linewidth=1))

# Часть 2: от верха двери до потолка
left_wall_top = [[0, door_gap_bottom + door_width, 0], [0, room_height, 0], 
                 [0, room_height, ceiling_height], [0, door_gap_bottom + door_width, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([left_wall_top], facecolors='lightpink', alpha=0.4, edgecolors='black', linewidth=1))

# Часть 3: над дверью
left_wall_above_door = [[0, door_gap_bottom, 0], [0, door_gap_bottom + door_width, 0], 
                        [0, door_gap_bottom + door_width, ceiling_height], [0, door_gap_bottom, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([left_wall_above_door], facecolors='lightpink', alpha=0.3, edgecolors='black', linewidth=1))

# Дверь в открытом состоянии (повёрнута на 90°)
door_open = [[0, door_gap_bottom, 0], [door_leaf, door_gap_bottom, 0], 
             [door_leaf, door_gap_bottom, ceiling_height], [0, door_gap_bottom, ceiling_height]]
ax3d.add_collection3d(Poly3DCollection([door_open], facecolors='brown', alpha=0.6, edgecolors='black', linewidth=2))

# Короб труб
pipe_box = [
    [box_x, box_y, 0], [box_x + box_width, box_y, 0], 
    [box_x + box_width, box_y + box_height, 0], [box_x, box_y + box_height, 0],
    [box_x, box_y, ceiling_height], [box_x + box_width, box_y, ceiling_height],
    [box_x + box_width, box_y + box_height, ceiling_height], [box_x, box_y + box_height, ceiling_height]
]
pipe_faces = [
    [pipe_box[0], pipe_box[1], pipe_box[2], pipe_box[3]],  # низ
    [pipe_box[4], pipe_box[5], pipe_box[6], pipe_box[7]],  # верх
    [pipe_box[0], pipe_box[1], pipe_box[5], pipe_box[4]],  # перед
    [pipe_box[2], pipe_box[3], pipe_box[7], pipe_box[6]],  # зад
    [pipe_box[0], pipe_box[3], pipe_box[7], pipe_box[4]],  # лево
    [pipe_box[1], pipe_box[2], pipe_box[6], pipe_box[5]]   # право
]
ax3d.add_collection3d(Poly3DCollection(pipe_faces, facecolors='red', alpha=0.5, edgecolors='darkred', linewidth=2))

# Подписи в 3D
ax3d.text(room_width/2, room_height/2, -10, f'{room_width}×{room_height} см', 
         ha='center', va='center', fontsize=10, color='blue')
ax3d.text(room_width/2, -10, ceiling_height/2, f'Высота: {ceiling_height} см', 
         ha='center', va='center', fontsize=10, color='green', rotation=90)
ax3d.text(box_x + box_width/2, box_y + box_height/2, ceiling_height/2, 'Трубы', 
         ha='center', va='center', fontsize=9, color='red')

# Настройки 3D вида
ax3d.set_xlim(0, room_width)
ax3d.set_ylim(0, room_height)
ax3d.set_zlim(0, ceiling_height)
ax3d.set_xlabel('X (см)')
ax3d.set_ylabel('Y (см)')
ax3d.set_zlabel('Z (см)')
ax3d.set_title('3D Проекция комнаты (вид изнутри)', fontsize=13, fontweight='bold', pad=20)

# Ракурс камеры
ax3d.view_init(elev=25, azim=-50)

plt.tight_layout()
plt.savefig('room_plan_2d_3d.png', dpi=150, bbox_inches='tight')
print("План комнаты (2D + 3D) сохранён в файл 'room_plan_2d_3d.png'")
plt.show()