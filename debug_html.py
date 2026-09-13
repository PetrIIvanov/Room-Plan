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

debug_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Дебаг - Дверь от петли</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
        .container { display: flex; gap: 20px; }
        #canvas-container { width: 800px; height: 600px; border: 2px solid #333; background: white; }
        .info-panel { flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>🔍 Дебаг - Дверь начинается от петли</h1>
    
    <div class="container">
        <div id="canvas-container"></div>
        
        <div class="info-panel">
            <h2>Параметры двери:</h2>
            <ul>
                <li>Проём: от Z=34 до Z=109 (75 см)</li>
                <li>Петли: X=-8, Z=34</li>
                <li>Дверь открыта: от X=-8 до X=67</li>
                <li>Дверь НЕ центрирована, начинается от петли!</li>
            </ul>
            
            <div style="margin-top: 20px; padding: 10px; background: #fff3cd; border-radius: 4px;">
                <strong>Управление:</strong><br>
                🖱️ Левая кнопка — вращение<br>
                🖱️ Правая кнопка — перемещение<br>
                🖱️ Колёсико — zoom
            </div>
        </div>
    </div>

    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);

        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 10000);
        camera.position.set(300, 200, 300);
        camera.lookAt(0, 100, 75);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(200, 300, 200);
        scene.add(dirLight);

        // Функция создания коробки
        function createBox(x, y_mpl, z_mpl, w, h, d, material) {
            const geometry = new THREE.BoxGeometry(w, h, d);
            const mesh = new THREE.Mesh(geometry, material);
            const z_three = """ + str(room_height) + """ - z_mpl - d;
            mesh.position.set(x + w/2, y_mpl + h/2, z_three + d/2);
            return mesh;
        }

        // Материалы
        const wallMaterial = new THREE.MeshLambertMaterial({ color: 0xffb6c1, transparent: true, opacity: 0.5 });
        const doorMaterial = new THREE.MeshLambertMaterial({ color: 0x8b4513, transparent: true, opacity: 0.8 });

        // Пол
        scene.add(createBox(0, 0, 0, """ + str(room_width) + """, 0.1, """ + str(room_height) + """, 
            new THREE.MeshLambertMaterial({ color: 0xd3d3d3, transparent: true, opacity: 0.3 })));

        // Потолок
        scene.add(createBox(0, """ + str(ceiling_height) + """, 0, """ + str(room_width) + """, 0.1, """ + str(room_height) + """,
            new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.3 })));

        // Правая стена
        scene.add(createBox(""" + str(room_width) + """, 0, 0, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, """ + str(room_height) + """, wallMaterial));

        // Задняя стена
        scene.add(createBox(0, 0, """ + str(room_height) + """, """ + str(room_width) + """, """ + str(ceiling_height) + """, """ + str(wall_thickness) + """, wallMaterial));

        // Передняя стена
        scene.add(createBox(0, 0, 0, """ + str(room_width) + """, """ + str(ceiling_height) + """, """ + str(wall_thickness) + """, wallMaterial));

        // ЛЕВАЯ СТЕНА С ПРОЁМОМ (разбита на 2 части)
        
        // Нижняя часть: от Z=0 до Z=34
        scene.add(createBox(0, 0, 0, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, """ + str(door_gap_bottom) + """, wallMaterial));

        // Верхняя часть: от Z=109 до Z=153
        const upperZ = """ + str(door_gap_bottom + door_width) + """;
        const upperHeight = """ + str(room_height) + """ - upperZ;
        scene.add(createBox(0, 0, upperZ, """ + str(wall_thickness) + """, """ + str(ceiling_height) + """, upperHeight, wallMaterial));

        // ДВЕРЬ В ОТКРЫТОМ СОСТОЯНИИ - НАЧИНАЕТСЯ ОТ ПЕТЛИ
        // Петли: X=-8, Z=34 (в matplotlib)
        // Дверь идёт от X=-8 до X=67 (75 см вглубь комнаты)
        // По Y: от 0 до 222
        // По Z: центрирована на 34, толщина 4 см (от 32 до 36)
        
        // В Three.js координатах:
        // X: от -8 до 67, центр в 29.5, ширина 75
        // Y: от 0 до 222, центр в 111, высота 222
        // Z: от 32 до 36, центр в 34, глубина 4
        
        const doorX_start = """ + str(hinge_x) + """;  // -8
        const doorX_end = """ + str(hinge_x + door_leaf) + """;  // 67
        const doorX_center = (doorX_start + doorX_end) / 2;  // 29.5
        const doorX_width = doorX_end - doorX_start;  // 75
        
        const doorY_start = 0;
        const doorY_end = """ + str(ceiling_height) + """;
        const doorY_center = (doorY_start + doorY_end) / 2;  // 111
        const doorY_height = doorY_end - doorY_start;  // 222
        
        const doorZ_mpl = """ + str(hinge_y) + """;  // 34
        const doorZ_thickness = """ + str(door_thickness) + """;  // 4
        const doorZ_start_mpl = doorZ_mpl - doorZ_thickness/2;  // 32
        const doorZ_end_mpl = doorZ_mpl + doorZ_thickness/2;  // 36
        
        // Перевод Z в Three.js
        const doorZ_three = """ + str(room_height) + """ - doorZ_mpl - doorZ_thickness;  // 115
        const doorZ_center_three = doorZ_three + doorZ_thickness/2;  // 117
        
        const doorGeometry = new THREE.BoxGeometry(doorX_width, doorY_height, doorZ_thickness);
        const door = new THREE.Mesh(doorGeometry, doorMaterial);
        door.position.set(doorX_center, doorY_center, doorZ_center_three);
        scene.add(door);

        // Маркер петель
        const hingeZ_three = """ + str(room_height) + """ - """ + str(hinge_y) + """;
        const hingeMarker = new THREE.Mesh(
            new THREE.SphereGeometry(5, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xff0000 })
        );
        hingeMarker.position.set(""" + str(hinge_x) + """, """ + str(ceiling_height/2) + """, hingeZ_three);
        scene.add(hingeMarker);

        // Подписи
        function createTextSprite(text, position, color) {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = 256;
            canvas.height = 128;
            context.fillStyle = color;
            context.font = 'bold 40px Arial';
            context.fillText(text, 10, 80);
            
            const texture = new THREE.CanvasTexture(canvas);
            const material = new THREE.SpriteMaterial({ map: texture });
            const sprite = new THREE.Sprite(material);
            sprite.position.copy(position);
            sprite.scale.set(80, 40, 1);
            return sprite;
        }

        scene.add(createTextSprite('Проём', new THREE.Vector3(-30, 100, """ + str(room_height/2) + """), 'red'));
        scene.add(createTextSprite('Дверь от петли', new THREE.Vector3(30, 150, 30), 'brown'));
        scene.add(createTextSprite('Петли', new THREE.Vector3(-20, 180, hingeZ_three), 'red'));

        // Сетка
        const gridHelper = new THREE.GridHelper(300, 10, 0x888888, 0xcccccc);
        gridHelper.position.set(0, 0.5, """ + str(room_height/2) + """);
        scene.add(gridHelper);

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

with open('room_plan/debug_door_v2.html', 'w', encoding='utf-8') as f:
    f.write(debug_html)

print("✅ Создан файл: room_plan/debug_door_v2.html")
print(" Откройте его в браузере")
print("🔍 Теперь дверь начинается от петли (-8) и идёт до X=67")
print("\n📸 Сделайте скриншот и пришлите!")