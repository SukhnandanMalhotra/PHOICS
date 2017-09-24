var canvas= document.querySelector('canvas');
canvas.width=500;
canvas.height=500;
 var c = canvas.getContext('2d');
/*var c = canvas.getContext('2d');
c.rect(20,20,40,40);
c.stroke();*/
var width=40;
function animate(){
	requestAnimationFrame(animate);
	c.clearRect(5,5,500,500);
   
    
     c.rect(20,20,width,40);
     c.strokeStyle='red';
     c.stroke();
      width += 5;
      if(width>100){
    	width += 0;
    }
}
animate();