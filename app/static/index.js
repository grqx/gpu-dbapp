document.addEventListener("DOMContentLoaded", function () {
    let cnt = 0;
    const counterElement = document.getElementById("magic-counter");
    const counterBtn = document.getElementById("magic-cntr-btn");
    counterBtn.onclick = () => {
        counterElement.innerHTML = ++cnt;
    };
});
