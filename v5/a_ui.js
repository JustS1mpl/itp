/* ===================== ИТП 6 — интерфейс: оболочка, Путь, Практика, Профиль, Настройки =====================
   Экраны строятся только из данных TOPICS: число тем, число и порядок островков любые,
   новая тема появляется на Пути сама. Ничего о конкретных темах здесь не записано. */
var ITPV='__VER__';

/* --- значки интерфейса: рисуются кодом (SVG), цвет берут из currentColor --- */
var IC={
 path:'<path class="f" d="M3 6.5a3.5 3.5 0 1 0 7 0 3.5 3.5 0 0 0-7 0zM14 17.5a3.5 3.5 0 1 0 7 0 3.5 3.5 0 0 0-7 0z" fill="currentColor" stroke="none"/><circle cx="6.5" cy="6.5" r="2.6"/><circle cx="17.5" cy="17.5" r="2.6"/><path d="M9.1 6.5H15a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h5.9"/>',
 prac:'<circle class="f" cx="12" cy="12" r="9" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/>',
 code:'<rect class="f" x="2.5" y="4" width="19" height="16" rx="4" fill="currentColor" stroke="none"/><path d="M8.5 8.5 5 12l3.5 3.5M15.5 8.5 19 12l-3.5 3.5M13.2 6.8l-2.4 10.4"/>',
 bun:'<path class="f" d="M12 21c4 0 7-2.3 7-5.5S16 9.6 12 9.6 5 12.3 5 15.5 8 21 12 21z" fill="currentColor" stroke="none"/><path d="M12 21c4 0 7-2.3 7-5.5S16 9.6 12 9.6 5 12.3 5 15.5 8 21 12 21z"/><path d="M9.6 10C8.3 6.9 7.9 3.4 9.3 3s2.7 3.1 2.9 6.6M14.4 10c1.3-3.1 1.7-6.6.3-7s-2.7 3.1-2.9 6.6"/><circle cx="9.7" cy="15.2" r=".95" fill="currentColor" stroke="none"/><circle cx="14.3" cy="15.2" r=".95" fill="currentColor" stroke="none"/>',
 chev:'<path d="m9 6 6 6-6 6"/>',
 down:'<path d="m6 9 6 6 6-6"/>',
 back:'<path d="M15 5 8 12l7 7"/>',
 x:'<path d="M6 6l12 12M18 6 6 18"/>',
 play:'<path d="M7 5.2v13.6a1 1 0 0 0 1.5.86l11-6.8a1 1 0 0 0 0-1.72l-11-6.8A1 1 0 0 0 7 5.2z" fill="currentColor" stroke="none"/>',
 bulb:'<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0 0 12 3z"/>',
 more:'<circle cx="5" cy="12" r="1.6" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.6" fill="currentColor" stroke="none"/>',
 file:'<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
 check:'<path d="m5 12.5 4.5 4.5L19 7.5"/>',
 lock:'<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 arrow:'<path d="M12 5v14M6 13l6 6 6-6"/>',
 search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
 gear:'<circle cx="12" cy="12" r="3.2"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/>'
};
/* значки Phosphor Icons (MIT, github.com/phosphor-icons/core 2.1.1): duotone — контур и полупрозрачная заливка, check — bold.
   Один стиль для галочек серии, вех «Что ты уже умеешь», подсказки и «Поделиться» */
var PH={'download-simple':'<path d="M216,48V208H40V48A16,16,0,0,1,56,32H200A16,16,0,0,1,216,48Z" class="d" opacity="0.2"/><path d="M224,144v64a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8V144a8,8,0,0,1,16,0v56H208V144a8,8,0,0,1,16,0Zm-101.66,5.66a8,8,0,0,0,11.32,0l40-40a8,8,0,0,0-11.32-11.32L136,124.69V32a8,8,0,0,0-16,0v92.69L93.66,98.34a8,8,0,0,0-11.32,11.32Z"/>','address-book':'<path d="M208,32H64a8,8,0,0,0-8,8V216a8,8,0,0,0,8,8H208a8,8,0,0,0,8-8V40A8,8,0,0,0,208,32ZM136,144a32,32,0,1,1,32-32A32,32,0,0,1,136,144Z" class="d" opacity="0.2"/><path d="M83.19,174.4a8,8,0,0,0,11.21-1.6,52,52,0,0,1,83.2,0,8,8,0,1,0,12.8-9.6A67.88,67.88,0,0,0,163,141.51a40,40,0,1,0-53.94,0A67.88,67.88,0,0,0,81.6,163.2,8,8,0,0,0,83.19,174.4ZM112,112a24,24,0,1,1,24,24A24,24,0,0,1,112,112Zm96-88H64A16,16,0,0,0,48,40V64H32a8,8,0,0,0,0,16H48v40H32a8,8,0,0,0,0,16H48v40H32a8,8,0,0,0,0,16H48v24a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V40A16,16,0,0,0,208,24Zm0,192H64V40H208Z"/>',
 'calculator':'<path d="M176,64v48H80V64Z" class="d" opacity="0.2"/><path d="M80,120h96a8,8,0,0,0,8-8V64a8,8,0,0,0-8-8H80a8,8,0,0,0-8,8v48A8,8,0,0,0,80,120Zm8-48h80v32H88ZM200,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V40A16,16,0,0,0,200,24Zm0,192H56V40H200ZM100,148a12,12,0,1,1-12-12A12,12,0,0,1,100,148Zm40,0a12,12,0,1,1-12-12A12,12,0,0,1,140,148Zm40,0a12,12,0,1,1-12-12A12,12,0,0,1,180,148Zm-80,40a12,12,0,1,1-12-12A12,12,0,0,1,100,188Zm40,0a12,12,0,1,1-12-12A12,12,0,0,1,140,188Zm40,0a12,12,0,1,1-12-12A12,12,0,0,1,180,188Z"/>',
 'chart-bar':'<path d="M208,40V208H152V40Z" class="d" opacity="0.2"/><path d="M224,200h-8V40a8,8,0,0,0-8-8H152a8,8,0,0,0-8,8V80H96a8,8,0,0,0-8,8v40H48a8,8,0,0,0-8,8v64H32a8,8,0,0,0,0,16H224a8,8,0,0,0,0-16ZM160,48h40V200H160ZM104,96h40V200H104ZM56,144H88v56H56Z"/>',
 'chat-circle-text':'<path d="M224,128A96,96,0,0,1,79.93,211.11h0L42.54,223.58a8,8,0,0,1-10.12-10.12l12.47-37.39h0A96,96,0,1,1,224,128Z" class="d" opacity="0.2"/><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,210.93a16,16,0,0,0,20.24,20.24l34.05-11.35A104,104,0,1,0,128,24Zm0,192a87.87,87.87,0,0,1-44.06-11.81,8,8,0,0,0-4-1.08,7.85,7.85,0,0,0-2.53.42L40,216,52.47,178.6a8,8,0,0,0-.66-6.54A88,88,0,1,1,128,216Zm40-104a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,112Zm0,32a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,144Z"/>',
 'check':'<path d="M232.49,80.49l-128,128a12,12,0,0,1-17,0l-56-56a12,12,0,1,1,17-17L96,183,215.51,63.51a12,12,0,0,1,17,17Z"/>',
 'export':'<path d="M208,104V216H48V104Z" class="d" opacity="0.2"/><path d="M216,112v96a16,16,0,0,1-16,16H56a16,16,0,0,1-16-16V112A16,16,0,0,1,56,96H80a8,8,0,0,1,0,16H56v96H200V112H176a8,8,0,0,1,0-16h24A16,16,0,0,1,216,112ZM93.66,69.66,120,43.31V136a8,8,0,0,0,16,0V43.31l26.34,26.35a8,8,0,0,0,11.32-11.32l-40-40a8,8,0,0,0-11.32,0l-40,40A8,8,0,0,0,93.66,69.66Z"/>',
 'folder-open':'<path d="M208,88v24H69.77a8,8,0,0,0-7.59,5.47L32,208V64a8,8,0,0,1,8-8H93.33a8,8,0,0,1,4.8,1.6L128,80h72A8,8,0,0,1,208,88Z" class="d" opacity="0.2"/><path d="M245,110.64A16,16,0,0,0,232,104H216V88a16,16,0,0,0-16-16H130.67L102.94,51.2a16.14,16.14,0,0,0-9.6-3.2H40A16,16,0,0,0,24,64V208a8,8,0,0,0,8,8H211.1a8,8,0,0,0,7.59-5.47l28.49-85.47A16.05,16.05,0,0,0,245,110.64ZM93.34,64,123.2,86.4A8,8,0,0,0,128,88h72v16H69.77a16,16,0,0,0-15.18,10.94L40,158.7V64Zm112,136H43.1l26.67-80H232Z"/>',
 'game-controller':'<path d="M216.86,207.57a28,28,0,0,1-24.66-7.77L150.09,152H172a51.94,51.94,0,0,0,51.2-61h0l16.36,84.17A28,28,0,0,1,216.86,207.57Z" class="d" opacity="0.2"/><path d="M176,112H152a8,8,0,0,1,0-16h24a8,8,0,0,1,0,16ZM104,96H96V88a8,8,0,0,0-16,0v8H72a8,8,0,0,0,0,16h8v8a8,8,0,0,0,16,0v-8h8a8,8,0,0,0,0-16ZM241.48,200.65a36,36,0,0,1-54.94,4.81c-.12-.12-.24-.24-.35-.37L146.48,160h-37L69.81,205.09l-.35.37A36.08,36.08,0,0,1,44,216,36,36,0,0,1,8.56,173.75a.68.68,0,0,1,0-.14L24.93,89.52A59.88,59.88,0,0,1,83.89,40H172a60.08,60.08,0,0,1,59,49.25c0,.06,0,.12,0,.18l16.37,84.17a.68.68,0,0,1,0,.14A35.74,35.74,0,0,1,241.48,200.65ZM172,144a44,44,0,0,0,0-88H83.89A43.9,43.9,0,0,0,40.68,92.37l0,.13L24.3,176.59A20,20,0,0,0,58,194.3l41.92-47.59a8,8,0,0,1,6-2.71Zm59.7,32.59-8.74-45A60,60,0,0,1,172,160h-4.2L198,194.31a20.09,20.09,0,0,0,17.46,5.39,20,20,0,0,0,16.23-23.11Z"/>',
 'graduation-cap':'<path d="M216,113.07v53.22a8,8,0,0,1-2,5.31c-11.3,12.59-38.9,36.4-86,36.4s-74.68-23.81-86-36.4a8,8,0,0,1-2-5.31V113.07L128,160Z" class="d" opacity="0.2"/><path d="M251.76,88.94l-120-64a8,8,0,0,0-7.52,0l-120,64a8,8,0,0,0,0,14.12L32,117.87v48.42a15.91,15.91,0,0,0,4.06,10.65C49.16,191.53,78.51,216,128,216a130,130,0,0,0,48-8.76V240a8,8,0,0,0,16,0V199.51a115.63,115.63,0,0,0,27.94-22.57A15.91,15.91,0,0,0,224,166.29V117.87l27.76-14.81a8,8,0,0,0,0-14.12ZM128,200c-43.27,0-68.72-21.14-80-33.71V126.4l76.24,40.66a8,8,0,0,0,7.52,0L176,143.47v46.34C163.4,195.69,147.52,200,128,200Zm80-33.75a97.83,97.83,0,0,1-16,14.25V134.93l16-8.53ZM188,118.94l-.22-.13-56-29.87a8,8,0,0,0-7.52,14.12L171,128l-43,22.93L25,96,128,41.07,231,96Z"/>',
 'keyboard':'<path d="M232,64V192a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V64a8,8,0,0,1,8-8H224A8,8,0,0,1,232,64Z" class="d" opacity="0.2"/><path d="M224,48H32A16,16,0,0,0,16,64V192a16,16,0,0,0,16,16H224a16,16,0,0,0,16-16V64A16,16,0,0,0,224,48Zm0,144H32V64H224V192Zm-16-64a8,8,0,0,1-8,8H56a8,8,0,0,1,0-16H200A8,8,0,0,1,208,128Zm0-32a8,8,0,0,1-8,8H56a8,8,0,0,1,0-16H200A8,8,0,0,1,208,96ZM72,160a8,8,0,0,1-8,8H56a8,8,0,0,1,0-16h8A8,8,0,0,1,72,160Zm96,0a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,160Zm40,0a8,8,0,0,1-8,8h-8a8,8,0,0,1,0-16h8A8,8,0,0,1,208,160Z"/>',
 'lightbulb':'<path d="M208,104a79.86,79.86,0,0,1-30.59,62.92A24.29,24.29,0,0,0,168,186v6a8,8,0,0,1-8,8H96a8,8,0,0,1-8-8v-6a24.11,24.11,0,0,0-9.3-19A79.87,79.87,0,0,1,48,104.45C47.76,61.09,82.72,25,126.07,24A80,80,0,0,1,208,104Z" class="d" opacity="0.2"/><path d="M176,232a8,8,0,0,1-8,8H88a8,8,0,0,1,0-16h80A8,8,0,0,1,176,232Zm40-128a87.55,87.55,0,0,1-33.64,69.21A16.24,16.24,0,0,0,176,186v6a16,16,0,0,1-16,16H96a16,16,0,0,1-16-16v-6a16,16,0,0,0-6.23-12.66A87.59,87.59,0,0,1,40,104.49C39.74,56.83,78.26,17.14,125.88,16A88,88,0,0,1,216,104Zm-16,0a72,72,0,0,0-73.74-72c-39,.92-70.47,33.39-70.26,72.39a71.65,71.65,0,0,0,27.64,56.3A32,32,0,0,1,96,186v6h64v-6a32.15,32.15,0,0,1,12.47-25.35A71.65,71.65,0,0,0,200,104Zm-16.11-9.34a57.6,57.6,0,0,0-46.56-46.55,8,8,0,0,0-2.66,15.78c16.57,2.79,30.63,16.85,33.44,33.45A8,8,0,0,0,176,104a9,9,0,0,0,1.35-.11A8,8,0,0,0,183.89,94.66Z"/>',
 'plant':'<path d="M138.54,149.46C106.62,96.25,149.18,43.05,239.63,48.37,245,138.82,191.75,181.39,138.54,149.46ZM16.26,88.26c-3.8,64.61,34.21,95,72.21,72.21C111.27,122.47,80.87,84.46,16.26,88.26Z" class="d" opacity="0.2"/><path d="M247.63,47.89a8,8,0,0,0-7.52-7.52c-51.76-3-93.32,12.74-111.18,42.22-11.8,19.48-11.78,43.16-.16,65.74a71.37,71.37,0,0,0-14.17,26.95L98.33,159c7.82-16.33,7.52-33.36-1-47.49C84.09,89.73,53.62,78,15.79,80.27a8,8,0,0,0-7.52,7.52c-2.23,37.83,9.46,68.3,31.25,81.5A45.82,45.82,0,0,0,63.44,176,54.58,54.58,0,0,0,87,170.33l25,25V224a8,8,0,0,0,16,0V194.51a55.61,55.61,0,0,1,12.27-35,73.91,73.91,0,0,0,33.31,8.4,60.9,60.9,0,0,0,31.83-8.86C234.89,141.21,250.67,99.65,247.63,47.89ZM86.06,146.74l-24.41-24.4a8,8,0,0,0-11.31,11.31l24.41,24.41c-9.61,3.18-18.93,2.39-26.94-2.46C32.47,146.31,23.79,124.32,24,96c28.31-.25,50.31,8.47,59.6,23.81C88.45,127.82,89.24,137.14,86.06,146.74Zm111.06-1.36c-13.4,8.11-29.15,8.73-45.15,2l53.69-53.7a8,8,0,0,0-11.31-11.32L140.65,136c-6.76-16-6.15-31.76,2-45.15,13.94-23,47-35.8,89.33-34.83C232.94,98.34,220.14,131.44,197.12,145.38Z"/>',
 'ranking':'<path d="M40,96H88V208H32V104A8,8,0,0,1,40,96Zm176,40H168v72h56V144A8,8,0,0,0,216,136Z" class="d" opacity="0.2"/><path d="M112.41,102.53a8,8,0,0,1,5.06-10.12l12-4A8,8,0,0,1,140,96v40a8,8,0,0,1-16,0V107.1l-1.47.49A8,8,0,0,1,112.41,102.53ZM248,208a8,8,0,0,1-8,8H16a8,8,0,0,1,0-16h8V104A16,16,0,0,1,40,88H80V56A16,16,0,0,1,96,40h64a16,16,0,0,1,16,16v72h40a16,16,0,0,1,16,16v56h8A8,8,0,0,1,248,208Zm-72-64v56h40V144ZM96,200h64V56H96Zm-56,0H80V104H40Z"/>',
 'repeat':'<path d="M224,64v64a64,64,0,0,1-64,64H32V128A64,64,0,0,1,96,64Z" class="d" opacity="0.2"/><path d="M24,128A72.08,72.08,0,0,1,96,56H204.69L194.34,45.66a8,8,0,0,1,11.32-11.32l24,24a8,8,0,0,1,0,11.32l-24,24a8,8,0,0,1-11.32-11.32L204.69,72H96a56.06,56.06,0,0,0-56,56,8,8,0,0,1-16,0Zm200-8a8,8,0,0,0-8,8,56.06,56.06,0,0,1-56,56H51.31l10.35-10.34a8,8,0,0,0-11.32-11.32l-24,24a8,8,0,0,0,0,11.32l24,24a8,8,0,0,0,11.32-11.32L51.31,200H160a72.08,72.08,0,0,0,72-72A8,8,0,0,0,224,120Z"/>',
 'robot':'<path d="M200,56H56A24,24,0,0,0,32,80V192a24,24,0,0,0,24,24H200a24,24,0,0,0,24-24V80A24,24,0,0,0,200,56ZM164,184H92a20,20,0,0,1,0-40h72a20,20,0,0,1,0,40Z" class="d" opacity="0.2"/><path d="M200,48H136V16a8,8,0,0,0-16,0V48H56A32,32,0,0,0,24,80V192a32,32,0,0,0,32,32H200a32,32,0,0,0,32-32V80A32,32,0,0,0,200,48Zm16,144a16,16,0,0,1-16,16H56a16,16,0,0,1-16-16V80A16,16,0,0,1,56,64H200a16,16,0,0,1,16,16ZM72,108a12,12,0,1,1,12,12A12,12,0,0,1,72,108Zm88,0a12,12,0,1,1,12,12A12,12,0,0,1,160,108Zm4,28H92a28,28,0,0,0,0,56h72a28,28,0,0,0,0-56Zm-24,16v24H116V152ZM80,164a12,12,0,0,1,12-12h8v24H92A12,12,0,0,1,80,164Zm84,12h-8V152h8a12,12,0,0,1,0,24Z"/>',
 'sword':'<path d="M141.66,201,129,213.66a8,8,0,0,1-11.32,0L92,188,58.35,221.66a8,8,0,0,1-11.32,0L34.34,209a8,8,0,0,1,0-11.31L68,164,42.34,138.36a8,8,0,0,1,0-11.32L55,114.34a8,8,0,0,1,11.32,0l75.3,75.3A8,8,0,0,1,141.66,201Z" class="d" opacity="0.2"/><path d="M216,32H152a8,8,0,0,0-6.34,3.12l-64,83.21L72,108.69a16,16,0,0,0-22.64,0l-12.69,12.7a16,16,0,0,0,0,22.63l20,20-28,28a16,16,0,0,0,0,22.63l12.69,12.68a16,16,0,0,0,22.62,0l28-28,20,20a16,16,0,0,0,22.64,0l12.69-12.7a16,16,0,0,0,0-22.63l-9.64-9.64,83.21-64A8,8,0,0,0,224,104V40A8,8,0,0,0,216,32ZM52.69,216,40,203.32l28-28L80.68,188Zm70.61-8L48,132.71,60.7,120,136,195.31ZM208,100.06l-81.74,62.88L115.32,152l50.34-50.34a8,8,0,0,0-11.32-11.31L104,140.68,93.07,129.74,155.94,48H208Z"/>'};
function phi(n,cls){return'<svg class="phi'+(cls?' '+cls:'')+'" viewBox="0 0 256 256" width="24" height="24" fill="currentColor" aria-hidden="true" focusable="false">'+PH[n]+'</svg>'}
function ico(n,cls){return'<svg class="'+(cls||'')+'" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+IC[n]+'</svg>'}
/* знак приложения: тот же наклонный шестиугольник-остров, что и на Пути */

/* --- кролик (картинка встроена в файл) --- */
function rabbit(st){var s=IMG[st]||(st==='rolled'?IMG.grump||IMG.grumphead:IMG.eat);return'<div class="rw im '+st+'"><img src="'+s+'" alt="" draggable="false"></div>'}
/* тень под лапами: где стоят лапы, считается по пикселям каждого спрайта (нижние непрозрачные ряды), а не подгоняется
   на глаз — так тень всегда ровно под кроликом, и у нового спрайта тоже. FEET[src] = {l, r, y} в долях картинки */
var FEET={};
function feetOf(src,cb){
  if(FEET[src])return cb&&cb(FEET[src]);
  var im=new Image();im.onload=function(){try{
    var W=Math.min(240,im.naturalWidth),H=Math.round(W*im.naturalHeight/im.naturalWidth),c=document.createElement('canvas');c.width=W;c.height=H;
    var x=c.getContext('2d');x.drawImage(im,0,0,W,H);var d=x.getImageData(0,0,W,H).data,yb=-1,X,Y;
    for(Y=H-1;Y>=0&&yb<0;Y--)for(X=0;X<W;X++)if(d[(Y*W+X)*4+3]>140){yb=Y;break}
    if(yb<0)return;
    var l=W,r=0,band=Math.max(2,Math.round(H*.06));
    for(Y=yb;Y>yb-band&&Y>=0;Y--)for(X=0;X<W;X++)if(d[(Y*W+X)*4+3]>140){if(X<l)l=X;if(X>r)r=X}
    FEET[src]={l:l/W,r:(r+1)/W,y:(yb+1)/H};if(cb)cb(FEET[src])}catch(e){}};im.src=src}
function feetCss(){
  var css='';
  ['eat','happy','grump','rolled','wow','cool'].forEach(function(st){var s=IMG[st]||(st==='rolled'?IMG.grump||IMG.grumphead:null);if(!s)return;
    feetOf(s,function(f){var pad=(f.r-f.l)*.12,L=Math.max(0,f.l-pad),R=Math.max(0,1-f.r-pad);
      css+=':root:not([data-theme=dark]) .rw.im.'+st+'::after{left:'+(L*100).toFixed(1)+'%;right:'+(R*100).toFixed(1)+'%;bottom:'+((1-f.y)*100-4).toFixed(1)+'%}\n';
      var el=document.getElementById('feet');if(!el){el=document.createElement('style');el.id='feet';document.head.appendChild(el)}el.textContent=css})})}
feetCss();
/* окончания по выбранному обращению: m — парень, f — девушка, n — нейтрально (если не указано) */
function G(m,f,n){return S.g==='f'?f:S.g==='m'?m:(n===undefined?m:n)}
function tabFn(){return({home:home,pr:practice,ed:editor,prof:profile})[CURTAB]||home}
var SBACK=null,SKEY='';
/* show() с подсказкой, какой это экран: по ней выбирается направление перехода */
function scr(key,h,tab){SKEY=key;show(h,tab)}

/* --- шапка: «ИТП» слева открывает настройки, справа серия и опыт --- */
function head(){
  var f=S.fz.n,s=streakNow();
  return'<div class="top"><button class="logo" id="ttl" aria-label="ИТП. Открыть настройки">'+'<span class="lgw">ИТП</span>'+'</button><div class="chips"><button class="chip" id="hs" aria-label="Серия: '+s+' '+pl(s,['день','дня','дней'])+(f?', заморозок: '+f:'')+'">🥕 <span>'+s+'</span>'+(f?'<span class="fzm">❄️'+f+'</span>':'')+'</button><button class="chip" id="hx" aria-label="Опыт: '+S.xp+'">⭐ <span>'+S.xp+'</span></button></div></div>'}
/* шапка вложенных экранов: значок экрана в плашке, заголовок с подписью, справа — своё для экрана (кольцо прогресса), если есть.
   Серию и опыт тут не показываем: они только на четырёх вкладках (владелец) */
function subTop(t,em,sub,back,c,n){
  return'<div class="top ls sub"><button class="icon" id="x" aria-label="'+(back||'Назад')+'">'+ico('back')+'</button><div class="stw"><span class="sti" aria-hidden="true">'+em+'</span><div class="stt"><h1>'+esc(t)+'</h1>'+(sub?'<p>'+sub+'</p>':'')+'</div></div>'+
   (n?'<div class="ring" style="--p:'+Math.round(c/n*100)+'" role="img" aria-label="'+c+' из '+n+'"><span>'+c+'/'+n+'</span></div>':'')+'</div>'}
function ttl(t,sub){return'<div class="ttl"><div><h1>'+esc(t)+'</h1>'+(sub?'<p class="mu">'+sub+'</p>':'')+'</div></div>'}
function bindHead(re){
  HRE=re;$('hs').onclick=streakSheet;$('hx').onclick=levelSheet;chipFx();
  $('ttl').onclick=function(){SBACK=tabFn();settings()}}
/* тонкая линия под шапкой появляется, когда страницу прокрутили */
(function(){var m=document.createElement('i');m.setAttribute('aria-hidden','true');m.style.cssText='position:absolute;top:0;left:0;width:1px;height:6px;pointer-events:none';document.body.prepend(m);
  if(window.IntersectionObserver)new IntersectionObserver(function(e){document.documentElement.classList.toggle('scr',!e[0].isIntersecting)}).observe(m)})();

/* --- серия, заморозки, уровень --- */
/* U1-12: галочка дня серии — значок check из Phosphor (bold), без символа ✓ из шрифта */
var WCHK=phi('check','wck');
function weekRow(mode){
  var w=wkStart(),t=day(new Date()),nm=['Пн','Вт','Ср','Чт','Пт','Сб','Вс'],h='<div class="wk" role="list" aria-label="Эта неделя">';
  for(var i=0;i<7;i++){
    var d=dadd(w,i),a=S.hist[d]&&S.hist[d].les>0,fz=S.fz.u.indexOf(d)>=0&&!a,g=!!S.gm[d],cl,ic,st;
    if(mode==='g'){cl=g?'on':(d>t?'fu':'');ic=g?WCHK:'';st=g?'цель выполнена':'нет'}
    else{cl=a?'on':fz?'fz':(d>t?'fu':'');ic=a?WCHK:fz?'❄️':'';st=a?'занимался':fz?'заморозка':'нет'}
    h+='<div class="wd '+cl+(d===t?' td':'')+'" role="listitem" aria-label="'+nm[i]+': '+st+'"><span aria-hidden="true">'+nm[i]+'</span><i aria-hidden="true">'+ic+'</i></div>'}
  return h+'</div>'}
function fzLeft(){return 15-S.fz.p}
function streakSheet(){
  var s=streakNow(),f=S.fz,l=fzLeft();
  modal('<div class="ssh"><h2 class="sr-only">Серия</h2><div class="big">🥕 <b>'+s+'</b></div><p class="mu" style="text-align:center;margin:0">'+(s?pl(s,['день','дня','дней'])+' подряд':'Пройди островок сегодня, и серия начнётся')+'</p>'+weekRow('a')+'<div class="fzr"><div class="fzi">'+[0,1].map(function(i){return'<span class="fzs'+(i<f.n?' on':'')+'" aria-hidden="true">❄️</span>'}).join('')+'</div><div class="fzt"><b>Заморозки: '+f.n+' из 2</b><span class="mu">'+(f.n>=2?'Максимум. Заморозка потратится сама, если пропустишь день.':'Новая через '+l+' '+pl(l,['островок','островка','островков'])+'. Тратится сама, если пропустишь день.')+'</span></div></div><p class="mu" style="text-align:center;margin:0">Рекорд серии: '+Math.max(S.max,s)+'</p></div>',[['Понятно']])}
function levelSheet(){
  var L=lvlInfo(S.xp);
  modal('<div class="ssh"><h2 class="sr-only">Опыт и уровень</h2><div class="big">⭐ <b>'+S.xp+'</b></div><p class="mu" style="text-align:center;margin:0">Уровень '+L.l+'</p><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+L.p+'" aria-label="Прогресс уровня"><i class="grow" style="width:'+L.p+'%"></i></div><p class="mu" style="text-align:center;margin:0">До уровня '+(L.l+1)+': ещё '+L.left+' ⭐</p></div>',[['Понятно']])}

/* --- переход «введение → курс» --- */
function reveal(){
  var rm=RM();REV=1;home();REV=0;
  var gc0=app.querySelector('.gcard');if(gc0)gc0.classList.add('rv');
  var intro=app.querySelector('.topic.intro'),rest=[].slice.call(app.querySelectorAll('.topic.rv,.gcard.rv'));
  window.scrollTo(0,0);
  var ov=null,anims=[],tms=[],ended=false;
  function T(f,ms){tms.push(setTimeout(f,ms))}
  function A(el,kf,op){var a=el.animate(kf,op);anims.push(a);return a}
  function end(){
    if(ended)return;ended=true;tms.forEach(clearTimeout);anims.forEach(function(a){try{a.cancel()}catch(e){}});
    if(ov){ov.remove();ov=null}
    if(intro&&intro.parentNode)intro.remove();
    rest.forEach(function(e){e.classList.remove('rv')});
    window.scrollTo(0,0);var c=app.querySelector('.isl.cur');if(c)c.scrollIntoView({block:'center'});
    links();jumpWatch();
  }
  if(!intro||!rest.length){end();return}
  if(rm){
    A(intro,[{opacity:1},{opacity:0}],{duration:400,fill:'forwards'});
    rest.forEach(function(e,k){A(e,[{opacity:0},{opacity:1}],{duration:500,delay:400+k*120,fill:'both'})});
    T(end,1300);return}
  var ib=intro.querySelector('.isl');
  /* центр считаем по раскладке (offset*), а не по getBoundingClientRect: при переходе экрана #app ещё едет (transform), и вспышка стартовала не из центра */
  var lx=0,ly=0,le=ib;while(le){lx+=le.offsetLeft;ly+=le.offsetTop;le=le.offsetParent}
  var cx=lx+ib.offsetWidth/2-window.pageXOffset,cy=ly+ib.offsetHeight/2-window.pageYOffset;
  var rc=getComputedStyle(ib).getPropertyValue('--ti').trim()||'#3D7FEA';
  var cols=[rc,rc,'var(--gold)','var(--carrot)','#fff'];
  ov=document.createElement('div');ov.id='rvfx';ov.style.setProperty('--rc',rc);
  var h='<i class="bl"></i><i class="rn"></i><i class="rn"></i><i class="rn"></i>';
  for(var n=0;n<18;n++)h+='<i class="pt"></i>';
  ov.innerHTML=h;document.body.appendChild(ov);ov.onclick=end;
  [].forEach.call(ov.children,function(e){e.style.left=cx+'px';e.style.top=cy+'px'});
  var X='translate(-50%,-50%) ';
  snd('ach');
  A(ov.querySelector('.bl'),[{opacity:0,transform:X+'scale(.3)'},{opacity:1,transform:X+'scale(1.4)',offset:.3},{opacity:0,transform:X+'scale(4.2)'}],{duration:1500,easing:'cubic-bezier(.2,.7,.2,1)',fill:'both'});
  [].forEach.call(ov.querySelectorAll('.rn'),function(r,k){A(r,[{opacity:.9,transform:X+'scale(.5)'},{opacity:0,transform:X+'scale(3.6)'}],{duration:1200,delay:k*170,easing:'cubic-bezier(.15,.7,.2,1)',fill:'both'})});
  [].forEach.call(ov.querySelectorAll('.pt'),function(p,k){
    var ang=Math.random()*6.283,d=70+Math.random()*120,sz=3+Math.random()*4;
    p.style.width=p.style.height=sz+'px';p.style.color=cols[k%cols.length];
    A(p,[{opacity:0,transform:X+'translate(0,0) scale(.4)'},{opacity:1,transform:X+'translate('+Math.cos(ang)*d*.55+'px,'+Math.sin(ang)*d*.55+'px) scale(1)',offset:.35},{opacity:0,transform:X+'translate('+Math.cos(ang)*d+'px,'+(Math.sin(ang)*d-26)+'px) scale(.2)'}],{duration:900+Math.random()*600,delay:120+k*22,easing:'cubic-bezier(.2,.7,.3,1)',fill:'both'})});
  A(ib,[{transform:'scale(1)',filter:'brightness(1)'},{transform:'scale(1.14)',filter:'brightness(1.18)',offset:.4},{transform:'scale(1)',filter:'brightness(1)'}],{duration:800,easing:'cubic-bezier(.3,1.3,.5,1)'});
  T(function(){A(intro,[{opacity:1,transform:'none',filter:'blur(0)'},{opacity:0,transform:'translateY(-16px) scale(.97)',filter:'blur(6px)'}],{duration:520,easing:'cubic-bezier(.5,0,.8,.5)',fill:'forwards'})},700);
  var k2=0;
  T(function(){
    intro.style.display='none';window.scrollTo(0,0);snd('level');
    rest.forEach(function(e,k){A(e,[{opacity:0,transform:'translateY(30px) scale(.97)',filter:'blur(8px)'},{opacity:1,transform:'none',filter:'blur(0)'}],{duration:800,delay:k*140,easing:'cubic-bezier(.2,.8,.2,1)',fill:'both'})});
    rest.forEach(function(e){[].forEach.call(e.querySelectorAll('.ilw'),function(il){if(k2>14)return;A(il,[{opacity:0,scale:'.55'},{opacity:1,scale:'1.06',offset:.7},{opacity:1,scale:'1'}],{duration:620,delay:520+(k2++)*95,easing:'cubic-bezier(.3,1.1,.5,1)',fill:'both'})})});
  },1230);
  T(end,1230+1500+Math.min(rest.length,4)*140+15*95);
}

/* --- линии между островами: считаются по раскладке (offset*), поэтому анимации их не сдвигают --- */
var LRO=null,LFT=0;
/* зигзаг тропинки: сдвиг островка по кругу из четырёх (центр, вправо, центр, влево); 56 — изгиб заметнее, чем прежние 46 (владелец) */
var ZZ=[0,56,0,-56];
function lkX(el){var m=/translateX\((-?[\d.]+)px\)/.exec(el.style.transform||'');return m?+m[1]:0}
function links(){curOnce(links0)}
function links0(){
  var ns='http://www.w3.org/2000/svg';
  app.querySelectorAll('.path').forEach(function(pa){
    var old=pa.querySelector('.cn');if(old)old.remove();
    var it=pa.querySelectorAll('.ilw'),i=pa.dataset.i;
    if(it.length<2)return;
    var pw=pa.offsetWidth,ph=pa.offsetHeight;pa.dataset.lsz=pw+'x'+ph;
    /* тема с норой: три равных промежутка — край экрана, нора, островок, край; на широком экране промежуток между норой
       и островком не больше 56 px, а пара стоит по центру колонки (на телефоне это одно и то же).
       Отходит от норы только её островок: если двигать и соседей, сбивается зигзаг тропинки; считается до линий */
    /* нор у темы может быть несколько, по разные стороны: сдвиг считается для островка каждой.
       Положения всех островков темы считаются ниже одной волной */
    var ws=[].slice.call(pa.querySelectorAll('.ilw')),B=function(r){return ZZ[r%4]},own={},hb=[];
    pa.querySelectorAll('.bur').forEach(function(bu){var aw=bu.parentNode,L=bu.classList.contains('l'),nw=bu.querySelector('.nwr'),g=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gut'))||16;
      var vb=nw.offsetWidth*80/92,G=Math.min(56,(pw+2*g-vb-106)/3),x0=(pw-vb-106-G)/2,c0=aw.offsetLeft+aw.offsetWidth/2+(+aw.dataset.b);
      var hd=Math.max(-90,Math.min(90,(L?x0+vb+G+53:pw-x0-vb-G-53)-c0)),q=ws.indexOf(aw);
      own[q]=B(q)+hd;
      hb.push([bu,aw,nw,L,x0,vb])});
    /* волна: боковые островки — вершины через один (вправо, влево), островок с норой — та же вершина, только дальше, если нора просит места;
       средний островок — посередине между соседями, поэтому у норы тропинка не ломается и не сплющивается */
    var xs=ws.map(function(w,r){if(r%2===0)return 0;var sg=r%4===1?1:-1;return r in own?sg*Math.max(sg*own[r],ZZ[1]):sg*ZZ[1]});
    xs=xs.map(function(x,r){return r%2?x:r in own?own[r]:((r>0?xs[r-1]:0)+(r<xs.length-1?xs[r+1]:0))/2});
    ws.forEach(function(w,r){w.style.transform='translateX('+Math.round(xs[r])+'px)'});
    hb.forEach(function(a){var bu=a[0],aw=a[1],nw=a[2];bu.style.right='auto';bu.style.left=(a[3]?a[4]:pw-a[4]-a[5])-nw.offsetLeft-nw.offsetWidth*6/92-aw.offsetLeft-lkX(aw)+'px'});
    var sv=document.createElementNS(ns,'svg');sv.setAttribute('class','cn');sv.setAttribute('width',pw);sv.setAttribute('height',ph);sv.setAttribute('aria-hidden','true');
    var fresh=[];
    for(var j=0;j<it.length-1;j++){
      var a=it[j],b=it[j+1],bi=b.querySelector('.isl');
      var x1=a.offsetLeft+lkX(a)+a.offsetWidth/2,y1=a.offsetTop+a.offsetHeight+2;
      var x2=b.offsetLeft+lkX(b)+bi.offsetLeft+bi.offsetWidth/2,y2=b.offsetTop+bi.offsetTop+10,ym=(y1+y2)/2;
      var d='M'+x1+' '+y1+' C'+x1+' '+ym+' '+x2+' '+ym+' '+x2+' '+y2,key=i+'-'+j;
      var base=document.createElementNS(ns,'path');base.setAttribute('d',d);base.setAttribute('class','seg');sv.appendChild(base);
      if(S.d[key]&&isOpen(i,j+1)){var lp=document.createElementNS(ns,'path');lp.setAttribute('d',d);var tc=(bi.className.match(/ty-\w/)||[''])[0];lp.setAttribute('class','seg lit '+tc);sv.appendChild(lp);if(!LIT[key]){LIT[key]=1;fresh.push([lp,b])}}
    }
    if(!pa.dataset.lk)pa.dataset.lk=Date.now();
    if(pa.classList.contains('stg')&&!RM()){var el=(Date.now()-pa.dataset.lk)/1000,dl=.2+Math.min(it.length,8)*.045;if(el<dl+.6)sv.style.animation='cnin .6s ease '+(dl-el)+'s both'}
    pa.insertBefore(sv,pa.firstChild);
    /* новый открытый островок: линия дорисовывается, потом остров «всплывает» с волной */
    fresh.forEach(function(f,n){
      var L=f[0].getTotalLength();f[0].style.strokeDasharray=L;f[0].style.strokeDashoffset=L;f[0].getBoundingClientRect();
      f[0].style.transition='stroke-dashoffset .9s cubic-bezier(.4,0,.2,1) '+(n*.9)+'s';f[0].style.strokeDashoffset=0;
      setTimeout(function(){f[1].classList.remove('wait');if(!RM()){var ic=f[1].querySelector('.isl');if(ic)f[1].style.setProperty('--ti',getComputedStyle(ic).getPropertyValue('--ti'));f[1].classList.add('unl');snd('unlock');setTimeout(function(){f[1].classList.remove('unl')},950)}},900*(n+1)+60);
    });
  });
  linksWatch();
}
/* перерисовка, если размер колонки изменился (подгрузился шрифт, перенеслась подпись) */
function linksWatch(){
  if(!LFT&&document.fonts&&document.fonts.ready){LFT=1;document.fonts.ready.then(function(){if(app.querySelector('.path'))links()})}
  if(!window.ResizeObserver)return;
  if(LRO)LRO.disconnect();
  var busy=0;
  LRO=new ResizeObserver(function(){
    if(busy)return;busy=1;
    requestAnimationFrame(function(){busy=0;var ch=false;app.querySelectorAll('.path').forEach(function(p){if(p.dataset.lsz&&p.dataset.lsz!==p.offsetWidth+'x'+p.offsetHeight)ch=true});if(ch)links()})});
  app.querySelectorAll('.path').forEach(function(p){LRO.observe(p)});
}

/* --- островки --- */
/* cur() (текущий островок) обходит весь курс; при отрисовке Пути его зовут для каждого острова,
   поэтому на время отрисовки ответ запоминается один раз */
var CUR1=null;
/* «где я остановился» — сразу за самым дальним пройденным островком на Пути;
   всё, что раньше этой точки и не пройдено, считается пропущенным, но остаётся открытым.
   Доп. главы (кроличьи норы) в расчёте не участвуют: нора — ответвление, флажок на Пути остаётся там, где ученик свернул */
var FRN1=null;
function FRN(){if(FRN1)return FRN1;var li=-1,lj=-1,i,j,r=null;
  for(i=0;i<TOPICS.length;i++)if(!TOPICS[i].opt)for(j=0;j<ni(i);j++)if(S.d[i+'-'+j]){li=i;lj=j}
  if(li<0)r=[Math.max(S.start,0),0];
  else{for(i=li,j=lj+1;i<TOPICS.length&&!r;i++,j=0)if(!TOPICS[i].opt)for(;j<ni(i);j++)if(!S.d[i+'-'+j]){r=[i,j];break}
    if(!r)r=[TOPICS.length,0]}
  if(CUR1!==null)FRN1=r;return r}
function bfr(i,j){var f=FRN();return i<f[0]||(i===f[0]&&j<f[1])}
/* ближайшая теория перед островком в его теме (-1, если её нет): без неё пропущенный островок не открывается */
function thPrev(i,j){for(var x=j-1;x>=0;x--)if(IT(i,x).t==='theory')return x;return -1}
function cur(){if(CUR1!==null)return CUR1;var f=FRN();if(f[0]<TOPICS.length)return f[0]+'-'+f[1];
  for(var i=Math.max(S.start,0);i<TOPICS.length;i++)if(!TOPICS[i].opt)for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return i+'-'+j;return''}
/* доп. главы (opt:1) необязательны: путь идёт мимо них, в счёт тем и завершение обучения они не входят */
/* --- кроличьи норы: доп. глава не стоит в ряду тем, а уходит ответвлением от последнего островка темы перед ней --- */
var HOLE=-1;
function holePar(i){for(var p=i-1;p>=0;p--)if(!TOPICS[p].opt)return p;return-1}
function holesOf(p){var a=[];for(var i=p+1;i<TOPICS.length&&TOPICS[i].opt;i++)a.push(i);return a}
/* внутри норы островки открываются по порядку; «ты здесь» — первый непройденный */
function ocur(i){for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return i+'-'+j;return''}
function ostarted(i){for(var j=0;j<ni(i);j++)if(S.d[i+'-'+j])return true;return false}
/* островок темы, рядом с которым нора и после которого глава открывается: after из данных главы, иначе последний */
function holeAt(i){var p=holePar(i),l=p<0?0:ni(p)-1,a=TOPICS[i].after;return a!=null?Math.min(a,l):l}
/* нора зелёная, когда пройден её островок, тема пропущена при выборе старта или глава уже начата; в режиме разработчика — всегда.
   То, что островок остался позади на карте (bfr), не в счёт: ученик мог уйти вперёд, не пройдя его, и нора зеленела зря */
/* где нора стоит на карте темы p: {островок: нора}. Норе нужен боковой островок (у среднего места сбоку нет).
   Норы «после всей темы» (их место — последний островок) разносим по теме равномерно, с первой четверти до конца, а не кучей в конце (владелец);
   нора с явным местом внутри темы стоит у него. Нора открыта всегда, место — только подсказка, когда в неё удобно заглянуть */
function holeSpots(p){var hs=holesOf(p),l=ni(p)-1,hp={},odd=function(a){return a%2?a:a<l?a+1:Math.max(a-1,0)},
  tail=hs.filter(function(o){return holeAt(o)===l}),k=tail.length,s0=odd(Math.max(1,Math.round((l+1)/4)));
  function put(o,a){a=odd(a);for(var d=0;d<=l;d+=2){if(a-d>=0&&!(a-d in hp)){hp[a-d]=o;return}if(a+d<=l&&!(a+d in hp)){hp[a+d]=o;return}}
    for(var c=0;c<=l;c++)if(!(c in hp)){hp[c]=o;return}}
  hs.forEach(function(o){if(holeAt(o)!==l)put(o,holeAt(o))});
  tail.forEach(function(o,n){put(o,k<2?l:Math.round(l-n*(l-s0)/(k-1)))});
  return hp}
function holeSpot(o){var p=holePar(o);if(p<0)return 0;var hp=holeSpots(p);for(var j in hp)if(hp[j]===o)return+j;return holeAt(o)}
function holeVis(i){var p=holePar(i),k=holeSpot(i);return p<0||TOPICS[p].intro||(typeof DEV==='function'&&DEV())||!!S.d[p+'-'+k]||p<S.start||ostarted(i)}
function holeName(t){return String(t.n||'').split(':')[0]}
/* нора — «вывернутый островок»: тот же шестиугольник и ракурс (точки HEX, viewBox), только утопленный в землю.
   Сверху бортик с низкой боковой гранью, внутри видны три дальние стенки (опущенные на глубину верхние рёбра
   уменьшенного шестиугольника), ниже дно. Рядом, за дальним углом, — наклонённый знак со стрелкой вниз. Цвета — в CSS (--hlt, --hw, --hb, --sgn) */
var NHN=0;
/* знак — с внешней стороны, подальше от тропинки: у норы слева он левее ямы, у норы справа (r) — правее, наклон наружу */
function burrowSvg(r){var id='nh'+(++NHN),I='M18.6 34 L31.9 19.2 L60.1 19.2 L73.4 34 L60.1 48.8 L31.9 48.8 Z';
  return'<svg class="nsv" viewBox="0 8 92 74" aria-hidden="true" focusable="false"><defs><clipPath id="'+id+'"><path d="'+I+'"/></clipPath></defs><g class="npt"><path class="rs" d="M9 34 L27 54 L65 54 L83 34 L83 40 L65 60 L27 60 L9 40 Z"/><path class="rt" d="M9 34 L27 14 L65 14 L83 34 L65 54 L27 54 Z"/><g clip-path="url(#'+id+')"><path class="w" d="'+I+'"/><path class="w wl" d="M18.6 34 L31.9 19.2 L31.9 32.2 L18.6 47 Z"/><path class="w wr" d="M60.1 19.2 L73.4 34 L73.4 47 L60.1 32.2 Z"/><path class="b" d="M18.6 47 L31.9 32.2 L60.1 32.2 L73.4 47 L60.1 61.8 L31.9 61.8 Z"/></g></g><g class="sgw"><g class="sg" transform="'+(r?'translate(44 -5) rotate(9 24 24)':'translate(-16 -5) rotate(-9 24 24)')+'"><ellipse class="sf" cx="24.6" cy="25.2" rx="5" ry="2.7"/><rect class="sp" x="22.3" y="4" width="2.7" height="21.4" rx="1"/><rect class="sps" x="24.6" y="4" width="1.7" height="21.4" rx=".8"/><path class="sbk" d="M8 -6 L16 8 L32 8 L40 -6 L40 -2.5 L32 11.5 L16 11.5 L8 -2.5 Z"/><path class="sb" d="M8 -6 L16 -20 L32 -20 L40 -6 L32 8 L16 8 Z"/><path class="sa" d="M24 -13v12M18.5 -6.5l5.5 5.5 5.5-5.5"/></g></g></svg>'}
/* в нору можно зайти всегда; бледная (lk), пока не пройден её островок темы, потом зелёная */
/* норы, которые уже видели открытыми: только что открывшаяся нора один раз зеленеет и знак подпрыгивает */
var HOP=null;
function burrow(o,side){
  var t=TOPICS[o],m=ni(o),c=0,op=holeVis(o),fr=op&&!HOP[o];for(var j=0;j<m;j++)if(S.d[o+'-'+j])c++;
  if(op)HOP[o]=1;if(fr&&!RM())setTimeout(function(){snd('unlock')},1500);
  var dn=c===m,st=dn?'пройдена':c?c+' из '+m:'';
  return'<button class="bur '+side+(op?'':' lk')+(dn?' dn':'')+(fr&&!RM()?' fr':'')+'" data-o="'+o+'" aria-label="'+esc('Доп. глава: '+t.n+' ('+st+')')+'"><span class="nwr">'+burrowSvg(side.charAt(0)==='r')+(dn?'<i class="bd ok"></i>':'')+'</span><span class="ntx">'+esc(holeName(t))+(st?'<small>'+st+'</small>':'')+'</span></button>'}
function hole(i){HOLE=i;curOnce(function(){hole0(i)})}
function hole0(i){BACK=home;fzApply();
  var t=TOPICS[i],p=holePar(i),n=ni(i),c=0;for(var j=0;j<n;j++)if(S.d[i+'-'+j])c++;
  var h=subTop(holeName(t),'🐇',c===n?'Нора пройдена':'Кроличья нора','Назад на Путь',c,n)+
   '<section class="topic hole" aria-label="'+esc('Доп. глава: '+t.n)+'"><div class="hhd'+(c===n?' dn':'')+'"><span class="nwr">'+burrowSvg()+'</span><h2>'+esc(t.n)+'</h2><p class="mu">'+esc(t.s||'')+'</p><p class="hnt">Доп. глава по желанию: открыта всегда, заходи, когда интересно. В счёт тем не входит, опыт за островки начисляется как обычно.</p><div class="hpr"><div class="ring" style="--p:'+Math.round(c/Math.max(1,n)*100)+'" role="img" aria-label="Пройдено '+c+' из '+n+'"><span>'+c+'/'+n+'</span></div><span>'+(c===n?'Глава пройдена':c?'Пройдено '+c+' из '+n:'Ещё не начата')+'</span></div></div>'+
   '<div class="path'+(RM()?'':' stg')+'" data-i="'+i+'">';
  for(var j2=0;j2<n;j2++)h+=island(i,j2,j2);
  scr('hole',h+'</div></section>','home');links();
  $('x').onclick=function(){HOLE=-1;home();var b=app.querySelector('.bur[data-o="'+i+'"]');if(b)b.scrollIntoView({block:'center'})};
  app.querySelectorAll('.isl').forEach(function(b){b.onclick=function(e){e.stopPropagation();islandPop(b)}});
  var cu=app.querySelector('.isl.cur');if(cu&&c)cu.scrollIntoView({block:'center'});else window.scrollTo(0,0);
}
function allDone(){return TOPICS.every(function(t,i){return t.intro||t.opt||tdone(i)})}
function NT(){return TOPICS.filter(function(t){return!t.intro&&!t.opt}).length}
function ND(){return TOPICS.filter(function(t,i){return!t.intro&&!t.opt&&(tdone(i)||i<S.start)}).length}
function curOnce(f){var o=CUR1,of=FRN1;CUR1=null;FRN1=null;CUR1=cur();try{return f()}finally{CUR1=o;FRN1=of}}
/* объёмный наклонный шестиугольник: верх, бок, блик, свечение; тень на воде и галочка рисуются в CSS (меньше узлов на длинном Пути) */
var HEX='<svg class="hx" viewBox="0 8 92 74" width="118" height="92" aria-hidden="true" focusable="false"><path class="gl" d="M9 34 L27 14 L65 14 L83 34 L83 46 L65 66 L27 66 L9 46 Z"/><path class="sd" d="M9 34 L27 54 L65 54 L83 34 L83 46 L65 66 L27 66 L9 46 Z"/><path d="M9 34 L27 14 L65 14 L83 34 L65 54 L27 54 Z"/><path class="sh" d="M13 33 L29 17 L63 17 L57 23 L31 23 L19 33 Z"/></svg>';
var ITY={theory:['t','📖','Теория'],flash:['f','✏️','Вопросы'],test:['c','💻','Код'],project:['p','🚀','Мини-проект']};
function ity(it){return ITY[it.t]||['a','⭐','Островок']}
function island(i,j,n,dx){
  var o=TOPICS[i].opt,k=i+'-'+j,it=IT(i,j),d=S.d[k],op=isOpen(i,j),c=(o?ocur(i):cur())===k,nx=!c&&!d&&!o&&nxI(i,j),wt=j>0&&S.d[i+'-'+(j-1)]&&!LIT[i+'-'+(j-1)];
  var ty=ity(it),lb=it.n||'',off=ZZ[j%4]+(dx||0),st=d?'пройдено':(op?(c?'ты здесь':'открыто'):'закрыто');
  return'<div class="ilw'+(wt?' wait':'')+(c?' cu':'')+'" style="--n:'+Math.min(n||0,9)+';transform:translateX('+off+'px)">'+(c?'<div class="flag" aria-hidden="true">'+(TOPICS[i].intro||o&&!ostarted(i)?'Начни здесь':'🚩 Ты остановился здесь')+'</div>':'')+'<button class="isl ty-'+ty[0]+' '+(d?'dn':(op?'op':'lk'))+(c?' cur':'')+(nx?' nx':'')+'" data-i="'+i+'" data-j="'+j+'" aria-label="'+esc(ty[2]+': '+lb+' ('+st+')')+'"'+(c?' aria-current="step"':'')+'>'+HEX+'<span class="ic">'+ty[1]+'</span>'+(d?'<i class="bd ok"></i>':(op?'':'<i class="bd">🔒</i>'))+'</button><div class="mu">'+esc(lb)+(it.t==='project'?'<br><small>'+(/^(skip|seen)$/.test(S.at[k])?'пропущен':'по желанию')+'</small>':'')+'</div></div>'}
/* сколько читать теорию: по объёму текста, примерно 160 слов в минуту */
function readMin(it){var t=String(it.html||'').replace(/<pre[\s\S]*?<\/pre>/g,' ').replace(/<[^>]+>/g,' '),w=t.split(/\s+/).filter(Boolean).length,c=(String(it.html||'').match(/<pre>/g)||[]).length;return Math.max(1,Math.round(w/160+c*.25))}
function goalCard(all){
  var d=goalDone(),g=S.goal,ok=d>=g,cu=cur(),nx=null;
  if(cu){var p=cu.split('-');nx=IT(+p[0],+p[1])}
  /* сверху приветствие во всю ширину (ник до 20 символов помещается целиком); в центре крупно — что дальше;
     кнопка во всю ширину; под ней тихая строка цели с маленьким кольцом */
  var ty=nx?ity(nx):null,mt=ty?ty[2]+(nx.t==='theory'?' · ≈ '+readMin(nx)+' мин':''):'';
  return'<section class="gcard" aria-label="Сегодня"><div class="gh">Привет, <b>'+nk(S.nick)+'</b>!</div>'+
   (all?'<p class="gall">Курс пройден. Кролик гордится тобой.</p>':cu?'<div class="gnx ty-'+ty[0]+'"><span class="gic" aria-hidden="true">'+ty[1]+'</span><span class="gnt"><small>'+esc(mt)+'</small><b>'+esc(nx.n||'')+'</b></span></div><button class="btn" id="gc">'+(d?'Продолжить':'Начать')+'</button>':'')+
   '<div class="gg'+(ok?' ok':'')+'"><span class="ring" role="img" aria-label="Цель дня: '+d+' из '+g+'"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8"/><circle class="v" cx="10" cy="10" r="8" pathLength="100"'+(ok?'':' stroke-dasharray="'+Math.round(d/g*100)+' 100"')+'/></svg></span>'+(ok?'Цель дня выполнена':'Цель дня: '+d+' из '+g)+'</div></section>'}
function home(){if(HOLE>=0&&TOPICS[HOLE]&&TOPICS[HOLE].opt)return hole(HOLE);HOLE=-1;curOnce(home0)}
function home0(){BACK=home;fzApply();
  var all=allDone();
  if(PE.length){scr('home',head()+'<div class="fb bad"><b>Ошибка в данных тем</b>'+PE.map(esc).join('<br>')+'</div>','home');bindHead(home);return}
  var first=TOPICS[0]&&TOPICS[0].intro&&S.start===0&&!tdone(0)&&!REV;
  var h=head()+'<h1 class="sr-only">Путь</h1>'+(first?'':goalCard(all)),num=0,cu=cur(),ci=cu?+cu.split('-')[0]:-1;
  TOPICS.forEach(function(t,i){
    if(t.opt)return;if(!t.intro)num++;if(!vis(i))return;
    var c=0;(t.items||[]).forEach(function(x,j){if(S.d[i+'-'+j])c++});
    var pc=Math.round(c/Math.max(1,ni(i))*100),dn=tdone(i);
    h+='<section class="topic'+(t.intro?' intro':'')+(REV&&!t.intro?' rv':'')+'" aria-label="'+esc(t.intro?t.n:'Тема '+num+': '+t.n)+'">'+(t.intro?'<div class="ihead"><h2>'+esc(t.n)+'</h2><p class="mu">'+esc(t.s||'')+'</p></div>':'<div class="thead'+(dn?' done':'')+(i===ci?' now':'')+'"><div class="tn'+(dn?' ok':'')+'" aria-hidden="true">'+(dn?'':num)+'</div><div class="tt"><h2>'+esc(t.n)+'</h2><div class="mu">'+esc(t.s||'')+((i<S.start||i<FRN()[0])&&!dn?' · пропущено':'')+'</div></div><div class="ring" style="--p:'+pc+'" role="img" aria-label="Пройдено '+c+' из '+ni(i)+'"><span>'+c+'/'+ni(i)+'</span></div></div>')+'<div class="path'+(RM()?'':' stg')+'" data-i="'+i+'">';
    /* нора — примерно за пять островков до конца темы, у островка, сдвинутого вбок (нечётный), в свободном месте с другой стороны */
    if(!HOP){HOP={};TOPICS.forEach(function(x,o){if(x.opt&&holeVis(o))HOP[o]=1})}
    var hp=holeSpots(i);
    for(var j=0;j<ni(i);j++){var hw=j in hp?1:0,
      /* островок с норой отходит от неё (точный сдвиг считает links0; здесь — начальный, чтобы не прыгало) */
      w=island(i,j,j,hw*(j%4===1?1:-1)*34);
      if(hw)w=w.replace('<div class="ilw','<div data-b="'+ZZ[j%4]+'" data-hw="'+hw+'" class="ilw nhb').replace(/<\/div>$/,burrow(hp[j],j%4===1?'l':'r')+'</div>');
      h+=w}
    h+='</div></section>'});
  scr('home',h+'<aside class="jump" aria-label="Быстрый переход"><button id="jmp" aria-label="К текущему островку">'+ico('arrow')+'</button></aside>','home');bindHead(home);links();
  app.querySelectorAll('.isl').forEach(function(b){b.onclick=function(e){e.stopPropagation();islandPop(b)}});
  app.querySelectorAll('.bur').forEach(function(b){b.onclick=function(e){e.stopPropagation();popClose();hole(+b.dataset.o)}});
  var c=app.querySelector('.isl.cur');if(c&&!REV)c.scrollIntoView({block:'center'});
  var gc=$('gc');if(gc)gc.onclick=function(){var k=cur();if(!k)return;var p=k.split('-');BACK=home;go(+p[0],+p[1])};
  jumpWatch();
}
function toCur(){var t=app.querySelector('.isl.cur')||app.querySelector('.isl.nx');if(t)t.scrollIntoView({block:'center',behavior:RM()?'auto':'smooth'})}
/* кнопка «к текущему»: видна, только когда текущий островок ушёл за экран, стрелка показывает направление */
var JIO=null;
function jumpWatch(){
  if(JIO){JIO.disconnect();JIO=null}
  var j=$('jmp'),t=app.querySelector('.isl.cur')||app.querySelector('.isl.nx');
  if(!j)return;if(!t||!window.IntersectionObserver){j.remove();return}
  j.onclick=toCur;
  JIO=new IntersectionObserver(function(es){es.forEach(function(e){var off=!e.isIntersecting;j.classList.toggle('on',off);j.classList.toggle('up',off&&e.boundingClientRect.top<0);j.setAttribute('aria-hidden',off?'false':'true');j.tabIndex=off?0:-1})},{rootMargin:'-60px 0px -90px 0px'});
  JIO.observe(t);
}
/* карточка островка: что это, сколько займёт, сколько опыта, одна кнопка */
function popClose(){var o=app.querySelector('.ipop');if(!o)return;app.classList.remove('pk');var b=app.querySelector('.isl.sel');if(b)b.classList.remove('sel');document.removeEventListener('click',popOut,true);if(RM()){o.remove();return}o.classList.add('out');setTimeout(function(){o.remove()},180)}
function popOut(e){if(!e.target.closest('.ipop')&&!e.target.closest('.isl'))popClose()}
function islandPop(b){
  var i=+b.dataset.i,j=+b.dataset.j,was=b.classList.contains('sel');
  var o0=app.querySelector('.ipop');if(o0){o0.remove();app.classList.remove('pk');var s0=app.querySelector('.isl.sel');if(s0)s0.classList.remove('sel');document.removeEventListener('click',popOut,true)}
  if(was)return;
  var it=IT(i,j),k=i+'-'+j,ty=ity(it),d=S.d[k],op=isOpen(i,j),meta='',txt='',btn='',sk='';
  if(it.t==='theory')meta='≈ '+readMin(it)+' мин';
  else if(it.t==='flash')meta=it.q.length+' '+pl(it.q.length,['вопрос','вопроса','вопросов']);
  else if(it.t==='test')meta=it.tasks.length+' '+pl(it.tasks.length,['задание','задания','заданий']);
  else if(it.t==='project')meta='по желанию';
  var xp=it.t==='flash'?20:it.t==='test'?60:it.t==='project'?(it.bonus>0?it.bonus|0:40):0;
  var tp=!op&&!TOPICS[i].opt&&(i<S.start||bfr(i,j))?thPrev(i,j):-1;
  if(tp>=0){snd('lock');txt='Сначала прочитай теорию «'+esc(IT(i,tp).n||'')+'»: этот островок по ней.';btn='<button class="btn" id="ipt">Читать теорию</button>'}
  else if(!op){snd('lock');txt='Откроется, когда пройдёшь островки перед ним.';btn='<button class="btn g" id="ipc">К текущему островку</button>'}
  else if(d){
    txt=S.at[k]==='seen'?'Проект пропущен, эталон открыт. Решить можно, но уже без опыта.':S.at[k]==='skip'?'Этот проект пропущен. Сделай его сейчас и получи +'+xp+' ⭐.':(xp?'Пройдено. Опыт за этот островок уже получен, повторять можно сколько угодно.':'Пройдено. Можно перечитать в любой момент.');
    btn='<button class="btn" id="ipg">'+(/^(skip|seen)$/.test(S.at[k])?'Сделать проект':it.t==='theory'?'Перечитать':'Повторить')+'</button>'}
  else{
    txt=it.t==='theory'?'Прочитай и нажми «'+G('Я прочитал','Я прочитала','Прочитано')+'» в конце. Выделенные слова открывают описание.':it.t==='flash'?'Выбирай верный ответ. Ошибки вернутся в конце островка.':it.t==='test'?'Пиши программы, проверка запустит их на тестах.':'Задача покрупнее. Можно пропустить, тема всё равно засчитается.';
    if(xp)txt+=' Награда: до +'+xp+' ⭐.';
    btn='<button class="btn" id="ipg">'+(it.t==='project'?'Начать проект':'Начать')+'</button>';
    if(it.t==='project')sk='<button class="btn t" id="ips">Пропустить</button>'}
  var pa=b.closest('.path'),w=b.closest('.ilw'),br=b.getBoundingClientRect();
  var o=document.createElement('div');o.className='ipop ty-'+ty[0];o.setAttribute('role','dialog');o.setAttribute('aria-label',ty[2]+': '+(it.n||''));
  o.innerHTML='<div class="ipk"><span class="tg"><i></i>'+ty[2]+'</span><span class="mu">'+(d?'✓ пройдено':meta)+'</span></div><h3>'+esc(it.n||ty[2])+'</h3><p>'+txt+'</p><div class="row">'+btn+sk+'</div>';
  o.style.top=(w.offsetTop+w.offsetHeight+10)+'px';
  pa.appendChild(o);b.classList.add('sel');app.classList.add('pk');
  /* стрелка карточки смотрит точно на остров, даже если карточка уже ширины дорожки */
  /* считаем по раскладке, а не по getBoundingClientRect: карточка в момент замера ещё «въезжает» (scale/translate) и стрелка съезжала */
  var ix=w.offsetLeft+lkX(w)+b.offsetLeft+b.offsetWidth/2;
  o.style.setProperty('--ax',Math.max(24,Math.min(o.offsetWidth-24,ix-o.offsetLeft))+'px');
  var g=$('ipg');if(g)g.onclick=function(){BACK=home;popClose();go(i,j)};
  var s=$('ips');if(s)s.onclick=function(){popClose();projSkip(i,j)};
  var cc=$('ipc');if(cc)cc.onclick=function(){popClose();toCur()};
  var tt=$('ipt');if(tt)tt.onclick=function(){BACK=home;popClose();go(i,tp)};
  setTimeout(function(){document.addEventListener('click',popOut,true)},0);
  /* карточку должно быть видно целиком; пока она «въезжает» (scale), она ниже настоящей — после анимации докручиваем */
  function vis(){if(o.isConnected)o.scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})}
  requestAnimationFrame(function(){vis();var fb=g||cc||tt;if(fb)fb.focus({preventScroll:true})});o.addEventListener('animationend',vis,{once:true});
}
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&app.querySelector('.ipop')&&!document.querySelector('.modal')){e.stopImmediatePropagation();e.preventDefault();var b=app.querySelector('.isl.sel');popClose();if(b)b.focus()}},true);

/* --- приветствие и повторение после перерыва --- */
function greet(){
  var t=day(new Date());fzApply();
  if(S.seen===t)return home();
  var away=S.seen?dnum(t)-dnum(S.seen):0;S.seen=t;save();
  var s=streakNow(),lost=S.streak>=2&&s===0;
  scr('greet','<div class="onb center gr">'+rabbit('eat')+'<h1>Привет, '+nk(S.nick)+'!</h1><p class="lead">'+(lost?'Серия в '+S.streak+' '+pl(S.streak,['день','дня','дней'])+' прервалась'+(away>=3?', тебя не было '+away+' '+pl(away,['день','дня','дней']):'')+'. Не страшно: новая начнётся сегодня.':away>=3?'Тебя не было '+away+' '+pl(away,['день','дня','дней'])+'. Кролик скучал.':s?'Серия: '+s+' '+pl(s,['день','дня','дней'])+'. Не прерывай её сегодня.':'Кролик завтракает и ждёт тебя.')+'</p><button class="btn pulse" id="go">Начать</button></div>');
  $('go').onclick=function(){home();if(away>=3)setTimeout(function(){repeatAsk(away)},400)};
}
function passed(type){var a=[];TOPICS.forEach(function(t,i){(t.items||[]).forEach(function(x,j){if(x.t===type&&S.d[i+'-'+j])a.push([i,j])})});return a}
function repeatAsk(away){
  if(!ST('rep')||S.rp===day(new Date())||!passed('flash').length)return;
  modal('<h2>Давно не виделись</h2><p>Тебя не было '+away+' '+pl(away,['день','дня','дней'])+'. Повторим 3 вопроса из пройденного?</p><p class="mu">Это разминка: опыт за неё не начисляется.</p>',[['Давай',function(){S.rp=day(new Date());save();repeat3()}],['Позже',function(){S.rp=day(new Date());save()},1]])}

/* --- практика --- */
function row(ic,t,sub,a,dis,rt){return'<button class="li" data-a="'+a+'"'+(dis?' disabled':'')+'><span class="lic" aria-hidden="true">'+ic+'</span><span class="lt">'+t+(sub?'<small>'+sub+'</small>':'')+'</span>'+(rt?'<span class="lv">'+rt+'</span>':ico('chev','ch'))+'</button>'}
/* кубики-украшение: только контур, вектор (иконка dices из набора Lucide, лицензия ISC) */
var DICE='<svg class="pdeco" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect width="12" height="12" x="2" y="10" rx="2" ry="2"/><path d="m17.92 14 3.5-3.5a2.24 2.24 0 0 0 0-3l-5-4.92a2.24 2.24 0 0 0-3 0L10 6"/><path class="dpp" d="M6 18h.01M10 14h.01M15 6h.01M18 9h.01"/></svg>';
function practice(){BACK=practice;PRW=0;
  var nf=passed('flash').length,nt=passed('test').length;
  /* главный режим — крупная карточка с кубиками вместо значка; два других — тихие строки под ней */
  function pc(a,ic,t,s,dis,big,lab){return'<button class="pcard'+(big?' big':'')+'" data-a="'+a+'"'+(dis?' disabled aria-disabled="true"':'')+'>'+(big?DICE:'<span class="pic" aria-hidden="true">'+ic+'</span>')+'<b>'+t+'</b><small>'+s+'</small><span class="go">'+(dis?ico('lock')+'Сначала пройди островок':lab+ico('chev'))+'</span></button>'}
  scr('practice',head()+ttl('Практика','Без опыта: прогресс и серия не меняются')+'<div class="prc">'+
   pc('rf','🎲','Случайный вопрос','Вопросы из пройденных островков, пока не закроешь',!nf,1,'Начать')+
   '<div class="prl">'+pc('rc','💻','Случайный код','Задание из пройденных',!nt,0,'Решить')+
   pc('r3','🔁','Разминка','3 вопроса по пройденному',!nf,0,'Начать')+'</div></div>'+
   (S.cn.rc?'<p class="pnote">Верных ответов в тренировках: <b>'+S.cn.rc+'</b></p>':''),'pr');
  bindHead(practice);
  app.querySelectorAll('.pcard').forEach(function(b){b.onclick=function(){if(b.disabled)return;({rf:rndFlash,rc:rndCode,r3:repeat3})[b.dataset.a]()}})}
function oge(){practice()}
/* вопрос в тренировке: та же раскладка, что у островка с вопросами */
function askQ(q,o){
  var sel=-1,ch=false,right=false,ord=q.o.map(function(x,n){return n}).sort(function(){return Math.random()-.5});
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Выйти">'+ico('x')+'</button><div class="grow">'+o.mid+'</div></div><h1 class="sr-only">Тренировка</h1><h2 class="q">'+(typeof qfmt==='function'?qfmt(q.q):esc(q.q))+'</h2>'+(q.v||'')+(q.c?'<pre>'+hl(q.c)+'</pre>':'')+optsHtml(q,ord);
  scr('askq',h+dockHtml('<button class="btn" id="go" disabled>Проверить</button>',0,1));if(q.v)imgZoom(app);
  $('x').onclick=o.exit;
  var g=$('go'),os=app.querySelectorAll('.opt');
  optKeys(os,function(b){if(ch)return;sel=+b.dataset.k;os.forEach(function(x){x.classList.remove('sel');x.setAttribute('aria-pressed','false')});b.classList.add('sel');b.setAttribute('aria-pressed','true');g.disabled=false});
  g.onclick=function(){
    if(ch){o.next();return}
    ch=true;right=sel===q.a;fx(right);
    os.forEach(function(x){var k=+x.dataset.k;x.disabled=true;if(k===q.a)x.classList.add('ok');else if(k===sel)x.classList.add('no')});
    if(right)PRW=0;else PRW++;
    dockState(right,right?'Верно!':'Неверно',esc(q.e||'')+xm(q),right?'':errMood(PRW));
    g.textContent=o.last&&o.last()?'Закончить':'Дальше';o.done(right);g.focus()}}
var RND={r:0,t:0,last:null};
function rndWarn(go){if(S.rnd)return go();modal('<h2>Бесконечный режим</h2><p>Задания идут одно за другим, пока не закроешь режим крестиком. Опыт не начисляется, прогресс не меняется.</p>',[['Понятно',function(){S.rnd=1;save();go()}],['Отмена',null,1]])}
function allFlashQ(){var a=[];passed('flash').forEach(function(p){IT(p[0],p[1]).q.forEach(function(q,n){a.push({q:q,k:p[0]+'-'+p[1]+'-'+n})})});return a}
function rndFlash(){
  if(!passed('flash').length){toast('Сначала пройди хотя бы один островок с вопросами');return}
  rndWarn(function(){RND.r=0;RND.t=0;RND.last=null;rfNext()})}
function rfNext(){
  var P=allFlashQ();if(!P.length){practice();return}
  var x;do{x=P[Math.floor(Math.random()*P.length)]}while(P.length>1&&x.k===RND.last);RND.last=x.k;
  askQ(x.q,{mid:'<span class="lstep">🎲 Верно '+RND.r+' из '+RND.t+'</span>',exit:practice,next:rfNext,done:function(r){RND.t++;if(r){RND.r++;rcInc()}}})}
function repeat3(){
  var P=allFlashQ();if(!P.length){toast('Сначала пройди хотя бы один островок с вопросами');return}
  P.sort(function(){return Math.random()-.5});var Q=P.slice(0,3),st=Q.map(function(){return 0}),n=0,ok=0;
  function bar(){return'<div class="sbar" role="img" aria-label="Вопрос '+(n+1)+' из '+Q.length+'">'+st.map(function(v,k){return'<i class="'+(v===1?'ok':v===2?'bad':k===n?'cu':'')+'"></i>'}).join('')+'</div>'}
  function step(){
    if(n>=Q.length){
      var all=ok===Q.length;
      scr('done','<div class="fin">'+(all?rabbit('happy'):'')+'<h1>Повторено: '+ok+' из '+Q.length+'</h1><p class="lead">'+(all?'Всё помнишь. Отлично.':'Ничего страшного, это просто разминка.')+'</p></div>'+dockHtml('<button class="btn" id="go">Готово</button><button class="btn t" id="rp">Ещё раз</button>',1));
      $('go').onclick=home;$('rp').onclick=repeat3;if(all){snd('solve');ach('rep1')}return}
    askQ(Q[n].q,{mid:bar(),exit:home,last:function(){return n===Q.length-1},next:function(){n++;step()},done:function(r){st[n]=r?1:2;if(r)ok++;var sb=app.querySelector('.sbar');if(sb)sb.outerHTML=bar()}})}
  step()}
function rndCode(){
  if(!passed('test').length){toast('Сначала пройди хотя бы один островок с кодом');return}
  rndWarn(function(){RND.last=null;rcNext()})}
function rcNext(){
  var P=passed('test'),T=[];P.forEach(function(p){IT(p[0],p[1]).tasks.forEach(function(q,n){T.push({q:q,k:p[0]+'-'+p[1]+'-'+n})})});
  if(!T.length){practice();return}
  var x;do{x=T[Math.floor(Math.random()*T.length)]}while(T.length>1&&x.k===RND.last);RND.last=x.k;var q=x.q;
  scr('rcode','<h1 class="sr-only">Случайный код</h1><div class="top ls"><button class="icon" id="x" aria-label="Выйти">'+ico('x')+'</button><span class="lstep grow">🎲 Случайный код</span>'+(q.h?'<button class="icon" id="hb" aria-label="Подсказка">'+ico('bulb')+'</button>':'')+'</div>'+taskCard(q)+'<div id="hint"></div>'+edCard('Решение','# Пиши код здесь\n'+(q.starter||''),0,'# Пиши код здесь\n'+(q.starter||''))+conHtml()+'<div id="fb"></div>'+dockHtml('<button class="btn" id="chk">Проверить</button>'));
  $('x').onclick=practice;
  var c=$('code'),sync=initEd(c,function(){});sync();
  if(q.h)$('hb').onclick=function(){snd('hint');$('hb').classList.add('on');$('hint').innerHTML='<div class="fb"><b>Подсказка</b>'+hintTx(q.h)+'</div>';$('hint').scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})};
  skReady();chkPulse();runBind(c);
  $('chk').onclick=async function(){
    var b=$('chk');if(!SKOK)fbSet('<div class="fb"><b>Загружаю среду Python…</b></div>');
    if(!(await needSk()))return;
    b.disabled=true;var v=await judge(q,c.value);
    if(!v.ok){fx(false);b.disabled=false;PRW++;fbSet(badFb(v.h,errMood(PRW)));return}
    PRW=0;fx(true,'test');rcInc();
    fbSet('<div class="fb"><b>Все тесты пройдены!</b>Опыт не начисляется, это тренировка.</div>');
    dockSet('<button class="btn" id="nx">Ещё задание</button>'+(q.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':''),1);
    $('nx').onclick=rcNext;if(q.sol)$('sl').onclick=function(){solModal(q.sol)}}}
function chkPulse(){var c=$('code'),b=$('chk');if(!c||!b)return;function u(){var v=c.value.trim();b.classList.toggle('pulse',v!==''&&v!=='# Пиши код здесь')}u();c.addEventListener('input',u)}
/* полоса уровня на экранах итога: заполняется от старого значения к новому */
function xpStrip(gain){
  var L=lvlInfo(S.xp),L0=lvlInfo(Math.max(0,S.xp-(gain||0))),p0=L0.l===L.l?L0.p:0;
  return'<div class="xps"><div class="xph"><b>Уровень '+L.l+'</b><span class="mu">до '+(L.l+1)+': ещё '+L.left+' ⭐</span></div><div class="bar" style="height:12px" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+L.p+'" aria-label="Прогресс уровня"><i class="xpb" style="width:'+p0+'%" data-p="'+L.p+'"></i></div></div>'}
function xpStripRun(){var b=app.querySelector('.xpb');if(!b)return;setTimeout(function(){b.style.width=b.dataset.p+'%'},RM()?0:450)}

/* --- достижения-дискеты --- */
function hsh(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function fdate(d){var p=d.split('-');return(+p[2])+' '+MON[+p[1]-1]+' '+p[0]}
function floppyFace(a){return'<div class="fface" style="--fc:'+a.c+'" aria-hidden="true"><div class="fsh"><i></i></div><div class="flb"><div class="fe">'+a.e+'</div><div class="fn">'+esc(a.n)+'</div></div></div>'}
function floppyBtn(a){return'<button class="fd" data-id="'+a.id+'" style="--fc:'+a.c+';--lean:'+((hsh(a.id)%5)-2)*1.4+'deg" aria-label="Достижение: '+esc(a.n)+'"><span class="fb3" aria-hidden="true"><span class="ff"><span class="fm"></span><span class="fl"><em>'+a.e+'</em></span></span><span class="fsx"><span class="fsn"></span><em>'+a.e+'</em></span><span class="fbk"></span></span><i class="fsd"></i></button>'}
function shelf(){
  /* общее число достижений не показываем: это тайна */
  var L=ACH.filter(function(a){return S.ach[a.id]}).sort(function(a,b){return S.ach[a.id]<S.ach[b.id]?-1:S.ach[a.id]>S.ach[b.id]?1:0}),hz=ST('sh')==='h',per=Math.max(4,Math.min(10,Math.floor((Math.min(innerWidth,640)-80)/(ST('fl')==='flat'?22:44))));
  var h='<div class="card shelfc"><div class="sh-h"><b>Достижения</b><span class="mu">Получено: '+L.length+'</span></div>';
  if(!L.length)return h+'<div class="shrow"></div><p class="mu" style="margin:10px 0 0">Здесь появятся дискеты за твои успехи. За что их дают, узнаешь сам.</p></div>';
  if(hz)h+='<div class="shrow hs" tabindex="0" aria-label="Полка с дискетами">'+L.map(floppyBtn).join('')+'</div>';
  else for(var r=0;r<L.length;r+=per){h+='<div class="shrow">'+L.slice(r,r+per).map(floppyBtn).join('')+'</div>'}
  return h+'</div>'}
function fdOpen(btn){
  var a=achDef(btn.dataset.id);if(!a||btn.dataset.busy)return;btn.dataset.busy=1;
  snd('disk');vib(12);MSIL=1;
  var an=RM()?null:btn.animate([{transform:'translateY(0)'},{transform:'translateY(-30px) rotate(-3deg)'}],{duration:260,easing:'cubic-bezier(.2,.9,.3,1.2)',fill:'forwards'});
  setTimeout(function(){
    var m=modal('<div class="fwin">'+floppyFace(a)+'<h2>'+esc(a.n)+'</h2><p class="fd2">'+esc(a.d)+'</p><p class="mu">Получено '+fdate(S.ach[a.id])+'</p></div>',[['Закрыть',null,1]]);
    new MutationObserver(function(x,o){if(!document.body.contains(m)){o.disconnect();if(an)an.cancel();delete btn.dataset.busy}}).observe(document.body,{childList:true});
  },RM()?0:230)}

/* --- профиль --- */
/* U1-13: кроличьи норы — сколько пройдено целиком (в профиле и в «Поделиться» — только когда пройдена хотя бы одна) */
function HN(){return TOPICS.filter(function(t){return t.opt}).length}
function HD(){return TOPICS.filter(function(t,i){if(!t.opt||!ni(i))return false;for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return false;return true}).length}
function shareTxt(){var n=ND(),h=HD(),s=streakNow();return'Я учу Python в ИТП! Уже '+G('прошёл','прошла','пройдено')+' '+n+' '+pl(n,['тему','темы','тем'])+(h?' и '+h+' '+pl(h,['кроличью нору','кроличьи норы','кроличьих нор'])+' из '+HN():'')+(s?', '+s+' '+pl(s,['день','дня','дней'])+' подряд':'')+', '+S.xp+' XP. Попробуй и ты!'}
/* --- U1-7: «Что ты уже умеешь» — шкала курса как в Duolingo. Очки — пройденные островки (и в норах тоже, вступление не в счёт);
   веха — конец темы: её порог равен числу островков основного курса до неё включительно --- */
/* значки вех — из того же набора Phosphor (duotone) */
/* у каждой вехи свой значок. Каких нет в наборе Phosphor выше, нарисованы здесь в том же стиле (контур и полупрозрачная заливка, сетка 256) */
(function(){var o=' fill="none" stroke="currentColor" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"',d=' opacity="0.2"';
 PH.receipt='<path d="M64 40h128v176l-21.3-16-21.4 16-21.3-16-21.4 16-21.3-16L64 216Z"'+d+'/><path d="M64 40h128v176l-21.3-16-21.4 16-21.3-16-21.4 16-21.3-16L64 216Z"'+o+'/><path d="M96 96h64M96 136h64"'+o+'/>';
 PH.signpost='<circle cx="128" cy="140" r="24"'+d+'/><path d="M128 224v-84M128 140 72 84M128 140l56-56M72 124V84h40M184 124V84h-40"'+o+'/>';
 PH.scissors='<circle cx="76" cy="184" r="28"'+d+'/><circle cx="180" cy="184" r="28"'+d+'/><circle cx="76" cy="184" r="28"'+o+'/><circle cx="180" cy="184" r="28"'+o+'/><path d="M96 164 200 40M160 164 56 40"'+o+'/>';
 PH.braces='<rect x="104" y="104" width="48" height="48" rx="8"'+d+'/><path d="M96 40c-24 0-32 12-32 32v32c0 16-8 24-24 24 16 0 24 8 24 24v32c0 20 8 32 32 32M160 40c24 0 32 12 32 32v32c0 16 8 24 24 24-16 0-24 8-24 24v32c0 20-8 32-32 32"'+o+'/>';
 PH.shield='<path d="M128 32 208 64v56c0 56-40 92-80 104-40-12-80-48-80-104V64Z"'+d+'/><path d="M128 32 208 64v56c0 56-40 92-80 104-40-12-80-48-80-104V64Z"'+o+'/><path d="m96 128 24 24 44-44"'+o+'/>';
 PH.cube='<path d="M128 32 216 80 128 128 40 80Z"'+d+'/><path d="M128 32 216 80v96l-88 48-88-48V80ZM40 80l88 48 88-48M128 128v96"'+o+'/>';
 PH.tree='<rect x="96" y="32" width="64" height="48" rx="8"'+d+'/><rect x="96" y="32" width="64" height="48" rx="8"'+o+'/><rect x="32" y="176" width="64" height="48" rx="8"'+o+'/><rect x="160" y="176" width="64" height="48" rx="8"'+o+'/><path d="M128 80v48M64 176v-24a24 24 0 0 1 24-24h80a24 24 0 0 1 24 24v24"'+o+'/>';
 PH.grid='<rect x="98" y="98" width="60" height="60"'+d+'/><rect x="40" y="40" width="176" height="176" rx="16"'+o+'/><path d="M40 98h176M40 158h176M98 40v176M158 40v176"'+o+'/>';
 PH.globe='<circle cx="128" cy="128" r="88"'+d+'/><circle cx="128" cy="128" r="88"'+o+'/><ellipse cx="128" cy="128" rx="38" ry="88"'+o+'/><path d="M40 128h176M56 88h144M56 168h144"'+o+'/>'})();
var SKI={sprout:'plant',msg:'chat-circle-text',kbd:'keyboard',rcpt:'receipt',fork:'signpost',loop:'repeat',cut:'scissors',list:'address-book',fn:'braces',shield:'shield',file:'folder-open',sort:'ranking',cube:'cube',tree:'tree',grid:'grid',chart:'chart-bar',web:'globe',cap:'graduation-cap'};
function ski(k){return phi(SKI[k])}
/* знак-остров: тот же наклонный шестиугольник, что на Пути, плоский, в цвет акцента */
var SKHX='<svg class="skx" viewBox="6 10 80 56" aria-hidden="true" focusable="false"><path class="s" d="M9 34 L27 54 L65 54 L83 34 L83 44 L65 64 L27 64 L9 44 Z"/><path d="M9 34 L27 14 L65 14 L83 34 L65 54 L27 54 Z"/></svg>';
/* вехи как в Duolingo: короткое действие из жизни, которое уже по силам; can — то же для реплики «Значит, ты уже можешь…» */
var SKL=[['','sprout','Начинаем',''],
 ['Начало знакомства','msg','Пишу первые программы','писать и запускать свои программы'],
 ['Переменные и ввод','kbd','Программа меня слушает','запоминать данные и спрашивать их у человека'],
 ['Оформление вывода','rcpt','Красиво вывожу результат','красиво оформлять то, что печатает программа'],
 ['Условия','fork','Программа принимает решения','учить программу выбирать, что делать'],
 ['Циклы в циклах','loop','Повторяю без копипаста','повторять действия циклами, даже вложенными'],
 ['Срезы и кортежи','cut','Режу строки и списки','вырезать из строк и списков нужные куски'],
 ['Словари и множества','list','Храню данные по ключам','хранить данные в словарях и множествах'],
 ['Гибкие функции','fn','Пишу свои функции','писать гибкие функции и передавать их друг другу'],
 ['Исключения','shield','Программа не падает','ловить ошибки, чтобы программа не падала'],
 ['Файлы и форматы данных','file','Работаю с файлами','читать и сохранять файлы, CSV и JSON'],
 ['Поиск и сортировка','sort','Ищу и сортирую быстро','быстро искать и сортировать данные'],
 ['Классы и объекты','cube','Создаю свои объекты','описывать вещи из жизни своими классами'],
 ['Наследование','tree','Строю семейства классов','строить одни классы на основе других'],
 ['Массивы и математика','grid','Считаю целыми массивами','считать сразу по целым массивам чисел'],
 ['Таблицы данных','chart','Разбираю таблицы данных','разбирать большие таблицы и считать по ним итоги'],
 ['Запросы к серверам','web','Общаюсь с серверами','получать данные с сервера и отправлять их туда'],
 ['Итоговые проекты','cap','Курс пройден','собирать большие программы из всего, что знаешь']];
/* вехи считаются по основному курсу: порог вехи — число его островков до конца темы, поэтому норы сюда не входят (с ними «Курс пройден» открывался раньше конца курса);
   пропущенные при выборе старта и пропущенные кнопкой островки засчитываются (владелец) */
function skPts(){var n=0;TOPICS.forEach(function(t,i){if(t.intro||t.opt)return;for(var j=0;j<ni(i);j++){var k=i+'-'+j;if(S.d[k]||i<S.start||S.at[k]==='skip'||S.at[k]==='seen')n++}});return n}
function skHole(){var n=0;TOPICS.forEach(function(t,i){if(t.opt)for(var j=0;j<ni(i);j++)if(S.d[i+'-'+j])n++});return n}
function skList(){var c=0,th={};TOPICS.forEach(function(t,i){if(t.intro||t.opt)return;c+=ni(i);th[t.n]=c});
  return SKL.map(function(m){return{t:m[0]?th[m[0]]:0,e:m[1],n:m[2],c:m[3]}}).filter(function(m){return m.t!==undefined})}
function skNow(){var p=skPts(),L=skList(),k=0;L.forEach(function(m,i){if(p>=m.t)k=i});return{p:p,L:L,k:k}}
/* U1-7: новое умение — окно после итога островка (как в Duolingo «теперь ты можешь…») с переходом на страницу.
   S.skk — последнее показанное; -1 у старых сохранений: тогда запоминаем текущее молча, без окна за прошлое */
function skNew(){var k=skNow().k;if(S.skk<0){S.skk=k;save();return false}return k>S.skk}
function skPop(then){
  var s=skNow(),m=s.L[s.k];S.skk=s.k;save();
  var o=modal('<div class="skm"><span class="skd" aria-hidden="true">'+ski(m.e)+'</span><p class="skr">Новое умение</p><h2>'+esc(m.n)+'</h2>'+rbSay('Теперь ты можешь '+esc(m.c)+'!')+'</div>',
   [['Посмотреть прогресс',function(){var f=then;then=null;setTimeout(function(){skills(f)},RM()?0:200)}],['Поделиться',function(){skShare();return false},1],['Дальше',null,1]]);
  var rm=o.remove;o.remove=function(){rm.call(o);if(then){var f=then;then=null;setTimeout(f,RM()?0:200)}};
  snd('ach');return o}
/* реплика кролика: голова без подложки и пузырь с хвостиком, как у персонажей Duolingo */
function rbSay(t){var hd=IMG.wowhead||IMG.eat;return'<div class="gsay">'+(hd?'<img class="gav" src="'+hd+'" alt="" draggable="false">':'')+'<p>'+t+'</p></div>'}
/* back — куда вернуться: в настройки (по умолчанию) или дальше по пути из окна нового умения */
/* U1-7: картинка «Я могу…» для «Поделиться». Без кролика и островка: логотип Python рядом с числом (как флаг у Duolingo),
   крупно «Я могу …!», а внизу — окно редактора с маленькой программой, которая и есть это умение, и её вывод.
   Логотип Python — товарный знак Python Software Foundation, используется без изменений, чтобы назвать язык (правила PSF это разрешают) */
var PYLOGO='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0.21 -0.077 110 110"><linearGradient id="a" gradientUnits="userSpaceOnUse" x1="63.8159" y1="56.6829" x2="118.4934" y2="1.8225" gradientTransform="matrix(1 0 0 -1 -53.2974 66.4321)"><stop offset="0" stop-color="#387EB8"/><stop offset="1" stop-color="#366994"/></linearGradient><path fill="url(#a)" d="M55.023-0.077c-25.971,0-26.25,10.081-26.25,12.156c0,3.148,0,12.594,0,12.594h26.75v3.781c0,0-27.852,0-37.375,0c-7.949,0-17.938,4.833-17.938,26.25c0,19.673,7.792,27.281,15.656,27.281c2.335,0,9.344,0,9.344,0s0-9.765,0-13.125c0-5.491,2.721-15.656,15.406-15.656c15.91,0,19.971,0,26.531,0c3.902,0,14.906-1.696,14.906-14.406c0-13.452,0-17.89,0-24.219C82.054,11.426,81.515-0.077,55.023-0.077z M40.273,8.392c2.662,0,4.813,2.150,4.813,4.813c0,2.661-2.151,4.813-4.813,4.813s-4.813-2.151-4.813-4.813C35.46,10.542,37.611,8.392,40.273,8.392z"/><linearGradient id="b" gradientUnits="userSpaceOnUse" x1="97.0444" y1="21.6321" x2="155.6665" y2="-34.5308" gradientTransform="matrix(1 0 0 -1 -53.2974 66.4321)"><stop offset="0" stop-color="#FFE052"/><stop offset="1" stop-color="#FFC331"/></linearGradient><path fill="url(#b)" d="M55.397,109.923c25.959,0,26.282-10.271,26.282-12.156c0-3.148,0-12.594,0-12.594H54.897v-3.781c0,0,28.032,0,37.375,0c8.009,0,17.938-4.954,17.938-26.25c0-23.322-10.538-27.281-15.656-27.281c-2.336,0-9.344,0-9.344,0s0,10.216,0,13.125c0,5.491-2.631,15.656-15.406,15.656c-15.91,0-19.476,0-26.532,0c-3.892,0-14.906,1.896-14.906,14.406c0,14.475,0,18.265,0,24.219C28.366,100.497,31.562,109.923,55.397,109.923z M70.148,101.454c-2.662,0-4.813-2.151-4.813-4.813s2.150-4.813,4.813-4.813c2.661,0,4.813,2.151,4.813,4.813S72.809,101.454,70.148,101.454z"/></svg>';
/* у каждой вехи — своя маленькая программа и её вывод */
var SKCODE={msg:['print("Привет, мир!")','Привет, мир!'],
 kbd:['name = input("Как тебя зовут? ")\nprint("Привет,", name)','Как тебя зовут? Влад\nПривет, Влад'],
 rcpt:['price = 349.9\nprint(f"Итого: {price:>8.2f} ₽")','Итого:   349.90 ₽'],
 fork:['age = int(input())\nif age >= 12:\n    print("Заходи!")\nelse:\n    print("Подрасти немного")','13\nЗаходи!'],
 loop:['for i in range(1, 5):\n    print("*" * i)','*\n**\n***\n****'],
 cut:['text = "Привет, мир!"\nprint(text[:6])\nprint(text[::-1])','Привет\n!рим ,тевирП'],
 list:['count = {}\nfor w in "ля ля ля оу".split():\n    count[w] = count.get(w, 0) + 1\nprint(count)',"{'ля': 3, 'оу': 1}"],
 fn:['def greet(*names, sep=", "):\n    return "Привет, " + sep.join(names)\n\nprint(greet("Аня", "Макс"))','Привет, Аня, Макс'],
 shield:['try:\n    n = int("сорок")\nexcept ValueError:\n    print("Это не число!")','Это не число!'],
 file:['with open("scores.csv") as f:\n    for line in f:\n        print(line.strip())','Аня,97\nМакс,85'],
 sort:['scores = [42, 97, 65, 88]\nscores.sort(reverse=True)\nprint(scores[:3])','[97, 88, 65]'],
 cube:['class Item:\n    def __init__(self, name, qty):\n        self.name = name\n        self.qty = qty\n\nprint(Item("мяч", 12).qty)','12'],
 tree:['class Hero:\n    hp = 100\n\nclass Mage(Hero):\n    mana = 50\n\nprint(Mage().hp, Mage().mana)','100 50'],
 grid:['import numpy as np\n\nimg = np.zeros((3, 3), int)\nimg[1, 1] = 255\nprint(img.sum())','255'],
 chart:['import pandas as pd\n\ndf = pd.read_csv("games.csv")\nprint(df["score"].mean())','78.4'],
 web:['import requests\n\nr = requests.get(URL + "/notes")\nprint(len(r.json()), "заметки")','3 заметки'],
 cap:['project = Project("мой бот")\nproject.build()\nproject.share()','Готово!']};
var SKBG={'':['#0B2E09','#1F6516','#43A034'],carrot:['#4A2302','#B65E08','#F08C1A'],pink:['#3E0A1B','#952746','#D9557A'],blue:['#081A44','#1A479A','#3B7BE6'],violet:['#170D3D','#4E31A8','#7E62E8']};
function skImg(cb,vr,k){
  var s=skNow(),m=s.L[k==null?s.k:k],P=k==null?s.p:Math.max(m.t,1),W=1080,H=1920,cv=document.createElement('canvas');cv.width=W;cv.height=H;
  var g=cv.getContext('2d'),F='Nunito,system-ui,-apple-system,"Segoe UI",sans-serif',MF='"Cascadia Code","Cascadia Mono",Consolas,ui-monospace,monospace',C=SKBG[ST('acc')]||SKBG[''],cd=SKCODE[m.e]||SKCODE.msg;cd=[cd[0],cd[1].replace(/Влад/g,String(S.nick||'Влад').slice(0,14))];
  function star(x,y,r,a){g.save();g.globalAlpha=a;var gl=g.createRadialGradient(x,y,0,x,y,r*1.6);gl.addColorStop(0,'rgba(255,255,255,.45)');gl.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=gl;g.beginPath();g.arc(x,y,r*1.6,0,6.283);g.fill();
    g.fillStyle='#fff';g.beginPath();g.moveTo(x,y-r);g.quadraticCurveTo(x,y,x+r*.38,y);g.quadraticCurveTo(x,y,x,y+r);g.quadraticCurveTo(x,y,x-r*.38,y);g.quadraticCurveTo(x,y,x,y-r);g.fill();g.restore()}
  function rr(x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}
  function wrap(t,mw){var w=t.split(' '),L=[],c='';w.forEach(function(x){var n=c?c+' '+x:x;if(g.measureText(n).width>mw&&c){L.push(c);c=x}else c=n});if(c)L.push(c);return L}
  /* подсветка: те же роли, что в редакторе ИТП — ключевые слова, строки, числа, вызовы, комментарии */
  var KW=/^(def|class|return|for|in|if|elif|else|import|from|as|with|while|True|False|None|and|or|not|print)$/;
  function line(t,x,y){var re=/(#.*$)|("[^"]*"|'[^']*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+)|([^\sA-Za-z_\d"'#]+)/g,mm;
    while((mm=re.exec(t))){var tx=mm[0],col='#E6E1D8';
      if(mm[1])col='#7F8794';else if(mm[2])col='#A8DC76';else if(mm[3])col='#F5A35C';
      else if(mm[4]){col=tx==='print'?'#E68BD8':KW.test(tx)?'#C99BFF':t.slice(re.lastIndex).trimStart().charAt(0)==='('?'#7EB8FF':'#E6E1D8'}else if(mm[6])col='#9AA3AF';
      g.fillStyle=col;g.fillText(tx,x,y);x+=g.measureText(tx).width}}
  function draw(logo){
    /* фон: тёмный тон акента сверху, светлее к низу; мягкое свечение за окном кода */
    var bg=g.createLinearGradient(0,0,W*.3,H);bg.addColorStop(0,C[0]);bg.addColorStop(.55,C[1]);bg.addColorStop(1,C[2]);g.fillStyle=bg;g.fillRect(0,0,W,H);
    var gw=g.createRadialGradient(W*.5,H*.74,60,W*.5,H*.74,760);gw.addColorStop(0,'rgba(255,255,255,.22)');gw.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=gw;g.fillRect(0,0,W,H);
    /* знаки кода, рассыпанные по фону, как конфетти */
    g.save();g.fillStyle='rgba(255,255,255,.07)';g.font='800 120px '+MF;g.textAlign='center';[['{ }',150,330,-12],['( )',930,300,10],[':',990,760,0],['#',90,820,-8],['[ ]',940,1090,8],['=',120,1180,0],['"',980,1500,-6]].forEach(function(q){g.save();g.translate(q[1],q[2]);g.rotate(q[3]*Math.PI/180);g.fillText(q[0],0,0);g.restore()});g.restore();
    /* шапка */
    g.textBaseline='alphabetic';g.textAlign='left';g.fillStyle='#fff';g.font='900 72px '+F;g.fillText('ИТП',96,170);
    g.font='700 28px '+F;g.fillStyle='rgba(255,255,255,.62)';g.fillText('И так, программирование',98,212);
    g.textAlign='right';g.font='800 30px '+F;g.fillStyle='rgba(255,255,255,.7)';g.fillText('ЧТО Я УМЕЮ',W-96,166);
    /* раскладка: логотип с числом, подпись, «Я могу…», окно кода — одной группой по центру между шапкой и низом */
    var code=cd[0].split('\n'),out=cd[1].split('\n'),lh=64,pw=W-150,ph=112+code.length*lh+40+out.length*lh+26;
    g.font='900 88px '+F;var L=wrap('Я могу '+m.c+'!',W-160),tot=250+70+L.length*106+90+ph,y0=290+Math.max(0,(H-170-290-tot)/2);
    var yc=y0+90,ls=170;g.font='900 200px '+F;var num=String(P),nw=g.measureText(num).width,x0=(W-(ls+44+nw))/2;
    if(logo){g.save();g.shadowColor='rgba(0,0,0,.28)';g.shadowBlur=30;g.shadowOffsetY=10;g.drawImage(logo,x0,yc-ls/2-8,ls,ls);g.restore()}
    g.textAlign='left';g.fillStyle='#fff';g.fillText(num,x0+ls+44,yc+70);
    g.textAlign='center';g.font='800 38px '+F;g.fillStyle='rgba(255,255,255,.72)';g.fillText(pl(P,['островок пройден','островка пройдено','островков пройдено'])+' на Python',W/2,yc+168);
    g.font='900 88px '+F;g.fillStyle='#fff';var hy=y0+250+70+64;L.forEach(function(l,i){g.fillText(l,W/2,hy+i*106)});
    var top=hy+(L.length-1)*106+40+90;
    g.save();g.translate(W/2,top+ph/2);g.rotate(-3*Math.PI/180);g.translate(-pw/2,-ph/2);
    g.shadowColor='rgba(0,0,0,.42)';g.shadowBlur=64;g.shadowOffsetY=26;rr(0,0,pw,ph,38);g.fillStyle='#16181C';g.fill();g.shadowColor='transparent';
    g.strokeStyle='rgba(255,255,255,.1)';g.lineWidth=2;rr(1,1,pw-2,ph-2,37);g.stroke();
    /* заголовок окна: маленький логотип и имя файла */
    if(logo)g.drawImage(logo,42,30,42,42);g.font='700 32px '+F;g.fillStyle='rgba(255,255,255,.55)';g.textAlign='left';g.fillText('skill.py',98,63);
    g.fillStyle='rgba(255,255,255,.08)';g.fillRect(0,98,pw,2);
    g.font='600 40px '+MF;code.forEach(function(l,i){var y=98+60+i*lh;g.fillStyle='rgba(255,255,255,.25)';g.textAlign='right';g.fillText(String(i+1),80,y);g.textAlign='left';line(l,112,y)});
    var oy=98+24+code.length*lh;g.save();rr(0,0,pw,ph,38);g.clip();g.fillStyle='rgba(255,255,255,.05)';g.fillRect(0,oy,pw,ph-oy);g.restore();g.fillStyle='rgba(255,255,255,.08)';g.fillRect(0,oy,pw,2);
    g.font='600 38px '+MF;out.forEach(function(l,i){g.fillStyle='#E6E1D8';g.fillText(l,112,oy+58+i*lh)});g.fillStyle='#7CD06A';g.fillText('›',62,oy+58);
    g.restore();
    star(110,top-30,38,.9);star(985,top-80,30,.85);star(990,1830,46,.9);star(70,1790,24,.7);star(880,y0-20,18,.6);
    cb(cv)}
  var im=new Image();
  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){im.onload=function(){draw(im)};im.onerror=function(){draw(null)};im.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(PYLOGO)})}
/* «Поделиться умением» — как в Duolingo: картинка крупно на затемнённом размытом фоне, сверху крестик, снизу «Сохранить» и «Отправить».
   Закрывается крестиком, Esc, «назад» и нажатием мимо картинки */
function skShare(k){
  var s=skNow(),m=s.L[k==null?s.k:k],BLOB=null,tx='Я учу Python в ИТП и уже могу '+m.c+'! Пройдено '+s.p+' '+pl(s.p,['островок','островка','островков'])+'.',prev=document.activeElement;
  var o=document.createElement('div');o.className='shov';o.setAttribute('role','dialog');o.setAttribute('aria-modal','true');o.setAttribute('aria-label','Поделиться умением');
  o.innerHTML='<button class="icon shx" aria-label="Закрыть">'+ico('x')+'</button><div class="shcard" id="shcard"><i class="shsk" aria-hidden="true"></i></div>'+
   '<div class="shbt"><button class="btn shs" id="shsv">'+phi('download-simple')+'Сохранить</button>'+(navigator.share?'<button class="btn shs" id="shgo">'+phi('export')+'Отправить</button>':'')+'</div>';
  document.body.appendChild(o);snd('open');
  var gone=false;function close(){if(gone)return;gone=true;snd('close');document.removeEventListener('keydown',kd,true);o.classList.add('out');if(prev&&prev.focus)try{prev.focus({preventScroll:true})}catch(e){}setTimeout(function(){o.remove()},RM()?0:200)}
  function kd(e){if(e.key==='Escape'){e.preventDefault();e.stopPropagation();close()}}
  document.addEventListener('keydown',kd,true);
  o.onclick=function(e){if(e.target===o)close()};o.querySelector('.shx').onclick=close;
  function need(){if(!BLOB){toast('Картинка ещё рисуется');return false}return true}
  $('shsv').onclick=function(){if(!need())return;saveFile('itp-skill.png',BLOB);ach('share');toast('Картинка сохранена')};
  if($('shgo'))$('shgo').onclick=function(){if(!need())return;var d={text:tx},f;try{f=new File([BLOB],'itp-skill.png',{type:'image/png'})}catch(e){}if(f&&navigator.canShare&&navigator.canShare({files:[f]}))d.files=[f];
    navigator.share(d).then(function(){ach('share')}).catch(function(){})};
  setTimeout(function(){var b=$('shsv');if(b)b.focus({preventScroll:true})},60);
  skImg(function(cv){var h=$('shcard');if(!h||gone)return;cv.setAttribute('role','img');cv.setAttribute('aria-label','Картинка: я могу '+m.c);h.innerHTML='';h.appendChild(cv);h.classList.add('rdy');cv.toBlob(function(b){BLOB=b},'image/png')},0,k)}
function skills(back){
  var s=skNow(),L=s.L,m=L[s.k];
  var h=subTop('Что ты уже умеешь','🏆',L[s.k+1]?'Дальше: '+esc(L[s.k+1].n||''):'Все умения открыты','',s.k,L.length-1)+'<div class="skp">'+
   '<div class="skh"><span class="sklogo" role="img" aria-label="Python">'+PYLOGO+'</span><b>'+s.p+'</b></div><p class="mu skn">'+pl(s.p,['островок пройден','островка пройдено','островков пройдено'])+' из '+L[L.length-1].t+', пропущенные тоже считаются'+(skHole()?'. И ещё '+skHole()+' в норах':'')+'</p>'+
   rbSay(s.k?'Значит, ты уже можешь '+esc(m.c)+'!':'Пройди первую тему, и здесь появится, что ты уже можешь')+(s.k?'<button class="btn t skshb" id="sksh">'+phi('export')+'Поделиться</button>':'')+
   '<h2 class="skov">Прогресс</h2><ol class="skl">'+L.map(function(x,i){var on=s.p>=x.t,nw=i===s.k;return'<li class="'+(on?'on':'')+(nw?' now':'')+(i+1<L.length&&s.p>=L[i+1].t?' fl':'')+'"><span class="skd">'+ski(x.e)+'</span><span class="sktx"><small>'+SKHX+x.t+'</small><b>'+esc(x.n)+'</b></span></li>'}).join('')+'</ol></div>';
  scr('skills',h);if($('sksh'))$('sksh').onclick=function(){skShare()};
  /* режим разработчика: нажми на любую веху — откроется её картинка «Я могу…» */
  if(DEV())app.querySelectorAll('.skl li').forEach(function(li,i){if(!i)return;li.classList.add('dv');li.setAttribute('role','button');li.tabIndex=0;li.onclick=function(){skShare(i)};li.onkeydown=function(e){if(e.key==='Enter')skShare(i)}});$('x').onclick=function(){if(typeof back==='function')back();else{SBACK=SBACK||profile;settings()}}}
/* U1-9: цель дня и цель серии выбираются в одном окне (sgChooser в a_screens.js) */
function goalSheet(){sgChooser(function(){if(CURTAB!=='prof')return;KEEPSCR=1;SKEY='profile';var y=window.scrollY;profile();window.scrollTo(0,y)})}
function profile(){BACK=profile;
  var n=ND(),LV=lvlInfo(S.xp),d=goalDone(),g=S.goal,gp=Math.min(100,Math.round(d/g*100)),f=S.fz,s=streakNow();
  var rows=TOPICS.map(function(t,i){var c=0,l=[];(t.items||[]).forEach(function(x,j){var e=S.es[i+'-'+j]||0;c+=e;if(e>0)l.push({j:j,n:x.n,e:e,ic:ity(x)[1]})});return{i:i,n:t.n,c:c,l:l}}).filter(function(r){return r.c>0}).sort(function(a,b){return b.c-a.c});
  var EM=3,more=rows.length>EM;
  function erow(r,k){return'<div class="eg2"'+(k>=EM?' hidden':'')+'><div class="erow"><span>'+esc(r.n)+'</span><b aria-label="ошибок: '+r.c+'">'+r.c+'</b></div><div class="elist">'+r.l.map(function(x){return'<button class="elink" data-i="'+r.i+'" data-j="'+x.j+'"><span class="et">'+x.ic+'&nbsp;'+esc(x.n)+'<small>ошибок: '+x.e+'</small></span><span class="eg">Отработать</span></button>'}).join('')+'</div></div>'}
  scr('profile',head()+'<h1 class="sr-only">Профиль</h1><div class="pf">'+
   '<div class="hero"><div class="pav" aria-hidden="true">'+rabbit('eat')+'</div><div class="hn"><b class="nmx">'+nk(S.nick)+'</b><div class="lvp"><span class="pill">Уровень '+LV.l+'</span><span class="mu">до '+(LV.l+1)+': ещё '+LV.left+' ⭐</span></div><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+LV.p+'" aria-label="Прогресс уровня"><i class="grow" style="width:'+LV.p+'%"></i></div></div></div>'+
   '<div class="tiles"><button class="tile tbig'+(s>=100?' d3':s>=10?' d2':'')+'" id="tst"><span aria-hidden="true">🥕</span><span><b>'+s+'</b><small>'+pl(s,['день','дня','дней'])+' подряд</small></span>'+(f.n?'<i class="fzm" aria-label="заморозок: '+f.n+'">❄️'+f.n+'</i>':'')+'</button><div class="tcol"><div class="tile"><span aria-hidden="true">🏆</span><span><b>'+Math.max(S.max,s)+'</b><small>рекорд серии</small></span></div><button class="tile" id="txp"><span aria-hidden="true">⭐</span><span><b>'+S.xp+'</b><small>опыта</small></span></button><div class="tile"><span aria-hidden="true">📚</span><span><b>'+n+' из '+NT()+'</b><small>тем пройдено</small></span></div>'+(HD()?'<div class="tile"><span aria-hidden="true">🐰</span><span><b>'+HD()+' из '+HN()+'</b><small>нор пройдено</small></span></div>':'')+'</div></div>'+
   '<section class="psec"><div class="ch2"><b>Цель дня</b><button class="btn t" id="gset">'+g+' '+pl(g,['островок','островка','островков'])+' ›</button></div><div class="psf"><div class="bar gbar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+gp+'" aria-label="Цель дня: '+d+' из '+g+'"><i class="grow" style="width:'+gp+'%"></i></div>'+weekRow('g')+(S.sg.n?'<p class="mu gnote">Цель серии: '+Math.min(s,S.sg.n)+' из '+S.sg.n+' '+pl(S.sg.n,['дня','дней','дней'])+' подряд, за неё +'+SGX[S.sg.n]+' ⭐.</p>':'<p class="mu gnote">Цель серии не выбрана. Нажми на цель дня, чтобы выбрать.</p>')+'</div></section>'+
   shelf()+
   '<section class="psec"><div class="ch2"><b>Активность</b></div><div class="psf">'+calHtml()+'</div></section>'+
   (rows.length?'<section class="psec"><div class="ch2"><b>Работа над ошибками</b></div><div class="psf">'+rows.map(erow).join('')+(more?'<button class="btn t emore" id="emr">Показать все темы ('+rows.length+')</button>':'')+'<p class="mu enote">Пройди островок без ошибок, и он исчезнет из списка.</p></div></section>':'')+
   '<div class="lst">'+row('📖','Изученные функции','Словарь с твоими заметками','dc')+(TOPICS[0]&&TOPICS[0].intro&&!S.d['0-0']?row('🏝️','Знакомство с ИТП','Как устроено приложение','intr'):'')+row('📤','Поделиться прогрессом','Картинка со статистикой','sh')+row('⚙️','Настройки','Вид, звук, обучение, резервная копия','st')+'</div>'+
   '<p class="pfoot"><button class="ver" id="vr" aria-label="ИТП '+ITPV+'. ИТП означает: И так, программирование"><u>ИТП '+ITPV+'</u><span class="vt" role="tooltip">ИТП — «И так, программирование»</span></button></p></div>','prof');
  /* подпись месяца стоит у его первого дня и часто уезжает влево за край — под лентой сразу сегодняшний день, потом тот, на который нажали */
  bindHead(profile);calBind();var ci0=$('ci');if(ci0&&!ci0.textContent)ci0.textContent=calText(day(new Date()));var csc=app.querySelector('.csc');if(csc){csc.tabIndex=0;csc.setAttribute('aria-label','Календарь активности, листается вбок')}
  var vr=$('vr'),vt;vr.onclick=function(){vr.classList.add('on');clearTimeout(vt);vt=setTimeout(function(){vr.classList.remove('on')},2500)};
  $('tst').onclick=streakSheet;$('txp').onclick=levelSheet;$('gset').onclick=goalSheet;
  if($('emr'))$('emr').onclick=function(){app.querySelectorAll('.eg2[hidden]').forEach(function(x){x.hidden=false});this.remove()};
  app.querySelectorAll('.fd').forEach(function(b){b.onclick=function(){fdOpen(b)}});
  app.querySelectorAll('.lst .li').forEach(function(b){b.onclick=function(){var a=b.dataset.a;if(a==='dc')dict();else if(a==='sh')share();else if(a==='intr'){BACK=profile;theory(0,0)}else if(a==='st'){SBACK=profile;settings()}}});
  app.querySelectorAll('.elink').forEach(function(b){b.onclick=function(){BACK=profile;go(+b.dataset.i,+b.dataset.j)}});
}

/* --- настройки (второй уровень: без нижней панели, назад — туда, откуда пришли) --- */
/* подсказка: строки, которые целиком код (print(...), a = int(input()), for ...), — моноширинным, как в теории */
function hintTx(h){return String(h||'').split('\n').map(function(l){return/^([A-Za-z_][\w.]*\s*(\(|\[|=|\+=|-=)|(for|if|elif|else|while|def|import|from|return)\b)/.test(l.trim())?'<code class="hcl">'+esc(l)+'</code>':esc(l)}).join('<br>')}
function SW(k,on,lab){return'<button class="sw" role="switch" aria-checked="'+(on?'true':'false')+'" data-k="'+k+'"'+(lab?' aria-label="'+esc(lab)+'"':'')+'></button>'}
function SG(k,opts,cur){return'<div class="segc" role="radiogroup">'+opts.map(function(o){var on=String(cur)===String(o[0]);return'<button role="radio" aria-checked="'+on+'" data-k="'+k+'" data-v="'+o[0]+'" class="'+(on?'on':'')+'">'+o[1]+'</button>'}).join('')+'</div>'}
function SR(ic,t,sub,ctl,a){var blk=ctl&&/segc|swa|type="range"/.test(ctl),sw=ctl&&/class="sw"/.test(ctl);if(sw)ctl=ctl.replace('class="sw"','class="sw" aria-label="'+esc(t)+'"');return(a?'<button class="li" data-a="'+a+'">':'<div class="li static'+(blk?' blk':'')+(sw?' tg':'')+'">')+'<span class="lic" aria-hidden="true">'+ic+'</span><span class="lt">'+t+(sub?'<small>'+sub+'</small>':'')+'</span>'+(ctl||ico('chev','ch'))+(a?'</button>':'</div>')}
function setSet(k,v){
  if(k==='theme'){themeSwap(function(){S.theme=v;save();applyPrefs()});return}
  if(k==='mute'){S.mute=v?0:1}else if(k==='goal'){S.goal=+v}else if(k==='g'){S.g=v}else if(k==='hc'){S.hc=v?0:1}
  else{S.set[k]=(typeof v==='number'||typeof v==='boolean')?v:(/^\d+$/.test(v)?+v:v)}
  save();applyPrefs();
  if(k==='emo'){if(ST('emo')){emoLoad();if(EM.map)emoOn()}else emoOff()}
  if(k==='goal')goalCheck()}
function settings(){
  var h=subTop('Настройки','⚙️',S.nick?esc(S.nick):'');
  h+='<div class="sec">Внешний вид</div><div class="lst">'+
   SR('🎨','Тема','',SG('theme',[['','Авто'],['light','Светлая'],['dark','Тёмная']],S.theme))+
   SR('🖌️','Цвет акцента','Кнопки, полоски, выделение','<div class="swa" role="radiogroup" aria-label="Цвет акцента">'+[['','#2B8420','Зелёный'],['carrot','#F08C1A','Морковный'],['pink','#C73B63','Розовый'],['blue','#2563D0','Синий'],['violet','#6C4BD6','Фиолетовый']].map(function(c){var on=ST('acc')===c[0];return'<button role="radio" aria-checked="'+on+'" data-k="acc" data-v="'+c[0]+'" style="background:'+c[1]+';color:'+c[1]+'" class="'+(on?'on':'')+'" aria-label="'+c[2]+'"></button>'}).join('')+'</div>')+
   SR('🔤','Размер текста','',SG('tz',[[90,'Мелкий'],[100,'Обычный'],[115,'Крупный'],[130,'Огромный']],ST('tz')))+
   SR('✨','Анимации','«Выкл» подойдёт слабым устройствам и тем, кого они отвлекают',SG('anim',[['full','Все'],['less','Меньше'],['off','Выкл']],ST('anim')))+
   SR('😀','Смайлики Windows 11','Встроены и выглядят одинаково на всех устройствах',SW('emo',ST('emo')))+
   SR('🎉','Конфетти','Салют, когда тема пройдена',SW('gc',ST('gc')))+
   SR('🐰','Шапка профиля','Где стоит кролик',SG('ph',[['card','Карточка'],['corner','В углу'],['pop','Из плитки']],ST('ph')))+
   SR('🌊','Узор на фоне','Точки — как тропинка между островками; пятна — мягкие цветные пятна, как раньше; пусто — ровный фон',SG('bgp',[['dots','Точки'],['blobs','Пятна'],['none','Пусто']],ST('bgp')))+'</div>';
  h+='<div class="sec">Полка достижений</div><div class="lst">'+
   SR('🗄️','Когда дискет много','',SG('sh',[['v','Вторая полка ниже'],['h','Листать вбок']],ST('sh')))+
   SR('💾','Вид дискет','',SG('fl',[['tilt','Объёмные'],['flat','Плоские']],ST('fl')))+'</div>';
  h+='<div class="sec">Звук и отклик</div><div class="lst">'+
   SR('🔊','Звук','Главный выключатель: выкл — полная тишина',SW('mute',!S.mute))+
   SR('🎚️','Громкость','','<input type="range" min="0" max="100" step="5" value="'+ST('vol')+'" id="vol" aria-label="Громкость">')+
   SR('👆','Звуки интерфейса','Касания, переходы и окна. Ответы, опыт и награды звучат всегда',SW('sfx',ST('sfx')))+
   SR('⌨️','Звуки набора кода','Очень тихий щелчок клавиш в редакторе',SW('ks',ST('ks')))+
   SR('📳','Вибрация','При ошибке и успехе',SW('vib',ST('vib')))+'</div>';
  h+='<div class="sec">Обучение</div><div class="lst">'+
   SR('🎯','Цель дня','Сколько островков в день',SG('goal',[[1,'1'],[2,'2'],[3,'3']],S.goal))+
   SR('⌨️','Печатать теорию по буквам','Выкл: текст появится сразу',SW('ty',ST('ty')))+
   SR('📑','Оглавление теории','Слева на широких экранах',SW('toc',ST('toc')))+
   SR('📐','Пример в задании','Компактно: ввод и вывод рядом, больше места для кода',SG('exl',[['c','Компактно'],['b','Крупно']],ST('exl')))+
   SR('🔁','Повторение после перерыва','3 вопроса, если не заходил 3 дня и больше',SW('rep',ST('rep')))+
   SR('💡','Спрашивать про подсказку','Напомнить, что опыт будет вдвое меньше',SW('hc',!S.hc))+'</div>';
  h+='<div class="sec">Редактор кода</div><div class="lst">'+
   SR('🔠','Размер кода','',SG('cf',[[13,'S'],[15,'M'],[17,'L'],[19,'XL']],ST('cf')))+
   SR('🔢','Номера строк','',SW('ln',ST('ln')))+
   SR('🧩','Закрывать скобки и кавычки','Сама допишет пару',SW('ac',ST('ac')))+'</div>';
  var skn=skNow();
  h+='<div class="sec">Профиль и данные</div><div class="lst">'+
   SR('🌱','Что ты уже умеешь',skn.k?esc(skn.L[skn.k].n)+', '+skn.p+' '+pl(skn.p,['островок','островка','островков']):'Шкала умений курса','','skl')+
   plRow()+SR('🐰','Никнейм',nk(S.nick),'','nick')+
   SR('🙂','Обращение','Для правильных окончаний в тексте',SG('g',[['m','Парень'],['f','Девушка'],['','Не указывать']],S.g||''))+
   SR('💾','Резервная копия','Сохранить или загрузить прогресс','','bk')+
   SR('🧹','Сбросить оформление','Вернуть вид и звук как было','','rs1')+
   SR('🗑️','Сбросить прогресс','Удалит всё, кроме сохранённых кодов и звука','','rs2')+'</div>';
  h+='<div class="sec">О приложении</div><div class="lst">'+(KBD?SR('⌨️','Горячие клавиши','','','kb'):'')+SR('📖','Прочитать введение','Знакомство с ИТП ещё раз','','intro')+SR('🐇','ИТП','«И так, программирование»','<span class="lv" id="egv">'+ITPV+'</span>')+'</div><div style="height:24px"></div>';
  scr('settings',h,null);HRE=settings;
  $('x').onclick=function(){(SBACK||profile)()};
  function again(){var yy=window.scrollY;KEEPSCR=1;SKEY='settings';settings();window.scrollTo(0,yy)}
  app.querySelectorAll('.sw').forEach(function(b){b.onclick=function(e){e.stopPropagation();var on=b.getAttribute('aria-checked')!=='true';var k=b.dataset.k;b.setAttribute('aria-checked',on?'true':'false');if(!on)snd('off');setSet(k,on?1:0);if(on)snd('on')}});
  /* строку с выключателем можно нажать целиком: так проще попасть пальцем */
  app.querySelectorAll('.li.tg').forEach(function(r){r.onclick=function(e){if(e.target.closest('.sw'))return;var s=r.querySelector('.sw');if(s)s.click()}});
  app.querySelectorAll('.segc button,.swa button').forEach(function(b){b.onclick=function(){var g=b.parentNode;g.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-checked',x===b?'true':'false')});setSet(b.dataset.k,b.dataset.v);snd('click');if(g.classList.contains('segc'))segPos(g,true)}});
  eggBind();
  var v=$('vol');v.oninput=function(){S.set.vol=+v.value;save();sxVol(VOLK())};v.onchange=function(){snd('ok')};
  app.querySelectorAll('.lst button.li').forEach(function(b){b.onclick=function(){var a=b.dataset.a;
    if(a==='nick')askName('Никнейм',S.nick,function(n){n=Array.from(n).slice(0,20).join('');if(nkBad(n)){snd('bad');toast('🐰 Так ник назвать нельзя');return false}S.nick=n;save();again();toast('Никнейм изменён')},20);
    else if(a==='bk')backup();
    else if(a==='skl')skills();
    else if(a==='kb')keys();
    else if(a==='intro'){BACK=function(){settings()};theory(0,0)}
    else if(a==='rs1')modal('<h2>Сбросить оформление?</h2><p>Тема, цвет, размер текста, звук и другие настройки станут как в начале. Прогресс не изменится.</p>',[['Сбросить',function(){themeSwap(function(){S.set=clean({}).set;S.theme='';S.mute=0;save();applyPrefs();emoLoad();again()});toast('Настройки сброшены')},0,1],['Отмена',null,1]]);
    else if(a==='rs2')modal('<h2>Сбросить весь прогресс?</h2><p>Опыт, серия, пройденные островки, достижения и настройки оформления удалятся, знакомство начнётся заново. Сохранённые коды и звук останутся. Отменить это нельзя.</p>',[['Да, сбросить',function(){S=clean({mute:S.mute,sv:S.sv,ec:S.ec,cur:S.cur,nick:''});applyTheme();seedLit();save();nick()},0,1],['Отмена',null,1]])}});
}
/* --- оглавление теории (широкие экраны) --- */
var TOCS=null;
function tocKill(){var o=document.getElementById('toc');if(o)o.remove();if(TOCS){window.removeEventListener('scroll',TOCS);TOCS=null}}
function tocBuild(){
  tocKill();if(!ST('toc'))return;var tb=$('tb');if(!tb)return;
  var hs=[].slice.call(tb.querySelectorAll('h3'));if(hs.length<2)return;
  var a=document.createElement('nav');a.id='toc';a.setAttribute('aria-label','Оглавление');
  a.innerHTML='<div class="tct">Оглавление</div>'+hs.map(function(h,k){h.id='tcs'+k;return'<button data-k="'+k+'">'+esc(h.textContent)+'</button>'}).join('');
  document.body.appendChild(a);
  var bs=[].slice.call(a.querySelectorAll('button'));
  bs.forEach(function(b){b.onclick=function(){tb.click();hs[+b.dataset.k].scrollIntoView({behavior:RM()?'auto':'smooth',block:'start'})}});
  function spy(){var y=innerHeight*.32,c=-1;hs.forEach(function(h,k){if(h.offsetParent&&h.getBoundingClientRect().top<y)c=k});if(window.scrollY>0&&window.scrollY+innerHeight>=document.documentElement.scrollHeight-6){for(var q=hs.length-1;q>=0;q--)if(hs[q].offsetParent){c=q;break}}bs.forEach(function(b,k){b.classList.toggle('on',k===c)})}
  TOCS=spy;window.addEventListener('scroll',spy,{passive:true});if(window.ResizeObserver){var ro=new ResizeObserver(function(){if(!a.isConnected||!TOCS){ro.disconnect();return}TOCS()});ro.observe(document.body)}setTimeout(spy,50)}

/* --- рост серии и опыта в шапке --- */
var LSK=null,LXP=null;
function chipFx(){
  var hs=$('hs'),hx=$('hx');if(!hs||!hx)return;
  var s=streakNow(),x=S.xp;
  if(LSK!==null&&s>LSK)snd('streak');
  if(LSK!==null&&s>LSK&&!RM())hs.animate([{transform:'scale(1)'},{transform:'scale(1.25) rotate(-4deg)'},{transform:'scale(1)'}],{duration:520,easing:'cubic-bezier(.3,1.6,.5,1)'});
  if(LXP!==null&&x>LXP){
    var el=hx.querySelector('span:last-child'),a=LXP,t0=performance.now();
    if(RM()){el.textContent=x;snd('xpt',{k:0})}else{hx.animate([{transform:'scale(1)'},{transform:'scale(1.18)'},{transform:'scale(1)'}],{duration:600,easing:'cubic-bezier(.3,1.4,.5,1)'});
    var xt=xpTick();(function st(t){var k=Math.min(1,(t-t0)/700),vv=Math.round(a+(x-a)*(1-Math.pow(1-k,3)));el.textContent=vv;xt(vv-a);if(k<1)requestAnimationFrame(st)})(t0)}}
  LSK=s;LXP=x}
