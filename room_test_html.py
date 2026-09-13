import os

os.makedirs('room_plan', exist_ok=True)

room_width = 247
room_height = 153
ceiling_height = 222
wall_thickness = 8

door_gap_bottom = 34
door_gap_top = 44
door_width = 75
door_leaf = 75
door_thickness = 4

hinge_x = -8
hinge_y = 34

box_width = 27
box_height = 18
box_x = room_width - box_width
box_y = room_height - box_height

bike_length = 180
bike_width = 88
bike_height = 106
bike_x = room_width - bike_length
bike_y = 0

shelf_length = 240
shelf_width = 40
shelf_height = 180
shelf_x = room_width - shelf_length
shelf_y = room_height - shelf_width

final_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>План комнаты - Интерактивная 3D модель</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; }
        #canvas-container { width: 100%; height: 700px; border: 2px solid #333; border-radius: 4px; margin: 20px 0; }
        .controls-info { background: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .info { background: #e8f4f8; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 Интерактивная 3D модель комнаты</h1>
        
        <div class="info">
            <h3>Характеристики:</h3>
            <ul>
                <li>Размеры: """ + str(room_width) + """ × """ + str(room_height) + """ × """ + str(ceiling_height) + """ см</li>
                <li>Площадь: """ + f"{room_width*room_height/10000:.2f}" + """ м²</li>
                <li>Стены: """ + str(wall_thickness) + """ см</li>
            </ul>
        </div>

        <div class="controls-info">
            <strong>Управление:</strong><br>
            🖱️ Левая кнопка — вращение | Правая кнопка — перемещение | Колёсико — zoom
        </div>
        
        <div id="canvas-container"></div>
    </div>

    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf5f5f5);

        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 10000);
        camera.position.set(400, 300, 400);
        camera.lookAt(100, 100, 75);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(200, 300, 200);
        scene.add(dirLight);

        // ПРАВИЛЬНАЯ ФУНКЦИЯ СОЗДАНИЯ КОРОБКИ
        function createBox(x, y, z, w, h, d, material) {
            const geometry = new THREE.BoxGeometry(w, h, d);
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(x + w/2, y + h/2, z + d/2);
            return mesh;
        }

        // Материалы
        const materials = {
            floor: new THREE.MeshLambertMaterial({ color: 0xd3d3d3, transparent: true, opacity: 0.5 }),
            ceiling: new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.3 }),
            rightWall: new THREE.MeshLambertMaterial({ color: 0xadd8e6, transparent: true, opacity: 0.5 }),
            topWall: new THREE.MeshLambertMaterial({ color: 0x90ee90, transparent: true, opacity: 0.5 }),
            bottomWall: new THREE.MeshLambertMaterial({ color: 0xffffe0, transparent: true, opacity: 0.5 }),
            leftWall: new THREE.MeshLambertMaterial({ color: 0xffb6c1, transparent: true, opacity: 0.5 }),
            door: new THREE.MeshLambertMaterial({ color: 0x8b4513, transparent: true, opacity: 0.8 }),
            bikes: new THREE.MeshLambertMaterial({ color: 0xc0c0c0, transparent: true, opacity: 0.7 }),
            shelves: new THREE.MeshLambertMaterial({ color: 0xf5deb3, transparent: true, opacity: 0.7 }),
            pipes: new THREE.MeshLambertMaterial({ color: 0xff6347, transparent: true, opacity: 0.6 }),
        };

        // Пол: Y=0
        scene.add(createBox(0, 0, 0, """ + str(room_width) + """, 0.1, """ + str(room_height) + """, materials.floor));

        // Потолок: Y=222
        scene.add(createBox(0, """ + str(ceiling_height) + """, 0, """ + str(room_width) + """, 0.1, """ + str(room_height) + """, materials.ceiling));

        // Правая стена: X=247, толщина 8 по X
        scene.add(createBox(""" + str(room_width) + """, 0, 0, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, """ + str(room_height) + """, materials.rightWall));

        // Задняя стена: Z=153, толщина 8 по Z
        scene.add(createBox(0, 0, """ + str(room_height) + """, """ + str(room_width) + """, """ + str(ceiling_height) + """, """ + str(wall_thickness) + """, materials.topWall));

        // Передняя стена: Z=0, толщина 8 по Z
        scene.add(createBox(0, 0, 0, """ + str(room_width) + """, """ + str(ceiling_height) + """, """ + str(wall_thickness) + """, materials.bottomWall));

        // Левая стена: X=0, толщина 8 по X
        scene.add(createBox(0, 0, 0, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, """ + str(room_height) + """, materials.leftWall));

        // Дверь закрыта: X=-8, Y=34, толщина 4 по X
        scene.add(createBox(""" + str(hinge_x - 2) + """, """ + str(hinge_y) + """, 0, """ + str(door_thickness) + """, """ + str(ceiling_height) + """, """ + str(door_leaf) + """, materials.door));

        // Велосипеды: X=67, Y=0, Z=0
        scene.add(createBox(""" + str(bike_x) + """, 0, 0, """ + str(bike_length) + """, """ + str(bike_height) + """, """ + str(bike_width) + """, materials.bikes));

        // Полки: X=7, Y=0, Z=113
        scene.add(createBox(""" + str(shelf_x) + """, 0, """ + str(shelf_y) + """, """ + str(shelf_length) + """, """ + str(shelf_height) + """, """ + str(shelf_width) + """, materials.shelves));

        // Трубы: X=220, Y=0, Z=135
        scene.add(createBox(""" + str(box_x) + """, 0, """ + str(box_y) + """, """ + str(box_width) + """, """ + str(ceiling_height) + """, """ + str(box_height) + """, materials.pipes));

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }

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

with open('room_plan/index_final.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("✅ Создан файл: room_plan/index_final.html")
print("📂 Откройте его в браузере")
print("🎮 Теперь комната должна выглядеть правильно!")