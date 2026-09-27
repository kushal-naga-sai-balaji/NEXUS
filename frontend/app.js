/**
 * NEXUS // DEAL INTELLIGENCE AGENT - CLIENT LOGIC
 * High-performance state-driven application with interactive Hindsight memory engine
 */

class NexusApp {
  constructor() {
    this.currentDealId = 'deal-acme-titan';
    this.deals = [];
    this.activeTab = 'cockpit';
    this.memoryFilterTier = 'all';
    this.currentContrastScenario = 'cfo_pricing';
    this.guidedDemoStep = 0;
    this.memoryNodes = [];
    this.learningCurveData = [];
    this.selectedLearningStage = 1;
    this.enterpriseArtifacts = null;
    this.selectedArtifact = 'ciso_email';

    this.init();
  }

  async init() {
    this.setupEventListeners();
    await this.checkHealth();
    await this.loadDeals();
    await this.loadMemoryBank();
    await this.loadLearningCurve();
    await this.loadEnterpriseArtifacts();
    await this.loadContrastMode(this.currentContrastScenario);
  }

  // ==================== EVENT LISTENERS ====================
  setupEventListeners() {
    // Navigation Tabs
    document.querySelectorAll('.nav-tab').forEach(tabBtn => {
      tabBtn.addEventListener('click', (e) => {
        const tab = tabBtn.dataset.tab;
        this.switchTab(tab);
      });
    });

    // Guided Demo Launcher & Controls
    document.getElementById('btn-guided-demo').addEventListener('click', () => {
      this.startGuidedDemo();
    });
    document.getElementById('demo-next-btn').addEventListener('click', () => {
      this.nextGuidedStep();
    });
    document.getElementById('demo-prev-btn').addEventListener('click', () => {
      this.prevGuidedStep();
    });
    document.getElementById('demo-close-btn').addEventListener('click', () => {
      this.exitGuidedDemo();
    });

    // Tactical Briefing Generator
    document.getElementById('btn-generate-briefing').addEventListener('click', () => {
      this.generateBriefing();
    });

    // Objection Coach
    document.getElementById('btn-submit-objection').addEventListener('click', () => {
      this.coachObjection();
    });
    document.querySelectorAll('.preset-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        document.getElementById('objection-input-text').value = chip.dataset.objection;
        this.coachObjection();
      });
    });

    // Memory Bank Search & Tier Filters
    document.getElementById('btn-search-memory').addEventListener('click', () => {
      this.searchMemory();
    });
    document.getElementById('memory-search-query').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.searchMemory();
    });
    document.getElementById('btn-refresh-memory').addEventListener('click', () => {
      this.loadMemoryBank();
    });
    document.querySelectorAll('.tier-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tier-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.memoryFilterTier = btn.dataset.tier;
        this.renderMemoryCards();
      });
    });

    // Contrast Mode Scenarios
    document.querySelectorAll('.scenario-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.currentContrastScenario = btn.dataset.scenario;
        this.loadContrastMode(this.currentContrastScenario);
      });
    });

    // Strategic Reflection Trigger
    document.getElementById('btn-trigger-reflect').addEventListener('click', () => {
      this.triggerStrategicReflection();
    });

    // Artifacts Sub-Tabs
    document.querySelectorAll('.artifact-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.artifact-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.selectedArtifact = btn.dataset.artifact;
        this.renderArtifact(btn.dataset.artifact);
      });
    });

    // Modals
    this.setupModals();
  }

  setupModals() {
    // Ingest Modal
    const modalIngest = document.getElementById('modal-ingest');
    document.getElementById('btn-open-ingest-modal').addEventListener('click', () => {
      modalIngest.style.display = 'flex';
    });
    document.getElementById('close-modal-ingest').addEventListener('click', () => {
      modalIngest.style.display = 'none';
    });
    document.getElementById('cancel-modal-ingest').addEventListener('click', () => {
      modalIngest.style.display = 'none';
    });
    document.getElementById('submit-modal-ingest').addEventListener('click', () => {
      this.submitIngestInteraction();
    });

    // Retain Modal
    const modalRetain = document.getElementById('modal-retain');
    document.getElementById('btn-open-retain-modal').addEventListener('click', () => {
      const activeDeal = this.getActiveDeal();
      if (activeDeal) {
        document.getElementById('modal-retain-bank').value = activeDeal.bank_id;
      }
      modalRetain.style.display = 'flex';
    });
    document.getElementById('close-modal-retain').addEventListener('click', () => {
      modalRetain.style.display = 'none';
    });
    document.getElementById('cancel-modal-retain').addEventListener('click', () => {
      modalRetain.style.display = 'none';
    });
    document.getElementById('submit-modal-retain').addEventListener('click', () => {
      this.submitRetainMemory();
    });

    // Settings Modal
    const modalSettings = document.getElementById('modal-settings');
    document.getElementById('btn-open-settings').addEventListener('click', () => {
      modalSettings.style.display = 'flex';
      this.checkHealth();
    });
    document.getElementById('close-modal-settings').addEventListener('click', () => {
      modalSettings.style.display = 'none';
    });
    document.getElementById('cancel-modal-settings').addEventListener('click', () => {
      modalSettings.style.display = 'none';
    });
    document.getElementById('save-modal-settings').addEventListener('click', () => {
      this.saveSettings();
    });
  }

  // ==================== HEALTH & API CALLS ====================
  async checkHealth() {
    try {
      const res = await fetch('/api/health');
      const data = await res.json();
      const dot = document.getElementById('connection-status-dot');
      const text = document.getElementById('connection-status-text');
      const healthBox = document.getElementById('settings-health-box');

      if (data.hindsight.is_cloud_active) {
        dot.className = 'status-indicator live';
        text.innerText = 'Hindsight Cloud Live';
        if (healthBox) healthBox.innerHTML = `🟢 <strong>Connected to Hindsight Cloud</strong><br>Base URL: ${data.hindsight.base_url}<br>LLM Model: ${data.llm.model}`;
      } else {
        dot.className = 'status-indicator live';
        text.innerText = 'Hindsight Hybrid Active';
        if (healthBox) healthBox.innerHTML = `⚡ <strong>Biomimetic Hybrid Engine Active</strong><br>${data.hindsight.connection_status}<br>LLM Model: ${data.llm.model} (Fallback & Groq ready)`;
      }
    } catch (e) {
      console.warn('Health check failed:', e);
    }
  }

  async loadDeals() {
    try {
      const res = await fetch('/api/deals');
      this.deals = await res.json();
      this.renderSidebarDeals();
      this.renderActiveDeal();
      this.updatePipelineStats();
    } catch (e) {
      console.error('Failed to load deals:', e);
    }
  }

  getActiveDeal() {
    return this.deals.find(d => d.id === this.currentDealId) || this.deals[0];
  }

  updatePipelineStats() {
    const totalArr = this.deals.reduce((acc, d) => acc + (d.arr_target || 0), 0);
    const totalMem = this.memoryNodes.length || 12;
    document.getElementById('header-total-arr').innerText = `$${(totalArr / 1000000).toFixed(2)}M`;
    document.getElementById('header-memory-count').innerText = `${totalMem} Nodes`;
  }

  // ==================== RENDERING ====================
  renderSidebarDeals() {
    const container = document.getElementById('deal-list-container');
    container.innerHTML = '';

    this.deals.forEach(deal => {
      const card = document.createElement('div');
      card.className = `deal-card ${deal.id === this.currentDealId ? 'active' : ''}`;
      card.id = `sidebar-deal-${deal.id}`;
      card.innerHTML = `
        <div class="deal-card-top">
          <span class="deal-card-name" title="${deal.name}">${deal.name}</span>
          <span class="deal-card-arr">$${(deal.arr_target / 1000).toFixed(0)}k</span>
        </div>
        <div class="deal-card-meta">
          <span>${deal.stage}</span>
          <span class="deal-health-pill ${deal.health_score > 80 ? 'high' : 'med'}">${deal.health_score}% Health</span>
        </div>
      `;
      card.addEventListener('click', () => {
        this.currentDealId = deal.id;
        document.querySelectorAll('.deal-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        this.renderActiveDeal();
        this.loadMemoryBank();
      });
      container.appendChild(card);
    });
  }

  renderActiveDeal() {
    const deal = this.getActiveDeal();
    if (!deal) return;

    // Header Banner
    const banner = document.getElementById('cockpit-deal-header');
    banner.innerHTML = `
      <div class="banner-deal-info">
        <h1>${deal.name}</h1>
        <p>${deal.company} &bull; ${deal.industry} &bull; ${deal.employees.toLocaleString()} employees</p>
      </div>
      <div class="banner-deal-metrics">
        <div class="metric-block">
          <div class="metric-title">Target ARR</div>
          <div class="metric-number">$${(deal.arr_target / 1000).toFixed(0)}k</div>
        </div>
        <div class="metric-block">
          <div class="metric-title">Deal Health</div>
          <div class="metric-number highlight-green">${deal.health_score}%</div>
        </div>
        <div class="metric-block">
          <div class="metric-title">Current Stage</div>
          <div class="metric-number" style="font-size: 1.1rem; color: #fff;">${deal.stage}</div>
        </div>
      </div>
    `;

    // Stakeholders
    const stContainer = document.getElementById('stakeholder-matrix-container');
    stContainer.innerHTML = '';
    document.getElementById('stakeholder-count-badge').innerText = `${deal.stakeholders.length} Stakeholders`;

    deal.stakeholders.forEach(st => {
      const card = document.createElement('div');
      card.className = 'stakeholder-card';
      card.innerHTML = `
        <div class="stakeholder-top">
          <div>
            <span class="stakeholder-name">${st.name}</span>
            <span class="stakeholder-role"> &bull; ${st.role}</span>
          </div>
          <span class="stakeholder-disposition">${st.disposition}</span>
        </div>
        <div class="stakeholder-focus"><strong>Focus:</strong> ${st.focus}</div>
        <div class="stakeholder-focus" style="color: var(--primary-light); font-style: italic;">"${st.notes}"</div>
      `;
      stContainer.appendChild(card);
    });

    // Populate briefing select
    const briefSelect = document.getElementById('brief-stakeholder-select');
    briefSelect.innerHTML = '';
    deal.stakeholders.forEach(st => {
      const opt = document.createElement('option');
      opt.value = st.name;
      opt.innerText = `${st.name} (${st.role})`;
      briefSelect.appendChild(opt);
    });

    // Competitors
    const compContainer = document.getElementById('competitor-radar-container');
    compContainer.innerHTML = '';
    deal.competitors_mentioned.forEach(comp => {
      const item = document.createElement('div');
      item.className = 'competitor-item';
      item.innerHTML = `
        <div class="competitor-header">
          <span class="competitor-name">${comp.name}</span>
          <span class="competitor-threat">Threat: ${comp.threat_level}</span>
        </div>
        <div class="competitor-counter">
          <strong>Winning Counter-Position:</strong> ${comp.counter_position}
        </div>
      `;
      compContainer.appendChild(item);
    });

    // Interactions Timeline
    const timelineContainer = document.getElementById('interactions-timeline-container');
    timelineContainer.innerHTML = '';
    deal.interactions.forEach(int => {
      const item = document.createElement('div');
      item.className = 'timeline-item';

      let objectionsHtml = '';
      if (int.objections && int.objections.length > 0) {
        objectionsHtml = int.objections.map(obj => `
          <div class="objection-pill-box">
            <span class="objection-label">⚠️ Raised Objection (${obj.category || 'General'}):</span>
            ${obj.text}
          </div>
          ${obj.winning_tactic ? `
            <div class="winning-tactic-box">
              <span class="winning-label">🛡️ Proven Winning Counter:</span>
              ${obj.winning_tactic}
            </div>
          ` : ''}
        `).join('');
      }

      item.innerHTML = `
        <div class="timeline-header">
          <span class="timeline-type">${int.type} &bull; ${int.stakeholder}</span>
          <span class="timeline-date">${int.date}</span>
        </div>
        <div class="timeline-summary">${int.summary}</div>
        ${objectionsHtml}
      `;
      timelineContainer.appendChild(item);
    });
  }

  switchTab(tabName) {
    this.activeTab = tabName;
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    const activeBtn = document.querySelector(`.nav-tab[data-tab="${tabName}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    const activePane = document.getElementById(`pane-${tabName}`);
    if (activePane) activePane.classList.add('active');

    if (tabName === 'memory') this.loadMemoryBank();
    if (tabName === 'reflection') this.triggerStrategicReflection(false);
    if (tabName === 'learning') this.loadLearningCurve();
    if (tabName === 'artifacts') this.loadEnterpriseArtifacts();
  }

  // ==================== TACTICAL BRIEFING ====================
  async generateBriefing() {
    const deal = this.getActiveDeal();
    const stakeholder = document.getElementById('brief-stakeholder-select').value;
    const callType = document.getElementById('brief-call-type-select').value;
    const outputContainer = document.getElementById('briefing-output-container');

    outputContainer.innerHTML = `
      <div class="empty-state">
        <div class="pulse-dot" style="margin: 0 auto 1rem auto; width: 14px; height: 14px;"></div>
        <h3>Executing Hindsight TEMPR Recall...</h3>
        <p>Scanning ${deal.bank_id} and global sales memory for stakeholder psychology and winning scripts.</p>
      </div>
    `;

    try {
      const res = await fetch(`/api/deals/${deal.id}/brief`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stakeholder_name: stakeholder, call_type: callType })
      });
      const data = await res.json();

      let markdown = data.briefing_markdown;
      // Convert markdown headers and bullet points to HTML
      let html = markdown
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
        .replace(/> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/^- (.*$)/gim, '<li>$1</li>')
        .replace(/\n\n/gim, '<br>');

      outputContainer.innerHTML = `
        <div class="briefing-content-view">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px;">
            <span class="card-badge highlight">Hindsight TEMPR Recall: ${data.memories_used_count || 6} Nodes Synthesized</span>
            <span style="font-size: 0.8rem; color: var(--text-dim); font-family: var(--font-mono);">Engine: ${data.source}</span>
          </div>
          ${html}
        </div>
      `;
    } catch (e) {
      outputContainer.innerHTML = `<p style="color: var(--rose);">Failed to generate briefing: ${e.message}</p>`;
    }
  }

  // ==================== OBJECTION COACH ====================
  async coachObjection() {
    const deal = this.getActiveDeal();
    const objectionText = document.getElementById('objection-input-text').value.trim();
    if (!objectionText) return;

    const resultContainer = document.getElementById('coaching-result-container');
    resultContainer.style.display = 'block';
    resultContainer.innerHTML = `
      <div style="text-align: center; padding: 2rem;">
        <span class="pulse-dot" style="display: inline-block; margin-bottom: 10px;"></span>
        <p>Recalling past won deals & synthesizing calibrated counter-response...</p>
      </div>
    `;

    try {
      const res = await fetch(`/api/deals/${deal.id}/coach`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ objection_text: objectionText })
      });
      const data = await res.json();

      resultContainer.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
          <span class="card-badge highlight">Calibrated Tactical Rebuttal</span>
          <span style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--emerald);">Confidence: ${(data.confidence_score * 100).toFixed(0)}%</span>
        </div>

        <div class="coach-box">
          <div class="coach-box-title reframe">1. Psychological Reframe Strategy</div>
          <p style="color: #e2e8f0; font-size: 0.92rem;">${data.reframe_strategy}</p>
        </div>

        <div class="coach-box">
          <div class="coach-box-title script">2. Battle-Tested Response (Say this to the buyer)</div>
          <div class="coach-quote-box">
            "${data.recommended_response}"
          </div>
        </div>

        <div class="coach-box">
          <div class="coach-box-title tradeoff">3. Give-Get Margin Concession Boundary</div>
          <p style="color: #fef08a; font-size: 0.9rem;">${data.give_get_tradeoff}</p>
        </div>

        <div class="coach-box">
          <div class="coach-box-title citation">4. Historical Memory Citation</div>
          <p style="color: var(--purple-light); font-size: 0.85rem; font-style: italic;">${data.past_deal_citation}</p>
        </div>
      `;
    } catch (e) {
      resultContainer.innerHTML = `<p style="color: var(--rose);">Error during coaching synthesis: ${e.message}</p>`;
    }
  }

  // ==================== MEMORY BANK VISUALIZER ====================
  async loadMemoryBank() {
    const deal = this.getActiveDeal();
    try {
      const res = await fetch(`/api/hindsight/graph?bank_id=${deal ? deal.bank_id : ''}`);
      const data = await res.json();
      this.memoryNodes = data.nodes || [];

      // Update counts
      const stats = data.stats || {};
      document.getElementById('count-all-tiers').innerText = this.memoryNodes.length;
      document.getElementById('count-world-tier').innerText = stats.world_facts || 0;
      document.getElementById('count-exp-tier').innerText = stats.experiences || 0;
      document.getElementById('count-obs-tier').innerText = stats.observations || 0;
      document.getElementById('count-op-tier').innerText = stats.opinions || 0;

      document.getElementById('meter-world-count').innerText = stats.world_facts || 0;
      document.getElementById('meter-exp-count').innerText = stats.experiences || 0;
      document.getElementById('meter-obs-count').innerText = stats.observations || 0;
      document.getElementById('meter-op-count').innerText = stats.opinions || 0;

      this.updatePipelineStats();
      this.renderMemoryCards();
    } catch (e) {
      console.error('Failed to load memory graph:', e);
    }
  }

  renderMemoryCards() {
    const container = document.getElementById('memory-cards-container');
    container.innerHTML = '';

    const filtered = this.memoryNodes.filter(n => {
      if (this.memoryFilterTier === 'all') return true;
      return n.tier.toLowerCase() === this.memoryFilterTier.toLowerCase();
    });

    if (filtered.length === 0) {
      container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-dim); padding: 2rem;">No memories in this tier yet.</div>';
      return;
    }

    filtered.forEach(node => {
      const card = document.createElement('div');
      card.className = `memory-node-card tier-${node.tier}`;
      card.innerHTML = `
        <div class="memory-node-top">
          <span class="memory-tier-badge">${node.tier} Tier</span>
          <span style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-dim);">${node.id}</span>
        </div>
        <div class="memory-node-text">${node.full_text || node.label}</div>
        <div class="memory-tag-list">
          ${(node.tags || []).map(t => `<span class="memory-tag">#${t}</span>`).join('')}
        </div>
      `;
      container.appendChild(card);
    });
  }

  async searchMemory() {
    const query = document.getElementById('memory-search-query').value.trim();
    if (!query) {
      this.loadMemoryBank();
      return;
    }

    const deal = this.getActiveDeal();
    const container = document.getElementById('memory-cards-container');
    container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--primary-light); padding: 2rem;">Running Hindsight TEMPR Multi-Strategy Search...</div>';

    try {
      const res = await fetch('/api/hindsight/recall', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bank_id: deal.bank_id, query: query, max_results: 8 })
      });
      const results = await res.json();

      container.innerHTML = '';
      if (!results || results.length === 0) {
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-dim); padding: 2rem;">No matching memories found for query.</div>';
        return;
      }

      results.forEach(node => {
        const card = document.createElement('div');
        card.className = `memory-node-card tier-${node.tier || 'Experience'}`;
        card.innerHTML = `
          <div class="memory-node-top">
            <span class="memory-tier-badge">${node.tier || 'Recalled'} Tier</span>
            <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--emerald);">Match Score: ${node.score || 0.85}</span>
          </div>
          <div class="memory-node-text">${node.text}</div>
          <div class="memory-tag-list">
            ${(node.tags || []).map(t => `<span class="memory-tag">#${t}</span>`).join('')}
          </div>
        `;
        container.appendChild(card);
      });
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">TEMPR search error: ${e.message}</div>`;
    }
  }

  // ==================== MEMORY CONTRAST MODE ====================
  async loadContrastMode(scenarioType) {
    const container = document.getElementById('contrast-grid-container');
    try {
      const res = await fetch(`/api/contrast/${scenarioType}?deal_id=${this.currentDealId}`);
      const data = await res.json();

      container.innerHTML = `
        <!-- Left Side: Standard LLM / No Memory -->
        <div class="contrast-side-card amnesia">
          <div class="side-header">
            <span class="side-badge amnesia-badge">${data.standard_agent.badge}</span>
            <span style="font-size: 0.75rem; color: var(--rose);">Amnesiac Session</span>
          </div>
          <h3 style="color: #fff; font-size: 1.15rem; margin-bottom: 8px;">${data.standard_agent.behavior}</h3>
          <div class="side-dialogue">
            ${data.standard_agent.dialogue}
          </div>
          <ul class="side-points-list">
            ${data.standard_agent.flaws.map(f => `<li><span>❌</span> ${f}</li>`).join('')}
          </ul>
          <div class="side-outcome-box">
            <strong>Outcome:</strong> ${data.standard_agent.outcome}
          </div>
        </div>

        <!-- Right Side: Nexus with Hindsight Memory -->
        <div class="contrast-side-card hindsight">
          <div class="side-header">
            <span class="side-badge hindsight-badge">${data.hindsight_agent.badge}</span>
            <span style="font-size: 0.75rem; color: var(--emerald);">Persistent Cognitive Memory</span>
          </div>
          <h3 style="color: #fff; font-size: 1.15rem; margin-bottom: 8px;">${data.hindsight_agent.behavior}</h3>
          <div class="side-dialogue">
            ${data.hindsight_agent.dialogue}
          </div>
          <ul class="side-points-list">
            ${data.hindsight_agent.hindsight_superpowers.map(s => `<li><span>⚡</span> ${s}</li>`).join('')}
          </ul>
          <div class="side-outcome-box">
            <strong>Outcome:</strong> ${data.hindsight_agent.outcome}
          </div>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<p style="color: var(--rose);">Error loading contrast data: ${e.message}</p>`;
    }
  }

  // ==================== STRATEGIC REFLECTION ====================
  async triggerStrategicReflection(scroll = true) {
    const deal = this.getActiveDeal();
    const container = document.getElementById('reflection-output-container');
    container.innerHTML = `
      <div style="text-align: center; padding: 3rem;">
        <span class="pulse-dot" style="display: inline-block; width: 14px; height: 14px; margin-bottom: 12px;"></span>
        <h3>Running Hindsight Reflect Across Memory Banks...</h3>
        <p>Synthesizing emerging competitor counter-playbooks and buyer psychology models.</p>
      </div>
    `;

    try {
      const res = await fetch(`/api/deals/${deal.id}/reflect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bank_id: deal.bank_id,
          query: "Synthesize enterprise win-loss patterns, competitor counter-playbooks, and pricing concession elasticity."
        })
      });
      const data = await res.json();

      container.innerHTML = `
        <div class="reflection-card">
          <h4>🧠 Synthesized Market Mental Models</h4>
          <ul class="conclusions-list">
            ${(data.key_conclusions || []).map(c => `<li class="conclusion-item">${c}</li>`).join('')}
          </ul>

          <h4 style="margin-top: 1.75rem;">⚔️ Living Competitive Playbooks</h4>
          <div class="playbooks-grid">
            ${(data.recommended_playbooks || []).map(p => `
              <div class="playbook-card">
                <div class="playbook-title">${p.title}</div>
                <div class="playbook-trigger"><strong>Trigger:</strong> ${p.trigger}</div>
                <div class="playbook-tactic"><strong>Winning Action:</strong> ${p.tactic}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;

      // Refresh memory cards because reflect creates a new Opinion node!
      this.loadMemoryBank();
    } catch (e) {
      container.innerHTML = `<p style="color: var(--rose);">Reflection error: ${e.message}</p>`;
    }
  }

  // ==================== GUIDED DEMO FLOW ====================
  startGuidedDemo() {
    this.guidedDemoStep = 1;
    document.getElementById('guided-demo-banner').style.display = 'flex';
    this.renderGuidedStep(1);
  }

  exitGuidedDemo() {
    this.guidedDemoStep = 0;
    document.getElementById('guided-demo-banner').style.display = 'none';
  }

  async nextGuidedStep() {
    if (this.guidedDemoStep < 4) {
      this.guidedDemoStep++;
      await this.renderGuidedStep(this.guidedDemoStep);
    }
  }

  async prevGuidedStep() {
    if (this.guidedDemoStep > 1) {
      this.guidedDemoStep--;
      await this.renderGuidedStep(this.guidedDemoStep);
    }
  }

  async renderGuidedStep(stepNum) {
    document.getElementById('demo-step-badge').innerText = `STEP ${stepNum} OF 4`;
    document.getElementById('demo-prev-btn').disabled = (stepNum === 1);
    document.getElementById('demo-next-btn').disabled = (stepNum === 4);

    if (stepNum === 1) {
      document.getElementById('demo-step-title').innerText = "Day 1: Cold Discovery & Grounding";
      document.getElementById('demo-step-desc').innerText = "Marcus Vance (CTO) reveals custom RAG failure. Retaining architecture facts into Hindsight's World & Experience tiers.";
      this.switchTab('cockpit');
      await this.loadDeals();
    } else if (stepNum === 2) {
      document.getElementById('demo-step-title').innerText = "Day 30: Security Interrogation & Instant Memory Recall";
      document.getElementById('demo-step-desc').innerText = "CISO Elena Rostova challenges multi-tenant memory leakage. Nexus recalls cryptographic namespace isolation.";
      this.switchTab('coaching');
      document.getElementById('objection-input-text').value = "How can you guarantee our customer data in your memory banks won't leak into other clients' agent sessions or be used to train models?";
      await this.coachObjection();
    } else if (stepNum === 3) {
      document.getElementById('demo-step-title').innerText = "Day 60: CFO Price War & Competitor Trap";
      document.getElementById('demo-step-desc').innerText = "CFO David Sterling demands a 32% Datadog discount match. Nexus pre-call briefing equips the rep with the $170k margin defense script.";
      this.switchTab('briefing');
      document.getElementById('brief-call-type-select').value = "Executive Pricing & Concession Showdown";
      await this.generateBriefing();
    } else if (stepNum === 4) {
      document.getElementById('demo-step-title').innerText = "Day 90: Deep Strategic Reflection & Playbook Synthesis";
      document.getElementById('demo-step-desc').innerText = "Hindsight runs 'reflect' across all deal banks, synthesizing Datadog Displacement Playbooks and updating sales mental models.";
      this.switchTab('reflection');
      await this.triggerStrategicReflection();
    }
  }

  // ==================== MODAL SUBMISSIONS ====================
  async submitIngestInteraction() {
    const deal = this.getActiveDeal();
    const intType = document.getElementById('modal-interaction-type').value;
    const stakeholder = document.getElementById('modal-stakeholder-name').value;
    const transcript = document.getElementById('modal-transcript-text').value.trim();

    if (!transcript) return alert('Please enter transcript or notes.');

    try {
      const res = await fetch(`/api/deals/${deal.id}/interact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transcript: transcript,
          interaction_type: intType,
          stakeholder_name: stakeholder || null
        })
      });
      await res.json();
      document.getElementById('modal-ingest').style.display = 'none';
      document.getElementById('modal-transcript-text').value = '';
      await this.loadDeals();
      await this.loadMemoryBank();
      alert('Interaction analyzed and committed to Hindsight Memory Bank!');
    } catch (e) {
      alert(`Ingestion error: ${e.message}`);
    }
  }

  async submitRetainMemory() {
    const bankId = document.getElementById('modal-retain-bank').value;
    const tier = document.getElementById('modal-retain-tier').value;
    const content = document.getElementById('modal-retain-content').value.trim();
    const tags = document.getElementById('modal-retain-tags').value.split(',').map(t => t.trim()).filter(Boolean);

    if (!content) return alert('Please enter memory content.');

    try {
      const res = await fetch('/api/hindsight/retain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bank_id: bankId,
          content: content,
          tier: tier,
          node_type: tier.toLowerCase(),
          tags: tags
        })
      });
      await res.json();
      document.getElementById('modal-retain').style.display = 'none';
      document.getElementById('modal-retain-content').value = '';
      await this.loadMemoryBank();
      alert('Memory successfully retained in Hindsight!');
    } catch (e) {
      alert(`Retain error: ${e.message}`);
    }
  }

  // ==================== LEARNING CURVE ====================
  async loadLearningCurve() {
    try {
      const res = await fetch('/api/learning-curve');
      this.learningCurveData = await res.json();
      this.renderLearningCurve();
      this.selectLearningStage(this.selectedLearningStage || 1);
    } catch (e) {
      console.error('Failed to load learning curve:', e);
    }
  }

  renderLearningCurve() {
    const container = document.getElementById('learning-stages-container');
    if (!container) return;
    container.innerHTML = '';

    this.learningCurveData.forEach(st => {
      const card = document.createElement('div');
      card.className = `stage-step-card badge-${st.badge_color} ${st.stage === this.selectedLearningStage ? 'active' : ''}`;
      card.innerHTML = `
        <div class="stage-card-top">
          <span class="stage-num-badge">${st.status}</span>
          <span class="stage-timeline-tag">${st.timeline}</span>
        </div>
        <div class="stage-label-text">${st.label}</div>
        <div class="competence-bar-wrapper">
          <div class="competence-fill" style="width: ${st.competence}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="stage-impact-pill">${st.memory_impact}</span>
          <span style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700;">${st.competence}%</span>
        </div>
      `;
      card.addEventListener('click', () => {
        this.selectLearningStage(st.stage);
      });
      container.appendChild(card);
    });
  }

  selectLearningStage(stageNum) {
    this.selectedLearningStage = stageNum;
    document.querySelectorAll('.stage-step-card').forEach((card, idx) => {
      card.classList.toggle('active', (idx + 1) === stageNum);
    });

    const st = this.learningCurveData.find(s => s.stage === stageNum);
    const detailContainer = document.getElementById('stage-detail-container');
    if (!st || !detailContainer) return;

    detailContainer.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-subtle); padding-bottom: 12px; margin-bottom: 1rem;">
        <div>
          <h3 style="color: #fff; font-family: var(--font-display); font-size: 1.25rem;">
            Stage ${st.stage}: ${st.label} &bull; <span style="color: var(--primary-light);">${st.status}</span>
          </h3>
          <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">${st.summary}</p>
        </div>
        <div style="text-align: right;">
          <span class="card-badge highlight" style="font-size: 0.82rem;">${st.memory_impact}</span>
          <div style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: var(--emerald); margin-top: 4px;">
            ${st.competence}% Competence
          </div>
        </div>
      </div>

      <div class="dialogue-compare-grid">
        <div class="dialogue-box before">
          <div class="dialogue-header">❌ Without Memory (Amnesiac AI / Day 1)</div>
          <div class="dialogue-quote">
            ${st.sample_dialogue_before}
          </div>
          <div style="margin-top: 10px; font-size: 0.78rem; color: #fca5a5;">
            Result: Generic marketing fluff. Forgets prior meetings. Slashes price or triggers 4-week compliance freeze.
          </div>
        </div>

        <div class="dialogue-box after">
          <div class="dialogue-header">⚡ Powered by Vectorize Hindsight (Persistent Memory)</div>
          <div class="dialogue-quote">
            ${st.sample_dialogue_after}
          </div>
          <div style="margin-top: 10px; font-size: 0.78rem; color: #6ee7b7;">
            Result: Recalls past agreements, validates CISO threat model, defends $170k in ARR margins.
          </div>
        </div>
      </div>
    `;
  }

  // ==================== ENTERPRISE ARTIFACTS ====================
  async loadEnterpriseArtifacts() {
    try {
      const res = await fetch('/api/artifacts');
      this.enterpriseArtifacts = await res.json();
      this.renderArtifact(this.selectedArtifact || 'ciso_email');
    } catch (e) {
      console.error('Failed to load enterprise artifacts:', e);
    }
  }

  renderArtifact(artifactType) {
    this.selectedArtifact = artifactType;
    const container = document.getElementById('artifact-viewer-container');
    if (!container || !this.enterpriseArtifacts) return;

    if (artifactType === 'ciso_email') {
      const email = this.enterpriseArtifacts.ciso_email_thread;
      container.innerHTML = `
        <div class="email-artifact-card">
          <table class="email-header-table">
            <tr><td class="label">From:</td><td>${email.from}</td></tr>
            <tr><td class="label">To:</td><td>${email.to}</td></tr>
            <tr><td class="label">Date:</td><td>${email.date}</td></tr>
            <tr><td class="label">Subject:</td><td style="color: #fff; font-weight: 600;">${email.subject}</td></tr>
          </table>
          <div class="email-body-text">${email.body}</div>
        </div>
      `;
    } else if (artifactType === 'quote_sheet') {
      const quote = this.enterpriseArtifacts.enterprise_quote_sheet;
      const rows = quote.items.map(it => `
        <tr>
          <td style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-dim);">${it.sku}</td>
          <td><strong>${it.desc}</strong></td>
          <td style="text-align: center;">${it.qty}</td>
          <td class="number">${it.unit}</td>
          <td class="number">${it.total}</td>
        </tr>
      `).join('');

      container.innerHTML = `
        <div class="card" style="padding: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
              <h3 style="color: #fff; font-size: 1.2rem;">${quote.title}</h3>
              <p style="color: var(--text-muted); font-size: 0.84rem;">Client: ${quote.client} &bull; Term: ${quote.term}</p>
            </div>
            <span class="card-badge highlight" style="font-size: 0.85rem;">${quote.margin_preserved}</span>
          </div>

          <table class="quote-sheet-table">
            <thead>
              <tr>
                <th>SKU</th>
                <th>Item Description</th>
                <th>Qty</th>
                <th style="text-align: right;">Unit Price</th>
                <th style="text-align: right;">Total Price</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
              <tr class="quote-summary-row">
                <td colspan="4" style="text-align: right; color: #fff;">Effective Annual Recurring Revenue (ARR):</td>
                <td class="number" style="font-size: 1.1rem; color: #10b981;">${quote.effective_arr}</td>
              </tr>
            </tbody>
          </table>
        </div>
      `;
    } else if (artifactType === 'teardown') {
      const td = this.enterpriseArtifacts.competitor_teardown;
      const rows = td.comparison.map(c => `
        <tr>
          <td style="font-weight: 600; color: #fff;">${c.metric}</td>
          <td style="color: #fca5a5; background: rgba(244,63,94,0.04);">${c.datadog}</td>
          <td style="color: #6ee7b7; background: rgba(16,185,129,0.04); font-weight: 500;">${c.nexus}</td>
        </tr>
      `).join('');

      container.innerHTML = `
        <div class="card" style="padding: 1.5rem;">
          <h3 style="color: #fff; font-size: 1.2rem; margin-bottom: 1rem;">${td.title}</h3>
          <table class="quote-sheet-table">
            <thead>
              <tr>
                <th style="width: 25%;">Evaluation Metric</th>
                <th style="width: 37.5%; color: #fca5a5;">Datadog APM & Logs</th>
                <th style="width: 37.5%; color: #6ee7b7;">Nexus + Vectorize Hindsight</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
            </tbody>
          </table>
        </div>
      `;
    }
  }

  async saveSettings() {
    const key = document.getElementById('input-hindsight-key').value.trim();
    const url = document.getElementById('input-hindsight-url').value.trim();
    const groqKey = document.getElementById('input-groq-key').value.trim();

    try {
      const res = await fetch('/api/settings/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          hindsight_api_key: key || null,
          hindsight_base_url: url || null,
          groq_api_key: groqKey || null
        })
      });
      await res.json();
      await this.checkHealth();
      document.getElementById('modal-settings').style.display = 'none';
      alert('Settings updated successfully!');
    } catch (e) {
      alert(`Settings update error: ${e.message}`);
    }
  }
}

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  window.nexus = new NexusApp();
});
