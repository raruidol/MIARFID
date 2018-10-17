/**
* Proyecto final GPC: Sistema Solar
*
* oct, 2018
*/

var renderer, scene, camera;
var cameraControls;
var stats;
var galaxia, jupiter, marte, mercurio, moon, neptuno, saturno, sun, tierra, urano, venus;
var enfoque;
var speedcontrol;
var sizecontrol;
var angulo=0;
var ini = Date.now();
var antes = Date.now();
var Jdist = 1278.412010
var Madist = 727.93664
var Medist = 557.909175
var Modist = 50
var Ndist = 2200.252900
var Sdist = 1600.725400
var Tdist = 649.597879
var Udist = 1800.972200
var Vdist = 608.208930
var Jsize= 69.911;
var Ssize= 58.232;
var Usize= 25.362;
var Nsize= 24.622;
var Tsize = 6.371;
var Vsize= 6.052;
var Masize= 3.390;
var Mesize= 2.440;
var Ssize = 150.000;
var Mosize = 200;

init();
loadScene();
setupGUI();
render();

function init(){

  // Configurar el canvas y motor de render
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor( new THREE.Color(0x0000AA) );
  document.getElementById('container').appendChild(renderer.domElement);

  // Instanciar una estructura de datos Escena
  scene = new THREE.Scene();

  // Instanciar una camara
  var aspectRatio = window.innerWidth/window.innerHeight;
  camera = new THREE.PerspectiveCamera(45, aspectRatio, 0.1, 1000000);
  camera.position.set(3000,1500,3000);
  camera.lookAt(new THREE.Vector3(0,0,0));
  scene.add(camera);

  // Interaccion con la camara a traves de OrbitControls.js
  cameraControls = new THREE.OrbitControls(camera, renderer.domElement );
  cameraControls.target.set(0,1,0);

  // Atender al evento de resize
  window.addEventListener('resize', updateAspectRatio);

  // Estadísticas de uso
  stats = new Stats();
  stats.setMode(0);
  stats.domElement.style.position = 'absolute';
  stats.domElement.style.bottom = '0px';
  stats.domElement.style.left = '0px';
  document.getElementById('container').appendChild(stats.domElement);

  // Luz provinente de otras estrellas
  var luzAmbiente = new THREE.AmbientLight(0x333333);
  scene.add(luzAmbiente);

  // Luz solar
  var sol = new THREE.PointLight('white', 0.8);
  sol.position.set(0,0,0);
  scene.add(sol)

}

function setupGUI(){
  //Definir el objeto controlador
  effectController = {
    Velocidad: 1.0,
    Velang: 1.0,
    Tamaño: 1.0,
    Camara: "Sistema"
  };

  var gui = new dat.GUI();

  var h   = gui.addFolder("Configuración del sistema");

  h.add(effectController,"Velocidad",0 , 20).name("Velocidad");

  h.add(effectController, "Velang", 0, 5, 0.5).name("Rotación");

  h.add(effectController,"Tamaño",0 , 5).name("Tamaño planetas");

  h.add(effectController,"Camara",["Sistema","Mercurio","Venus", "Tierra", "Marte", "Jupiter", "Saturno", "Neptuno", "Urano"]).name("Selección").listen().onChange(function(planet) {

    if (planet == "Sistema"){enfoque = sun;}

    else if (planet == "Mercurio"){enfoque = mercurio;}

    else if (planet == "Venus"){enfoque = venus;}

    else if (planet == "Tierra"){enfoque = tierra;}

    else if (planet == "Marte"){enfoque = venus;}

    else if (planet == "Jupiter"){enfoque = jupiter;}

    else if (planet == "Saturno"){enfoque = saturno;}

    else if (planet == "Neptuno"){enfoque = neptuno;}

    else if (planet == "Urano"){enfoque = urano;}

  });
}

function loadScene(){

  var loader = new THREE.ObjectLoader();

  loader.load('models/shrek.json',
    function(obj){
      obj.scale.set(-0.01,0.01,-0.01);
      obj.position.set(0,0,0);
      console.log('Cargado');
      scene.add(obj);
      });

  // Definicion de los objetos
  galaxia = new THREE.Object3D();
  jupiter = new THREE.Object3D();
  marte = new THREE.Object3D();
  mercurio = new THREE.Object3D();
  moon = new THREE.Object3D();
  neptuno = new THREE.Object3D();
  saturno = new THREE.Object3D();
  sun = new THREE.Object3D();
  tierra = new THREE.Object3D();
  urano = new THREE.Object3D();
  venus = new THREE.Object3D();

  //Creación de la galaxia
  var texturaGalaxia = new THREE.TextureLoader().load("./tex/galaxia.jpg");
  var geometriaGalaxia	= new THREE.SphereGeometry(50000, 64, 64);
  var materialGalaxia = new THREE.MeshBasicMaterial( {map: texturaGalaxia, side: THREE.BackSide});

  galaxia = new THREE.Mesh(geometriaGalaxia, materialGalaxia);
  galaxia.castShadow = true;
	galaxia.receiveShadow = true;
  scene.add(galaxia);

  // Creación de jupiter
  var texturaJupiter = new THREE.TextureLoader().load("./tex/jupiter.jpg");
  var geometriaJupiter	= new THREE.SphereGeometry(69.911, 64, 64);
  var materialJupiter = new THREE.MeshPhongMaterial( {map: texturaJupiter});

  jupiter = new THREE.Mesh(geometriaJupiter, materialJupiter);
  jupiter.castShadow = true;
	jupiter.receiveShadow = true;
  jupiter.position.set(1278.412010,0,1278.412010);
  scene.add(jupiter);

  // Creación de marte
  var texturaMarte = new THREE.TextureLoader().load("./tex/marte.jpg");
  var geometriaMarte	= new THREE.SphereGeometry(3.390, 64, 64);
  var materialMarte = new THREE.MeshPhongMaterial( {map: texturaMarte});

  marte = new THREE.Mesh(geometriaMarte, materialMarte);
  marte.castShadow = true;
	marte.receiveShadow = true;
  marte.position.set(727.93664,0,727.93664);
  scene.add(marte);

  // Creación de mercurio
  var texturaMercurio = new THREE.TextureLoader().load("./tex/mercurio.jpg");
  var geometriaMercurio	= new THREE.SphereGeometry(2.440, 64, 64);
  var materialMercurio = new THREE.MeshPhongMaterial( {map: texturaMercurio});

  mercurio = new THREE.Mesh(geometriaMercurio, materialMercurio);
  mercurio.castShadow = true;
  mercurio.receiveShadow = true;
  mercurio.position.set(557.909175,0,557.909175);
  scene.add(mercurio);

  // Creación de moon
  var texturaMoon = new THREE.TextureLoader().load("./tex/moon.jpg");
  var geometriaMoon	= new THREE.SphereGeometry(1.7, 64, 64);
  var materialMoon = new THREE.MeshPhongMaterial( {map: texturaMoon});

  moon = new THREE.Mesh(geometriaMoon, materialMoon);
  moon.castShadow = true;
  moon.receiveShadow = true;
  moon.position.set(50,0,50);
  scene.add(moon);

  // Creación de neptuno
  var texturaNeptuno = new THREE.TextureLoader().load("./tex/neptuno.jpg");
  var geometriaNeptuno	= new THREE.SphereGeometry(24.622, 64, 64);
  var materialNeptuno = new THREE.MeshPhongMaterial( {map: texturaNeptuno});

  neptuno = new THREE.Mesh(geometriaNeptuno, materialNeptuno);
  neptuno.castShadow = true;
  neptuno.receiveShadow = true;
  neptuno.position.set(1700.252900,0,1700.252900);
  scene.add(tierra);

  // Creación de saturno
  var texturaSaturno = new THREE.TextureLoader().load("./tex/saturno.jpg");
  var geometriaSaturno	= new THREE.SphereGeometry(58.232, 64, 64);
  var materialSaturno = new THREE.MeshPhongMaterial( {map: texturaSaturno});

  saturno = new THREE.Mesh(geometriaSaturno, materialSaturno);
  saturno.castShadow = true;
  saturno.receiveShadow = true;
  saturno.position.set(1400.725400,0,1400.725400);
  scene.add(saturno);

  // Creación de sun
  var texturaSun = new THREE.TextureLoader().load("./tex/sun.jpg");
  var geometriaSun	= new THREE.SphereGeometry(150.000, 64, 64);
  var materialSun = new THREE.MeshPhongMaterial( {color: 'yellow',map: texturaSun, lightMap: texturaSun, shading: THREE.SmoothShading});

  sun = new THREE.Mesh(geometriaSun, materialSun);
  sun.castShadow = true;
  sun.receiveShadow = true;
  sun.position.set(-100,0,0);
  scene.add(sun);

  // Creación de la tierra
  var texturaTierra = new THREE.TextureLoader().load("./tex/tierra.jpg");
  var geometriaTierra	= new THREE.SphereGeometry(6.371, 64, 64);
  var materialTierra = new THREE.MeshPhongMaterial( {map: texturaTierra});

  tierra = new THREE.Mesh(geometriaTierra, materialTierra);
  tierra.castShadow = true;
	tierra.receiveShadow = true;
  tierra.position.set(649.597879,0,649.597879);
  scene.add(tierra);

  // Creación de la urano
  var texturaUrano = new THREE.TextureLoader().load("./tex/urano.jpg");
  var geometriaUrano	= new THREE.SphereGeometry(25.362, 64, 64);
  var materialUrano = new THREE.MeshPhongMaterial( {map: texturaUrano});

  urano = new THREE.Mesh(geometriaUrano, materialUrano);
  urano.castShadow = true;
	urano.receiveShadow = true;
  urano.position.set(1500.972200,0,1500.972200);
  scene.add(urano);

  // Creación de la venus
  var texturaVenus = new THREE.TextureLoader().load("./tex/venus.jpg");
  var geometriaVenus	= new THREE.SphereGeometry(6.052, 64, 64);
  var materialVenus = new THREE.MeshPhongMaterial( {map: texturaVenus});

  venus = new THREE.Mesh(geometriaVenus, materialVenus);
  venus.castShadow = true;
	venus.receiveShadow = true;
  venus.position.set(608.208930,0,608.208930);
  scene.add(venus);

  enfoque = sun;


}

function updateAspectRatio(){
  //  Renovar las dimensiones del viewPort y la matriz de proyeccion
  renderer.setSize(window.innerWidth, window.innerHeight);

  aspectRatio = window.innerWidth/window.innerHeight;
  camera.aspect = aspectRatio;
  camera.updateProjectionMatrix();
}

function update(){

  // Rotación própia de los planetas
  var ahora = Date.now();
  var vueltasXsg = effectController.Velang;
  angulo += vueltasXsg * Math.PI * ((ahora-antes)/2000);

  mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
  venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
  tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
  marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
  jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
  saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
  neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
  urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

  moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)


  var scale = effectController.Tamaño;

  if (enfoque == sun){
    mercurio.rotation.y = angulo;
    venus.rotation.y = angulo;
    tierra.rotation.y = angulo;
    marte.rotation.y = angulo;
    jupiter.rotation.y = angulo;
    saturno.rotation.y = angulo;
    neptuno.rotation.y = angulo;
    urano.rotation.y = angulo;
    sun.rotation.y = angulo/5;


    // Orbitación de los planetas alrededor del sol
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037 *effectController.Velocidad),0,Medist*Math.sin((ahora-ini) * 0.00037 *effectController.Velocidad))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 *effectController.Velocidad),0,Vdist*Math.sin((ahora-ini) * 0.00019 *effectController.Velocidad))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 *effectController.Velocidad),0,Tdist*Math.sin((ahora-ini) * 0.00012 *effectController.Velocidad))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 *effectController.Velocidad),0,Madist*Math.sin((ahora-ini) * 0.00021 *effectController.Velocidad))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 *effectController.Velocidad),0,Jdist*Math.sin((ahora-ini) * 0.0001 *effectController.Velocidad))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 *effectController.Velocidad),0,Sdist*Math.sin((ahora-ini) * 0.0002 *effectController.Velocidad))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 *effectController.Velocidad),0,Ndist*Math.sin((ahora-ini) * 0.0000275 *effectController.Velocidad))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 *effectController.Velocidad),0,Udist*Math.sin((ahora-ini) * 0.000054 *effectController.Velocidad))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    // Escalado de los planetas
    mercurio.scale.x = scale;
    mercurio.scale.y = scale;
    mercurio.scale.z = scale;
    venus.scale.x = scale;
    venus.scale.y = scale;
    venus.scale.z = scale;
    tierra.scale.x = scale;
    tierra.scale.y = scale;
    tierra.scale.z = scale;
    moon.scale.x = scale;
    moon.scale.y = scale;
    moon.scale.z = scale;
    marte.scale.x = scale;
    marte.scale.y = scale;
    marte.scale.z = scale;
    jupiter.scale.x = scale;
    jupiter.scale.y = scale;
    jupiter.scale.z = scale;
    saturno.scale.x = scale;
    saturno.scale.y = scale;
    saturno.scale.z = scale;
    neptuno.scale.x = scale;
    neptuno.scale.y = scale;
    neptuno.scale.z = scale;
    urano.scale.x = scale;
    urano.scale.y = scale;
    urano.scale.z = scale;
  }

  if (enfoque == mercurio){
    mercurio.rotation.y = angulo;
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037 *effectController.Velocidad),0,Medist*Math.sin((ahora-ini) * 0.00037 *effectController.Velocidad))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    mercurio.scale.x = scale;
    mercurio.scale.y = scale;
    mercurio.scale.z = scale;
  }

  if (enfoque == venus){
    venus.rotation.y = angulo;
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 *effectController.Velocidad),0,Vdist*Math.sin((ahora-ini) * 0.00019 *effectController.Velocidad))
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))

    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    venus.scale.x = scale;
    venus.scale.y = scale;
    venus.scale.z = scale;
  }

  if (enfoque == tierra){
    tierra.rotation.y = angulo;
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 *effectController.Velocidad),0,Tdist*Math.sin((ahora-ini) * 0.00012 *effectController.Velocidad))
    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))

    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    tierra.scale.x = scale;
    tierra.scale.y = scale;
    tierra.scale.z = scale;
    moon.scale.x = scale;
    moon.scale.y = scale;
    moon.scale.z = scale;
  }

  if (enfoque == marte){
    marte.rotation.y = angulo;
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 *effectController.Velocidad),0,Madist*Math.sin((ahora-ini) * 0.00021 *effectController.Velocidad))

    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    marte.scale.x = scale;
    marte.scale.y = scale;
    marte.scale.z = scale;
  }

  if (enfoque == jupiter){
    jupiter.rotation.y = angulo;

    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 *effectController.Velocidad),0,Jdist*Math.sin((ahora-ini) * 0.0001 *effectController.Velocidad))
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))

    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    jupiter.scale.x = scale;
    jupiter.scale.y = scale;
    jupiter.scale.z = scale;
  }

  if (enfoque == saturno){
    saturno.rotation.y = angulo;
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 *effectController.Velocidad),0,Sdist*Math.sin((ahora-ini) * 0.0002 *effectController.Velocidad))
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))

    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    saturno.scale.x = scale;
    saturno.scale.y = scale;
    saturno.scale.z = scale;
  }

  if (enfoque == neptuno){
    neptuno.rotation.y = angulo;
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 *effectController.Velocidad),0,Ndist*Math.sin((ahora-ini) * 0.0000275 *effectController.Velocidad))
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))

    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 ),0,Udist*Math.sin((ahora-ini) * 0.000054 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    neptuno.scale.x = scale;
    neptuno.scale.y = scale;
    neptuno.scale.z = scale;
  }

  if (enfoque == urano){
    urano.rotation.y = angulo;
    urano.position.set(Udist*Math.cos((ahora-ini) * 0.000054 *effectController.Velocidad),0,Udist*Math.sin((ahora-ini) * 0.000054 *effectController.Velocidad))
    mercurio.position.set(Medist*Math.cos((ahora-ini) * 0.00037),0,Medist*Math.sin((ahora-ini) * 0.00037 ))
    venus.position.set(Vdist*Math.cos((ahora-ini) * 0.00019 ),0,Vdist*Math.sin((ahora-ini) * 0.00019 ))
    tierra.position.set(Tdist*Math.cos((ahora-ini) * 0.00012 ),0,Tdist*Math.sin((ahora-ini) * 0.00012 ))
    marte.position.set(Madist*Math.cos((ahora-ini) * 0.00021 ),0,Madist*Math.sin((ahora-ini) * 0.00021 ))
    jupiter.position.set(Jdist*Math.cos((ahora-ini) * 0.0001 ),0,Jdist*Math.sin((ahora-ini) * 0.0001 ))
    saturno.position.set(Sdist*Math.cos((ahora-ini) * 0.0002 ),0,Sdist*Math.sin((ahora-ini) * 0.0002 ))
    neptuno.position.set(Ndist*Math.cos((ahora-ini) * 0.0000275 ),0,Ndist*Math.sin((ahora-ini) * 0.0000275 ))

    moon.position.set(Modist * Math.cos((ahora-ini) * 0.002 * effectController.Velocidad) + tierra.position.x, 0, Modist * Math.sin((ahora-ini) * 0.002 * effectController.Velocidad)+tierra.position.z)

    urano.scale.x = scale;
    urano.scale.y = scale;
    urano.scale.z = scale;
  }

  antes = ahora;

  stats.update()
  cameraControls.update();

}

function render(){
  requestAnimationFrame(render);
  update();
  renderer.render(scene, camera);

}
