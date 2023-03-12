from api.app import create_app
from fastapi.responses import HTMLResponse

app = create_app()

@app.get("/", response_class=HTMLResponse)
def read_root():
    html = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Three.js Cube Example</title>
    <style>
      body { margin: 0; }
      canvas { display: block; }
    </style>
  </head>
  <body>
    <script src="https://cdn.jsdelivr.net/npm/three@0.137.0/build/three.min.js"></script>
    <script>
      // Create a scene
      const scene = new THREE.Scene();

      // Create a camera
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 5;

      // Create a renderer
      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      // Create a cube with the color #B7D0D0
      const geometry = new THREE.BoxGeometry(1, 1, 1);
      const material = new THREE.MeshBasicMaterial({ color: 0xB7D0D0 });
      const cube = new THREE.Mesh(geometry, material);

      // Add the cube to the scene
      scene.add(cube);

      // Render the scene
      function animate() {
        requestAnimationFrame(animate);
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        renderer.render(scene, camera);
      }
      animate();
    </script>
  </body>
</html>
"""

    return HTMLResponse(content=html, status_code=200)  