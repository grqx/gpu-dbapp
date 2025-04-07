document.addEventListener("DOMContentLoaded", function () {
    let cnt = 0;
    const counterElement = document.getElementById("magic-counter");
    counterElement.innerHTML = cnt;
    const counterBtn = document.getElementById("magic-cntr-btn");
    counterBtn.onmousedown = (e) => {
        e.preventDefault();
        counterElement.innerHTML = ++cnt;
    };
    counterBtn.oncontextmenu = e => e.preventDefault();
});
