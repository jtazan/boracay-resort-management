* {
  box-sizing: border-box;
}

:root {
  --bg: #0f172a;
  --panel: #111827;
  --panel-alt: #1f2937;
  --soft: #e5e7eb;
  --muted: #94a3b8;
  --accent: #22c55e;
  --warning: #f59e0b;
  --danger: #ef4444;
  --primary: #38bdf8;
  --border: rgba(148, 163, 184, 0.18);
  --shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
}

html, body {
  margin: 0;
  font-family: Inter, "Segoe UI", sans-serif;
  background: linear-gradient(180deg, #020817, #111827);
  color: var(--soft);
}

body {
  min-height: 100vh;
}

.app-shell {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: rgba(15, 23, 42, 0.85);
  border-right: 1px solid var(--border);
  padding: 24px 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 36px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary), #60a5fa);
  color: white;
  font-weight: 700;
}

.eyebrow {
  margin: 0 0 6px;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
}

h1, h2, h3, p {
  margin-top: 0;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-link {
  text-decoration: none;
  color: var(--soft);
  background: rgba(148, 163, 184, 0.06);
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 10px 12px;
  transition: 0.2s ease;
}

.nav-link:hover, .nav-link.active {
  background: rgba(56, 189, 248, 0.12);
  border-color: rgba(56, 189, 248, 0.2);
}

.main-panel {
  padding: 28px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}

.primary-btn {
  border: none;
  background: linear-gradient(135deg, var(--primary), #2563eb);
  color: white;
  border-radius: 10px;
  padding: 12px 16px;
  cursor: pointer;
  font-weight: 600;
}

.panel-section {
  margin-bottom: 28px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 16px;
}

.stat-card, .property-card, .network-card, .alert-card, .card {
  background: rgba(17, 24, 39, 0.9);
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: var(--shadow);
}

.stat-card {
  padding: 18px;
}

.stat-card .label {
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.stat-card .value {
  font-size: clamp(1.5rem, 2vw, 2.2rem);
  font-weight: 700;
  margin: 10px 0 6px;
}

.stat-card .meta {
  color: var(--accent);
  font-weight: 600;
}

.properties-grid, .network-grid, .alerts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.property-card, .network-card, .alert-card {
  padding: 18px;
}

.property-card h4, .network-card h4, .alert-card h4 {
  margin-bottom: 16px;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin: 8px 0;
  color: var(--muted);
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 700;
  background: rgba(34, 197, 94, 0.12);
  color: #a7f3d0;
}

.badge.warning {
  background: rgba(245, 158, 11, 0.12);
  color: #fcd34d;
}

.badge.danger {
  background: rgba(239, 68, 68, 0.12);
  color: #fca5a5;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.two-column {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr;
  gap: 20px;
}

.card {
  padding: 18px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  text-align: left;
  padding: 10px 8px;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
}

th {
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 11px;
}

.form-card form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  color: var(--muted);
  font-size: 12px;
}

input, select {
  border: 1px solid var(--border);
  border-radius: 10px;
  background: rgba(15, 23, 42, 0.7);
  color: var(--soft);
  padding: 10px 12px;
}

.error-banner {
  margin-bottom: 16px;
  border-radius: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(239, 68, 68, 0.35);
  background: rgba(239, 68, 68, 0.12);
  color: #fecaca;
}

.hidden {
  display: none;
}

@media (max-width: 900px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .two-column {
    grid-template-columns: 1fr;
  }
}
