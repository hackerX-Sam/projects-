const alertForm = document.getElementById('alertForm');
const helpForm = document.getElementById('helpForm');
const alertList = document.getElementById('alertList');
const helpList = document.getElementById('helpList');

// Submit alert
alertForm.onsubmit = async (e) => {
  e.preventDefault();
  const type = document.getElementById('type').value;
  const location = document.getElementById('location').value;
  await fetch('http://localhost:3000/api/alert', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type, location })
  });
  alertForm.reset();
  loadAlerts();
};

// Submit help
helpForm.onsubmit = async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const need = document.getElementById('need').value;
  await fetch('http://localhost:3000/api/help', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, need })
  });
  helpForm.reset();
  loadHelp();
};

// Load alerts
async function loadAlerts() {
  const res = await fetch('http://localhost:3000/api/alerts');
  const data = await res.json();
  alertList.innerHTML = data.map(a => `<li>${a.type} at ${a.location}</li>`).join('');
}

// Load help
async function loadHelp() {
  const res = await fetch('http://localhost:3000/api/help');
  const data = await res.json();
  helpList.innerHTML = data.map(h => `<li>${h.name} needs ${h.need}</li>`).join('');
}

loadAlerts();
loadHelp();
