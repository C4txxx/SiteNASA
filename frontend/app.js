// Ajusta o máximo do input de data para hoje
const birthdateInput = document.getElementById("birthdate");
const today = new Date().toISOString().slice(0, 10);
birthdateInput.max = today;

const form = document.getElementById("apod-form");
const statusEl = document.getElementById("status");
const imgEl = document.getElementById("apod-image");
const placeholderEl = document.getElementById("placeholder");
const titleEl = document.getElementById("apod-title");
const dateEl = document.getElementById("apod-date");
const explanationEl = document.getElementById("apod-explanation");
const hdLinkEl = document.getElementById("hd-link");

// Altere aqui se o backend estiver em outra URL/porta
const API_BASE_URL = "http://127.0.0.1:8000";

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const birthdate = birthdateInput.value;
  if (!birthdate) {
    statusEl.textContent = "Por favor, selecione sua data de nascimento.";
    statusEl.classList.add("error");
    return;
  }

  statusEl.textContent = "Buscando imagem da NASA...";
  statusEl.classList.remove("error");

  try {
    const response = await fetch(
      `${API_BASE_URL}/apod?date=${encodeURIComponent(birthdate)}`
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const message =
        errorData?.detail ||
        "Não foi possível buscar a imagem. Tente outra data.";
      throw new Error(message);
    }

    const data = await response.json();

    // Atualiza UI
    imgEl.src = data.url;
    imgEl.alt = data.title || "Imagem APOD";
    imgEl.style.display = "block";
    placeholderEl.style.display = "none";

    titleEl.textContent = data.title || "Imagem APOD";
    dateEl.textContent = data.date || "";
    explanationEl.textContent =
      data.explanation || "Descrição não disponível para essa imagem.";

    if (data.hdurl) {
      hdLinkEl.href = data.hdurl;
      hdLinkEl.style.display = "inline-flex";
    } else {
      hdLinkEl.style.display = "none";
    }

    statusEl.textContent = "Imagem carregada com sucesso.";
  } catch (error) {
    console.error(error);
    statusEl.textContent = error.message || "Erro inesperado.";
    statusEl.classList.add("error");
  }
});

