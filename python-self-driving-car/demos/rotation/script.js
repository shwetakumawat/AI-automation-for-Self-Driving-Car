const screen = document.querySelector("#screen");
const angleOutput = document.querySelector("#angle");
const speedCtrl = document.querySelector("#speed");


screen.width = 1000;
screen.height = 700;

/**@type {CanvasRenderingContext2D} */
const ctx = screen.getContext("2d");

function drawQuad(p0, p1, p2, p3, color) {
  const path = new Path2D();
  path.moveTo(origin[0] + p0[0], origin[1] + p0[1]);
  path.lineTo(origin[0] + p1[0], origin[1] + p1[1]);
  path.lineTo(origin[0] + p2[0], origin[1] + p2[1]);
  path.lineTo(origin[0] + p3[0], origin[1] + p3[1]);
  path.lineTo(origin[0] + p0[0], origin[1] + p0[1]);
  path.closePath();
  ctx.fillStyle = color;
  ctx.fill(path);
  ctx.stroke(path);
}

// define a origin so that it's not 0.0 at top left
const origin = [300, 300];

// original points, not mutated
const squarePoints = [
  [100, 100],
  [200, 100],
  [200, 200],
  [100, 200],
];

const originRotatingPoints = structuredClone(squarePoints);
const centerRotatingPoints = structuredClone(squarePoints);

let angle = 0;

const main = () => {
  ctx.clearRect(0, 0, screen.width, screen.height);

  ctx.beginPath();

  // draw the origin point
  ctx.arc(origin[0], origin[1], 5, 0, 2 * Math.PI);
  ctx.stroke();

  // draw rect
  drawQuad(squarePoints[0], squarePoints[1], squarePoints[2], squarePoints[3], "rgba(0, 0, 0, 0.5)");

  // draw rect rotating about the origin
  drawQuad(
    originRotatingPoints[0],
    originRotatingPoints[1],
    originRotatingPoints[2],
    originRotatingPoints[3],
    "rgba(255, 0, 0, 0.5)"
  );
  for (let i = 0; i < squarePoints.length; i++) {
    // rotate the points using the rotation matrix 
    // [x]   [cos(angle) -sin(angle)] [x]
    // [y] = [sin(angle)  cos(angle)] [y]
    originRotatingPoints[i][0] = squarePoints[i][0] * Math.cos(angle) - squarePoints[i][1] * Math.sin(angle);
    originRotatingPoints[i][1] = squarePoints[i][0] * Math.sin(angle) + squarePoints[i][1] * Math.cos(angle);
  }

  // draw rect rotating about its center
  const rectCenter = [150, 150];
  drawQuad(
    centerRotatingPoints[0],
    centerRotatingPoints[1],
    centerRotatingPoints[2],
    centerRotatingPoints[3],
    "rgba(0, 255, 0, 0.5)"
  );
  for (let i = 0; i < squarePoints.length; i++) {
    // first translate the points so that the center of the rect is at the origin
    const translatedPoint = [squarePoints[i][0] - rectCenter[0], squarePoints[i][1] - rectCenter[1]];
    // perform rotation that add the offset back
    centerRotatingPoints[i][0] =
      translatedPoint[0] * Math.cos(angle) - translatedPoint[1] * Math.sin(angle) + rectCenter[0];
    centerRotatingPoints[i][1] =
      translatedPoint[0] * Math.sin(angle) + translatedPoint[1] * Math.cos(angle) + rectCenter[1];
  }

  // change the angle
  angle += 0.05;
  if (angle > 2 * Math.PI) {
    angle = 0;
  }
  angleOutput.value = angle;
}

let intervalId = setInterval(main, 167);

let renderSpeed = 100;
speedCtrl.addEventListener("input", () => {
  renderSpeed = parseFloat(speedCtrl.value);
  clearInterval(intervalId);
  intervalId = setInterval(main, renderSpeed);
  console.log(renderSpeed)
});