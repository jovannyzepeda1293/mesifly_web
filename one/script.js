// Pega aquí la URL del Apps Script publicado (ver apps-script.gs).
const ENDPOINT = "https://script.google.com/macros/s/AKfycbxsf8wo6lpvZgMnVsTs05aFLJB4kQ64Dqm5XgrVB-QGF-NRP-7yawO0rIsoehrvfzEh/exec";
const f = document.getElementById("lead"), msg = document.getElementById("msg");
f?.addEventListener("submit", async e => {
  e.preventDefault();
  if (f.website.value) return; // honeypot anti-bots
  if (ENDPOINT.startsWith("PEGA")) { msg.className = "bad"; msg.textContent = "Formulario aún sin conectar."; return; }
  const b = f.querySelector("button"); b.disabled = true; msg.className = ""; msg.textContent = "Enviando…";
  try {
    // no-cors: Apps Script no devuelve cabeceras CORS; la respuesta es opaca pero el POST llega.
    await fetch(ENDPOINT, { method: "POST", mode: "no-cors", body: new URLSearchParams(new FormData(f)) });
    f.reset(); msg.className = "ok"; msg.textContent = "¡Listo! Estás en la lista. Te avisaremos cuando abramos.";
  } catch { msg.className = "bad"; msg.textContent = "No se pudo enviar. Intenta de nuevo."; }
  b.disabled = false;
});
