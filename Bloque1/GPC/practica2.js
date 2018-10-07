
var renderer, scene, camera;

init();
loadScene();
render();

function init(){

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight)
    renderer.setClearColor(new THREE.Color(0xFFFFFF));
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    var aspectRatio = window.innerWidth / window.innerHeight;

	camera = new THREE.PerspectiveCamera(40,aspectRatio,1,2000);
	camera.position.set(350,350,350);
	camera.lookAt(new THREE.Vector3(0,60,0));
}

function loadScene(){


	var robot = new THREE.Object3D();
	var brazo = new THREE.Object3D();
	var antebrazo = new THREE.Object3D();
	var material = new THREE.MeshBasicMaterial( {color: 'red', wireframe: true} );

	// Definición del suelo
	var forma_Suelo = new THREE.PlaneGeometry( 1000, 1000, 10, 10 );
	var suelo = new THREE.Mesh( forma_Suelo, material );

  suelo.rotation.x=-Math.PI/2;

	// Construcción de la base
	var forma_Base = new THREE.CylinderGeometry( 50, 50, 15, 25 );
	var base = new THREE.Mesh( forma_Base, material );

	// Construcción del eje
	var forma_Eje = new THREE.CylinderGeometry( 20, 20, 18, 25 );
	var eje = new THREE.Mesh( forma_Eje, material );
	eje.rotation.x=Math.PI/2;

	// Construcción del espárrago
	var forma_Esparrago = new THREE.BoxGeometry( 18, 120, 12 );
	var esparrago = new THREE.Mesh( forma_Esparrago, material );
	esparrago.position.y=75;

	// Construcción de la rótula
	var forma_Rotula = new THREE.SphereGeometry( 20, 20, 20 );
	var rotula = new THREE.Mesh( forma_Rotula, material );
	rotula.position.y=135;

	// Construcción del disco
	var forma_Disco = new THREE.CylinderGeometry( 22, 22, 6, 25 );
	var disco = new THREE.Mesh( forma_Disco, material );
	disco.position.y=135;

	// Construcción de los nervios
	var forma_primer_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var primer_nervio = new THREE.Mesh( forma_primer_Nervio, material);
	primer_nervio.position.x =10;
	primer_nervio.position.y=175;
	primer_nervio.position.z=10;

	var forma_segundo_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var segundo_nervio = new THREE.Mesh( forma_segundo_Nervio, material );
	segundo_nervio.position.x =10;
	segundo_nervio.position.y=175;
	segundo_nervio.position.z=-10;

	var forma_tercer_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var tercer_nervio = new THREE.Mesh( forma_tercer_Nervio, material );
	tercer_nervio.position.x =-10;
	tercer_nervio.position.y=175;
	tercer_nervio.position.z=-10;

	var forma_cuarto_Nervio = new THREE.BoxGeometry( 4, 80, 4 );
	var cuarto_nervio = new THREE.Mesh( forma_cuarto_Nervio, material );
	cuarto_nervio.position.x =-10;
	cuarto_nervio.position.y=175;
	cuarto_nervio.position.z=10;

	// Construcción de la mano
	var forma_Mano = new THREE.CylinderGeometry( 15, 15, 40, 25 );
	var mano = new THREE.Mesh(forma_Mano, material);
	var matrizRotacionMano= new THREE.Matrix4();
	var matrizTranslacionMano= new THREE.Matrix4();
	mano.matrixAutoUpdate=false;
	matrizRotacionMano.makeRotationX(Math.PI/2);
	matrizTranslacionMano.makeTranslation(0,215,0);
	mano.matrix= matrizTranslacionMano.multiply(matrizRotacionMano);

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


	var pinzaIz = new THREE.Mesh(mallaPinza,material);
	var pinzaDe = new THREE.Mesh(mallaPinza,material);

	var matrizRotacionPinzaIz = new THREE.Matrix4();
	var matrizTranslacionPinzaIz = new THREE.Matrix4();
	pinzaIz.matrixAutoUpdate =false;
	matrizRotacionPinzaIz.makeRotationX(-Math.PI/2);
	matrizTranslacionPinzaIz.makeTranslation(25,20,10);
	pinzaIz.matrix = matrizTranslacionPinzaIz.multiply(matrizRotacionPinzaIz);

	var matrizRotacionPinzaDe = new THREE.Matrix4();
	var matrizTranslacionPinzaDe = new THREE.Matrix4();
	pinzaDe.matrixAutoUpdate = false;
	matrizRotacionPinzaDe.makeRotationX(Math.PI/2);
	matrizTranslacionPinzaDe.makeTranslation(25,-20,-10);
	pinzaDe.matrix = matrizTranslacionPinzaDe.multiply(matrizRotacionPinzaDe);

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

function render(){
    requestAnimationFrame(render);
    renderer.render(scene,camera);
}
