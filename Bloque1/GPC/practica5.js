var robot, base;
var brazo,antebrazo,mano,pinzaIz, pinzaDe;
var renderer, scene, camera;
// Camaras
var planta;
// Lado de la ventana por la que miro
var L = 100;
init();
loadScene();
render();

function setCameras( ar ){

  // Camaras ortograficas
  var camaraOrtografica;

  if(ar > 1){

    // Left, right, top, bottom, near, far
    camaraOrtografica = new THREE.OrthographicCamera(-L*ar ,L*ar, L, -L, 0.1, 10000);

  }
  else{
    camaraOrtografica = new THREE.OrthographicCamera(-L ,L, L*ar, -L*ar, 0.1, 10000);

  }

  planta = camaraOrtografica.clone();
  planta.position.set(0,L*4.5,0);
  planta.lookAt(new THREE.Vector3(0, 0, 0));
  planta.up = new THREE.Vector3(0,1,0);

  // Camara perspectiva
  camera = new THREE.PerspectiveCamera(80, ar, 0.1, 2000);
  camera.position.set(200,300,100);
  camera.lookAt(new THREE.Vector3(0,0,0));

  scene.add(planta);
  scene.add(camera);

}

function init(){

  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setClearColor(new THREE.Color(0xFFFFFF));
  renderer.shadowMap.enabled = true;
  document.getElementById('container').appendChild(renderer.domElement);

  renderer.autoClear = false;

  scene = new THREE.Scene();

  // Instanciar una camara
  var aspectRatio = window.innerWidth/window.innerHeight;

  setCameras(window.innerWidth/window.innerHeight);


  // Interaccion con la camara a traves de OrbitControls.js
  cameraControls = new THREE.OrbitControls(camera, renderer.domElement );
  cameraControls.noKeys = true;
  cameraControls.target.set(0,0,0);

  // Atender al evento de resize
  window.addEventListener('resize', updateAspectRatio);

  // Luces
  var luzAmbiente = new THREE.AmbientLight(0x222222);
  scene.add(luzAmbiente);

  var luzDireccional = new THREE.DirectionalLight('white', 0.4);
  luzDireccional.position.set(0,1,0);
  scene.add(luzDireccional);


  var luzPuntual = new THREE.PointLight('white', 0.4);
  luzPuntual.position.set(0,250,0);
  //scene.add(luzPuntual);

  var luzFocal = new THREE.SpotLight('white', 0.6);
  luzFocal.position.set(250, 500, 250);
  luzFocal.target.position.set(400,1600,400);
  luzFocal.angle = Math.PI/4;
  luzFocal.penumbra = 1;

  //Ayudantes para luz focal
  luzFocal.shadow.camera.near = 100;
  luzFocal.shadow.camera.far = 2500;
  luzFocal.shadow.camera.fov = 60;
  //scene.add(new THREE.CameraHelper(luzFocal.shadow.camera));

    //sombras
  luzFocal.castShadow = true;
  scene.add(luzFocal);


  robotController = {
  		giro1: 0,
  		giro2: 0,
  		giro3: 0,
  		giro4: 0,
  		giro5: 0,
  		separacion: 0
  	}

  	var gui = new dat.GUI();
  	var h = gui.addFolder("Controles");
  	h.add( robotController, "giro1", -180, 180, 1).name("Giro Base");
  	h.add( robotController, "giro2", -45, 45, 1).name("Giro Brazo");
  	h.add( robotController, "giro3", -180, 180, 1).name("Giro Antebrazo Y");
  	h.add( robotController, "giro4", -90, 90, 1).name("Giro Antebrazo Z");
  	h.add( robotController, "giro5", -40, 220, 1).name("Giro Pinza");
  	h.add( robotController, "separacion", 0, 15, 1).name("Separacion pinza");

  	window.addEventListener('keydown', handleKey, false);
}

function handleKey(event) {

  if ( event.keyCode == 39 || event.keyCode==68) {
  	robot.position.x+=10;
  }
  if ( (event.keyCode == 38 || event.keyCode==87)) {
    robot.position.z-=10;
  }
  if ( (event.keyCode == 37 || event.keyCode==65)) {
    robot.position.x-=10;
  }
  if ((event.keyCode == 40 || event.keyCode==83)) {
    robot.position.z+=10;
  }

}

function loadScene(){


	robot = new THREE.Object3D();
	brazo = new THREE.Object3D();
	antebrazo = new THREE.Object3D();
	var material = new THREE.MeshLambertMaterial( {color: 'blue', wireframe: false, side: THREE.DoubleSide} );
  var texturaMetal = new THREE.TextureLoader().load("./images/metal_128x128.jpg");
  var texturaSuelo = new THREE.TextureLoader().load("./images/pisometalico_1024.jpg");
  var texturaMadera = new THREE.TextureLoader().load('./images/wood512.jpg');

  var path = './images/';
  var urls = [path + 'posx.jpg', path + 'negx.jpg',
              path + 'posy.jpg', path + 'negy.jpg',
              path + 'posz.jpg', path + 'negz.jpg'];

  var texturaEntorno = new THREE.CubeTextureLoader().load(urls);

  var materialSuelo = new THREE.MeshPhongMaterial( {map: texturaSuelo});
	var materialMetal = new THREE.MeshPhongMaterial( {map: texturaMetal, side: THREE.DoubleSide});
	var materialMadera = new THREE.MeshLambertMaterial( {map: texturaMadera, side: THREE.DoubleSide});
  var materialRotula = new THREE.MeshPhongMaterial({color: 'white',
                                                    envMap : texturaEntorno,
                                                    specular: 'white',
                                                    shininess: 50,
                                                    wireframe: false});

  var shader = THREE.ShaderLib.cube;
  shader.uniforms.tCube.value = texturaEntorno;
  var materialEntorno = new THREE.ShaderMaterial({
    fragmentShader: shader.fragmentShader,
    vertexShader: shader.vertexShader,
    uniforms: shader.uniforms,
    depthWrite: false,
    side: THREE.BackSide
  });

  var habitacion = new THREE.Mesh(new THREE.CubeGeometry(1000,1000,1000),materialEntorno);
  scene.add(habitacion);

	// Definición del suelo
	var forma_Suelo = new THREE.PlaneGeometry( 1000, 1000, 10, 10 );
	var suelo = new THREE.Mesh( forma_Suelo, materialSuelo );

  suelo.rotation.x=-Math.PI/2;
  suelo.receiveShadow = true;

	// Construcción de la base
	var forma_Base = new THREE.CylinderGeometry( 50, 50, 15, 25 );
	base = new THREE.Mesh( forma_Base, materialMetal );
  base.castShadow = true;
  base.receiveShadow = true;

	// Construcción del eje
	var forma_Eje = new THREE.CylinderGeometry( 20, 20, 18, 25 );
	var eje = new THREE.Mesh( forma_Eje, materialMetal );
	eje.rotation.x=Math.PI/2;
  eje.castShadow = true;
  eje.receiveShadow = true;

	// Construcción del espárrago
	var forma_Esparrago = new THREE.BoxGeometry( 18, 120, 12 );
	var esparrago = new THREE.Mesh( forma_Esparrago, materialMadera );
	esparrago.position.y=75;
  esparrago.castShadow = true;
  esparrago.receiveShadow = true;

	// Construcción de la rótula
	var forma_Rotula = new THREE.SphereGeometry( 20, 20, 20 );
	var rotula = new THREE.Mesh( forma_Rotula, materialRotula );
	rotula.position.y=135;
  rotula.castShadow = true;
  rotula.receiveShadow = true;

	// Construcción del disco
	var forma_Disco = new THREE.CylinderGeometry( 22, 22, 6, 25 );
	var disco = new THREE.Mesh( forma_Disco, materialMetal );
	disco.position.y=135;
  disco.castShadow = true;
  disco.receiveShadow = true;

	// Construcción de los nervios
	var forma_primer_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var primer_nervio = new THREE.Mesh( forma_primer_Nervio, materialMadera);
	primer_nervio.position.x =10;
	primer_nervio.position.y=175;
	primer_nervio.position.z=10;
  primer_nervio.castShadow = true;
  primer_nervio.receiveShadow = true;

	var forma_segundo_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var segundo_nervio = new THREE.Mesh( forma_segundo_Nervio, materialMadera );
	segundo_nervio.position.x =10;
	segundo_nervio.position.y=175;
	segundo_nervio.position.z=-10;
  segundo_nervio.castShadow = true;
  segundo_nervio.receiveShadow = true;

	var forma_tercer_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var tercer_nervio = new THREE.Mesh( forma_tercer_Nervio, materialMadera );
	tercer_nervio.position.x =-10;
	tercer_nervio.position.y=175;
	tercer_nervio.position.z=-10;
  tercer_nervio.castShadow = true;
  tercer_nervio.receiveShadow = true;

	var forma_cuarto_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var cuarto_nervio = new THREE.Mesh( forma_cuarto_Nervio, materialMadera );
	cuarto_nervio.position.x =-10;
	cuarto_nervio.position.y=175;
	cuarto_nervio.position.z=10;
  cuarto_nervio.castShadow = true;
  cuarto_nervio.receiveShadow = true;

	// Construcción de la mano
	var forma_Mano = new THREE.CylinderGeometry( 15, 15, 40, 25 );
	mano = new THREE.Mesh(forma_Mano, materialMadera);
	var matrizRotacionMano= new THREE.Matrix4();
	var matrizTranslacionMano= new THREE.Matrix4();
	mano.matrixAutoUpdate=false;
	matrizRotacionMano.makeRotationX(Math.PI/2);
	matrizTranslacionMano.makeTranslation(0,215,0);
	mano.matrix= matrizTranslacionMano.multiply(matrizRotacionMano);
  mano.castShadow = true;
  mano.receiveShadow = true;

	// Construcción de las pinzas
	var mallaPinza	= new THREE.Geometry();
	var coordenadas = [-18,0,0, 0,0,0, 18,4,0, 18,16,0, 0,20,0, -18,20,0, -18,20,-4, 0,20,-4, 18,16,-2, 18,4,-2, 0,0,-4, -18,0,-4];

	var indices= [0,1,4, 4,5,0, 1,10,7, 7,4,1, 6,7,10, 10,11,6, 6,11,0, 0,5,6, 7,6,5, 5,4,7, 0,1,10, 10,11,0,
	1,2,3, 3,4,1, 2,9,8, 8,3,2, 7,8,9, 9,10,7, 8,7,4, 4,3,8, 2,1,10, 10,9,2];

	for(var i = 0; i<coordenadas.length;i+=3){
		var v = new THREE.Vector3(coordenadas[i],coordenadas[i+1],coordenadas[i+2]);
		mallaPinza.vertices.push(v);
	}

	for(var i=0; i<indices.length;i+=3){
		var triangulo= new THREE.Face3(indices[i],indices[i+1],indices[i+2]);
		mallaPinza.faces.push(triangulo);
	}


	pinzaIz = new THREE.Mesh(mallaPinza,material);
  pinzaIz.castShadow = true;
  pinzaIz.receiveShadow = true;
	pinzaDe = new THREE.Mesh(mallaPinza,material);
  pinzaDe.castShadow = true;
  pinzaDe.receiveShadow = true;


  // Mano desglose
	mano.add(pinzaIz);
	mano.add(pinzaDe);

  // Antebrazo desglose
	antebrazo.add(mano);
	antebrazo.add(primer_nervio);
	antebrazo.add(segundo_nervio);
	antebrazo.add(tercer_nervio);
	antebrazo.add(cuarto_nervio);
	antebrazo.add(disco);

  // Brazo desglose
	brazo.add(antebrazo);
	brazo.add(rotula);
	brazo.add(esparrago);
	brazo.add(eje);

  // Base desglose
	base.add(brazo);

  // Robot desglose
	robot.add(base);

  // Pintado de escena
	scene.add(suelo);
	scene.add(robot);


}

function updateAspectRatio(){
  //  Renovar las dimensiones del viewPort y la matriz de proyeccion
  renderer.setSize(window.innerWidth, window.innerHeight);

  aspectRatio = window.innerWidth/window.innerHeight;
  camera.aspect = aspectRatio;
  camera.updateProjectionMatrix();

  planta.aspect = 1
  planta.updateProjectionMatrix();


}

function update(){

  cameraControls.update();

  base.rotation.y = robotController.giro1*Math.PI/180;
	brazo.rotation.z = robotController.giro2*Math.PI/180;
	antebrazo.matrixAutoUpdate = false;
	var mt= new THREE.Matrix4();
	var mr= new THREE.Matrix4();
	var mr2= new THREE.Matrix4();
	var mt2= new THREE.Matrix4();

	mt.makeTranslation( 0,-135,0 );
	mr.makeRotationY(robotController.giro3*Math.PI/180);
	mr2.makeRotationZ(robotController.giro4*Math.PI/180);
	mt2.makeTranslation( 0,135,0 );
	antebrazo.matrix=mt2.multiply(mr2.multiply(mr.multiply(mt)));


	var matrizRotacionMano= new THREE.Matrix4();
	var matrizTranslacionMano= new THREE.Matrix4();
	mano.matrixAutoUpdate=false;
	matrizRotacionMano.makeRotationX(Math.PI/2);
	mr.makeRotationZ(robotController.giro5*Math.PI/180);
	matrizTranslacionMano.makeTranslation(0,215,0);
	mano.matrix= matrizTranslacionMano.multiply(mr.multiply(matrizRotacionMano));

	var matrizRotacionPinza= new THREE.Matrix4();
	var matrizTranslacionPinza= new THREE.Matrix4();
	pinzaIz.matrixAutoUpdate=false;
	matrizRotacionPinza.makeRotationX(-Math.PI/2);
	matrizTranslacionPinza.makeTranslation(25,20-robotController.separacion,10);
	pinzaIz.matrix= matrizTranslacionPinza.multiply(matrizRotacionPinza);

	var matrizRotacionPinzaDe= new THREE.Matrix4();
	var matrizTranslacionPinzaDe= new THREE.Matrix4();
	pinzaDe.matrixAutoUpdate=false;
	matrizRotacionPinzaDe.makeRotationX(Math.PI/2);
	matrizTranslacionPinzaDe.makeTranslation(25,-20+robotController.separacion,-10);
	pinzaDe.matrix= matrizTranslacionPinzaDe.multiply(matrizRotacionPinzaDe);
}

function render(){
    requestAnimationFrame(render);
    update();

    renderer.clear();

    renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
    renderer.render(scene, camera);

}
