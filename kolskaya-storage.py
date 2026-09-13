import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.gridspec as gridspec

# Размеры комнаты (в см)
room_width = 247
room_height = 153
ceiling_height = 222
wall_thickness = 8

# Дверь
door_gap_bottom = 34
door_gap_top = 44
door_width = room_height - door_gap_top - door_gap_bottom  # 75 см
door_leaf = 75
door_thickness = 4

# Петли за внешней стеной
hinge_x = -wall_thickness  # -8
hinge_y = door_gap_bottom  # 34

# Короб труб
box_width = 27
box_height = 18
box_x = room_width - box_width
box_y = room_height - box_height

# Велосипеды
bike_length = 180
bike_width = 88
bike_height = 106
bike_x = room_width - bike_length
bike_y = 0

# Полки
shelf_length = 240
shelf_width = 40
shelf_height = 180
shelf_x = room_width - shelf_length
shelf_y = room_height - shelf_width

# Фигура
fig = plt.figure(figsize=(24, 36))
gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1.2, 1.2], hspace=0.25)

# ============ 2D ПЛАН ============
ax2d = fig.add_subplot(gs[0])

# Внешние стены (серые прямоугольники)
for rect in [
    (-wall_thickness, -wall_thickness, room_width + 2*wall_thickness, wall_thickness),
    (-wall_thickness, room_height, room_width + 2*wall_thickness, wall_thickness),
    (room_width, -wall_thickness, wall_thickness, room_height + 2*wall_thickness),
    (-wall_thickness, -wall_thickness, wall_thickness, door_gap_bottom + wall_thickness),
    (-wall_thickness, door_gap_bottom + door_width, wall_thickness,
     room_height - door_gap_bottom - door_width + wall_thickness),
]:
    ax2d.add_patch(patches.Rectangle(
        (rect[0], rect[1]), rect[2], rect[3],
        linewidth=1, edgecolor='black', facecolor='gray', alpha=0.5))

# Внутренние стены
for seg in [
    ([0, room_width], [0, 0]),
    ([room_width, room_width], [0, room_height]),
    ([room_width, 0], [room_height, room_height]),
    ([0, 0], [0, door_gap_bottom]),
    ([0, 0], [door_gap_bottom + door_width, room_height]),
]:
    ax2d.plot(seg[0], seg[1], 'k-', linewidth=2)

# Проём
ax2d.plot([0, 0], [door_gap_bottom, door_gap_bottom + door_width], 'k--', lw=1, alpha=0.5)

# Дверь ЗАКРЫТА (в плоскости X=-8)
door_closed_rect = patches.Rectangle(
    (hinge_x - door_thickness/2, hinge_y), door_thickness, door_leaf,
    linewidth=2, edgecolor='brown', facecolor='saddlebrown', alpha=0.8,
    label='Дверь (закрыта)')
ax2d.add_patch(door_closed_rect)

# Петли
ax2d.plot(hinge_x, hinge_y, 'ro', markersize=10, label='Петли')

# Дуга открывания
theta = np.linspace(np.pi/2, 0, 50)
arc_x = hinge_x + door_leaf * np.cos(theta)
arc_y = hinge_y + door_leaf * np.sin(theta)
ax2d.plot(arc_x, arc_y, 'b--', linewidth=1.5, alpha=0.6)

# Дверь ОТКРЫТА
door_open_rect = patches.Rectangle(
    (hinge_x, hinge_y - door_thickness/2), door_leaf, door_thickness,
    linewidth=2, edgecolor='brown', facecolor='saddlebrown', alpha=0.4,
    label='Дверь (открыта)')
ax2d.add_patch(door_open_rect)

# Размер 67 см в комнату
ax2d.annotate('', xy=(0, hinge_y - 18), xytext=(hinge_x + door_leaf, hinge_y - 18),
            arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue'))
ax2d.text((hinge_x + door_leaf)/2, hinge_y - 24, '67 см (в комнату)',
        ha='center', va='top', fontsize=10, color='blue', fontweight='bold')

# Велосипеды
ax2d.add_patch(patches.Rectangle(
    (bike_x, bike_y), bike_length, bike_width,
    linewidth=2, edgecolor='darkgray', facecolor='silver', alpha=0.6))
ax2d.text(bike_x + bike_length/2, bike_y + bike_width/2, 'Велосипеды\n180×88×106',
         ha='center', va='center', fontsize=10, color='darkgray', fontweight='bold')

# Полки
ax2d.add_patch(patches.Rectangle(
    (shelf_x, shelf_y), shelf_length, shelf_width,
    linewidth=2, edgecolor='sienna', facecolor='wheat', alpha=0.6))
ax2d.text(shelf_x + shelf_length/2, shelf_y + shelf_width/2, 'Полки\n240×40×180',
         ha='center', va='center', fontsize=10, color='sienna', fontweight='bold')

# Трубы
ax2d.add_patch(patches.Rectangle(
    (box_x, box_y), box_width, box_height,
    linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.7))
ax2d.text(box_x + box_width/2, box_y + box_height/2, 'Трубы\n27×18',
         ha='center', va='center', fontsize=10, color='darkred')

# Размеры
offset = 20
ax2d.annotate('', xy=(0, -offset), xytext=(room_width, -offset),
            arrowprops=dict(arrowstyle='<->', lw=1.5))
ax2d.text(room_width/2, -offset - 10, f'{room_width} см',
        ha='center', va='top', fontsize=12, fontweight='bold')

ax2d.annotate('', xy=(room_width + offset, 0), xytext=(room_width + offset, room_height),
            arrowprops=dict(arrowstyle='<->', lw=1.5))
ax2d.text(room_width + offset + 12, room_height/2, f'{room_height} см',
        ha='left', va='center', fontsize=12, fontweight='bold', rotation=270)

# Размеры двери
for y1, y2, label in [
    (door_gap_bottom + door_width, room_height, f'{door_gap_top} см'),
    (door_gap_bottom, door_gap_bottom + door_width, f'{door_width} см (проём)'),
    (0, door_gap_bottom, f'{door_gap_bottom} см'),
]:
    ax2d.plot([-12, -12], [y1, y2], 'g-', lw=1)
    ax2d.plot([-14, -10], [y1, y1], 'g-', lw=1)
    ax2d.plot([-14, -10], [y2, y2], 'g-', lw=1)
    ax2d.text(-16, (y1+y2)/2, label, ha='right', va='center', fontsize=10, color='green')

# Трубы размеры
ax2d.annotate('', xy=(box_x, room_height+10), xytext=(room_width, room_height+10),
            arrowprops=dict(arrowstyle='<->', lw=1))
ax2d.text((box_x+room_width)/2, room_height+14, f'{box_width}', ha='center', va='bottom', fontsize=10, color='red')

ax2d.annotate('', xy=(room_width+10, box_y), xytext=(room_width+10, room_height),
            arrowprops=dict(arrowstyle='<->', lw=1))
ax2d.text(room_width+14, (box_y+room_height)/2, f'{box_height}', ha='left', va='center', fontsize=10, color='red', rotation=270)

# Толщина стены
ax2d.annotate('', xy=(-wall_thickness, -wall_thickness-8), xytext=(0, -wall_thickness-8),
            arrowprops=dict(arrowstyle='<->', lw=1))
ax2d.text(-wall_thickness/2, -wall_thickness-12, f'{wall_thickness}', ha='center', va='top', fontsize=9, color='gray')

ax2d.set_xlim(-40, room_width + 50)
ax2d.set_ylim(-40, room_height + 30)
ax2d.set_aspect('equal')
ax2d.grid(True, alpha=0.2, linestyle='--')
ax2d.set_xlabel('X (см)', fontsize=11)
ax2d.set_ylabel('Y (см)', fontsize=11)
ax2d.set_title('2D План комнаты (вид сверху)', fontsize=15, fontweight='bold')
ax2d.legend(loc='upper right', fontsize=11)

info = f'Площадь: {room_width*room_height/10000:.2f} м²\n'
info += f'Высота: {ceiling_height} см\n'
info += f'Объём: {room_width*room_height*ceiling_height/1e6:.2f} м³\n'
info += f'Стены: {wall_thickness} см\n'
info += f'Дверь: {door_leaf} см (полотно)'
ax2d.text(room_width-5, 10, info, ha='right', va='bottom', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))


# ============ Вспомогательная функция для 3D ============
def draw_wall(ax, p1, p2, p3, p4, color, alpha=0.4):
    """Рисует стену как простую полупрозрачную плоскость"""
    ax.add_collection3d(Poly3DCollection(
        [[p1, p2, p3, p4]],
        facecolors=color, alpha=alpha, edgecolors='black', linewidth=1))

def draw_room_3d(ax):
    # Пол
    draw_wall(ax, [0,0,0], [room_width,0,0], [room_width,room_height,0], [0,room_height,0],
              'lightgray', 0.3)
    # Потолок
    draw_wall(ax, [0,0,ceiling_height], [room_width,0,ceiling_height],
              [room_width,room_height,ceiling_height], [0,room_height,ceiling_height],
              'white', 0.15)

    # Правая стена (синяя)
    draw_wall(ax, [room_width,0,0], [room_width,room_height,0],
              [room_width,room_height,ceiling_height], [room_width,0,ceiling_height],
              'lightblue', 0.35)

    # Верхняя стена (зелёная)
    draw_wall(ax, [0,room_height,0], [room_width,room_height,0],
              [room_width,room_height,ceiling_height], [0,room_height,ceiling_height],
              'lightgreen', 0.35)

    # Нижняя стена (жёлтая)
    draw_wall(ax, [0,0,0], [room_width,0,0],
              [room_width,0,ceiling_height], [0,0,ceiling_height],
              'lightyellow', 0.35)

    # Левая стена — часть ниже двери (розовая)
    draw_wall(ax, [0,0,0], [0,door_gap_bottom,0],
              [0,door_gap_bottom,ceiling_height], [0,0,ceiling_height],
              'lightpink', 0.4)

    # Левая стена — часть выше двери (розовая)
    draw_wall(ax, [0,door_gap_bottom+door_width,0], [0,room_height,0],
              [0,room_height,ceiling_height], [0,door_gap_bottom+door_width,ceiling_height],
              'lightpink', 0.4)

    # Левая стена — перемычка над дверью (розовая, более прозрачная)
    draw_wall(ax, [0,door_gap_bottom,0], [0,door_gap_bottom+door_width,0],
              [0,door_gap_bottom+door_width,ceiling_height], [0,door_gap_bottom,ceiling_height],
              'lightpink', 0.25)

    # Дверь ЗАКРЫТА (в плоскости X=-8)
    dc = hinge_x - door_thickness/2
    draw_wall(ax, [dc, hinge_y, 0], [dc+door_thickness, hinge_y, 0],
              [dc+door_thickness, hinge_y+door_leaf, ceiling_height],
              [dc, hinge_y+door_leaf, ceiling_height],
              'saddlebrown', 0.75)

    # Дверь ОТКРЫТА (полупрозрачно)
    draw_wall(ax, [hinge_x, hinge_y-door_thickness/2, 0],
              [hinge_x+door_leaf, hinge_y-door_thickness/2, 0],
              [hinge_x+door_leaf, hinge_y-door_thickness/2, ceiling_height],
              [hinge_x, hinge_y-door_thickness/2, ceiling_height],
              'saddlebrown', 0.3)

    # Петли
    ax.scatter([hinge_x], [hinge_y], [ceiling_height/2], color='red', s=80, marker='o')

    # Велосипеды (параллелепипед)
    bf = [
        [[bike_x,bike_y,0],[bike_x+bike_length,bike_y,0],
         [bike_x+bike_length,bike_y+bike_width,0],[bike_x,bike_y+bike_width,0]],
        [[bike_x,bike_y,bike_height],[bike_x+bike_length,bike_y,bike_height],
         [bike_x+bike_length,bike_y+bike_width,bike_height],[bike_x,bike_y+bike_width,bike_height]],
        [[bike_x,bike_y,0],[bike_x+bike_length,bike_y,0],
         [bike_x+bike_length,bike_y,bike_height],[bike_x,bike_y,bike_height]],
        [[bike_x,bike_y+bike_width,0],[bike_x+bike_length,bike_y+bike_width,0],
         [bike_x+bike_length,bike_y+bike_width,bike_height],[bike_x,bike_y+bike_width,bike_height]],
        [[bike_x,bike_y,0],[bike_x,bike_y+bike_width,0],
         [bike_x,bike_y+bike_width,bike_height],[bike_x,bike_y,bike_height]],
        [[bike_x+bike_length,bike_y,0],[bike_x+bike_length,bike_y+bike_width,0],
         [bike_x+bike_length,bike_y+bike_width,bike_height],[bike_x+bike_length,bike_y,bike_height]],
    ]
    ax.add_collection3d(Poly3DCollection(bf, facecolors='silver', alpha=0.6, edgecolors='darkgray', linewidth=1))

    # Полки (параллелепипед)
    sf = [
        [[shelf_x,shelf_y,0],[shelf_x+shelf_length,shelf_y,0],
         [shelf_x+shelf_length,shelf_y+shelf_width,0],[shelf_x,shelf_y+shelf_width,0]],
        [[shelf_x,shelf_y,shelf_height],[shelf_x+shelf_length,shelf_y,shelf_height],
         [shelf_x+shelf_length,shelf_y+shelf_width,shelf_height],[shelf_x,shelf_y+shelf_width,shelf_height]],
        [[shelf_x,shelf_y,0],[shelf_x+shelf_length,shelf_y,0],
         [shelf_x+shelf_length,shelf_y,shelf_height],[shelf_x,shelf_y,shelf_height]],
        [[shelf_x,shelf_y+shelf_width,0],[shelf_x+shelf_length,shelf_y+shelf_width,0],
         [shelf_x+shelf_length,shelf_y+shelf_width,shelf_height],[shelf_x,shelf_y+shelf_width,shelf_height]],
        [[shelf_x,shelf_y,0],[shelf_x,shelf_y+shelf_width,0],
         [shelf_x,shelf_y+shelf_width,shelf_height],[shelf_x,shelf_y,shelf_height]],
        [[shelf_x+shelf_length,shelf_y,0],[shelf_x+shelf_length,shelf_y+shelf_width,0],
         [shelf_x+shelf_length,shelf_y+shelf_width,shelf_height],[shelf_x+shelf_length,shelf_y,shelf_height]],
    ]
    ax.add_collection3d(Poly3DCollection(sf, facecolors='wheat', alpha=0.6, edgecolors='sienna', linewidth=1))

    # Трубы (параллелепипед)
    pv = [
        [box_x,box_y,0],[box_x+box_width,box_y,0],
        [box_x+box_width,box_y+box_height,0],[box_x,box_y+box_height,0],
        [box_x,box_y,ceiling_height],[box_x+box_width,box_y,ceiling_height],
        [box_x+box_width,box_y+box_height,ceiling_height],[box_x,box_y+box_height,ceiling_height]
    ]
    pf = [
        [pv[0],pv[1],pv[2],pv[3]],[pv[4],pv[5],pv[6],pv[7]],
        [pv[0],pv[1],pv[5],pv[4]],[pv[2],pv[3],pv[7],pv[6]],
        [pv[0],pv[3],pv[7],pv[4]],[pv[1],pv[2],pv[6],pv[5]]
    ]
    ax.add_collection3d(Poly3DCollection(pf, facecolors='red', alpha=0.5, edgecolors='darkred', linewidth=2))

    # Подписи
    ax.text(bike_x+bike_length/2, bike_y+bike_width/2, bike_height+8, 'Велосипеды',
            ha='center', va='center', fontsize=10, color='darkgray')
    ax.text(shelf_x+shelf_length/2, shelf_y+shelf_width/2, shelf_height+8, 'Полки',
            ha='center', va='center', fontsize=10, color='sienna')
    ax.text(box_x+box_width/2, box_y+box_height/2, ceiling_height/2, 'Трубы',
            ha='center', va='center', fontsize=10, color='red')

    ax.set_xlim(-wall_thickness, room_width + wall_thickness)
    ax.set_ylim(-wall_thickness, room_height + wall_thickness)
    ax.set_zlim(0, ceiling_height)
    ax.set_xlabel('X (см)')
    ax.set_ylabel('Y (см)')
    ax.set_zlabel('Z (см)')


# ============ 3D ОБЩИЙ ВИД ============
ax3d_1 = fig.add_subplot(gs[1], projection='3d')
draw_room_3d(ax3d_1)
ax3d_1.view_init(elev=25, azim=-50)
ax3d_1.set_title('3D Проекция — общий вид', fontsize=15, fontweight='bold', pad=20)

# ============ 3D ВИД СО СТОРОНЫ ДВЕРИ ============
ax3d_2 = fig.add_subplot(gs[2], projection='3d')
draw_room_3d(ax3d_2)
ax3d_2.view_init(elev=15, azim=160)
ax3d_2.set_title('3D Проекция — вид со стороны двери', fontsize=15, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('room_plan_final_v5.png', dpi=150, bbox_inches='tight')
print("Сохранено: room_plan_final_v5.png")
plt.show()