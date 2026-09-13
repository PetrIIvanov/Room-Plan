import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.gridspec as gridspec
import os

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

# Создаём папку для результатов
os.makedirs('room_plan', exist_ok=True)

# ============ ФУНКЦИЯ РИСОВАНИЯ 2D ============
def draw_2d_plan(ax):
    # Внешние стены (серые прямоугольники)
    for rect in [
        (-wall_thickness, -wall_thickness, room_width + 2*wall_thickness, wall_thickness),
        (-wall_thickness, room_height, room_width + 2*wall_thickness, wall_thickness),
        (room_width, -wall_thickness, wall_thickness, room_height + 2*wall_thickness),
        (-wall_thickness, -wall_thickness, wall_thickness, door_gap_bottom + wall_thickness),
        (-wall_thickness, door_gap_bottom + door_width, wall_thickness,
         room_height - door_gap_bottom - door_width + wall_thickness),
    ]:
        ax.add_patch(patches.Rectangle(
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
        ax.plot(seg[0], seg[1], 'k-', linewidth=2)

    # Проём
    ax.plot([0, 0], [door_gap_bottom, door_gap_bottom + door_width], 'k--', lw=1, alpha=0.5)

    # Дверь ЗАКРЫТА
    door_closed_rect = patches.Rectangle(
        (hinge_x - door_thickness/2, hinge_y), door_thickness, door_leaf,
        linewidth=2, edgecolor='brown', facecolor='saddlebrown', alpha=0.8,
        label='Дверь (закрыта)')
    ax.add_patch(door_closed_rect)

    # Петли
    ax.plot(hinge_x, hinge_y, 'ro', markersize=10, label='Петли')

    # Дуга открывания
    theta = np.linspace(np.pi/2, 0, 50)
    arc_x = hinge_x + door_leaf * np.cos(theta)
    arc_y = hinge_y + door_leaf * np.sin(theta)
    ax.plot(arc_x, arc_y, 'b--', linewidth=1.5, alpha=0.6)

    # Дверь ОТКРЫТА
    door_open_rect = patches.Rectangle(
        (hinge_x, hinge_y - door_thickness/2), door_leaf, door_thickness,
        linewidth=2, edgecolor='brown', facecolor='saddlebrown', alpha=0.4,
        label='Дверь (открыта)')
    ax.add_patch(door_open_rect)

    # Размер 67 см
    ax.annotate('', xy=(0, hinge_y - 18), xytext=(hinge_x + door_leaf, hinge_y - 18),
                arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue'))
    ax.text((hinge_x + door_leaf)/2, hinge_y - 24, '67 см (в комнату)',
            ha='center', va='top', fontsize=10, color='blue', fontweight='bold')

    # Велосипеды
    ax.add_patch(patches.Rectangle(
        (bike_x, bike_y), bike_length, bike_width,
        linewidth=2, edgecolor='darkgray', facecolor='silver', alpha=0.6))
    ax.text(bike_x + bike_length/2, bike_y + bike_width/2, 'Велосипеды\n180×88×106',
             ha='center', va='center', fontsize=10, color='darkgray', fontweight='bold')

    # Полки
    ax.add_patch(patches.Rectangle(
        (shelf_x, shelf_y), shelf_length, shelf_width,
        linewidth=2, edgecolor='sienna', facecolor='wheat', alpha=0.6))
    ax.text(shelf_x + shelf_length/2, shelf_y + shelf_width/2, 'Полки\n240×40×180',
             ha='center', va='center', fontsize=10, color='sienna', fontweight='bold')

    # Трубы
    ax.add_patch(patches.Rectangle(
        (box_x, box_y), box_width, box_height,
        linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.7))
    ax.text(box_x + box_width/2, box_y + box_height/2, 'Трубы\n27×18',
             ha='center', va='center', fontsize=10, color='darkred')

    # Размеры
    offset = 20
    ax.annotate('', xy=(0, -offset), xytext=(room_width, -offset),
                arrowprops=dict(arrowstyle='<->', lw=1.5))
    ax.text(room_width/2, -offset - 10, f'{room_width} см',
            ha='center', va='top', fontsize=12, fontweight='bold')

    ax.annotate('', xy=(room_width + offset, 0), xytext=(room_width + offset, room_height),
                arrowprops=dict(arrowstyle='<->', lw=1.5))
    ax.text(room_width + offset + 12, room_height/2, f'{room_height} см',
            ha='left', va='center', fontsize=12, fontweight='bold', rotation=270)

    for y1, y2, label in [
        (door_gap_bottom + door_width, room_height, f'{door_gap_top} см'),
        (door_gap_bottom, door_gap_bottom + door_width, f'{door_width} см (проём)'),
        (0, door_gap_bottom, f'{door_gap_bottom} см'),
    ]:
        ax.plot([-12, -12], [y1, y2], 'g-', lw=1)
        ax.plot([-14, -10], [y1, y1], 'g-', lw=1)
        ax.plot([-14, -10], [y2, y2], 'g-', lw=1)
        ax.text(-16, (y1+y2)/2, label, ha='right', va='center', fontsize=10, color='green')

    ax.set_xlim(-40, room_width + 50)
    ax.set_ylim(-40, room_height + 30)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.set_xlabel('X (см)', fontsize=11)
    ax.set_ylabel('Y (см)', fontsize=11)
    ax.set_title('2D План комнаты (вид сверху)', fontsize=15, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11)

    info = f'Площадь: {room_width*room_height/10000:.2f} м²\n'
    info += f'Высота: {ceiling_height} см\n'
    info += f'Объём: {room_width*room_height*ceiling_height/1e6:.2f} м³\n'
    info += f'Стены: {wall_thickness} см\n'
    info += f'Дверь: {door_leaf} см (полотно)'
    ax.text(room_width-5, 10, info, ha='right', va='bottom', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# ============ ФУНКЦИЯ РИСОВАНИЯ 3D ============
def draw_3d_view(ax, elev, azim, title):
    # Пол
    ax.add_collection3d(Poly3DCollection(
        [[[0,0,0],[room_width,0,0],[room_width,room_height,0],[0,room_height,0]]],
        facecolors='lightgray', alpha=0.3, edgecolors='black', linewidth=1))
    # Потолок
    ax.add_collection3d(Poly3DCollection(
        [[[0,0,ceiling_height],[room_width,0,ceiling_height],
          [room_width,room_height,ceiling_height],[0,room_height,ceiling_height]]],
        facecolors='white', alpha=0.15, edgecolors='black', linewidth=1))

    # Правая стена
    ax.add_collection3d(Poly3DCollection(
        [[[room_width,0,0],[room_width,room_height,0],
          [room_width,room_height,ceiling_height],[room_width,0,ceiling_height]]],
        facecolors='lightblue', alpha=0.35, edgecolors='black', linewidth=1))

    # Верхняя стена
    ax.add_collection3d(Poly3DCollection(
        [[[0,room_height,0],[room_width,room_height,0],
          [room_width,room_height,ceiling_height],[0,room_height,ceiling_height]]],
        facecolors='lightgreen', alpha=0.35, edgecolors='black', linewidth=1))

    # Нижняя стена
    ax.add_collection3d(Poly3DCollection(
        [[[0,0,0],[room_width,0,0],
          [room_width,0,ceiling_height],[0,0,ceiling_height]]],
        facecolors='lightyellow', alpha=0.35, edgecolors='black', linewidth=1))

    # Левая стена — часть ниже двери
    ax.add_collection3d(Poly3DCollection(
        [[[0,0,0],[0,door_gap_bottom,0],
          [0,door_gap_bottom,ceiling_height],[0,0,ceiling_height]]],
        facecolors='lightpink', alpha=0.4, edgecolors='black', linewidth=1))

    # Левая стена — часть выше двери
    ax.add_collection3d(Poly3DCollection(
        [[[0,door_gap_bottom+door_width,0],[0,room_height,0],
          [0,room_height,ceiling_height],[0,door_gap_bottom+door_width,ceiling_height]]],
        facecolors='lightpink', alpha=0.4, edgecolors='black', linewidth=1))

    # Левая стена — перемычка над дверью
    ax.add_collection3d(Poly3DCollection(
        [[[0,door_gap_bottom,0],[0,door_gap_bottom+door_width,0],
          [0,door_gap_bottom+door_width,ceiling_height],[0,door_gap_bottom,ceiling_height]]],
        facecolors='lightpink', alpha=0.25, edgecolors='black', linewidth=1))

    # Дверь ЗАКРЫТА
    dc = hinge_x - door_thickness/2
    ax.add_collection3d(Poly3DCollection(
        [[[dc, hinge_y, 0], [dc+door_thickness, hinge_y, 0],
          [dc+door_thickness, hinge_y+door_leaf, ceiling_height],
          [dc, hinge_y+door_leaf, ceiling_height]]],
        facecolors='saddlebrown', alpha=0.75, edgecolors='black', linewidth=2))

    # Дверь ОТКРЫТА
    ax.add_collection3d(Poly3DCollection(
        [[[hinge_x, hinge_y-door_thickness/2, 0],
          [hinge_x+door_leaf, hinge_y-door_thickness/2, 0],
          [hinge_x+door_leaf, hinge_y-door_thickness/2, ceiling_height],
          [hinge_x, hinge_y-door_thickness/2, ceiling_height]]],
        facecolors='saddlebrown', alpha=0.3, edgecolors='black', linewidth=1))

    # Петли
    ax.scatter([hinge_x], [hinge_y], [ceiling_height/2], color='red', s=80, marker='o')

    # Велосипеды
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

    # Полки
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

    # Трубы
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
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title, fontsize=15, fontweight='bold', pad=20)

# ============ СОЗДАНИЕ ВСЕХ ИЗОБРАЖЕНИЙ ============
print("Генерация изображений...")

# 2D план
fig, ax = plt.subplots(figsize=(16, 12))
draw_2d_plan(ax)
plt.tight_layout()
plt.savefig('room_plan/2d_plan.png', dpi=150, bbox_inches='tight')
plt.close()
print("Сохранено: room_plan/2d_plan.png")

# 3D общий вид
fig = plt.figure(figsize=(16, 14))
ax = fig.add_subplot(111, projection='3d')
draw_3d_view(ax, 25, -50, '3D Проекция — общий вид')
plt.tight_layout()
plt.savefig('room_plan/3d_general.png', dpi=150, bbox_inches='tight')
plt.close()
print("Сохранено: room_plan/3d_general.png")

# 3D вид от двери
fig = plt.figure(figsize=(16, 14))
ax = fig.add_subplot(111, projection='3d')
draw_3d_view(ax, 15, 160, '3D Проекция — вид со стороны двери')
plt.tight_layout()
plt.savefig('room_plan/3d_door_view.png', dpi=150, bbox_inches='tight')
plt.close()
print("Сохранено: room_plan/3d_door_view.png")

# Общая картинка
fig = plt.figure(figsize=(24, 36))
gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1.2, 1.2], hspace=0.25)

ax2d = fig.add_subplot(gs[0])
draw_2d_plan(ax2d)

ax3d_1 = fig.add_subplot(gs[1], projection='3d')
draw_3d_view(ax3d_1, 25, -50, '3D Проекция — общий вид')

ax3d_2 = fig.add_subplot(gs[2], projection='3d')
draw_3d_view(ax3d_2, 15, 160, '3D Проекция — вид со стороны двери')

plt.savefig('room_plan/combined.png', dpi=150, bbox_inches='tight')
plt.close()
print("Сохранено: room_plan/combined.png")

# ============ ГЕНЕРАЦИЯ HTML С ИСПРАВЛЕННЫМИ КООРДИНАТАМИ ============
html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>План комнаты - Интерактивная 3D модель</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f0f0f0;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .images {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .image-box {
            text-align: center;
            padding: 10px;
            background: #fafafa;
            border-radius: 4px;
        }
        .image-box img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .image-box img:hover {
            transform: scale(1.02);
        }
        #canvas-container {
            width: 100%;
            height: 700px;
            border: 2px solid #333;
            border-radius: 4px;
            margin: 20px 0;
        }
        .info {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .controls-info {
            background: #fff3cd;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        
        /* Lightbox стили */
        .lightbox {
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            cursor: pointer;
        }
        .lightbox-content {
            margin: auto;
            display: block;
            max-width: 95%;
            max-height: 95%;
            object-fit: contain;
        }
        .lightbox-close {
            position: absolute;
            top: 20px;
            right: 40px;
            color: #fff;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            z-index: 10000;
        }
        .lightbox-close:hover {
            color: #bbb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 План комнаты</h1>
        
        <div class="info">
            <h3>Характеристики помещения:</h3>
            <ul>
                <li>Размеры: """ + str(room_width) + """ × """ + str(room_height) + """ см</li>
                <li>Высота потолка: """ + str(ceiling_height) + """ см</li>
                <li>Площадь: """ + f"{room_width*room_height/10000:.2f}" + """ м²</li>
                <li>Объём: """ + f"{room_width*room_height*ceiling_height/1e6:.2f}" + """ м³</li>
                <li>Толщина стен: """ + str(wall_thickness) + """ см</li>
                <li>Дверь: """ + str(door_width) + """ см (проём), """ + str(door_leaf) + """ см (полотно)</li>
            </ul>
        </div>

        <h2>📐 Статичные изображения (кликните для увеличения)</h2>
        <div class="images">
            <div class="image-box">
                <img src="2d_plan.png" alt="2D План" onclick="openLightbox(this.src)">
                <p><strong>2D План (вид сверху)</strong></p>
            </div>
            <div class="image-box">
                <img src="3d_general.png" alt="3D Общий вид" onclick="openLightbox(this.src)">
                <p><strong>3D Общий вид</strong></p>
            </div>
            <div class="image-box">
                <img src="3d_door_view.png" alt="3D Вид от двери" onclick="openLightbox(this.src)">
                <p><strong>3D Вид со стороны двери</strong></p>
            </div>
        </div>

        <h2> Интерактивная 3D модель</h2>
        <div class="controls-info">
            <strong>Управление:</strong><br>
            🖱️ <b>Левая кнопка мыши</b> — вращение камеры<br>
            🖱️ <b>Правая кнопка мыши</b> — перемещение<br>
            🖱️ <b>Колёсико</b> — приближение/удаление
        </div>
        <div id="canvas-container"></div>

        <h2> Общая схема (кликните для увеличения)</h2>
        <div class="image-box">
            <img src="combined.png" alt="Общая схема" style="max-width: 100%;" onclick="openLightbox(this.src)">
        </div>
    </div>

    <!-- Lightbox -->
    <div id="lightbox" class="lightbox" onclick="closeLightbox()">
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" id="lightbox-img">
    </div>

    <script>
        // Lightbox функции
        function openLightbox(src) {
            document.getElementById('lightbox').style.display = 'block';
            document.getElementById('lightbox-img').src = src;
        }

        function closeLightbox() {
            document.getElementById('lightbox').style.display = 'none';
        }

        // Закрытие по Escape
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeLightbox();
            }
        });

        // Инициализация Three.js
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf5f5f5);

        const camera = new THREE.PerspectiveCamera(
            60,
            container.clientWidth / container.clientHeight,
            0.1,
            10000
        );
        camera.position.set(400, 300, 400);
        camera.lookAt(100, 100, 75);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        // Контролы
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Освещение
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(200, 300, 200);
        directionalLight.castShadow = true;
        scene.add(directionalLight);

        // Материалы
        const materials = {
            floor: new THREE.MeshLambertMaterial({ color: 0xd3d3d3, transparent: true, opacity: 0.5 }),
            ceiling: new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.3 }),
            rightWall: new THREE.MeshLambertMaterial({ color: 0xadd8e6, transparent: true, opacity: 0.5 }),
            topWall: new THREE.MeshLambertMaterial({ color: 0x90ee90, transparent: true, opacity: 0.5 }),
            bottomWall: new THREE.MeshLambertMaterial({ color: 0xffffe0, transparent: true, opacity: 0.5 }),
            leftWall: new THREE.MeshLambertMaterial({ color: 0xffb6c1, transparent: true, opacity: 0.5 }),
            door: new THREE.MeshLambertMaterial({ color: 0x8b4513, transparent: true, opacity: 0.8 }),
            doorOpen: new THREE.MeshLambertMaterial({ color: 0x8b4513, transparent: true, opacity: 0.4 }),
            bikes: new THREE.MeshLambertMaterial({ color: 0xc0c0c0, transparent: true, opacity: 0.7 }),
            shelves: new THREE.MeshLambertMaterial({ color: 0xf5deb3, transparent: true, opacity: 0.7 }),
            pipes: new THREE.MeshLambertMaterial({ color: 0xff6347, transparent: true, opacity: 0.6 }),
        };

        // ФУНКЦИЯ СОЗДАНИЯ КОРОБКИ С ИНВЕРСИЕЙ Z
        // Matplotlib Y → Three.js Z (инвертировано: Z = room_height - Y)
        function createBox(x, y_mpl, z_mpl, w, h, d, material) {
            const geometry = new THREE.BoxGeometry(w, h, d);
            const mesh = new THREE.Mesh(geometry, material);
            const z_three = """ + str(room_height) + """ - z_mpl - d;  // Инверсия Z
            mesh.position.set(x + w/2, y_mpl + h/2, z_three + d/2);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            return mesh;
        }

        // Пол (Y=0, Z=0 в matplotlib)
        scene.add(createBox(0, 0, 0, """ + str(room_width) + """, 0.1, """ + str(room_height) + """, materials.floor));

        // Потолок (Y=222, Z=0 в matplotlib)
        scene.add(createBox(0, """ + str(ceiling_height) + """, 0, """ + str(room_width) + """, 0.1, """ + str(room_height) + """, materials.ceiling));

        // Правая стена (X=247, Y=0-222, Z=0-153)
        scene.add(createBox(""" + str(room_width) + """, 0, 0, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, """ + str(room_height) + """, materials.rightWall));

        // Задняя стена (X=0-247, Y=0-222, Z=153)
        scene.add(createBox(0, 0, """ + str(room_height) + """, """ + str(room_width) + """, """ + str(ceiling_height) + """, """ + str(wall_thickness) + """, materials.topWall));

        // Передняя стена (X=0-247, Y=0-222, Z=0)
        scene.add(createBox(0, 0, 0, """ + str(room_width) + """, """ + str(ceiling_height) + """, """ + str(wall_thickness) + """, materials.bottomWall));

        // Левая стена (X=0, Y=0-222, Z=0-153)
        scene.add(createBox(0, 0, 0, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, """ + str(room_height) + """, materials.leftWall));

        // Дверь ЗАКРЫТА (X=-8, Y=34-109, Z=0 в matplotlib)
        // Дверь: толщина 4 по X, высота 222 по Y, ширина 75 по Z
        scene.add(createBox(""" + str(hinge_x - door_thickness/2) + """, 0, """ + str(hinge_y) + """, 
                           """ + str(door_thickness) + """, """ + str(ceiling_height) + """, """ + str(door_leaf) + """, materials.door));

        // Велосипеды (X=67-247, Y=0-106, Z=0-88)
        scene.add(createBox(""" + str(bike_x) + """, 0, 0, """ + str(bike_length) + """, """ + str(bike_height) + """, """ + str(bike_width) + """, materials.bikes));

        // Полки (X=7-247, Y=0-180, Z=113-153)
        scene.add(createBox(""" + str(shelf_x) + """, 0, """ + str(shelf_y) + """, """ + str(shelf_length) + """, """ + str(shelf_height) + """, """ + str(shelf_width) + """, materials.shelves));

        // Трубы (X=220-247, Y=0-222, Z=135-153)
        scene.add(createBox(""" + str(box_x) + """, 0, """ + str(box_y) + """, """ + str(box_width) + """, """ + str(ceiling_height) + """, """ + str(box_height) + """, materials.pipes));

        // Анимация
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }

        // Адаптация размера
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });

        animate();
    </script>
</body>
</html>
"""

# Сохраняем HTML
with open('room_plan/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n✅ Готово!")
print("📁 Папка 'room_plan' содержит:")
print("   - 2d_plan.png (2D план)")
print("   - 3d_general.png (3D общий вид)")
print("   - 3d_door_view.png (3D вид от двери)")
print("   - combined.png (общая схема)")
print("   - index.html (интерактивная 3D модель с ИСПРАВЛЕНИЯМИ)")
print("\n🔧 Исправления:")
print("   ✅ Дверь теперь в правильной позиции (X=-8, Y=34)")
print("   ✅ Комната не отзеркалена (инверсия Z)")
print("\n🌐 Откройте index.html в браузере!")