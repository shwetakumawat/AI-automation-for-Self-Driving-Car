const screen = document.querySelector("#screen");


screen.width = 500;
screen.height = 500;

/**@type {CanvasRenderingContext2D} */
const ctx = screen.getContext("2d");

class Point {
  constructor(x, y, name) {
    this.x = x;
    this.y = y;
    this.name = name;
  }
  draw() {
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.arc(this.x, this.y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 12px Arial"
    ctx.fillText(this.name, this.x, this.y)
  }
}

function lerp(a, b, t) {
  return a + (b - a) * t
}

/**
 * get intersection
 * @param {Point} a - line 1 start
 * @param {Point} b - line 1 end
 * @param {Point} c - line 2 start
 * @param {Point} d - line 2 end
 */
function getIntersect(a, b, c, d) {
  // calculations
  const tTop = (d.x - c.x) * (a.y - c.y) - (d.y - c.y) * (a.x - c.x)
  const uTop = (c.y - a.y) * (a.x - b.x) - (c.x - a.x) * (a.y - b.y)

  // the divisor is the same
  const bottom = (d.y - c.y) * (b.x - a.x) - (d.x - c.x) * (b.y - a.y)

  // console.log(bottom)
  // bottom approaches 0 when the lines approaches parallel

  // if the lines are parallel and not colinear
  if (bottom === 0 ){
    return null;
  }
  
  const t = tTop / bottom;
  const u = uTop / bottom;

  // if the intersection is actually inside the lines
  if (t < 0 || t > 1 || u < 0 || u > 1) {
    return null;
  }

  return {
    point: new Point(
      lerp(a.x, b.x, t),
      lerp(a.y, b.y, t),
      "i"
    ),
    // can be used to calculate how far the intersect is from the starting point
    offset: t,
    u: u
  }
}


const a = new Point(200, 150, 'A');
const b = new Point(150, 250, 'B');
const c = new Point(50, 100, 'C');
const d = new Point(250, 200, 'D');

const points = [
  {pt: a, dragging: false},
  {pt: b, dragging: false},
  {pt: c, dragging: false},
  {pt: d, dragging: false}
];
screen.addEventListener("mousedown", e => {
  for (const point of points) {
    if (e.x < point.pt.x + 10 && 
        e.x > point.pt.x - 10 && 
        e.y < point.pt.y + 10 && 
        e.y > point.pt.y - 10) {
      point.dragging = true;
    }
  }
});

screen.addEventListener("mousemove", e => {
  for (const point of points) {
    if (!point.dragging) continue;
    point.pt.x = e.x;
    point.pt.y = e.y;
  }
})

screen.addEventListener("mouseup", e => {
  for (const point of points) {
    if (point.dragging) {
      point.dragging = false;
    }
  }
})


const tOutput = document.querySelector("#t");
const uOutput = document.querySelector("#u");
const line1Output = document.querySelector("#line1");
const line2Output = document.querySelector("#line2");
const intersectOutput = document.querySelector("#intersect");

function render() {
  ctx.clearRect(0, 0, screen.width, screen.height);
  
  ctx.beginPath();

  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);

  ctx.moveTo(c.x, c.y);
  ctx.lineTo(d.x, d.y);

  ctx.stroke();


  a.draw();
  b.draw();
  c.draw();
  d.draw();

  const intersection = getIntersect(a, b, c, d);
  if (intersection != null) { 
    intersection.point.draw();
  }

  tOutput.value = intersection?.offset ?? "null";
  uOutput.value = intersection?.u ?? "null";
  line1Output.value = `(${a.x}, ${a.y}) to (${b.x}, ${b.y})`;
  line2Output.value = `(${c.x}, ${c.y}) to (${d.x}, ${d.y})`;
  intersectOutput.value = intersection?.point ? `(${intersection.point.x}, ${intersection.point.y})` : "null";

  requestAnimationFrame(render);
}

render();