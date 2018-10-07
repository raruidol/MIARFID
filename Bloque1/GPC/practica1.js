/**
  Practica 01.
  sep,2018
*/

//Shader de vertices
var VSHADER_SOURCE =
'attribute vec3 posicion;                     \n'+
'attribute vec4 color;                        \n'+
'varying highp vec4 vColor;                   \n'+
'void main(){                                 \n'+
' gl_Position= vec4(posicion, 1.0);           \n'+
' gl_PointSize= 10.0;                         \n'+
' vColor = color;                         \n'+
'}                                            \n';

//Shader de fragmentos
var FSHADER_SOURCE =
'varying highp vec4 vColor;                     \n'+
'void main(){                                   \n'+
' gl_FragColor = vColor;                        \n'+
'}                                              \n';

//Globales
var bufferVertices = null;
var bufferColores = null;


function main(){
  //Recuperar el area de dibujo
  var canvas = document.getElementById("canvas");
  if(!canvas){
    console.log("Cyka blyat canvas");
    return;
  }

  //Recuperar el pincel
  var gl = getWebGLContext(canvas);
  if(!gl){
    console.log("C mamo el pinsel");
    return;
  }

  //Fijar el color de borrado
  gl.clearColor(0.0, 0.0, 0.3, 1.0);

  //Cargar, compilar y montar los shaders en un programa en GPU
  if(!initShaders(gl, VSHADER_SOURCE, FSHADER_SOURCE)){
    console.log("Liote en shaders");
    return;
  }

  //Localizar en GPU las variables atributos y uniform
  var coordenadas = gl.getAttribLocation(gl.program, 'posicion');

  //Crea un buffer, lo activa y lo enlaza con 'coordenadas'
  var bufferVertices = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, bufferVertices);
  gl.vertexAttribPointer(coordenadas, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(coordenadas);

  // Localiza el atributo color en el shader
  var colores = gl.getAttribLocation( gl.program, 'color');
  // Crea el buffer, lo activa y enlaza con coordenadas
  bufferColores = gl.createBuffer();
  gl.bindBuffer( gl.ARRAY_BUFFER, bufferColores );
  gl.vertexAttribPointer( colores, 4, gl.FLOAT, false, 0, 0 );
  gl.enableVertexAttribArray( colores );

  //Registrar una call back de raton
  canvas.onmousedown = function(evento){
    click(evento, gl, canvas);
  };

  var clicks = [];
  var coloresClicks = [];
  var colorFragmento;

  function click(evento, gl, canvas){
    //recuperar la posicion del click
    var xorig = evento.clientX;
    var yorig = evento.clientY;

    //Transformacion documento - gl
    var rect = evento.target.getBoundingClientRect();

    var x = ((xorig-rect.left) - canvas.width/2)*2/canvas.width;
    var y = (canvas.height/2 - (yorig-rect.top))*2/canvas.height;

    clicks.push(x); clicks.push(y); clicks.push(0.0);

    var d = 1.0 - Math.sqrt( (x*x + y*y) / 2.0 );
    for( var i = 0; i < 3; i++ ) coloresClicks.push(d);
    coloresClicks.push(1.0);

    render(gl);

  }

  function render(gl){

    var puntos = new Float32Array(clicks); // array de puntos
    var colores = new Float32Array(coloresClicks); // array de colores

    //Pintar el canvas con el color de borrado
    gl.clear(gl.COLOR_BUFFER_BIT);

    //Rellenar el buffer con las coordenadas de los clicks y
    //mandarlo a procesar al shader de vertices
    gl.bindBuffer( gl.ARRAY_BUFFER, bufferVertices );
    gl.bufferData( gl.ARRAY_BUFFER, puntos, gl.STATIC_DRAW );
    gl.bindBuffer( gl.ARRAY_BUFFER, bufferColores );
    gl.bufferData( gl.ARRAY_BUFFER, colores, gl.STATIC_DRAW );
    gl.drawArrays( gl.POINTS, 0, puntos.length/3 )
    gl.drawArrays( gl.LINE_STRIP, 0, puntos.length/3 )

  }
}
