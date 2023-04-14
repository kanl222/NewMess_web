

var engine = Matter.Engine.create();

// create renderer
var render = Matter.Render.create({
    element: document.body,
    engine: engine,
    options: {
        width: window.innerWidth,
        height: window.innerHeight,
        wireframes: false,

    }
});

// update renderer on window resize
window.addEventListener('resize', function () {
    Matter.Render.setPixelRatio(render, window.devicePixelRatio);
    Matter.Render.setStyle(render, 'width', window.innerWidth);
    Matter.Render.setStyle(render, 'height', window.innerHeight);
    Matter.Bounds.update(engine.world.bounds, [
            { x: 0, y: 0 },
            { x: window.innerWidth, y: window.innerHeight }
        ]);
});

// add renderer to the page
Matter.Render.run(render);

// add ground object
var ground = Matter.Bodies.rectangle(window.innerWidth/2, window.innerHeight-25, window.innerWidth, 50, { isStatic: true });
Matter.World.add(engine.world, ground);

var borderOptions = {
    isStatic: true,
    render: {
        fillStyle: '#f4f4f8'
    }
};
var element = document.getElementsByClassName('wrapper');
console.log(element,element[0].offsetHeight, element.clientWidth)
var border = Matter.Bodies.rectangle(window.innerWidth/2, window.innerHeight/2, element[0].offsetWidth, element[0].offsetHeight, { isStatic: true });
Matter.World.add(engine.world, border);

var borderTop = Matter.Bodies.rectangle(window.innerWidth/2, -10, window.innerWidth, 20, borderOptions);
var borderBottom = Matter.Bodies.rectangle(window.innerWidth/2, window.innerHeight+10, window.innerWidth, 20, borderOptions);
var borderLeft = Matter.Bodies.rectangle(-10, window.innerHeight/2, 20, window.innerHeight, borderOptions);
var borderRight = Matter.Bodies.rectangle(window.innerWidth+10, window.innerHeight/2, 20, window.innerHeight, borderOptions);

Matter.World.add(engine.world, [borderTop, borderBottom, borderLeft, borderRight]);

// add rectangle objects
var rectangles = [];
for (var i = 0; i < 10; i++) {
    var rectangle = Matter.Bodies.rectangle(Math.random()*window.innerWidth, Math.random()*window.innerHeight, 50, 50);
    rectangles.push(rectangle);
    Matter.World.add(engine.world, rectangle);
}

// add circular objects
var circles = [];
for (var i = 0; i < 5; i++) {
    var circle = Matter.Bodies.circle(Math.random()*window.innerWidth, Math.random()*window.innerHeight, 20);
    circles.push(circle);
    Matter.World.add(engine.world, circle);
}

// add triangle objects
var triangles = [];
for (var i = 0; i < 5; i++) {
    var triangle = Matter.Bodies.polygon(Math.random()*window.innerWidth, Math.random()*window.innerHeight, 3, 30);
    triangles.push(triangle);
    Matter.World.add(engine.world, triangle);
}

// create mouse constraint
var mouseConstraint = Matter.MouseConstraint.create(engine, {
    element: document.body,
    constraint: {
        render: {
            visible: false
        },
        stiffness: 0.8
    }
});
Matter.World.add(engine.world, mouseConstraint);

// start engine
Matter.Engine.run(engine);
