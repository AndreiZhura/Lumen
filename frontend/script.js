


const manifestDiv = document.getElementById('manifest');
function showNextLine() {
  if (index < lines.length) {
    const p = document.createElement('p');
    p.textContent = lines[index];
    manifestDiv.appendChild(p);
    index++;
    setTimeout(showNextLine, 1000);
  }
}
function startChat() {
  alert("Переход к ИИ-другу (в будущем подключим диалог).");
}
function askFromHeart() {
  alert("Форма для 'вопроса от сердца' будет доступна позже.");
}
function toggleMusic() {
  const music = document.getElementById('bgMusic');
  const btn = document.getElementById('musicBtn');
  if (music.paused) {
    music.play();
    btn.textContent = "Выключить музыку";
  } else {
    music.pause();
    btn.textContent = "Включить музыку";
  }
}
showNextLine();
