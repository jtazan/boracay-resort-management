const errorBanner = document.getElementById('error-banner');
const refreshBtn = document.getElementById('refresh-btn');
const statsGrid = document.getElementById('stats-grid');
const propertiesGrid = document.getElementById('properties-grid');
const networkGrid = document.getElementById('network-grid');
const reservationsTable = document.getElementById('reservations-table');
const alertsGrid = document.getElementById('alerts-grid');
const propertySelect = document.getElementById('property-select');
const reservationForm = document.getElementById('reservation-form');

function showError(message) {
  errorBanner.textContent = message;
  errorBanner.classList.remove('hidden');
}

function clearError() {
  errorBanner.textContent = '';
  errorBanner.classList.add('hidden');
}

function setStatusBadge(status) {
  if (!status) return '<span class="badge">Unknown</span>';
  const normalized = status.toLowerCase();
  if (normalized.includes('healthy') || normalized.includes('stable') || normalized.includes('confirmed') || normalized.includes('checked-in')) {
    return '<span class="badge">' + status + '</span>';
  }
  if (normalized.includes('warning') || normalized.includes('monitoring') || normalized.includes('pending')) {
    return '<span class="badge warning">' + status + '</span>';
  }
  return '<span class="badge danger">' + status + '</span>';
}

function renderStats(data) {
  const cards = [
    { label: 'Properties', value: data.total_properties, meta: `${data.healthy_properties} healthy` },
    { label: 'Rooms', value: data.total_rooms, meta: `${data.avg_occupancy}% avg occupancy` },
    { label: 'Network uptime', value: `${data.network_uptime}%`, meta: 'SLA target 99.9%' },
    { label: 'Open alerts', value: data.critical_alerts, meta: `${data.upcoming_stays} upcoming stays` },
  ];

  statsGrid.innerHTML = cards.map(card => `
    <div class="stat-card">
      <div class="label">${card.label}</div>
      <div class="value">${card.value}</div>
      <div class="meta">${card.meta}</div>
    </div>
  `).join('');
}

function renderProperties(properties) {
  propertiesGrid.innerHTML = properties.map(property => `
    <div class="property-card">
      <div class="meta-row">
        <h4>${property.name}</h4>
        ${setStatusBadge(property.status)}
      </div>
      <div class="meta-row">
        <span>${property.region}</span>
        <span>${property.occupancy}% occupied</span>
      </div>
      <div class="meta-row">
        <span>Rooms</span>
        <span>${property.room_count}</span>
      </div>
      <div class="meta-row">
        <span>Guest Wi-Fi</span>
        <span>${property.guest_wifi_status}</span>
      </div>
      <div class="meta-row">
        <span>Uptime</span>
        <span>${property.uptime}%</span>
      </div>
      <div class="meta-row">
        <span>Bandwidth</span>
        <span>${property.bandwidth} Mbps</span>
      </div>
    </div>
  `).join('');
}

function renderNetwork(segments) {
  networkGrid.innerHTML = segments.map(segment => `
    <div class="network-card">
      <div class="meta-row">
        <h4>VLAN ${segment.id}</h4>
        ${setStatusBadge(segment.status)}
      </div>
      <div class="meta-row">
        <span>${segment.name}</span>
        <span>${segment.subnet}</span>
      </div>
      <ul>
        ${segment.controls.map(control => `<li>${control}</li>`).join('')}
      </ul>
    </div>
  `).join('');
}

function renderReservations(reservations) {
  reservationsTable.innerHTML = reservations.map(item => `
    <tr>
      <td>${item.id}</td>
      <td>${item.guest_name}</td>
      <td>${item.property_name}</td>
      <td>${item.room_number}</td>
      <td>${setStatusBadge(item.status)}</td>
    </tr>
  `).join('');
}

function renderAlerts(alerts) {
  alertsGrid.innerHTML = alerts.map(alert => `
    <div class="alert-card">
      <div class="meta-row">
        <h4>${alert.id}</h4>
        <span class="badge ${alert.severity === 'Critical' ? 'danger' : alert.severity === 'Warning' ? 'warning' : ''}">${alert.severity}</span>
      </div>
      <p>${alert.message}</p>
      <div class="meta-row">
        <span>${alert.property}</span>
        <span>${alert.status}</span>
      </div>
    </div>
  `).join('');
}

function populatePropertyOptions(properties) {
  propertySelect.innerHTML = properties.map(property => `
    <option value="${property.id}">${property.name}</option>
  `).join('');
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.message || errorBody.error || 'Request failed');
  }

  return response.json();
}

async function loadDashboard() {
  clearError();
  try {
    const [dashboard, properties, segments, reservations, alerts] = await Promise.all([
      fetchJson('/api/dashboard'),
      fetchJson('/api/properties'),
      fetchJson('/api/network-segments'),
      fetchJson('/api/reservations'),
      fetchJson('/api/alerts'),
    ]);

    renderStats(dashboard);
    renderProperties(properties);
    renderNetwork(segments);
    renderReservations(reservations);
    renderAlerts(alerts);
    populatePropertyOptions(properties);
  } catch (error) {
    showError(`Failed to load dashboard: ${error.message}`);
  }
}

reservationForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearError();

  const formData = new FormData(reservationForm);
  const payload = {
    guest_name: formData.get('guest_name'),
    property_id: formData.get('property_id'),
    room_number: formData.get('room_number'),
    partner: formData.get('partner'),
    check_in: formData.get('check_in'),
    check_out: formData.get('check_out'),
    status: 'Confirmed',
  };

  try {
    await fetchJson('/api/reservations', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    reservationForm.reset();
    await loadDashboard();
  } catch (error) {
    showError(`Reservation failed: ${error.message}`);
  }
});

refreshBtn.addEventListener('click', loadDashboard);

loadDashboard();
