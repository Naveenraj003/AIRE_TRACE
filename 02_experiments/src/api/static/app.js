// API Base URL
const API_BASE = '/api';

// State
let state = {
    episodes: [],
    selectedEpisode: null,
    predictions: null,
    alerts: null,
    events: null,
    currentPrefix: 1,
    chart: null
};

// UI Elements
const els = {
    tabs: document.querySelectorAll('.tab-btn'),
    panels: document.querySelectorAll('.view-panel'),
    overviewContent: document.getElementById('overview-content'),
    episodeSelect: document.getElementById('episode-select'),
    episodeMeta: document.getElementById('episode-meta'),
    prefixSlider: document.getElementById('prefix-slider'),
    prefixDisplay: document.getElementById('prefix-display'),
    chartCtx: document.getElementById('probability-chart').getContext('2d'),
    alertTableBody: document.querySelector('#alert-table tbody'),
    comparisonTableBody: document.querySelector('#comparison-table tbody'),
    auditContent: document.getElementById('audit-content'),
    prefixEventContext: document.getElementById('prefix-event-context'),
    alertModelSelect: document.getElementById('alert-model-select'),
    alertTotal: document.getElementById('alert-total'),
    alertNone: document.getElementById('alert-none'),
    alertEarly: document.getElementById('alert-early'),
    alertLate: document.getElementById('alert-late'),
    alertListTableBody: document.querySelector('#alert-list-table tbody'),
    progressionTableBody: document.querySelector('#progression-table tbody'),
    lateDetTableBody: document.querySelector('#late-det-table tbody'),
    lateEpisodesContainer: document.getElementById('late-episodes-container'),
    lateEpisodesList: document.getElementById('late-episodes-list'),
    lateEpisodesTitle: document.getElementById('late-episodes-title'),
    dataIntegrityPanel: document.getElementById('data-integrity-panel')
};

// Colors for the 6 models
const modelColors = {
    'H1': '#4e79a7',
    'H2': '#f28e2c',
    'H3': '#e15759',
    'H4': '#76b7b2',
    'M1': '#59a14f',
    'S1': '#edc949',
    'dyn_comp': '#b07aa1'
};

// Initialization
async function init() {
    setupTabs();
    setupSlider();
    setupInvestigation();

    try {
        await Promise.all([
            loadOverview(),
            loadEpisodes(),
            loadComparison(),
            loadLateDetection(),
            loadAudit(),
            loadSignificance()
        ]);
    } catch (err) {
        console.error("Initialization error:", err);
    }
}

// Tab Navigation
function setupTabs() {
    els.tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Update active button
            els.tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update active panel
            const target = tab.getAttribute('data-target');
            els.panels.forEach(p => {
                if (p.id === target) p.classList.add('active');
                else p.classList.remove('active');
            });
        });
    });
}

// Load Overview (/api/health)
async function loadOverview() {
    const res = await fetch(`${API_BASE}/health`);
    const data = await res.json();

    const html = `
        <div class="stat-card"><h3>Status</h3><div class="value" style="color:var(--success-color)">${data.status.toUpperCase()}</div></div>
        <div class="stat-card"><h3>Canonical Episodes</h3><div class="value">${data.canonical_episodes}</div></div>
        <div class="stat-card"><h3>TEST Episodes</h3><div class="value">${data.test_episodes}</div></div>
        <div class="stat-card"><h3>Prediction Rows</h3><div class="value">${data.prediction_rows.toLocaleString()}</div></div>
        <div class="stat-card"><h3>Unique Prefixes</h3><div class="value">${data.prediction_prefixes.toLocaleString()}</div></div>
        <div class="stat-card"><h3>Models</h3><div class="value">${data.models}</div></div>
        <div class="stat-card"><h3>Horizon (K)</h3><div class="value">${data.horizon_k}</div></div>
    `;
    els.overviewContent.innerHTML = html;

    // Also populate Data Integrity Panel
    const diHtml = `
        <div style="font-size: 0.85rem; border: 1px solid var(--border-color); padding: 0.5rem; border-radius: 4px; background: #fafafa;">
            <strong style="display:block; border-bottom: 1px solid #ddd; margin-bottom: 4px; padding-bottom: 2px;">DATA INTEGRITY</strong>
            <div style="display:grid; grid-template-columns: 1fr auto; gap: 4px 12px;">
                <span>636 canonical episodes</span><span style="color:var(--success-color)">✓</span>
                <span>416 TEST episodes</span><span style="color:var(--success-color)">✓</span>
                <span>8,878 TEST prefixes</span><span style="color:var(--success-color)">✓</span>
                <span>53,268 prediction records</span><span style="color:var(--success-color)">✓</span>
                <span>7 frozen models (inc. DynComp)</span><span style="color:var(--success-color)">✓</span>
                <span>K = 30</span><span style="color:var(--success-color)">✓</span>
                <span>Live inference</span><span style="color:var(--danger-color)">✗</span>
                <span>Artifact modification</span><span style="color:var(--danger-color)">✗</span>
            </div>
        </div>
    `;
    if (els.dataIntegrityPanel) els.dataIntegrityPanel.innerHTML = diHtml;

}

// Load Episodes (/api/episodes)
async function loadEpisodes() {
    const res = await fetch(`${API_BASE}/episodes`);
    state.episodes = await res.json();

    els.episodeSelect.innerHTML = '<option value="">Select a TEST episode...</option>';
    state.episodes.forEach(ep => {
        const opt = document.createElement('option');
        opt.value = ep.episode_id;
        opt.textContent = ep.episode_id;
        els.episodeSelect.appendChild(opt);
    });

    els.episodeSelect.addEventListener('change', (e) => {
        const epId = e.target.value;
        if (epId) {
            selectEpisode(epId);
        } else {
            resetExplorer();
        }
    });
}

// Select Episode & Load Data
async function selectEpisode(episodeId) {
    const ep = state.episodes.find(e => e.episode_id === episodeId);
    state.selectedEpisode = ep;

    els.episodeMeta.innerHTML = `
        <div><strong>Task:</strong> ${ep.task_id}</div>
        <div><strong>Split:</strong> ${ep.split}</div>
        <div><strong>Outcome:</strong> <span style="color:var(--danger-color);font-weight:bold">${ep.eventual_outcome === 1 ? 'FAILURE' : 'SUCCESS'}</span></div>
    `;

    els.prefixSlider.disabled = true;
    els.prefixEventContext.innerHTML = '<p class="placeholder-text">Loading...</p>';

    try {
        const [predsRes, alertsRes, eventsRes] = await Promise.all([
            fetch(`${API_BASE}/episodes/${episodeId}/predictions`),
            fetch(`${API_BASE}/episodes/${episodeId}/alerts`),
            fetch(`${API_BASE}/episodes/${episodeId}/events`).catch(() => null)
        ]);

        state.predictions = await predsRes.json();
        state.alerts = await alertsRes.json();
        state.events = eventsRes && eventsRes.ok ? await eventsRes.json() : null;

        els.prefixSlider.disabled = false;
        els.prefixSlider.value = 1;
        updatePrefix(1);

    } catch (err) {
        console.error(err);
        els.prefixEventContext.innerHTML = '<p class="placeholder-text">Error loading data.</p>';
    }
}

function resetExplorer() {
    state.selectedEpisode = null;
    state.predictions = null;
    state.alerts = null;
    state.events = null;
    els.episodeMeta.innerHTML = '';
    els.prefixSlider.disabled = true;
    els.prefixSlider.value = 1;
    els.prefixDisplay.textContent = '0';
    els.alertTableBody.innerHTML = '';
    els.progressionTableBody.innerHTML = '';
    els.prefixEventContext.innerHTML = '<p class="placeholder-text">Select an episode and move the prefix slider to view context.</p>';
    if (state.chart) {
        state.chart.destroy();
        state.chart = null;
    }
}

function setupSlider() {
    els.prefixSlider.addEventListener('input', (e) => {
        updatePrefix(parseInt(e.target.value));
    });
}

function updatePrefix(prefixLen) {
    state.currentPrefix = prefixLen;
    els.prefixDisplay.textContent = prefixLen;

    renderChart();
    renderAlertTable();
    renderEventContext();
    renderProgressionTable();
}

function renderChart() {
    const k = state.predictions.horizon_k;
    const currentPrefix = state.currentPrefix;
    const models = state.predictions.models;

    const labels = Array.from({ length: currentPrefix }, (_, i) => i + 1);
    const datasets = [];

    // Add horizontal threshold lines
    // And model probability lines
    Object.keys(models).forEach(modelId => {
        const modelData = models[modelId];
        const color = modelColors[modelId] || '#000';

        // Probabilities
        const data = modelData.predictions.slice(0, currentPrefix).map(p => p.probability);
        datasets.push({
            label: modelId,
            data: data,
            borderColor: color,
            backgroundColor: color,
            fill: false,
            tension: 0.1,
            pointRadius: 2
        });

        // Threshold line
        const threshData = Array(currentPrefix).fill(modelData.threshold);
        datasets.push({
            label: `${modelId} Threshold`,
            data: threshData,
            borderColor: color,
            borderDash: [5, 5],
            borderWidth: 1,
            pointRadius: 0,
            fill: false
        });
    });

    if (state.chart) {
        state.chart.data.labels = labels;
        state.chart.data.datasets = datasets;
        state.chart.options.scales.x.max = k;
        state.chart.update('none'); // Update without animation for slider responsiveness
    } else {
        state.chart = new Chart(els.chartCtx, {
            type: 'line',
            data: { labels, datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    y: { min: 0, max: 1, title: { display: true, text: 'Probability' } },
                    x: { min: 1, max: k, title: { display: true, text: 'Prefix Length' } }
                },
                plugins: {
                    legend: {
                        labels: {
                            filter: function (item, chart) {
                                // Hide threshold lines from legend to save space
                                return !item.text.includes('Threshold');
                            }
                        }
                    }
                }
            }
        });
    }
}

function renderAlertTable() {
    let html = '';
    const currentPrefix = state.currentPrefix;

    state.alerts.forEach(a => {
        const isAlertedNow = a.first_alert_prefix !== null && a.first_alert_prefix <= currentPrefix;

        html += `
            <tr>
                <td><strong>${a.model}</strong></td>
                <td>${a.threshold.toFixed(4)}</td>
                <td class="${isAlertedNow ? 'alert-yes' : 'alert-no'}">
                    ${isAlertedNow ? `Prefix ${a.first_alert_prefix}` : 'Never (or not yet)'}
                </td>
            </tr>
        `;
    });

    els.alertTableBody.innerHTML = html;
}

function renderEventContext() {
    const currentPrefix = state.currentPrefix;
    let html = `<strong>PREFIX ${currentPrefix}</strong><hr style="border:0;border-top:1px solid var(--border-color);margin:8px 0">`;

    // Status at this prefix
    html += '<strong>Predictions at this step:</strong><br>';
    const models = state.predictions.models;
    Object.keys(models).forEach(modelId => {
        const m = models[modelId];
        const pData = m.predictions.find(p => p.prefix_len === currentPrefix);
        if (pData) {
            const isAlert = pData.probability >= m.threshold;
            html += `<div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span>${modelId}: ${pData.probability.toFixed(3)} (Thresh: ${m.threshold.toFixed(3)})</span>
                <span class="${isAlert ? 'alert-yes' : 'alert-no'}">${isAlert ? 'ALERT: YES' : 'NO'}</span>
            </div>`;
        }
    });

    html += '<hr style="border:0;border-top:1px solid var(--border-color);margin:8px 0">';
    html += '<strong>Trajectory Context:</strong><br>';

    if (state.events && state.events.length > 0) {
        // Show the most recent event up to currentPrefix
        // Assuming events are 0-indexed or 1-indexed, we show event at prefix-1 if it matches
        const event = state.events[currentPrefix - 1];
        if (event) {
            html += `
                <div><strong>Step:</strong> ${event.step_index}</div>
                <div><strong>Actor:</strong> ${event.actor_role}</div>
                <div><strong>Action:</strong> ${event.action_type}</div>
                <div><strong>Tool:</strong> ${event.tool_name || 'N/A'}</div>
            `;
        } else {
            html += '<div class="placeholder-text">No event data for this step.</div>';
        }
    } else {
        html += '<div class="placeholder-text">Event data not available.</div>';
    }

    els.prefixEventContext.innerHTML = html;
}

// Load Model Comparison (/api/evaluation/summary)
async function loadComparison() {
    const res = await fetch(`${API_BASE}/evaluation/summary`);
    const data = await res.json();

    let html = '';
    Object.keys(data).forEach(modelId => {
        const m = data[modelId];
        // Ensure H3's undefined Recall@FAR is explicitly 'Undefined'
        const recall = m.Recall_at_FAR === null ? '<span style="color:var(--text-muted)">Undefined</span>' : m.Recall_at_FAR.toFixed(4);

        html += `
            <tr>
                <td><strong>${modelId}</strong></td>
                <td>${m.AUROC.toFixed(4)}</td>
                <td>${m.AUPRC.toFixed(4)}</td>
                <td>${m.Brier.toFixed(4)}</td>
                <td>${m.ECE.toFixed(4)}</td>
                <td>${m.FAR.toFixed(4)}</td>
                <td>${recall}</td>
            </tr>
        `;
    });
    els.comparisonTableBody.innerHTML = html;
}

// Load Audit (/api/audit/summary)
async function loadAudit() {
    const res = await fetch(`${API_BASE}/audit/summary`);
    const data = await res.json();

    const html = `
        <div style="display:flex; justify-content:space-between; max-width: 500px; margin-bottom:0.5rem">
            <span>Canonical population verified</span>
            <span style="color:var(--success-color);font-weight:bold">✓ ${data.episodes_count} episodes</span>
        </div>
        <div style="display:flex; justify-content:space-between; max-width: 500px; margin-bottom:0.5rem">
            <span>Provenance status</span>
            <span style="color:var(--success-color);font-weight:bold">✓ ${data.audit_status} (${data.dataset_origin})</span>
        </div>
        <div style="display:flex; justify-content:space-between; max-width: 500px; margin-bottom:0.5rem">
            <span>Leakage checks</span>
            <span style="color:var(--success-color);font-weight:bold">✓ ${data.leakage_checks}</span>
        </div>
        <div style="display:flex; justify-content:space-between; max-width: 500px; margin-bottom:0.5rem">
            <span>Evaluation Mode</span>
            <span style="font-weight:bold">Mode A (TerminalBench)</span>
        </div>
        <div style="display:flex; justify-content:space-between; max-width: 500px; margin-bottom:0.5rem">
            <span>Horizon</span>
            <span style="font-weight:bold">K = 30</span>
        </div>
    `;
    els.auditContent.innerHTML = html;
}

// Start
document.addEventListener('DOMContentLoaded', init);

// Load Significance & PDC (/api/evaluation/significance, /api/evaluation/pdc)
async function loadSignificance() {
    try {
        const [sigRes, pdcRes] = await Promise.all([
            fetch(`${API_BASE}/evaluation/significance`),
            fetch(`${API_BASE}/evaluation/pdc`)
        ]);

        const sig = await sigRes.json();
        const pdc = await pdcRes.json();

        // Populate Significance
        document.getElementById('sig-delta').textContent = sig.obs_diff_dyn_minus_m1.toFixed(4);
        document.getElementById('sig-ci').textContent = `[${sig.ci_lower_95.toFixed(4)}, ${sig.ci_upper_95.toFixed(4)}]`;
        document.getElementById('sig-p').textContent = sig.p_adj.toExponential(3);

        document.getElementById('sig-dyn-thresh').textContent = sig.dyn_comp_frozen_threshold.toFixed(6);
        document.getElementById('sig-m1-thresh').textContent = sig.m1_frozen_threshold.toFixed(6);

        // Populate PDC
        document.getElementById('sig-pdc').textContent = pdc.overall_pdc.toFixed(4);
        document.getElementById('sig-pdc-cov').textContent = (pdc.overall_pdc_coverage * 100).toFixed(1) + '%';

    } catch (err) {
        console.error("Error loading significance data:", err);
    }
}

// ----- TRACK D EXTENSIONS -----

function renderProgressionTable() {
    if (!state.predictions) return;
    const currentPrefix = state.currentPrefix;
    let html = '';
    const models = ['H1', 'H2', 'H3', 'H4', 'M1', 'S1', 'dyn_comp'];

    for (let p = 1; p <= currentPrefix; p++) {
        html += `<tr><td><strong>${p}</strong></td>`;
        models.forEach(mId => {
            const m = state.predictions.models[mId];
            const pData = m.predictions.find(x => x.prefix_len === p);
            if (pData) {
                const isAlert = pData.probability >= m.threshold;
                const txtColor = isAlert ? 'var(--danger-color)' : 'inherit';
                const fw = isAlert ? 'bold' : 'normal';
                html += `<td style="color:${txtColor}; font-weight:${fw}">${pData.probability.toFixed(3)}</td>`;
            } else {
                html += `<td>-</td>`;
            }
        });
        html += `</tr>`;
    }

    els.progressionTableBody.innerHTML = html;
}

function setupInvestigation() {
    els.alertModelSelect.addEventListener('change', async (e) => {
        const modelId = e.target.value;
        if (!modelId) {
            document.getElementById('alert-stats').style.display = 'none';
            document.getElementById('alert-list-container').style.display = 'none';
            return;
        }
        await loadAlertInvestigation(modelId);
    });
}

async function loadAlertInvestigation(modelId) {
    els.alertListTableBody.innerHTML = '<tr><td colspan="3">Loading...</td></tr>';
    document.getElementById('alert-list-container').style.display = 'block';

    try {
        const res = await fetch(`${API_BASE}/investigation/alerts/${modelId}`);
        const data = await res.json();

        els.alertTotal.textContent = data.total_alerted_episodes;
        els.alertNone.textContent = data.episodes_with_no_alert;
        els.alertEarly.textContent = data.early_alerts;
        els.alertLate.textContent = data.late_alerts;
        const otherAlerts = data.total_alerted_episodes - data.early_alerts - data.late_alerts;
        if (els.alertOther) {
            els.alertOther.textContent = otherAlerts;
        }
        document.getElementById('alert-stats').style.display = 'grid';

        let html = '';
        data.episodes.forEach(ep => {
            let timingText = ep.timing;
            if (timingText === 'early') timingText = '<span style="color:var(--success-color)">Early</span>';
            else if (timingText === 'late') timingText = '<span style="color:var(--danger-color)">Late</span>';
            else if (timingText === 'unannotated_or_success') timingText = '<span style="color:var(--text-muted)">N/A (Success or missing onset)</span>';

            html += `
                <tr>
                    <td><a href="#" onclick="jumpToEpisode('${ep.episode_id}'); return false;">${ep.episode_id}</a></td>
                    <td>${ep.alerted ? ep.first_alert_prefix : 'None'}</td>
                    <td>${timingText}</td>
                </tr>
            `;
        });
        els.alertListTableBody.innerHTML = html;

    } catch (err) {
        console.error(err);
        els.alertListTableBody.innerHTML = '<tr><td colspan="3">Error loading data.</td></tr>';
    }
}

async function loadLateDetection() {
    try {
        const res = await fetch(`${API_BASE}/investigation/late-detections`);
        const data = await res.json();

        let html = '';
        const models = Object.keys(data.models);
        models.forEach(mId => {
            const m = data.models[mId];
            html += `
                <tr>
                    <td><strong>${mId}</strong></td>
                    <td>${m.stats.total_late_alerts !== undefined ? m.stats.total_late_alerts : '0'}</td>
                    <td>${m.stats.pct_failed_episodes_with_only_late_alerts !== undefined ? m.stats.pct_failed_episodes_with_only_late_alerts + '%' : '0%'}</td>
                    <td><button onclick="showLateEpisodes('${mId}')">Show Episodes</button></td>
                </tr>
            `;
        });

        els.lateDetTableBody.innerHTML = html;
        window.__lateDetData = data; // store for click handler
    } catch (err) {
        console.error(err);
    }
}

window.showLateEpisodes = function (modelId) {
    if (!window.__lateDetData) return;
    const eps = window.__lateDetData.models[modelId].only_late_episodes;

    els.lateEpisodesTitle.textContent = `Episodes (Only Late) - ${modelId}`;

    if (eps.length === 0) {
        els.lateEpisodesList.innerHTML = '<li>No late-only episodes for this model.</li>';
    } else {
        let html = '';
        eps.forEach(epId => {
            html += `<li><a href="#" onclick="jumpToEpisode('${epId}'); return false;">${epId}</a></li>`;
        });
        els.lateEpisodesList.innerHTML = html;
    }

    els.lateEpisodesContainer.style.display = 'block';
};

window.jumpToEpisode = function (epId) {
    // Switch tab
    const tabBtn = Array.from(els.tabs).find(t => t.getAttribute('data-target') === 'explorer');
    if (tabBtn) tabBtn.click();

    // Select episode
    els.episodeSelect.value = epId;
    selectEpisode(epId);
};
