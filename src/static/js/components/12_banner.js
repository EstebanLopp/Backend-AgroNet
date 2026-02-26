document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".banner");

  if (!container) return;

  const titles = [
    "COMPRA. VENDE. AYUDA.",
    "APOYA. PRODUCE. CRECE.",
    "CONSUME. LOCAL. AHORA."
  ];

  let index = 0;

  const titleElement = container.querySelector(".banner__title");
  const leftArrow = container.querySelector(".banner__arrow--left");
  const rightArrow = container.querySelector(".banner__arrow--right");

  if (!titleElement || !leftArrow || !rightArrow) return;

  const changeText = (i) => {
    titleElement.classList.remove("fade-in");
    void titleElement.offsetWidth;
    titleElement.innerHTML = titles[i].replace(/\./g, ".<br>");
    titleElement.classList.add("fade-in");
  };

  let autoChange = setInterval(() => {
    index = (index + 1) % titles.length;
    changeText(index);
  }, 3000);

  const restartAutoChange = () => {
    clearInterval(autoChange);
    autoChange = setInterval(() => {
      index = (index + 1) % titles.length;
      changeText(index);
    }, 10000);
  };

  leftArrow.addEventListener("click", () => {
    index = (index - 1 + titles.length) % titles.length;
    changeText(index);
    restartAutoChange();
  });

  rightArrow.addEventListener("click", () => {
    index = (index + 1) % titles.length;
    changeText(index);
    restartAutoChange();
  });

  changeText(index);
});