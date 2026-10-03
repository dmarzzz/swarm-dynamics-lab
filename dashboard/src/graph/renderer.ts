// One point batch and one line batch, no DOM node per source and no dependency on a scene engine.
export interface Vertex { x:number; y:number; color:string; alpha:number; size:number }
export function renderer(canvas: HTMLCanvasElement) {
 const gl = canvas.getContext('webgl', {alpha:true,antialias:true,premultipliedAlpha:false});
 if(!gl) {
 const ctx=canvas.getContext('2d')!;
 return { mode:'Canvas 2D', draw(points:Vertex[],lines:Vertex[],width:number,height:number,dpr:number) { canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);for(let i=0;i<lines.length;i+=2){ctx.globalAlpha=lines[i].alpha;ctx.strokeStyle=lines[i].color;ctx.beginPath();ctx.moveTo(lines[i].x,lines[i].y);ctx.lineTo(lines[i+1].x,lines[i+1].y);ctx.stroke();}for(const p of points){ctx.globalAlpha=p.alpha;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size/2,0,Math.PI*2);ctx.fill();}ctx.globalAlpha=1;}, dispose(){} };
 }
 const shader=(type:number,source:string)=>{const s=gl.createShader(type)!;gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s)||'Shader compile failed');return s;};
 const vs=shader(gl.VERTEX_SHADER,'attribute vec2 a_position; attribute vec4 a_color; attribute float a_size; uniform vec2 u_resolution; uniform float u_dpr; varying vec4 v_color; void main(){gl_Position=vec4(a_position/u_resolution*vec2(2.,-2.)+vec2(-1.,1.),0.,1.);gl_PointSize=a_size*u_dpr;v_color=a_color;}');
 const fs=shader(gl.FRAGMENT_SHADER,'precision mediump float; varying vec4 v_color; uniform bool u_points; void main(){float a=1.;if(u_points){float d=length(gl_PointCoord-vec2(.5));a=1.-smoothstep(.32,.5,d);}gl_FragColor=vec4(v_color.rgb,v_color.a*a);}');
 const program=gl.createProgram()!;gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);gl.useProgram(program);
 const buffer=gl.createBuffer()!;gl.bindBuffer(gl.ARRAY_BUFFER,buffer);
 for(const [name,size,offset] of [['a_position',2,0],['a_color',4,8],['a_size',1,24]] as const) {const a=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,size,gl.FLOAT,false,28,offset);}
 const resolution=gl.getUniformLocation(program,'u_resolution'),pixelRatio=gl.getUniformLocation(program,'u_dpr'),pointsUniform=gl.getUniformLocation(program,'u_points');
 gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
 let storage=new Float32Array(0); const rgb=new Map<string,number[]>();
 function batch(vertices:Vertex[],points:boolean){if(storage.length<vertices.length*7)storage=new Float32Array(vertices.length*7);let j=0;for(const p of vertices){let c=rgb.get(p.color);if(!c){const n=parseInt(p.color.slice(1),16);c=[(n>>16&255)/255,(n>>8&255)/255,(n&255)/255];rgb.set(p.color,c);}storage[j++]=p.x;storage[j++]=p.y;storage[j++]=c[0];storage[j++]=c[1];storage[j++]=c[2];storage[j++]=p.alpha;storage[j++]=p.size;}gl!.bufferData(gl!.ARRAY_BUFFER,storage.subarray(0,j),gl!.DYNAMIC_DRAW);gl!.uniform1i(pointsUniform,points?1:0);gl!.drawArrays(points?gl!.POINTS:gl!.LINES,0,vertices.length);}
 return {mode:'WebGL',draw(points:Vertex[],lines:Vertex[],width:number,height:number,dpr:number){const w=Math.round(width*dpr),h=Math.round(height*dpr);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}gl.viewport(0,0,w,h);gl.clear(gl.COLOR_BUFFER_BIT);gl.uniform2f(resolution,width,height);gl.uniform1f(pixelRatio,dpr);batch(lines,false);batch(points,true);},dispose(){gl.deleteBuffer(buffer);gl.deleteProgram(program);gl.deleteShader(vs);gl.deleteShader(fs);} };
}
