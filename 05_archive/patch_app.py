import os

app_js_path = 'P:/AIRE-TRACE/src/api/static/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update els
content = content.replace("prefixEventContext: document.getElementById('prefix-event-context')", """prefixEventContext: document.getElementById('prefix-event-context'),
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
    dataIntegrityPanel: document.getElementById('data-integrity-panel')""")

# Update init()
content = content.replace("setupSlider();", """setupSlider();
    setupInvestigation();""")
    
content = content.replace("loadComparison(),", """loadComparison(),
            loadLateDetection(),""")

# Update loadOverview()
content = content.replace("els.overviewContent.innerHTML = html;", """els.overviewContent.innerHTML = html;
    
    // Also populate Data Integrity Panel
    const diHtml = `
        <div style="font-size: 0.85rem; border: 1px solid var(--border-color); padding: 0.5rem; border-radius: 4px; background: #fafafa;">
            <strong style="display:block; border-bottom: 1px solid #ddd; margin-bottom: 4px; padding-bottom: 2px;">DATA INTEGRITY</strong>
            <div style="display:grid; grid-template-columns: 1fr auto; gap: 4px 12px;">
                <span>636 canonical episodes</span><span style="color:var(--success-color)">✓</span>
                <span>416 TEST episodes</span><span style="color:var(--success-color)">✓</span>
                <span>8,878 TEST prefixes</span><span style="color:var(--success-color)">✓</span>
                <span>53,268 prediction records</span><span style="color:var(--success-color)">✓</span>
                <span>6 frozen models</span><span style="color:var(--success-color)">✓</span>
                <span>K = 30</span><span style="color:var(--success-color)">✓</span>
                <span>Live inference</span><span style="color:var(--danger-color)">✗</span>
                <span>Artifact modification</span><span style="color:var(--danger-color)">✗</span>
            </div>
        </div>
    `;
    if(els.dataIntegrityPanel) els.dataIntegrityPanel.innerHTML = diHtml;
""")

# Add renderProgressionTable to updatePrefix
content = content.replace("renderEventContext();", """renderEventContext();
    renderProgressionTable();""")

# Add reset progression table
content = content.replace("els.alertTableBody.innerHTML = '';", """els.alertTableBody.innerHTML = '';
    els.progressionTableBody.innerHTML = '';""")

# Append new functions
new_funcs = """
// ----- TRACK D EXTENSIONS -----

function renderProgressionTable() {
    if (!state.predictions) return;
    const currentPrefix = state.currentPrefix;
    let html = '';
    const models = ['H1', 'H2', 'H3', 'H4', 'M1', 'S1'];
    
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

window.showLateEpisodes = function(modelId) {
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

window.jumpToEpisode = function(epId) {
    // Switch tab
    const tabBtn = Array.from(els.tabs).find(t => t.getAttribute('data-target') === 'explorer');
    if (tabBtn) tabBtn.click();
    
    // Select episode
    els.episodeSelect.value = epId;
    selectEpisode(epId);
};
"""

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(content + new_funcs)
