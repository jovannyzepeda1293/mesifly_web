// Google Sheets → Extensiones → Apps Script → pega esto → Implementar → Aplicación web
// (Ejecutar como: yo · Acceso: cualquiera). Copia la URL /exec en script.js (ENDPOINT).
// Debe crearse desde Extensiones → Apps Script de la propia hoja (así no depende del ID).
function doPost(e) {
  const p = e.parameter, s = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (s.getLastRow() === 0) s.appendRow(["Fecha","Nombre","Restaurante","Correo","Teléfono","País","Sucursales","Origen"]);
  const clean = v => String(v || "").slice(0, 200).replace(/^[=+\-@]/, "'$&"); // evita inyección de fórmulas
  s.appendRow([new Date(), clean(p.nombre), clean(p.restaurante), clean(p.correo), clean(p.telefono), clean(p.pais), clean(p.sucursales), "web"]);
  return ContentService.createTextOutput("ok");
}
