/**
 * NEXUS // DEAL INTELLIGENCE AGENT - CLIENT LOGIC
 * High-performance state-driven application with interactive Hindsight memory engine
 * Powers all 16 Core Deal Intelligence Capabilities
 */

class NexusApp {
  constructor() {
    this.currentDealId = 'deal-abc-security';
    this.deals = [];
    this.customers = [];
    this.tasks = [];
    this.activeTab = 'live-call';
    this.memoryFilterTier = 'all';
    this.guidedDemoStep = 0;
    this.memoryNodes = [];
    this.learningCurveData = [];
    this.selectedLearningStage = 1;
    this.enterpriseArtifacts = null;
    this.selectedArtifact = 'ciso_email';
    this.historicalDeals = [];
    this.liveDemoScript = [];
    this.liveDemoCurrentStep = 0;
    this.liveDemoIsStreaming = false;
    this.selectedRole = 'rep';
    this.liveSignalsCount = 0;
    this.lokiMode = 'deal';
    this.lokiHistory = [];
    this.isLokiOpen = false;
    this.isLokiExpanded = false;
    this.lokiCommands = [];

    this.init();
  }

  async init() {
    this.setupEventListeners();
    await this.checkHealth();
    await this.loadDeals();
    await this.loadCustomers();
    await this.loadTasks();
    await this.loadLiveDemoScript();
    await this.loadMemoryBank();
    await this.loadLearningCurve();
    await this.loadEnterpriseArtifacts();
    await this.loadLokiCommands();
    this.renderLiveDealMemorySidebar();
  }

  // ==================== EVENT LISTENERS ====================
  setupEventListeners() {
    // Navigation Tabs
    document.querySelectorAll('.nav-tab').forEach(tabBtn => {
      tabBtn.addEventListener('click', () => {
        const tab = tabBtn.dataset.tab;
        this.switchTab(tab);
      });
    });

    // 16 Capabilities Hub Jump-Tiles in Cockpit
    document.querySelectorAll('.cap-tile[data-jump-tab]').forEach(tile => {
      tile.addEventListener('click', () => {
        const targetTab = tile.dataset.jumpTab;
        this.switchTab(targetTab);
      });
    });

    // Header Account & Role Selectors
    const headerDealSelect = document.getElementById('header-deal-selector');
    if (headerDealSelect) {
      headerDealSelect.addEventListener('change', () => {
        this.currentDealId = headerDealSelect.value;
        this.renderSidebarDeals();
        this.renderActiveDeal();
        this.renderLiveDealMemorySidebar();
      });
    }

    const headerRoleSelect = document.getElementById('header-role-selector');
    if (headerRoleSelect) {
      headerRoleSelect.addEventListener('change', () => {
        this.selectedRole = headerRoleSelect.value;
      });
    }

    const btnStartLiveHeader = document.getElementById('btn-start-live-call-header');
    if (btnStartLiveHeader) {
      btnStartLiveHeader.addEventListener('click', () => {
        this.switchTab('live-call');
        this.startLiveDemoStream();
      });
    }

    const btnOpenBriefingModal = document.getElementById('btn-open-briefing-modal');
    if (btnOpenBriefingModal) {
      btnOpenBriefingModal.addEventListener('click', () => {
        this.openPreMeetingBriefingModal();
      });
    }

    // Live Call Cockpit Controls
    const btnRunLiveDemo = document.getElementById('btn-run-live-demo-stream');
    if (btnRunLiveDemo) {
      btnRunLiveDemo.addEventListener('click', () => this.startLiveDemoStream());
    }

    const btnAdvanceTurn = document.getElementById('btn-advance-demo-turn');
    if (btnAdvanceTurn) {
      btnAdvanceTurn.addEventListener('click', () => this.advanceLiveDemoStep());
    }

    const btnResetLiveCall = document.getElementById('btn-reset-live-call');
    if (btnResetLiveCall) {
      btnResetLiveCall.addEventListener('click', () => this.resetLiveCall());
    }

    const btnEndCallSummary = document.getElementById('btn-end-live-call-summary');
    if (btnEndCallSummary) {
      btnEndCallSummary.addEventListener('click', () => this.openPostMeetingSummaryModal());
    }

    const btnSendManualTranscript = document.getElementById('btn-send-manual-transcript');
    const manualTranscriptInput = document.getElementById('manual-transcript-input');
    if (btnSendManualTranscript && manualTranscriptInput) {
      const sendManual = () => {
        const text = manualTranscriptInput.value.trim();
        if (text) {
          this.handleManualSpeechInput(text);
          manualTranscriptInput.value = '';
        }
      };
      btnSendManualTranscript.addEventListener('click', sendManual);
      manualTranscriptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendManual();
      });
    }

    // Briefing Modal Controls
    const closeModalBriefing = document.getElementById('close-modal-briefing');
    if (closeModalBriefing) {
      closeModalBriefing.addEventListener('click', () => {
        document.getElementById('modal-pre-meeting-briefing').style.display = 'none';
      });
    }

    const btnBriefingLaunchCall = document.getElementById('btn-briefing-launch-call');
    if (btnBriefingLaunchCall) {
      btnBriefingLaunchCall.addEventListener('click', () => {
        document.getElementById('modal-pre-meeting-briefing').style.display = 'none';
        this.switchTab('live-call');
        this.startLiveDemoStream();
      });
    }

    const btnExportBriefing = document.getElementById('btn-export-briefing');
    if (btnExportBriefing) {
      btnExportBriefing.addEventListener('click', () => this.copyBriefingToClipboard());
    }

    // Post-Meeting Summary Modal Controls
    const closeModalSummaryApproval = document.getElementById('close-modal-summary-approval');
    const btnCancelSummaryApproval = document.getElementById('btn-cancel-summary-approval');
    if (closeModalSummaryApproval) {
      closeModalSummaryApproval.addEventListener('click', () => {
        document.getElementById('modal-post-meeting-summary').style.display = 'none';
      });
    }
    if (btnCancelSummaryApproval) {
      btnCancelSummaryApproval.addEventListener('click', () => {
        document.getElementById('modal-post-meeting-summary').style.display = 'none';
      });
    }

    const btnApproveSummaryCommit = document.getElementById('btn-approve-summary-commit');
    if (btnApproveSummaryCommit) {
      btnApproveSummaryCommit.addEventListener('click', () => this.approvePostMeetingSummary());
    }

    // Task creation modal
    const btnCreateTaskModal = document.getElementById('btn-create-task-modal');
    const modalCreateTask = document.getElementById('modal-create-task');
    if (btnCreateTaskModal && modalCreateTask) {
      btnCreateTaskModal.addEventListener('click', () => {
        modalCreateTask.style.display = 'flex';
      });
      document.getElementById('close-modal-task')?.addEventListener('click', () => {
        modalCreateTask.style.display = 'none';
      });
      document.getElementById('cancel-modal-task')?.addEventListener('click', () => {
        modalCreateTask.style.display = 'none';
      });
      document.getElementById('submit-modal-task')?.addEventListener('click', () => {
        this.submitCreateTask();
      });
    }

    // Deal Details Subtabs
    document.querySelectorAll('.details-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.details-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.renderDealDetails(btn.dataset.subtab);
      });
    });

    // Task Filter Chips
    document.querySelectorAll('.filter-chip[data-task-filter]').forEach(chip => {
      chip.addEventListener('click', () => {
        document.querySelectorAll('.filter-chip[data-task-filter]').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        this.loadTasks(chip.dataset.taskFilter);
      });
    });

    const btnJumpLiveFromInt = document.getElementById('btn-jump-live-call-from-int');
    if (btnJumpLiveFromInt) {
      btnJumpLiveFromInt.addEventListener('click', () => {
        this.switchTab('live-call');
        this.startLiveDemoStream();
      });
    }

    // Guided Demo Launcher & Controls (safe check)
    const btnGuidedDemo = document.getElementById('btn-guided-demo');
    if (btnGuidedDemo) btnGuidedDemo.addEventListener('click', () => this.startGuidedDemo());
    const demoNextBtn = document.getElementById('demo-next-btn');
    if (demoNextBtn) demoNextBtn.addEventListener('click', () => this.nextGuidedStep());
    const demoPrevBtn = document.getElementById('demo-prev-btn');
    if (demoPrevBtn) demoPrevBtn.addEventListener('click', () => this.prevGuidedStep());
    const demoCloseBtn = document.getElementById('demo-close-btn');
    if (demoCloseBtn) demoCloseBtn.addEventListener('click', () => this.exitGuidedDemo());

    // Tactical Briefing Generator
    const btnBriefing = document.getElementById('btn-generate-briefing');
    if (btnBriefing) {
      btnBriefing.addEventListener('click', () => this.generateBriefing());
    }

    // LOKI Header & Floating Launcher Buttons
    document.getElementById('btn-header-deal-xray')?.addEventListener('click', () => this.openDealXRay());
    document.getElementById('loki-btn-deal-xray')?.addEventListener('click', () => this.openDealXRay());
    document.getElementById('btn-header-loki-connect')?.addEventListener('click', () => this.openLokiConnect());
    document.getElementById('loki-btn-loki-connect')?.addEventListener('click', () => this.openLokiConnect());
    document.getElementById('loki-btn-exec-brief')?.addEventListener('click', () => this.openLokiBrief());
    document.getElementById('btn-header-toggle-loki')?.addEventListener('click', () => this.toggleLokiWorkspace());
    document.getElementById('loki-launcher-btn')?.addEventListener('click', () => this.toggleLokiWorkspace());
    document.getElementById('loki-btn-close-panel')?.addEventListener('click', () => this.toggleLokiWorkspace(false));
    document.getElementById('loki-btn-toggle-expand')?.addEventListener('click', () => this.toggleLokiExpand());

    // LOKI Input & Send
    document.getElementById('loki-send-btn')?.addEventListener('click', () => this.sendLokiQuery());
    const lokiInput = document.getElementById('loki-user-input');
    if (lokiInput) {
      lokiInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.sendLokiQuery();
        }
      });
      lokiInput.addEventListener('input', (e) => {
        const val = e.target.value;
        const slashDropdown = document.getElementById('loki-slash-dropdown');
        if (slashDropdown) {
          if (val.startsWith('/')) {
            slashDropdown.style.display = 'block';
          } else {
            slashDropdown.style.display = 'none';
          }
        }
      });
    }

    // Slash Dropdown Items
    document.querySelectorAll('.loki-slash-item').forEach(item => {
      item.addEventListener('click', () => {
        const cmd = item.dataset.cmd;
        if (lokiInput) lokiInput.value = cmd;
        const dropdown = document.getElementById('loki-slash-dropdown');
        if (dropdown) dropdown.style.display = 'none';
        this.sendLokiQuery(cmd);
      });
    });

    // LOKI Mode Tabs
    document.querySelectorAll('.loki-mode-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        this.setLokiMode(tab.dataset.mode);
      });
    });

    // LOKI Suggestion Chips
    document.querySelectorAll('.loki-chip-btn[data-query]').forEach(chip => {
      chip.addEventListener('click', () => {
        this.sendLokiQuery(chip.dataset.query);
      });
    });

    // LOKI Modals Close Buttons
    document.getElementById('close-modal-loki-connect')?.addEventListener('click', () => {
      document.getElementById('modal-loki-connect').style.display = 'none';
    });
    document.getElementById('btn-close-loki-connect')?.addEventListener('click', () => {
      document.getElementById('modal-loki-connect').style.display = 'none';
    });
    document.getElementById('btn-loki-connect-to-xray')?.addEventListener('click', () => {
      document.getElementById('modal-loki-connect').style.display = 'none';
      this.openDealXRay();
    });

    document.getElementById('close-modal-deal-xray')?.addEventListener('click', () => {
      document.getElementById('modal-deal-xray').style.display = 'none';
    });
    document.getElementById('btn-close-deal-xray')?.addEventListener('click', () => {
      document.getElementById('modal-deal-xray').style.display = 'none';
    });
    document.getElementById('btn-xray-ask-loki')?.addEventListener('click', () => {
      document.getElementById('modal-deal-xray').style.display = 'none';
      this.toggleLokiWorkspace(true);
      this.sendLokiQuery('Analyze all open deal risks and recommend our negotiation counter-strategy.');
    });

    document.getElementById('close-modal-loki-brief')?.addEventListener('click', () => {
      document.getElementById('modal-loki-brief').style.display = 'none';
    });
    document.getElementById('btn-close-loki-brief')?.addEventListener('click', () => {
      document.getElementById('modal-loki-brief').style.display = 'none';
    });
    document.getElementById('btn-copy-loki-brief')?.addEventListener('click', () => {
      const text = document.getElementById('loki-brief-content')?.innerText || '';
      navigator.clipboard.writeText(text);
      this.showToast('Executive brief copied to clipboard!');
    });

    // Objection Coach & Presets
    const btnSubmitObj = document.getElementById('btn-submit-objection');
    if (btnSubmitObj) {
      btnSubmitObj.addEventListener('click', () => this.coachObjection());
    }
    document.querySelectorAll('.preset-chip[data-objection]').forEach(chip => {
      chip.addEventListener('click', () => {
        const input = document.getElementById('objection-input-text');
        if (input) input.value = chip.dataset.objection;
        this.coachObjection();
      });
    });

    // Instant Deal Summary Actions
    const btnCopySummary = document.getElementById('btn-copy-summary');
    if (btnCopySummary) {
      btnCopySummary.addEventListener('click', () => this.copySummaryToClipboard());
    }
    const btnRefreshSummary = document.getElementById('btn-refresh-summary');
    if (btnRefreshSummary) {
      btnRefreshSummary.addEventListener('click', () => this.loadInstantSummary());
    }

    // Meeting Intelligence Controls
    const btnAnalyzeMeeting = document.getElementById('btn-analyze-meeting');
    if (btnAnalyzeMeeting) {
      btnAnalyzeMeeting.addEventListener('click', () => this.analyzeMeetingTranscript());
    }
    const presetCto = document.getElementById('preset-meeting-cto');
    if (presetCto) {
      presetCto.addEventListener('click', () => {
        document.getElementById('meeting-raw-transcript').value = "Marcus Vance (CTO): Our custom LangChain vector RAG on Postgres completely loses context across sessions. It hallucinated past SLA agreements and has zero temporal awareness. We need agents that retain cross-session memory without token explosion.";
        document.getElementById('meeting-stakeholder-input').value = "Marcus Vance (CTO)";
        this.analyzeMeetingTranscript();
      });
    }
    const presetCiso = document.getElementById('preset-meeting-ciso');
    if (presetCiso) {
      presetCiso.addEventListener('click', () => {
        document.getElementById('meeting-raw-transcript').value = "Elena Rostova (CISO): Before I sign off on technical clearance for Project Titan, I need mathematical proof that our customer vector memory is cryptographically partitioned and will never be piped to train upstream foundational LLMs.";
        document.getElementById('meeting-stakeholder-input').value = "Elena Rostova (CISO)";
        this.analyzeMeetingTranscript();
      });
    }
    const presetCfo = document.getElementById('preset-meeting-cfo');
    if (presetCfo) {
      presetCfo.addEventListener('click', () => {
        document.getElementById('meeting-raw-transcript').value = "David Sterling (CFO): Datadog came back with an aggressive 32% discount to renew our telemetry contract at $450,000 ARR. Unless you match their $450k price, we cannot justify switching to your platform.";
        document.getElementById('meeting-stakeholder-input').value = "David Sterling (CFO)";
        this.analyzeMeetingTranscript();
      });
    }

    // CRM Knowledge Search
    const btnCrmSearch = document.getElementById('btn-crm-search-submit');
    if (btnCrmSearch) {
      btnCrmSearch.addEventListener('click', () => {
        const query = document.getElementById('crm-search-input').value.trim();
        if (query) this.executeCRMSearch(query);
      });
    }
    const crmSearchInput = document.getElementById('crm-search-input');
    if (crmSearchInput) {
      crmSearchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const query = crmSearchInput.value.trim();
          if (query) this.executeCRMSearch(query);
        }
      });
    }
    document.querySelectorAll('.preset-chip[data-crm-q]').forEach(chip => {
      chip.addEventListener('click', () => {
        const q = chip.dataset.crmQ;
        if (crmSearchInput) crmSearchInput.value = q;
        this.executeCRMSearch(q);
      });
    });

    // Deal Comparison Benchmark Selector
    const benchSelect = document.getElementById('benchmark-deal-select');
    if (benchSelect) {
      benchSelect.addEventListener('change', () => {
        this.loadDealComparison(benchSelect.value);
      });
    }

    // Persistent Learning Feedback Modal
    const btnOpenFeedback = document.getElementById('btn-open-feedback-modal');
    const modalFeedback = document.getElementById('modal-feedback');
    if (btnOpenFeedback && modalFeedback) {
      btnOpenFeedback.addEventListener('click', () => modalFeedback.style.display = 'flex');
      document.getElementById('close-modal-feedback').addEventListener('click', () => modalFeedback.style.display = 'none');
      document.getElementById('cancel-modal-feedback').addEventListener('click', () => modalFeedback.style.display = 'none');
      document.getElementById('submit-modal-feedback').addEventListener('click', () => this.submitLearningFeedback());
    }

    // Memory Bank Search & Tier Filters
    const btnSearchMem = document.getElementById('btn-search-memory');
    if (btnSearchMem) {
      btnSearchMem.addEventListener('click', () => this.searchMemory());
    }
    const memQueryInput = document.getElementById('memory-search-query');
    if (memQueryInput) {
      memQueryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.searchMemory();
      });
    }
    const btnRefreshMem = document.getElementById('btn-refresh-memory');
    if (btnRefreshMem) {
      btnRefreshMem.addEventListener('click', () => this.loadMemoryBank());
    }
    document.querySelectorAll('.tier-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tier-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.memoryFilterTier = btn.dataset.tier;
        this.renderMemoryCards();
      });
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
    const btnOpenIngest = document.getElementById('btn-open-ingest-modal');
    if (btnOpenIngest && modalIngest) {
      btnOpenIngest.addEventListener('click', () => modalIngest.style.display = 'flex');
      document.getElementById('close-modal-ingest').addEventListener('click', () => modalIngest.style.display = 'none');
      document.getElementById('cancel-modal-ingest').addEventListener('click', () => modalIngest.style.display = 'none');
      document.getElementById('submit-modal-ingest').addEventListener('click', () => this.submitIngestInteraction());
    }

    // Retain Modal
    const modalRetain = document.getElementById('modal-retain');
    const btnOpenRetain = document.getElementById('btn-open-retain-modal');
    if (btnOpenRetain && modalRetain) {
      btnOpenRetain.addEventListener('click', () => {
        const activeDeal = this.getActiveDeal();
        if (activeDeal) document.getElementById('modal-retain-bank').value = activeDeal.bank_id;
        modalRetain.style.display = 'flex';
      });
      document.getElementById('close-modal-retain').addEventListener('click', () => modalRetain.style.display = 'none');
      document.getElementById('cancel-modal-retain').addEventListener('click', () => modalRetain.style.display = 'none');
      document.getElementById('submit-modal-retain').addEventListener('click', () => this.submitRetainMemory());
    }

    // Settings Modal
    const modalSettings = document.getElementById('modal-settings');
    const btnOpenSettings = document.getElementById('btn-open-settings');
    if (btnOpenSettings && modalSettings) {
      btnOpenSettings.addEventListener('click', () => {
        modalSettings.style.display = 'flex';
        this.checkHealth();
      });
      document.getElementById('close-modal-settings').addEventListener('click', () => modalSettings.style.display = 'none');
      document.getElementById('cancel-modal-settings').addEventListener('click', () => modalSettings.style.display = 'none');
      document.getElementById('save-modal-settings').addEventListener('click', () => this.saveSettings());
    }
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
    const totalMarginSaved = this.deals.reduce((acc, d) => {
      const saved = d.pricing_details ? (d.pricing_details.margin_saved || 0) : 0;
      return acc + saved;
    }, 0);
    const totalMem = this.memoryNodes.length || 12;

    document.getElementById('header-total-arr').innerText = `$${(totalArr / 1000000).toFixed(2)}M`;
    const savedElem = document.getElementById('header-margin-saved');
    if (savedElem) savedElem.innerText = `$${(totalMarginSaved / 1000).toFixed(0)}k`;
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
        this.loadTabContent(this.activeTab);
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
          <div class="metric-title">Margin Preserved</div>
          <div class="metric-number highlight-green">$${((deal.pricing_details ? deal.pricing_details.margin_saved : 170000) / 1000).toFixed(0)}k</div>
        </div>
        <div class="metric-block">
          <div class="metric-title">Deal Health</div>
          <div class="metric-number highlight-cyan">${deal.health_score}%</div>
        </div>
        <div class="metric-block">
          <div class="metric-title">Current Stage</div>
          <div class="metric-number" style="font-size: 1.05rem; color: #fff;">${deal.stage}</div>
        </div>
      </div>
    `;

    // Stakeholders in Cockpit
    const stContainer = document.getElementById('stakeholder-matrix-container');
    if (stContainer) {
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
            <span class="stakeholder-disposition">${st.influence || st.disposition}</span>
          </div>
          <div class="stakeholder-focus"><strong>Focus:</strong> ${st.focus}</div>
          <div class="stakeholder-focus" style="color: var(--primary-light); font-style: italic;">"${st.notes}"</div>
        `;
        stContainer.appendChild(card);
      });
    }

    // Briefing select
    const briefSelect = document.getElementById('brief-stakeholder-select');
    if (briefSelect) {
      briefSelect.innerHTML = '';
      deal.stakeholders.forEach(st => {
        const opt = document.createElement('option');
        opt.value = st.name;
        opt.innerText = `${st.name} (${st.role})`;
        briefSelect.appendChild(opt);
      });
    }

    // Competitors in Cockpit
    const compContainer = document.getElementById('competitor-radar-container');
    if (compContainer) {
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
    }

    // Timeline in Cockpit
    const timelineContainer = document.getElementById('interactions-timeline-container');
    if (timelineContainer) {
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
  }

  // ==================== TAB SWITCHING & FEATURE LOADERS ====================
  switchTab(tabName) {
    this.activeTab = tabName;
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    const activeBtn = document.querySelector(`.nav-tab[data-tab="${tabName}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    const activePane = document.getElementById(`pane-${tabName}`);
    if (activePane) {
      activePane.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    this.loadTabContent(tabName);
  }

  loadTabContent(tabName) {
    switch (tabName) {
      case 'summary':
        this.loadInstantSummary();
        break;
      case 'next-actions':
        this.loadNextActions();
        break;
      case 'objections':
        this.loadObjectionIntelligence();
        break;
      case 'winning-patterns':
        this.loadWinningPatterns();
        break;
      case 'stakeholders':
        this.loadStakeholderIntelligence();
        break;
      case 'competitors':
        this.loadCompetitorTracking();
        break;
      case 'pricing':
        this.loadPricingIntelligence();
        break;
      case 'meetings':
        this.initMeetingIntelligenceTab();
        break;
      case 'risks':
        this.loadDealRisks();
        break;
      case 'progress':
        this.loadDealProgress();
        break;
      case 'followups':
        this.loadFollowupIntelligence();
        break;
      case 'crm-search':
        // Ready for search
        break;
      case 'strategy':
        this.loadPersonalizedStrategy();
        break;
      case 'comparison':
        this.loadDealComparison();
        break;
      case 'live-call':
        this.renderLiveDealMemorySidebar();
        break;
      case 'customers':
        this.loadCustomers();
        break;
      case 'tasks':
        this.loadTasks();
        break;
      case 'deals':
        this.renderDealsPipeline();
        break;
      case 'deal-details':
        this.renderDealDetails('overview');
        break;
      case 'analytics':
        // Telemetry ready in DOM
        break;
      case 'integrations':
        // Ready in DOM
        break;
      case 'learning-evolution':
        this.loadPersistentLearning();
        break;
      case 'memory':
        this.loadMemoryBank();
        break;
      case 'learning':
        this.loadLearningCurve();
        break;
      case 'artifacts':
        this.loadEnterpriseArtifacts();
        break;
      case 'cockpit':
        this.renderActiveDeal();
        break;
    }
  }

  // ==================== FEATURE 2: INSTANT DEAL SUMMARY ====================
  async loadInstantSummary() {
    const container = document.getElementById('summary-content-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Synthesizing instant deal summary with Hindsight memory...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/summary`);
      const data = await res.json();
      this.cachedSummaryData = data;

      const talkingPointsHtml = (data.critical_talking_points || []).map(tp => `
        <li><span style="color: var(--cyan);">&bull;</span> ${tp}</li>
      `).join('');

      const landminesHtml = (data.immediate_danger_flags || []).map(df => `
        <li><span style="color: var(--rose);">⚠️</span> ${df}</li>
      `).join('');

      container.innerHTML = `
        <div class="summary-header-row">
          <div class="readiness-score-card">
            <div class="readiness-dial">${data.call_readiness_score || 92}%</div>
            <div class="readiness-label">Call Readiness Score</div>
            <p style="font-size: 0.75rem; color: var(--text-dim); margin-top: 6px;">Based on memory grounding, CISO alignment & pricing posture</p>
          </div>
          <div class="elevator-pitch-card">
            <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-dim); text-transform: uppercase; margin-bottom: 8px;">60-Second Executive Elevator Pitch</div>
            <div class="elevator-pitch-text">${data.executive_elevator_pitch}</div>
          </div>
        </div>

        <div class="summary-details-grid">
          <div class="summary-box">
            <div class="summary-box-title cyan">👥 Key Stakeholders & Alignment</div>
            <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5;">${data.key_stakeholders_summary}</p>
          </div>
          <div class="summary-box">
            <div class="summary-box-title emerald">💰 Commercial Status & Margin Defense</div>
            <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5;">${data.commercial_status}</p>
          </div>
          <div class="summary-box">
            <div class="summary-box-title amber">🎯 Critical Talking Points (Anchor on These)</div>
            <ul class="summary-bullet-list">${talkingPointsHtml}</ul>
          </div>
          <div class="summary-box">
            <div class="summary-box-title rose">⚠️ Fatal Landmines (What NOT to Say)</div>
            <ul class="summary-bullet-list">${landminesHtml}</ul>
          </div>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load summary: ${e.message}</div>`;
    }
  }

  copySummaryToClipboard() {
    if (!this.cachedSummaryData) return;
    const text = `NEXUS INSTANT DEAL SUMMARY // ${this.cachedSummaryData.deal_id}
Elevator Pitch: ${this.cachedSummaryData.executive_elevator_pitch}
Commercial Status: ${this.cachedSummaryData.commercial_status}
Key Talking Points:
${(this.cachedSummaryData.critical_talking_points || []).map(p => '- ' + p).join('\n')}
Fatal Landmines:
${(this.cachedSummaryData.immediate_danger_flags || []).map(p => '- ' + p).join('\n')}`;

    navigator.clipboard.writeText(text);
    const btn = document.getElementById('btn-copy-summary');
    if (btn) {
      const originalText = btn.innerText;
      btn.innerText = '✅ Copied!';
      setTimeout(() => btn.innerText = originalText, 2000);
    }
  }

  // ==================== FEATURE 3: NEXT-BEST ACTION ====================
  async loadNextActions() {
    const container = document.getElementById('next-actions-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Analyzing deal stage and calculating next actions...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/next-actions`);
      const actions = await res.json();

      container.innerHTML = actions.map(act => `
        <div class="action-card">
          <div class="action-card-header">
            <span class="action-priority-badge ${act.priority ? act.priority.toLowerCase() : 'medium'}">${act.priority || 'Action'}</span>
            <span style="font-size: 0.8rem; color: var(--text-dim); font-family: var(--font-mono);">${act.timing || 'Immediate'}</span>
          </div>
          <div class="action-title">${act.action}</div>
          <div class="action-meta-row">
            <div class="action-meta-item">Target: <strong>${act.target_stakeholder}</strong></div>
            <div class="action-meta-item">Channel: <strong>${act.channel}</strong></div>
          </div>
          <div class="action-impact-callout">
            <strong>Expected Velocity Impact:</strong> ${act.expected_impact}
          </div>
          ${act.script_template ? `
            <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-dim); margin-top: 4px;">Recommended Outreach Script / Message:</div>
            <div class="action-script-preview">${act.script_template}</div>
          ` : ''}
          <div class="action-card-footer">
            <button class="action-btn secondary small" onclick="navigator.clipboard.writeText('${encodeURIComponent(act.script_template || '')}'); alert('Outreach script copied!');">Copy Script</button>
            <button class="action-btn primary small" onclick="this.innerText='✅ Executed'; this.disabled=true;">Mark as Done</button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load actions: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 4: OBJECTION INTELLIGENCE ====================
  async loadObjectionIntelligence() {
    const container = document.getElementById('deal-objections-container');
    if (!container) return;

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/objections`);
      const data = await res.json();

      container.innerHTML = data.objections.map(obj => `
        <div class="deal-obj-card">
          <div class="deal-obj-top">
            <span class="deal-obj-category">${obj.category || 'General'} &bull; ${obj.stakeholder || 'Stakeholder'}</span>
            <span class="deal-obj-status ${obj.status === 'Resolved' ? 'resolved' : 'in-progress'}">${obj.status}</span>
          </div>
          <div class="deal-obj-quote">"${obj.text}"</div>
          ${obj.winning_tactic ? `
            <div class="deal-obj-tactic">
              <strong>Proven Winning Rebuttal:</strong> ${obj.winning_tactic}
            </div>
          ` : ''}
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load objections: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 5: WINNING PATTERNS ====================
  async loadWinningPatterns() {
    const container = document.getElementById('winning-patterns-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Matching winning patterns against Hindsight global repository...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/winning-patterns`);
      const data = await res.json();

      container.innerHTML = data.patterns.map(p => `
        <div class="pattern-card">
          <div class="pattern-header">
            <div class="pattern-name">${p.name}</div>
            <span class="pattern-source-badge">${p.source_deal}</span>
          </div>
          <div class="pattern-stat">📈 Proven Success: ${p.success_rate}</div>
          <div class="pattern-playbook">${p.playbook}</div>
          <div style="font-size: 0.8rem; color: var(--cyan);">Match: ${p.applicability}</div>
          <button class="action-btn small primary" style="margin-top: auto;" onclick="alert('Applied ${p.name} to deal strategy!');">Apply Playbook to Active Deal</button>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load patterns: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 6: STAKEHOLDER INTELLIGENCE ====================
  async loadStakeholderIntelligence() {
    const container = document.getElementById('stakeholders-deep-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Loading stakeholder intelligence dossier...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/stakeholders`);
      const data = await res.json();

      container.innerHTML = data.stakeholders.map(st => {
        const concernsHtml = (st.concerns || []).map(c => `<li>&bull; ${c}</li>`).join('');
        return `
          <div class="stakeholder-deep-card">
            <div class="sh-top-row">
              <div class="sh-name-role">
                <h3>${st.name}</h3>
                <p>${st.role}</p>
              </div>
              <span class="sh-influence-pill">${st.influence || st.disposition}</span>
            </div>
            <div class="sh-interest-gauge">
              <span>Interest / Alignment:</span>
              <div class="sh-gauge-bar">
                <div class="sh-gauge-fill" style="width: ${st.interest_score || 80}%;"></div>
              </div>
              <strong>${st.interest_score || 80}%</strong>
            </div>
            <div style="font-size: 0.84rem; color: var(--text-muted);"><strong>Primary Focus:</strong> ${st.focus}</div>
            ${concernsHtml ? `
              <div class="sh-concerns-box">
                <strong style="color: var(--amber); font-size: 0.78rem; text-transform: uppercase;">Key Concerns:</strong>
                <ul style="list-style: none; margin-top: 4px; color: var(--text-muted);">${concernsHtml}</ul>
              </div>
            ` : ''}
            <div class="sh-tips-box">
              <strong>Calibrated Communication Guidance:</strong><br>
              ${st.communication_tips || st.notes}
            </div>
          </div>
        `;
      }).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load stakeholders: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 7: COMPETITOR TRACKING ====================
  async loadCompetitorTracking() {
    const container = document.getElementById('competitors-deep-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Loading competitor intelligence radar...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/competitors`);
      const data = await res.json();

      container.innerHTML = data.competitors.map(comp => {
        const killPointsHtml = (comp.kill_points || []).map(kp => `
          <li class="comp-kill-point-item">⚔️ ${kp}</li>
        `).join('');

        return `
          <div class="comp-deep-card">
            <div class="comp-top-row">
              <h3 style="color: #fff; font-size: 1.2rem;">${comp.name}</h3>
              <span class="comp-threat-badge ${comp.threat_level.toLowerCase()}">Threat: ${comp.threat_level}</span>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">
              <strong>Customer Perception:</strong> ${comp.advantages_mentioned || 'Incumbent tooling'}
            </div>
            <div style="font-size: 0.85rem; color: var(--rose);">
              <strong>Observed Weakness:</strong> ${comp.weaknesses_mentioned || 'Lacks persistent memory'}
            </div>
            <div style="background: rgba(99, 102, 241, 0.08); border-left: 3px solid var(--primary); padding: 10px 12px; border-radius: 0 6px 6px 0; font-size: 0.85rem; color: #e0e7ff;">
              <strong>Battlecard Counter-Positioning:</strong><br>${comp.counter_position}
            </div>
            ${killPointsHtml ? `
              <div style="margin-top: 4px;">
                <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-dim); text-transform: uppercase; margin-bottom: 6px;">Disqualifying Kill Points (Ask Customer):</div>
                <ul class="comp-kill-points-list">${killPointsHtml}</ul>
              </div>
            ` : ''}
          </div>
        `;
      }).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load competitors: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 8: PRICING INTELLIGENCE ====================
  async loadPricingIntelligence() {
    const container = document.getElementById('pricing-cockpit-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Loading pricing intelligence metrics...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/pricing`);
      const data = await res.json();
      const p = data.pricing;

      const concessionRows = (p.concessions_log || []).map(c => `
        <tr>
          <td><strong>${c.item}</strong></td>
          <td class="number">${c.value}</td>
          <td><span class="card-badge ${c.status === 'Granted' ? 'highlight' : (c.status === 'Firmly Rejected' ? 'threat' : '')}">${c.status}</span></td>
          <td style="color: var(--text-muted); font-size: 0.84rem;">${c.trade_received}</td>
        </tr>
      `).join('');

      container.innerHTML = `
        <div class="pricing-metrics-banner">
          <div class="pricing-stat-box">
            <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); text-transform: uppercase;">Target ARR</span>
            <div class="pricing-stat-val cyan">$${(p.arr_target / 1000).toFixed(0)}k</div>
            <span style="font-size: 0.75rem; color: var(--text-muted);">List: $${((p.list_price || 700000) / 1000).toFixed(0)}k</span>
          </div>
          <div class="pricing-stat-box">
            <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); text-transform: uppercase;">Margin Preserved</span>
            <div class="pricing-stat-val emerald">$${((p.margin_saved || 170000) / 1000).toFixed(0)}k</div>
            <span style="font-size: 0.75rem; color: var(--emerald);">100% ARR Protected</span>
          </div>
          <div class="pricing-stat-box">
            <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); text-transform: uppercase;">Competitor Renewal Offer</span>
            <div class="pricing-stat-val rose">$${((p.competitor_offer || 450000) / 1000).toFixed(0)}k</div>
            <span style="font-size: 0.75rem; color: var(--rose);">32% Desperation Discount</span>
          </div>
          <div class="pricing-stat-box">
            <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); text-transform: uppercase;">Budget & Fiscal Deadline</span>
            <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 4px;">${p.budget_cycle || 'Ends Oct 31, 2026'}</div>
            <span style="font-size: 0.75rem; color: var(--amber);">Term: ${p.billing_term || '24 Months'}</span>
          </div>
        </div>

        <div class="card" style="padding: 1.25rem; margin-top: 1rem;">
          <h4 style="color: #fff; font-size: 1rem; margin-bottom: 0.75rem;">Concession Log & Give-Get Tracker</h4>
          <table class="concession-table">
            <thead>
              <tr>
                <th>Concession Item</th>
                <th>Estimated Value</th>
                <th>Status</th>
                <th>Value Traded / Extracted</th>
              </tr>
            </thead>
            <tbody>
              ${concessionRows}
            </tbody>
          </table>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load pricing: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 9: MEETING INTELLIGENCE ====================
  initMeetingIntelligenceTab() {
    // Tab ready
  }

  async analyzeMeetingTranscript() {
    const transcript = document.getElementById('meeting-raw-transcript').value.trim();
    if (!transcript) {
      alert('Please enter or select a transcript first.');
      return;
    }
    const stakeholder = document.getElementById('meeting-stakeholder-input').value.trim();
    const type = document.getElementById('meeting-type-input').value;
    const outputContainer = document.getElementById('meeting-output-container');

    outputContainer.style.display = 'flex';
    outputContainer.innerHTML = '<div class="loading-state">Analyzing meeting conversation, decisions & commitments...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/meetings/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transcript: transcript,
          interaction_type: type,
          stakeholder_name: stakeholder || null
        })
      });
      const data = await res.json();

      const decisionsHtml = (data.decisions || []).map(d => `<li>✅ ${d}</li>`).join('');
      const custActionHtml = (data.customer_action_items || []).map(a => `
        <li style="margin-bottom: 6px;"><strong>${a.owner}:</strong> ${a.item} <span style="color: var(--amber); font-size: 0.75rem;">(${a.due})</span></li>
      `).join('');
      const repActionHtml = (data.rep_action_items || []).map(a => `
        <li style="margin-bottom: 6px;"><strong>${a.owner}:</strong> ${a.item} <span style="color: var(--cyan); font-size: 0.75rem;">(${a.due})</span></li>
      `).join('');

      outputContainer.innerHTML = `
        <div class="meeting-decisions-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <h4 style="color: #fff; font-size: 1.05rem;">Meeting Summary & Executive Decisions</h4>
            <span class="card-badge highlight">Sentiment: ${Math.round((data.sentiment_score || 0.85) * 100)}% Positive</span>
          </div>
          <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 1rem;">${data.summary}</p>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 0.88rem; color: #a7f3d0;">${decisionsHtml}</ul>
        </div>

        <div class="action-items-grid">
          <div class="card" style="padding: 1.25rem;">
            <h5 style="color: var(--amber); font-size: 0.85rem; font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 0.75rem;">Customer Action Items</h5>
            <ul style="list-style: none; font-size: 0.85rem; color: var(--text-muted);">${custActionHtml}</ul>
          </div>
          <div class="card" style="padding: 1.25rem;">
            <h5 style="color: var(--cyan); font-size: 0.85rem; font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 0.75rem;">Nexus Rep Commitments</h5>
            <ul style="list-style: none; font-size: 0.85rem; color: var(--text-muted);">${repActionHtml}</ul>
          </div>
        </div>
      `;

      // Refresh memory & timeline in background
      this.loadMemoryBank();
    } catch (e) {
      outputContainer.innerHTML = `<div style="color: var(--rose);">Failed to analyze meeting: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 10: DEAL RISKS ====================
  async loadDealRisks() {
    const container = document.getElementById('risks-cockpit-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Running deal risk heuristics and sentiment radar...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/risks`);
      const data = await res.json();

      container.innerHTML = `
        <div style="display: flex; gap: 1rem; align-items: center; background: var(--bg-surface-elevated); padding: 1.25rem; border-radius: 10px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 2.2rem; font-weight: 800; font-family: var(--font-display); color: var(--emerald);">${data.health_score}%</div>
          <div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #fff;">Overall Risk Status: <span style="color: var(--emerald);">${data.overall_risk_level} Risk</span></div>
            <p style="font-size: 0.82rem; color: var(--text-muted);">${data.summary}</p>
          </div>
        </div>

        <div style="margin-top: 1rem;">
          <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 0.75rem;">Active Risk Flags & Recommended Mitigations:</h4>
          ${data.risk_factors.map(rf => `
            <div class="risk-factor-card ${rf.severity ? rf.severity.toLowerCase() : 'medium'}">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #fff; font-size: 0.95rem;">${rf.category}</strong>
                <span class="action-priority-badge ${rf.severity ? rf.severity.toLowerCase() : 'medium'}">${rf.severity} Severity</span>
              </div>
              <p style="font-size: 0.86rem; color: #fecdd3;">⚠️ ${rf.warning}</p>
              <div style="font-size: 0.84rem; color: #a7f3d0; background: rgba(16, 185, 129, 0.08); padding: 6px 10px; border-radius: 4px; margin-top: 4px;">
                <strong>Recommended Mitigation:</strong> ${rf.mitigation}
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load risks: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 11: DEAL PROGRESS ====================
  async loadDealProgress() {
    const container = document.getElementById('progress-cockpit-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Calculating stage gate completion and cycle days...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/progress`);
      const data = await res.json();

      const gatesHtml = (data.milestones || []).map((m, idx) => `
        <div class="gate-step ${m.status === 'Completed' ? 'completed' : (m.status === 'In Progress' ? 'in-progress' : '')}">
          <div style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-dim);">GATE ${idx + 1}</div>
          <strong style="color: #fff; font-size: 0.9rem;">${m.name}</strong>
          <span class="gate-status-pill" style="color: ${m.status === 'Completed' ? 'var(--emerald)' : (m.status === 'In Progress' ? 'var(--cyan)' : 'var(--text-dim)')};">${m.status}</span>
          <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">${m.summary}</p>
          <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: auto;">Owner: ${m.owner}</div>
        </div>
      `).join('');

      container.innerHTML = `
        <div style="display: flex; gap: 1.5rem; background: var(--bg-surface-elevated); padding: 1.25rem; border-radius: 10px; border: 1px solid var(--border-subtle); align-items: center;">
          <div>
            <div style="font-size: 2rem; font-weight: 800; font-family: var(--font-mono); color: var(--cyan);">${data.completion_percentage}%</div>
            <div style="font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase;">Milestone Completion</div>
          </div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--text-muted); margin-bottom: 6px;">
              <span>Deal Stage: <strong>${data.current_stage}</strong></span>
              <span>Velocity: <strong style="color: var(--emerald);">${data.velocity_status}</strong> (${data.cycle_days} Days in Cycle)</span>
            </div>
            <div style="height: 10px; background: rgba(255, 255, 255, 0.08); border-radius: 5px; overflow: hidden;">
              <div style="height: 100%; width: ${data.completion_percentage}%; background: linear-gradient(90deg, var(--cyan) 0%, var(--emerald) 100%);"></div>
            </div>
          </div>
        </div>

        <div style="margin-top: 1.5rem;">
          <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 0.75rem;">Stage-Gate Milestones:</h4>
          <div class="stage-gates-flow">${gatesHtml}</div>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load progress: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 12: FOLLOW-UP INTELLIGENCE ====================
  async loadFollowupIntelligence() {
    const container = document.getElementById('followups-cockpit-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Loading scheduled follow-ups and optimal contact windows...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/follow-ups`);
      const data = await res.json();

      container.innerHTML = data.follow_ups.map(fu => `
        <div class="followup-card">
          <div style="flex: 1;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
              <strong style="color: #fff; font-size: 1.05rem;">${fu.stakeholder}</strong>
              <span class="card-badge highlight">${fu.status} &bull; Due ${fu.due_date}</span>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">Topic: ${fu.topic}</p>
            <div style="font-size: 0.82rem; color: var(--amber); margin-top: 4px;">⏰ Optimal Contact Window: ${fu.optimal_timing} (${fu.recommended_channel})</div>
            <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 10px; margin-top: 8px; font-family: var(--font-mono); font-size: 0.82rem; color: var(--cyan);">
              ${fu.draft_message}
            </div>
          </div>
          <div style="margin-left: 1.5rem; display: flex; flex-direction: column; gap: 8px;">
            <button class="action-btn primary small" onclick="navigator.clipboard.writeText('${encodeURIComponent(fu.draft_message)}'); alert('Follow-up email copied to clipboard!');">Copy Email</button>
            <button class="action-btn secondary small" onclick="this.innerText='✅ Sent'; this.disabled=true;">Mark as Sent</button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load follow-ups: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 13: CRM KNOWLEDGE SEARCH ====================
  async executeCRMSearch(query) {
    const container = document.getElementById('crm-search-results-container');
    if (!container) return;
    container.style.display = 'flex';
    container.innerHTML = '<div class="loading-state">Searching Hindsight memory bank for verifiable answer...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });
      const data = await res.json();

      const sourcesHtml = (data.sources || []).map(s => `
        <span class="citation-chip">📜 Citation: ${s}</span>
      `).join('');

      container.innerHTML = `
        <div style="font-size: 0.85rem; font-family: var(--font-mono); color: var(--cyan); text-transform: uppercase;">Q: "${data.query}"</div>
        <div class="crm-answer-text">${data.answer}</div>
        <div class="citations-row">
          <span style="font-size: 0.78rem; color: var(--text-dim);">Source Verification:</span>
          ${sourcesHtml}
          <span style="margin-left: auto; font-size: 0.78rem; color: var(--emerald); font-family: var(--font-mono);">Confidence: ${Math.round((data.confidence || 0.95) * 100)}%</span>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Search failed: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 14: PERSONALIZED SALES STRATEGY ====================
  async loadPersonalizedStrategy() {
    const container = document.getElementById('strategy-cockpit-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Synthesizing personalized account sales strategy...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/strategy`);
      const data = await res.json();

      container.innerHTML = `
        <div class="card" style="padding: 1.5rem;">
          <div style="font-size: 0.8rem; font-family: var(--font-mono); color: var(--cyan); text-transform: uppercase; margin-bottom: 6px;">Primary Narrative Hook</div>
          <h3 style="color: #fff; font-size: 1.25rem; margin-bottom: 0.75rem;">${data.primary_strategic_narrative}</h3>
          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.5;">${data.executive_alignment_matrix}</p>
        </div>

        <div class="card" style="padding: 1.5rem; margin-top: 1rem;">
          <h4 style="color: #fff; font-size: 1rem; margin-bottom: 0.75rem;">Closing Blueprint & Stage Roadmap</h4>
          <div style="background: rgba(16, 185, 129, 0.08); border-left: 3px solid var(--emerald); padding: 12px 16px; border-radius: 0 6px 6px 0; font-size: 0.92rem; color: #a7f3d0;">
            ${data.closing_blueprint}
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
          <div class="card" style="padding: 1.25rem;">
            <h5 style="color: var(--emerald); font-size: 0.85rem; font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 0.6rem;">Approved Trade Concessions</h5>
            <ul style="list-style: none; font-size: 0.85rem; color: var(--text-muted);">
              ${(data.negotiation_boundary.approved_concessions || []).map(c => `<li>✅ ${c}</li>`).join('')}
            </ul>
          </div>
          <div class="card" style="padding: 1.25rem;">
            <h5 style="color: var(--rose); font-size: 0.85rem; font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 0.6rem;">Prohibited Concessions (Margin Traps)</h5>
            <ul style="list-style: none; font-size: 0.85rem; color: var(--text-muted);">
              ${(data.negotiation_boundary.prohibited_concessions || []).map(c => `<li>❌ ${c}</li>`).join('')}
            </ul>
          </div>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load strategy: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 15: DEAL COMPARISON ====================
  async loadDealComparison(benchmarkId = null) {
    const container = document.getElementById('comparison-display-container');
    const select = document.getElementById('benchmark-deal-select');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Running comparative benchmark analysis...</div>';

    try {
      const url = benchmarkId ? `/api/deals/${this.currentDealId}/compare` : `/api/deals/${this.currentDealId}/compare`;
      const res = benchmarkId 
        ? await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ benchmark_deal_id: benchmarkId }) })
        : await fetch(url);
      const data = await res.json();
      const comp = data.comparison;

      if (select && data.available_historical_deals) {
        select.innerHTML = data.available_historical_deals.map(d => `
          <option value="${d.id}" ${benchmarkId === d.id ? 'selected' : ''}>Benchmark: ${d.name}</option>
        `).join('');
      }

      container.innerHTML = `
        <table class="quote-sheet-table">
          <thead>
            <tr>
              <th style="width: 25%;">Comparison Dimension</th>
              <th style="width: 37.5%; color: var(--cyan);">Current Deal (${comp.current_deal.name})</th>
              <th style="width: 37.5%; color: var(--emerald);">Benchmark (${comp.benchmark_deal.name})</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Target / Final ARR</strong></td>
              <td class="number">$${(comp.current_deal.arr / 1000).toFixed(0)}k</td>
              <td class="number">$${(comp.benchmark_deal.final_arr / 1000).toFixed(0)}k</td>
            </tr>
            <tr>
              <td><strong>Primary Competitor</strong></td>
              <td>${comp.current_deal.competitor}</td>
              <td>${comp.benchmark_deal.competitor_faced}</td>
            </tr>
            <tr>
              <td><strong>Sales Cycle Days</strong></td>
              <td>48 Days (In Flight)</td>
              <td class="number">${comp.benchmark_deal.sales_cycle_days} Days (Closed Won)</td>
            </tr>
            <tr>
              <td><strong>Margin Preserved</strong></td>
              <td class="number" style="color: var(--emerald);">$170k vs Competitor</td>
              <td class="number" style="color: var(--emerald);">$${(comp.benchmark_deal.margin_preserved / 1000).toFixed(0)}k</td>
            </tr>
            <tr>
              <td><strong>Winning Tactic / Playbook</strong></td>
              <td style="color: var(--text-muted); font-size: 0.85rem;">Trading $50k migration engineering credit for 2-year commit at $620k+ ARR.</td>
              <td style="color: #a7f3d0; font-size: 0.85rem;">${comp.benchmark_deal.winning_tactic}</td>
            </tr>
          </tbody>
        </table>

        <div class="card" style="padding: 1.25rem; margin-top: 1.25rem;">
          <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 0.75rem;">Comparative AI Takeaways:</h4>
          <ul style="list-style: none; font-size: 0.88rem; color: var(--text-muted); display: flex; flex-direction: column; gap: 8px;">
            ${(comp.comparative_insights || []).map(ci => `<li>💡 ${ci}</li>`).join('')}
          </ul>
        </div>
      `;
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load comparison: ${e.message}</div>`;
    }
  }

  // ==================== FEATURE 16: PERSISTENT LEARNING ====================
  async loadPersistentLearning() {
    const container = document.getElementById('learning-insights-container');
    if (!container) return;
    container.innerHTML = '<div class="loading-state">Loading persistent cognitive learning log...</div>';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/learning`);
      const data = await res.json();

      container.innerHTML = data.learning_log.map(item => `
        <div class="lesson-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="card-badge highlight">${item.tier} &bull; ${item.category}</span>
            <span style="font-size: 0.75rem; color: var(--emerald); font-family: var(--font-mono);">${item.status} (${Math.round((item.confidence || 0.95) * 100)}% Confidence)</span>
          </div>
          <div style="font-size: 0.95rem; font-weight: 500; color: #fff; line-height: 1.5; margin-top: 4px;">"${item.insight}"</div>
          <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">Synthesized across ${item.deals_synthesized || 1} enterprise negotiation(s)</div>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<div style="color: var(--rose);">Failed to load learning log: ${e.message}</div>`;
    }
  }

  async submitLearningFeedback() {
    const cat = document.getElementById('modal-feedback-category').value;
    const tier = document.getElementById('modal-feedback-tier').value;
    const insight = document.getElementById('modal-feedback-insight').value.trim();
    const promote = document.getElementById('modal-feedback-promote').checked;
    if (!insight) return;

    try {
      await fetch(`/api/deals/${this.currentDealId}/learning/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: cat, tier: tier, insight: insight, promote_global: promote })
      });
      document.getElementById('modal-feedback').style.display = 'none';
      document.getElementById('modal-feedback-insight').value = '';
      alert('Outcome recorded into persistent memory!');
      this.loadPersistentLearning();
    } catch (e) {
      alert(`Error recording learning: ${e.message}`);
    }
  }

  // ==================== FEATURE 1: DEAL MEMORY BANK ====================
  async loadMemoryBank() {
    const container = document.getElementById('memory-cards-container');
    if (!container) return;

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/memory`);
      const data = await res.json();
      this.memoryNodes = data.all_nodes || [];

      // Update counters
      const stats = data.stats || {};
      const allCount = document.getElementById('count-all-tiers');
      if (allCount) allCount.innerText = stats.total_memories || this.memoryNodes.length;
      const wCount = document.getElementById('count-world-tier');
      if (wCount) wCount.innerText = stats.world_facts || 0;
      const eCount = document.getElementById('count-exp-tier');
      if (eCount) eCount.innerText = stats.experiences || 0;
      const oCount = document.getElementById('count-obs-tier');
      if (oCount) oCount.innerText = stats.observations || 0;
      const opCount = document.getElementById('count-op-tier');
      if (opCount) opCount.innerText = stats.opinions || 0;

      // Update meter counts in sidebar
      const mw = document.getElementById('meter-world-count');
      if (mw) mw.innerText = stats.world_facts || 0;
      const me = document.getElementById('meter-exp-count');
      if (me) me.innerText = stats.experiences || 0;
      const mo = document.getElementById('meter-obs-count');
      if (mo) mo.innerText = stats.observations || 0;
      const mop = document.getElementById('meter-op-count');
      if (mop) mop.innerText = stats.opinions || 0;

      this.renderMemoryCards();
      this.updatePipelineStats();
    } catch (e) {
      console.warn('Failed to load memory graph:', e);
    }
  }

  renderMemoryCards() {
    const container = document.getElementById('memory-cards-container');
    if (!container) return;

    const filtered = this.memoryNodes.filter(n => {
      if (this.memoryFilterTier === 'all') return true;
      return n.tier.toLowerCase() === this.memoryFilterTier.toLowerCase();
    });

    if (filtered.length === 0) {
      container.innerHTML = '<div class="empty-state">No memory nodes found in this tier.</div>';
      return;
    }

    container.innerHTML = filtered.map(n => `
      <div class="memory-card">
        <div class="memory-card-top">
          <span class="memory-tier-badge ${n.tier.toLowerCase()}">${n.tier}</span>
          <span style="font-size: 0.72rem; color: var(--text-dim); font-family: var(--font-mono);">${n.id}</span>
        </div>
        <div class="memory-card-text">${n.full_text || n.label}</div>
        <div class="memory-card-tags">
          ${(n.tags || []).map(t => `<span class="memory-tag">#${t}</span>`).join('')}
        </div>
      </div>
    `).join('');
  }

  async searchMemory() {
    const query = document.getElementById('memory-search-query').value.trim();
    if (!query) {
      this.loadMemoryBank();
      return;
    }

    try {
      const res = await fetch(`/api/hindsight/recall`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bank_id: this.getActiveDeal().bank_id, query: query, max_results: 10 })
      });
      const results = await res.json();
      this.memoryNodes = results.map(r => ({
        id: r.id,
        label: r.text,
        full_text: r.text,
        tier: r.tier || 'Experience',
        tags: r.tags || [],
        score: r.score
      }));
      this.renderMemoryCards();
    } catch (e) {
      console.warn('Memory search error:', e);
    }
  }

  async submitRetainMemory() {
    const bank = document.getElementById('modal-retain-bank').value;
    const tier = document.getElementById('modal-retain-tier').value;
    const content = document.getElementById('modal-retain-content').value.trim();
    const tags = document.getElementById('modal-retain-tags').value.split(',').map(t => t.trim()).filter(Boolean);

    if (!content) return;

    try {
      await fetch('/api/hindsight/retain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bank_id: bank, content: content, tier: tier, tags: tags })
      });
      document.getElementById('modal-retain').style.display = 'none';
      document.getElementById('modal-retain-content').value = '';
      alert('Memory node retained into Hindsight bank!');
      this.loadMemoryBank();
    } catch (e) {
      alert(`Retain error: ${e.message}`);
    }
  }

  // ==================== TACTICAL BRIEFING & COACHING ====================
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
          <span style="font-size: 0.8rem; color: var(--emerald); font-family: var(--font-mono);">Confidence: ${Math.round((data.confidence_score || 0.92) * 100)}%</span>
        </div>

        <div class="reframe-strategy-box">
          <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--cyan); text-transform: uppercase;">1. Tactical Reframe Strategy</div>
          <p style="font-size: 0.9rem; color: var(--text-main); margin-top: 4px;">${data.reframe_strategy}</p>
        </div>

        <div class="recommended-response-box" style="margin-top: 1rem;">
          <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--emerald); text-transform: uppercase;">2. Word-For-Word Executive Script</div>
          <p style="font-size: 1rem; color: #fff; font-weight: 500; line-height: 1.5; margin-top: 4px;">“${data.recommended_response}”</p>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
          <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid var(--amber); padding: 10px 12px; border-radius: 0 6px 6px 0;">
            <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--amber); text-transform: uppercase;">3. Give-Get Trade-off</div>
            <p style="font-size: 0.85rem; color: #fde68a; margin-top: 4px;">${data.give_get_tradeoff}</p>
          </div>
          <div style="background: rgba(139, 92, 246, 0.08); border-left: 3px solid var(--purple); padding: 10px 12px; border-radius: 0 6px 6px 0;">
            <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--purple-light); text-transform: uppercase;">4. Past Deal Citation</div>
            <p style="font-size: 0.85rem; color: #ddd6fe; margin-top: 4px;">${data.past_deal_citation}</p>
          </div>
        </div>
      `;
    } catch (e) {
      resultContainer.innerHTML = `<p style="color: var(--rose);">Failed to coach objection: ${e.message}</p>`;
    }
  }

  // ==================== GUIDED DEMO ENGINE ====================
  startGuidedDemo() {
    this.guidedDemoStep = 1;
    document.getElementById('guided-demo-banner').style.display = 'flex';
    this.executeGuidedDemoStep(1);
  }

  nextGuidedStep() {
    if (this.guidedDemoStep < 4) {
      this.guidedDemoStep++;
      this.executeGuidedDemoStep(this.guidedDemoStep);
    }
  }

  prevGuidedStep() {
    if (this.guidedDemoStep > 1) {
      this.guidedDemoStep--;
      this.executeGuidedDemoStep(this.guidedDemoStep);
    }
  }

  exitGuidedDemo() {
    document.getElementById('guided-demo-banner').style.display = 'none';
    this.guidedDemoStep = 0;
  }

  async executeGuidedDemoStep(stepNum) {
    document.getElementById('demo-step-badge').innerText = `STEP ${stepNum} OF 4`;
    document.getElementById('demo-prev-btn').disabled = (stepNum === 1);
    document.getElementById('demo-next-btn').innerText = (stepNum === 4) ? 'Finish Demo' : 'Next Step →';

    try {
      const res = await fetch(`/api/demo/step/${stepNum}`);
      const data = await res.json();
      document.getElementById('demo-step-title').innerText = data.title;
      document.getElementById('demo-step-desc').innerText = data.scenario;

      if (stepNum === 1) {
        this.switchTab('cockpit');
        await this.loadDeals();
      } else if (stepNum === 2) {
        this.switchTab('objections');
        document.getElementById('objection-input-text').value = data.objection_input;
        this.coachObjection();
      } else if (stepNum === 3) {
        this.switchTab('summary');
        this.loadInstantSummary();
      } else if (stepNum === 4) {
        this.switchTab('winning-patterns');
        this.loadWinningPatterns();
      }
    } catch (e) {
      console.warn('Guided step error:', e);
    }
  }

  // ==================== LEARNING CURVE & ARTIFACTS ====================
  async loadLearningCurve() {
    try {
      const res = await fetch('/api/learning-curve');
      this.learningCurveData = await res.json();
      this.renderLearningStages();
      this.renderLearningStageDetail(this.selectedLearningStage);
    } catch (e) {
      console.warn('Failed to load learning curve:', e);
    }
  }

  renderLearningStages() {
    const container = document.getElementById('learning-stages-container');
    if (!container) return;

    container.innerHTML = this.learningCurveData.map(st => `
      <div class="learning-stage-card ${st.stage === this.selectedLearningStage ? 'active' : ''}" onclick="window.nexus.selectLearningStage(${st.stage})">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <span style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-dim);">${st.timeline}</span>
          <span class="cap-badge ${st.badge_color}">${st.status}</span>
        </div>
        <div style="font-size: 1rem; font-weight: 700; color: #fff;">${st.label}</div>
        <div style="margin-top: 8px; display: flex; align-items: center; gap: 8px;">
          <div style="flex: 1; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
            <div style="height: 100%; width: ${st.competence}%; background: var(--${st.badge_color || 'primary'});"></div>
          </div>
          <span style="font-size: 0.78rem; font-family: var(--font-mono); font-weight: 700;">${st.competence}%</span>
        </div>
      </div>
    `).join('');
  }

  selectLearningStage(stageNum) {
    this.selectedLearningStage = stageNum;
    this.renderLearningStages();
    this.renderLearningStageDetail(stageNum);
  }

  renderLearningStageDetail(stageNum) {
    const container = document.getElementById('stage-detail-container');
    if (!container) return;
    const stage = this.learningCurveData.find(s => s.stage === stageNum) || this.learningCurveData[0];
    if (!stage) return;

    container.innerHTML = `
      <div style="background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h3 style="color: #fff; font-size: 1.15rem;">${stage.label}: ${stage.status}</h3>
          <span class="card-badge highlight">${stage.memory_impact}</span>
        </div>
        <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 1.25rem;">${stage.summary}</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
          <div style="background: rgba(244,63,94,0.06); border-left: 3px solid var(--rose); padding: 12px; border-radius: 0 6px 6px 0;">
            <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--rose); text-transform: uppercase;">Standard AI (Without Memory)</div>
            <p style="font-size: 0.88rem; color: #fecdd3; margin-top: 4px;">${stage.sample_dialogue_before}</p>
          </div>
          <div style="background: rgba(16,185,129,0.06); border-left: 3px solid var(--emerald); padding: 12px; border-radius: 0 6px 6px 0;">
            <div style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--emerald); text-transform: uppercase;">Nexus (With Hindsight Memory)</div>
            <p style="font-size: 0.88rem; color: #a7f3d0; font-weight: 500; margin-top: 4px;">${stage.sample_dialogue_after}</p>
          </div>
        </div>
      </div>
    `;
  }

  async loadEnterpriseArtifacts() {
    try {
      const res = await fetch('/api/artifacts');
      this.enterpriseArtifacts = await res.json();
      this.renderArtifact(this.selectedArtifact);
    } catch (e) {
      console.warn('Failed to load artifacts:', e);
    }
  }

  renderArtifact(artifactType) {
    this.selectedArtifact = artifactType;
    const container = document.getElementById('artifact-viewer-container');
    if (!container || !this.enterpriseArtifacts) return;

    if (artifactType === 'ciso_email') {
      const email = this.enterpriseArtifacts.ciso_email_thread;
      container.innerHTML = `
        <div class="card" style="padding: 1.5rem;">
          <table class="quote-sheet-table" style="margin-bottom: 1rem;">
            <tr><td style="width: 15%; color: var(--text-dim);">From:</td><td>${email.from}</td></tr>
            <tr><td style="color: var(--text-dim);">To:</td><td>${email.to}</td></tr>
            <tr><td style="color: var(--text-dim);">Date:</td><td>${email.date}</td></tr>
            <tr><td style="color: var(--text-dim);">Subject:</td><td style="color: #fff; font-weight: 600;">${email.subject}</td></tr>
          </table>
          <div style="font-family: var(--font-mono); font-size: 0.88rem; line-height: 1.6; white-space: pre-wrap; color: var(--text-main); background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 6px;">${email.body}</div>
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
      await fetch('/api/settings/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          hindsight_api_key: key || null,
          hindsight_base_url: url || null,
          groq_api_key: groqKey || null
        })
      });
      await this.checkHealth();
      document.getElementById('modal-settings').style.display = 'none';
      alert('Settings updated successfully!');
    } catch (e) {
      alert(`Settings update error: ${e.message}`);
    }
  }

  // ==================== LIVE DEMO & REAL-TIME 3-PANEL COCKPIT ====================
  async loadLiveDemoScript() {
    try {
      const res = await fetch('/api/demo/live-script');
      this.liveDemoScript = await res.json();
    } catch (e) {
      console.warn('Failed to load demo script from API:', e);
    }
  }

  async startLiveDemoStream() {
    this.switchTab('live-call');
    this.resetLiveCall();
    this.liveDemoIsStreaming = true;

    // Activate audio wave bars
    document.querySelectorAll('.wave-bar').forEach(b => b.classList.add('active'));

    const runBtn = document.getElementById('btn-run-live-demo-stream');
    if (runBtn) {
      runBtn.disabled = true;
      runBtn.innerHTML = '<span>⏳ STREAMING DIALOGUE...</span>';
    }

    for (let i = 0; i < this.liveDemoScript.length; i++) {
      if (!this.liveDemoIsStreaming) break;
      this.liveDemoCurrentStep = i + 1;
      const turn = this.liveDemoScript[i];
      this.renderTurn(turn);
      
      // Realistic conversational pause (2.4 seconds per turn)
      await new Promise(resolve => setTimeout(resolve, 2400));
    }

    if (runBtn) {
      runBtn.disabled = false;
      runBtn.innerHTML = '<span>▶ START LIVE DEMO</span>';
    }

    // Auto-trigger Post-Meeting Summary Modal (Section 23 & 28)
    setTimeout(() => {
      this.openPostMeetingSummaryModal();
    }, 1200);
  }

  advanceLiveDemoStep() {
    if (this.liveDemoCurrentStep >= this.liveDemoScript.length) {
      this.openPostMeetingSummaryModal();
      return;
    }
    const turn = this.liveDemoScript[this.liveDemoCurrentStep];
    this.liveDemoCurrentStep++;
    this.renderTurn(turn);
    if (this.liveDemoCurrentStep === this.liveDemoScript.length) {
      setTimeout(() => this.openPostMeetingSummaryModal(), 1200);
    }
  }

  resetLiveCall() {
    this.liveDemoIsStreaming = false;
    this.liveDemoCurrentStep = 0;
    this.liveSignalsCount = 0;

    const transcriptFeed = document.getElementById('live-transcript-feed');
    if (transcriptFeed) {
      transcriptFeed.innerHTML = `
        <div class="empty-state-hint" id="transcript-empty-hint" style="text-align: center; padding: 2rem 1rem; color: var(--text-dim);">
          <p style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎧</p>
          <p>Click <strong>▶ START LIVE DEMO</strong> or type below to stream customer dialogue.</p>
        </div>
      `;
    }

    const intelFeed = document.getElementById('live-intelligence-feed');
    if (intelFeed) {
      intelFeed.innerHTML = `
        <div class="empty-state-hint" id="intel-empty-hint" style="text-align: center; padding: 2.5rem 1.5rem; color: var(--text-dim);">
          <p style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</p>
          <p style="font-weight: 600; color: var(--text-muted); margin-bottom: 0.25rem;">Copilot Ingesting Audio Stream</p>
          <p style="font-size: 0.85rem;">Autonomous intent, objection classification, buying signals, and winning TCO counter-tactics will surface in real time.</p>
        </div>
      `;
    }

    const turnCounter = document.getElementById('live-turn-counter');
    if (turnCounter) turnCounter.innerText = '0 Turns';

    const sigCounter = document.getElementById('live-signals-count');
    if (sigCounter) sigCounter.innerText = '0 Signals';

    const runBtn = document.getElementById('btn-run-live-demo-stream');
    if (runBtn) {
      runBtn.disabled = false;
      runBtn.innerHTML = '<span>▶ START LIVE DEMO</span>';
    }

    this.renderLiveDealMemorySidebar();
  }

  renderTurn(turn) {
    const transcriptFeed = document.getElementById('live-transcript-feed');
    if (!transcriptFeed) return;

    const emptyHint = document.getElementById('transcript-empty-hint');
    if (emptyHint) emptyHint.remove();

    const isRep = turn.speaker.toLowerCase().includes('rep');
    const bubble = document.createElement('div');
    bubble.className = `transcript-bubble-item ${isRep ? 'rep' : 'customer'}`;
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    bubble.innerHTML = `
      <div class="bubble-meta">
        <span class="speaker-badge ${isRep ? 'rep' : 'customer'}">
          ${isRep ? '👤 Sales Rep' : '🏢 Rohan Sharma (CTO)'}
        </span>
        <span class="bubble-time">${timestamp}</span>
      </div>
      <div class="bubble-body">
        ${turn.text}
      </div>
    `;
    transcriptFeed.appendChild(bubble);
    transcriptFeed.scrollTop = transcriptFeed.scrollHeight;

    const turnCounter = document.getElementById('live-turn-counter');
    if (turnCounter) turnCounter.innerText = `${this.liveDemoCurrentStep} Turns`;

    if (turn.detected_event) {
      this.renderIntelligenceAlert(turn.detected_event);
    }
  }

  handleManualSpeechInput(text) {
    this.renderTurn({
      speaker: 'Customer (Rohan Sharma, CTO)',
      text: text,
      detected_event: text.toLowerCase().includes('price') || text.toLowerCase().includes('competitor') ? {
        type: 'objection',
        badge: '🔴 Pricing Objection Detected',
        title: 'Live Objection Identified',
        detail: `Customer mentioned: "${text}"`,
        priority: 'Critical',
        deal_memory: {
          budget: '₹25,00,000 ($300k)',
          competitor: 'Competitor X',
          previous_discount_request: '15%',
          decision_maker: 'CTO Rohan Sharma / CFO Anita Roy'
        },
        historical_pattern: 'ROI comparison worked in 4 similar deals (e.g. Deal #1024 FinTech ₹30L Won).',
        suggested_approach: 'Focus on total cost of ownership and measurable ROI. Ask whether concern is initial sticker price or overall implementation toil.',
        next_best_action: 'Ask whether the concern is initial price or overall implementation cost.'
      } : {
        type: 'signal',
        badge: '📌 Note Analyzed',
        title: 'Live Transcript Input',
        detail: text,
        priority: 'Positive'
      }
    });
  }

  renderIntelligenceAlert(event) {
    const intelFeed = document.getElementById('live-intelligence-feed');
    if (!intelFeed) return;

    const emptyHint = document.getElementById('intel-empty-hint');
    if (emptyHint) emptyHint.remove();

    this.liveSignalsCount++;
    const sigCounter = document.getElementById('live-signals-count');
    if (sigCounter) sigCounter.innerText = `${this.liveSignalsCount} Signals`;

    const card = document.createElement('div');
    const priorityClass = event.priority === 'Critical' ? 'critical' : (event.priority === 'High' ? 'important' : 'positive');
    card.className = `intel-card-alert ${priorityClass}`;

    let dealMemHtml = '';
    if (event.deal_memory) {
      dealMemHtml = `
        <div class="intel-memory-dossier">
          <div style="font-weight: 700; color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase;">Deal Memory Retrieved:</div>
          <div class="memory-pill-row">
            <span class="mem-chip">Budget: ${event.deal_memory.budget}</span>
            <span class="mem-chip">Competitor: ${event.deal_memory.competitor}</span>
            <span class="mem-chip">Discount Req: ${event.deal_memory.previous_discount_request}</span>
            <span class="mem-chip">Decision Maker: ${event.deal_memory.decision_maker}</span>
          </div>
        </div>
      `;
    }

    let patternHtml = '';
    if (event.historical_pattern) {
      patternHtml = `
        <div class="intel-pattern-box">
          <div class="pattern-title">🏆 Historical Pattern Citation</div>
          <p>${event.historical_pattern}</p>
        </div>
      `;
    }

    let approachHtml = '';
    if (event.suggested_approach) {
      approachHtml = `
        <div class="intel-approach-box">
          <div class="approach-title">💡 Suggested Talking Point</div>
          <p><strong>Approach:</strong> "${event.suggested_approach}"</p>
          ${event.next_best_action ? `<p style="margin-top: 6px; color: #a7f3d0;"><strong>Next Best Action:</strong> "${event.next_best_action}"</p>` : ''}
        </div>
      `;
    }

    card.innerHTML = `
      <div class="intel-header-badge-row">
        <span class="intel-event-tag ${priorityClass}">${event.badge || 'Signal Detected'}</span>
        <span class="badge-pill ${priorityClass}">${event.priority || 'Positive'}</span>
        <button class="why-btn btn-ask-why-intel" title="Ask LOKI why this was flagged">💡 WHY?</button>
      </div>
      <h4 style="font-size: 1rem; color: #fff; margin: 0;">${event.title}</h4>
      <p style="font-size: 0.88rem; color: var(--text-muted); margin: 0;">${event.detail}</p>
      ${dealMemHtml}
      ${patternHtml}
      ${approachHtml}
      <div class="intel-actions-toolbar">
        <button class="action-tool-btn primary btn-approve-intel">✓ Approve Recommendation</button>
        <button class="action-tool-btn success btn-mem-intel">🧠 Add to Memory</button>
        <button class="action-tool-btn btn-task-intel">📋 Create Task</button>
        <button class="action-tool-btn btn-dismiss-intel">✕ Dismiss</button>
      </div>
    `;

    card.querySelector('.btn-ask-why-intel')?.addEventListener('click', () => {
      this.askLokiWhy(this.currentDealId, event.title, event.detail);
    });

    card.querySelector('.btn-approve-intel')?.addEventListener('click', (e) => {
      e.target.innerHTML = '✓ Approved & Adopted';
      e.target.style.background = 'var(--emerald)';
    });
    card.querySelector('.btn-dismiss-intel')?.addEventListener('click', () => {
      card.style.opacity = '0';
      card.style.transform = 'translateX(20px)';
      setTimeout(() => card.remove(), 250);
    });
    card.querySelector('.btn-mem-intel')?.addEventListener('click', (e) => {
      e.target.innerHTML = '🧠 Retained';
      this.retainedQuickMemory(event.title, event.detail);
    });
    card.querySelector('.btn-task-intel')?.addEventListener('click', () => {
      const modal = document.getElementById('modal-create-task');
      if (modal) {
        document.getElementById('task-create-title').value = event.next_best_action || event.title;
        modal.style.display = 'flex';
      }
    });

    intelFeed.appendChild(card);
    intelFeed.scrollTop = intelFeed.scrollHeight;
  }

  async retainedQuickMemory(title, text) {
    const deal = this.getActiveDeal();
    if (!deal) return;
    try {
      await fetch('/api/hindsight/retain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bank_id: deal.bank_id,
          content: `${title}: ${text}`,
          tier: 'Observation',
          node_type: 'observation',
          tags: ['live_call_copilot', deal.id]
        })
      });
      await this.loadMemoryBank();
    } catch (e) {
      console.warn('Failed to retain quick memory:', e);
    }
  }

  renderLiveDealMemorySidebar() {
    const sidebar = document.getElementById('live-deal-memory-sidebar');
    if (!sidebar) return;

    const deal = this.getActiveDeal();
    if (!deal) return;

    const titleElem = document.getElementById('call-active-account-title');
    if (titleElem) {
      titleElem.innerHTML = `${deal.company || deal.name} &mdash; ${deal.name}`;
    }

    sidebar.innerHTML = `
      <div class="deal-memory-block">
        <div class="deal-summary-stat-grid">
          <div class="memory-stat-card">
            <span class="stat-title-small">Deal Value</span>
            <span class="stat-value-prominent" style="color: var(--primary-light);">${deal.deal_value_display || ('₹' + (deal.arr_target || 300000).toLocaleString())}</span>
          </div>
          <div class="memory-stat-card">
            <span class="stat-title-small">Deal Stage</span>
            <span class="stat-value-prominent text-cyan">${deal.stage || 'Negotiation'}</span>
          </div>
          <div class="memory-stat-card">
            <span class="stat-title-small">Health Score</span>
            <span class="stat-value-prominent text-emerald">${deal.health_score || 82}%</span>
          </div>
          <div class="memory-stat-card">
            <span class="stat-title-small">Hindsight Tier</span>
            <span class="stat-value-prominent text-amber">World & Exp</span>
          </div>
        </div>

        <div class="memory-section-box">
          <div class="section-label-bar">
            <span>Key Stakeholders</span>
            <span style="font-size: 0.7rem; color: var(--text-dim);">${(deal.stakeholders || []).length} Tracked</span>
          </div>
          ${(deal.stakeholders || []).slice(0, 2).map(s => `
            <div class="stakeholder-mini-item">
              <div>
                <strong>${s.name}</strong>
                <div style="font-size: 0.72rem; color: var(--text-dim);">${s.role}</div>
              </div>
              <span class="badge-pill warning" style="font-size: 0.7rem;">${s.influence}</span>
            </div>
          `).join('')}
        </div>

        <div class="memory-section-box">
          <div class="section-label-bar">
            <span>Validated Requirements</span>
            <span style="font-size: 0.7rem; color: var(--text-dim);">${(deal.requirements || []).length} Active</span>
          </div>
          ${(deal.requirements || []).map(r => `
            <div class="req-check-item">
              <span class="req-check-icon">✓</span>
              <span>${r.title}</span>
            </div>
          `).join('')}
        </div>

        <div class="memory-section-box">
          <div class="section-label-bar">
            <span>Competitor Tracking</span>
          </div>
          <div style="background: rgba(244,63,94,0.08); border: 1px solid rgba(244,63,94,0.25); border-radius: 6px; padding: 6px 8px; font-size: 0.78rem;">
            <strong style="color: #fda4af;">Competitor X (Active Anchor)</strong>
            <p style="margin-top: 2px; color: var(--text-muted);">Customer cited 15% discount. Counter with 74% MTTR reduction and low maintenance toil.</p>
          </div>
        </div>

        <div class="memory-section-box">
          <div class="section-label-bar">
            <span>Deal Risk Indicators</span>
          </div>
          <div style="background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); border-radius: 6px; padding: 6px 8px; font-size: 0.78rem;">
            <strong style="color: #fcd34d;">⚠ Medium Risk: Pricing Objection</strong>
            <p style="margin-top: 2px; color: var(--text-muted);">Requires formal TCO model submission to CFO Anita Roy before contract sign-off.</p>
          </div>
        </div>
      </div>
    `;
  }

  // ==================== PRE-MEETING 30S BRIEFING (SECTION 4) ====================
  async openPreMeetingBriefingModal() {
    const modal = document.getElementById('modal-pre-meeting-briefing');
    const body = document.getElementById('modal-briefing-body');
    if (!modal || !body) return;

    body.innerHTML = '<div class="loading-state">Synthesizing 30-second pre-meeting deal briefing...</div>';
    modal.style.display = 'flex';

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/briefing/structured`);
      const b = await res.json();
      this.cachedStructuredBriefing = b;

      body.innerHTML = `
        <div class="briefing-meta-grid">
          <div class="briefing-meta-card">
            <div class="briefing-meta-label">Customer Account</div>
            <div class="briefing-meta-val">${b.customer}</div>
          </div>
          <div class="briefing-meta-card">
            <div class="briefing-meta-label">Deal Stage</div>
            <div class="briefing-meta-val text-cyan">${b.deal_stage}</div>
          </div>
          <div class="briefing-meta-card">
            <div class="briefing-meta-label">Deal Value</div>
            <div class="briefing-meta-val" style="color: var(--primary-light);">${b.deal_value}</div>
          </div>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1rem;">
          <h4 style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.5rem;">Key Requirements:</h4>
          <ul style="padding-left: 1.25rem; font-size: 0.88rem; color: #e2e8f0; display: flex; flex-direction: column; gap: 4px;">
            ${(b.key_requirements || []).map(r => `<li>✓ ${r}</li>`).join('')}
          </ul>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
          <div style="background: rgba(244,63,94,0.06); border: 1px solid rgba(244,63,94,0.25); border-radius: 8px; padding: 0.75rem;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #fda4af; font-weight: 700;">Previous Objections:</div>
            <ul style="padding-left: 1rem; font-size: 0.82rem; margin-top: 4px; color: #fecdd3;">
              ${(b.previous_objections || []).map(o => `<li>⚠ ${o}</li>`).join('')}
            </ul>
          </div>

          <div style="background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.25); border-radius: 8px; padding: 0.75rem;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--purple-light); font-weight: 700;">Competitors:</div>
            <p style="font-size: 0.85rem; margin-top: 4px; color: #e2e8f0;">🥊 ${(b.competitors || []).join(', ')}</p>
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-dim); margin-top: 6px; font-weight: 700;">Decision Makers:</div>
            <p style="font-size: 0.82rem; margin-top: 2px; color: #cbd5e1;">👤 ${(b.decision_makers || []).join(', ')}</p>
          </div>
        </div>

        <div style="background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: 8px; padding: 0.85rem;">
          <div style="font-size: 0.75rem; text-transform: uppercase; color: #34d399; font-weight: 700; margin-bottom: 4px;">Recommended Strategic Focus:</div>
          <p style="font-size: 0.9rem; color: #f0fdf4; line-height: 1.45;">"${b.recommended_focus}"</p>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0.85rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.3); border-radius: 8px; font-size: 0.82rem;">
          <span style="color: #fcd34d;"><strong>Deal Risk Alert:</strong> ${b.risk}</span>
          <span class="badge-pill warning">Health: ${b.deal_health}%</span>
        </div>
      `;
    } catch (e) {
      body.innerHTML = `<div class="error-state">Failed to load briefing: ${e.message}</div>`;
    }
  }

  copyBriefingToClipboard() {
    if (!this.cachedStructuredBriefing) return;
    const b = this.cachedStructuredBriefing;
    const text = `NEXUS DEAL BRIEFING\nCustomer: ${b.customer}\nStage: ${b.deal_stage}\nValue: ${b.deal_value}\nRequirements: ${b.key_requirements.join(', ')}\nObjections: ${b.previous_objections.join(', ')}\nCompetitors: ${b.competitors.join(', ')}\nDecision Makers: ${b.decision_makers.join(', ')}\nRecommended Focus: ${b.recommended_focus}\nRisk: ${b.risk}`;
    navigator.clipboard.writeText(text);
    alert('Briefing copied to clipboard!');
  }

  // ==================== POST-MEETING SUMMARY APPROVAL (SECTION 11, 23 & 28) ====================
  openPostMeetingSummaryModal() {
    const modal = document.getElementById('modal-post-meeting-summary');
    if (!modal) return;

    document.getElementById('edit-summary-discussion').value = 
      "Strategic alignment meeting with CTO Rohan Sharma reviewing enterprise architecture, 24-month TCO, and December rollout timeline.";
    document.getElementById('edit-summary-requirements').value = 
      "- Enterprise Security Platform with persistent memory\n- Deployment before December 2026 (Hard compliance milestone)\n- 24/7 Dedicated Support SLA";
    document.getElementById('edit-summary-objections').value = 
      "- Customer cited Competitor X 15% renewal discount.\n- Successfully reframed via 74% MTTR reduction and maintenance toil elimination.";
    document.getElementById('edit-summary-decisions').value = 
      "Customer confirmed agreement to justify ₹25L ARR upon proposal delivery with 24/7 support tier guaranteed in contract.";
    document.getElementById('edit-summary-actions').value = 
      "- Send updated proposal with 24/7 support tier to Rohan Sharma & CFO Anita Roy\n- Reserve deployment engineering sprint starting November 1";
    document.getElementById('edit-summary-commitments').value = 
      "- Sales Rep: Deliver updated proposal within 24 hours\n- Customer: Rohan Sharma to sponsor proposal at executive committee meeting";

    modal.style.display = 'flex';
  }

  async approvePostMeetingSummary() {
    const modal = document.getElementById('modal-post-meeting-summary');
    const btn = document.getElementById('btn-approve-summary-commit');
    if (btn) btn.innerHTML = '<span>⏳ Persisting to Memory...</span>';

    const payload = {
      meeting_type: "Executive Solution Review",
      stakeholder: "Rohan Sharma (CTO)",
      key_discussion: document.getElementById('edit-summary-discussion').value,
      customer_requirements: document.getElementById('edit-summary-requirements').value.split('\n').map(s => s.replace(/^[-*•✓]\s*/, '').trim()).filter(Boolean),
      objections: document.getElementById('edit-summary-objections').value.split('\n').map(s => s.replace(/^[-*•]\s*/, '').trim()).filter(Boolean),
      decisions: document.getElementById('edit-summary-decisions').value.split('\n').filter(Boolean),
      action_items: document.getElementById('edit-summary-actions').value.split('\n').map(s => s.replace(/^[-*•]\s*/, '').trim()).filter(Boolean),
      commitments: document.getElementById('edit-summary-commitments').value.split('\n').filter(Boolean)
    };

    try {
      const res = await fetch(`/api/deals/${this.currentDealId}/meeting-summary/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (btn) btn.innerHTML = '✓ Approved & Committed!';
      setTimeout(() => {
        if (modal) modal.style.display = 'none';
        if (btn) btn.innerHTML = '✓ Approve & Commit to Persistent Deal Memory';
      }, 800);

      // Reload memory, tasks, and right panel
      await this.loadDeals();
      await this.loadTasks();
      await this.loadMemoryBank();
      this.renderLiveDealMemorySidebar();

      alert(`✅ Deal Memory Updated!\nInteraction recorded into Hindsight Graph.\n${data.new_tasks_created.length} new follow-up tasks created in the Tasks Engine.`);
    } catch (e) {
      alert(`Error approving summary: ${e.message}`);
      if (btn) btn.innerHTML = '✓ Approve & Commit to Persistent Deal Memory';
    }
  }

  // ==================== CUSTOMERS (SECTION 17) ====================
  async loadCustomers() {
    const container = document.getElementById('customers-cards-container');
    if (!container) return;

    try {
      const res = await fetch('/api/customers');
      this.customers = await res.json();

      container.innerHTML = this.customers.map(c => `
        <div class="card" style="margin: 0; background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
            <div>
              <h3 style="font-size: 1.2rem; color: #fff;">${c.name}</h3>
              <div style="font-size: 0.8rem; color: var(--text-dim);">${c.industry}</div>
            </div>
            <span class="badge-pill primary">${c.tier}</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem; line-height: 1.4;">${c.summary}</p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.8rem; margin-bottom: 1rem;">
            <div><span style="color: var(--text-dim);">Revenue:</span> <strong>${c.annual_revenue}</strong></div>
            <div><span style="color: var(--text-dim);">Employees:</span> <strong>${c.employees.toLocaleString()}</strong></div>
            <div><span style="color: var(--text-dim);">HQ:</span> <strong>${c.headquarters}</strong></div>
            <div><span style="color: var(--text-dim);">Primary Contact:</span> <strong>${c.primary_contact}</strong></div>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 0.75rem;">
            <span style="font-size: 0.75rem; color: var(--text-dim);">Owner: ${c.account_owner}</span>
            <button class="action-btn small primary" onclick="app.selectCustomerDeal('${c.active_deals[0]}')">Open Deal Cockpit &rarr;</button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      console.warn('Failed to load customers:', e);
    }
  }

  selectCustomerDeal(dealId) {
    this.currentDealId = dealId;
    const headerSelect = document.getElementById('header-deal-selector');
    if (headerSelect) headerSelect.value = dealId;
    this.renderSidebarDeals();
    this.renderActiveDeal();
    this.renderLiveDealMemorySidebar();
    this.switchTab('live-call');
  }

  // ==================== TASKS (SECTION 17) ====================
  async loadTasks(filter = 'all') {
    const container = document.getElementById('tasks-list-container');
    if (!container) return;

    try {
      const res = await fetch('/api/tasks');
      this.tasks = await res.json();

      const filtered = filter === 'all' ? this.tasks : this.tasks.filter(t => t.status === filter);
      const badgeCount = document.getElementById('badge-tasks-count');
      if (badgeCount) badgeCount.innerText = this.tasks.length;

      container.innerHTML = filtered.map(t => `
        <div class="task-card-item" style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: 10px;">
          <div style="display: flex; flex-direction: column; gap: 4px; flex: 1;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="badge-pill ${t.badge_color === 'rose' ? 'danger' : 'warning'}">${t.priority}</span>
              <strong style="font-size: 0.95rem; color: #fff;">${t.title}</strong>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-muted); display: flex; gap: 12px;">
              <span>Account: <strong>${t.customer}</strong></span>
              <span>Due: <strong>${t.due_date}</strong></span>
              <span>Assignee: <strong>${t.assigned_to}</strong></span>
              <span>Source: <em>${t.source}</em></span>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <button class="action-btn small ${t.status === 'Completed' ? 'success' : 'secondary'} btn-cycle-task-status" onclick="app.cycleTaskStatus('${t.id}')">
              ${t.status}
            </button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      console.warn('Failed to load tasks:', e);
    }
  }

  async cycleTaskStatus(taskId) {
    const task = this.tasks.find(t => t.id === taskId);
    if (!task) return;
    const flow = ['Pending Approval', 'In Progress', 'Approved', 'Completed'];
    const nextStatus = flow[(flow.indexOf(task.status) + 1) % flow.length];

    try {
      await fetch(`/api/tasks/${taskId}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus })
      });
      task.status = nextStatus;
      this.loadTasks();
    } catch (e) {
      console.error('Failed to update task status:', e);
    }
  }

  async submitCreateTask() {
    const dealId = document.getElementById('task-create-deal').value;
    const title = document.getElementById('task-create-title').value.trim();
    const priority = document.getElementById('task-create-priority').value;
    const due = document.getElementById('task-create-due').value;

    if (!title) {
      alert('Please enter a task title');
      return;
    }

    const customer = dealId === 'deal-abc-security' ? 'ABC Technologies' : 'Nova Systems';
    try {
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deal_id: dealId,
          customer: customer,
          title: title,
          priority: priority,
          badge_color: priority === 'Critical' ? 'rose' : 'amber',
          due_date: due,
          assigned_to: 'Sarah Jenkins',
          source: 'Manual Task Entry'
        })
      });
      await res.json();
      document.getElementById('modal-create-task').style.display = 'none';
      document.getElementById('task-create-title').value = '';
      await this.loadTasks();
    } catch (e) {
      alert(`Error creating task: ${e.message}`);
    }
  }

  // ==================== DEALS PIPELINE & DETAILS (SECTION 17 & 18) ====================
  renderDealsPipeline() {
    const container = document.getElementById('deals-pipeline-container');
    if (!container) return;

    container.innerHTML = this.deals.map(d => `
      <div class="card" style="margin: 0; background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
          <div>
            <h3 style="font-size: 1.15rem; color: #fff;">${d.name}</h3>
            <div style="font-size: 0.82rem; color: var(--text-dim);">${d.company} &bull; ${d.industry}</div>
          </div>
          <span class="badge-pill primary">${d.stage}</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">${d.summary}</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.82rem; margin-bottom: 1rem; background: rgba(0,0,0,0.25); padding: 0.75rem; border-radius: 8px;">
          <div><span style="color: var(--text-dim);">Deal Target:</span> <strong style="color: var(--primary-light);">${d.deal_value_display || ('₹' + (d.arr_target || 300000).toLocaleString())}</strong></div>
          <div><span style="color: var(--text-dim);">Health Score:</span> <strong class="text-emerald">${d.health_score}%</strong></div>
          <div><span style="color: var(--text-dim);">Competitor:</span> <strong>${(d.competitors_mentioned || [{}])[0].name || 'Competitor X'}</strong></div>
          <div><span style="color: var(--text-dim);">Memory Bank:</span> <strong>${d.bank_id}</strong></div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 0.75rem;">
          <button class="action-btn small secondary" onclick="app.selectCustomerDeal('${d.id}')">View Cockpit</button>
          <button class="action-btn small primary" onclick="app.selectCustomerDeal('${d.id}')">▶ Start Live Call</button>
        </div>
      </div>
    `).join('');
  }

  renderDealDetails(subtab = 'overview') {
    const container = document.getElementById('details-subtab-content');
    if (!container) return;
    const deal = this.getActiveDeal();
    if (!deal) return;

    const titleElem = document.getElementById('deal-details-title');
    if (titleElem) titleElem.innerText = `${deal.company}: ${deal.name}`;
    const badgeElem = document.getElementById('deal-details-stage-badge');
    if (badgeElem) badgeElem.innerText = deal.stage;

    switch (subtab) {
      case 'overview':
        container.innerHTML = `
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;">
            <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: 10px;">
              <h4 style="color: var(--primary-light); margin-bottom: 0.5rem;">Executive Narrative</h4>
              <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5;">${deal.summary}</p>
            </div>
            <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: 10px;">
              <h4 style="color: var(--primary-light); margin-bottom: 0.5rem;">Commercial Terms</h4>
              <p style="font-size: 0.88rem; margin-bottom: 4px;"><strong>Deal Value:</strong> ${deal.deal_value_display || ('₹' + (deal.arr_target || 300000).toLocaleString())}</p>
              <p style="font-size: 0.88rem; margin-bottom: 4px;"><strong>Stage:</strong> ${deal.stage}</p>
              <p style="font-size: 0.88rem; margin-bottom: 4px;"><strong>Health Score:</strong> ${deal.health_score}%</p>
              <p style="font-size: 0.88rem;"><strong>Memory Bank:</strong> <code>${deal.bank_id}</code></p>
            </div>
          </div>
        `;
        break;
      case 'stakeholders':
        container.innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 10px;">
            ${(deal.stakeholders || []).map(s => `
              <div style="padding: 0.85rem 1rem; background: rgba(255,255,255,0.03); border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <strong>${s.name}</strong> &bull; <span style="color: var(--text-dim);">${s.role} (${s.department})</span>
                  <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;"><strong>Priority:</strong> ${s.priority || s.notes || 'Enterprise Scalability'}</div>
                </div>
                <span class="badge-pill warning">${s.influence}</span>
              </div>
            `).join('')}
          </div>
        `;
        break;
      case 'requirements':
        container.innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${(deal.requirements || []).map(r => `
              <div style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.25); border-radius: 8px; display: flex; justify-content: space-between;">
                <span>✓ <strong>${r.title}</strong></span>
                <span class="badge-pill success">${r.status}</span>
              </div>
            `).join('')}
          </div>
        `;
        break;
      case 'competitors':
        container.innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 10px;">
            ${(deal.competitors_mentioned || []).map(c => `
              <div style="padding: 0.85rem 1rem; background: rgba(244,63,94,0.06); border: 1px solid rgba(244,63,94,0.25); border-radius: 8px;">
                <div style="display: flex; justify-content: space-between;">
                  <strong style="color: #fda4af;">🥊 ${c.name}</strong>
                  <span class="badge-pill danger">Mentions: ${c.mentions_count || 4}</span>
                </div>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;"><strong>Customer Perception:</strong> ${c.customer_perception || 'Lower initial price'}</p>
                <p style="font-size: 0.85rem; color: #a7f3d0; margin-top: 2px;"><strong>Our Advantage:</strong> ${c.our_advantage || 'Autonomous self-healing memory with 74% MTTR reduction'}</p>
              </div>
            `).join('')}
          </div>
        `;
        break;
      default:
        container.innerHTML = `
          <div style="padding: 1.5rem; background: rgba(255,255,255,0.02); border-radius: 10px; color: var(--text-muted);">
            <h4>${subtab.toUpperCase()} Data View</h4>
            <p style="font-size: 0.88rem; margin-top: 6px;">Persistent telemetry for <strong>${deal.name}</strong> stored in memory bank <code>${deal.bank_id}</code>.</p>
          </div>
        `;
    }
  }

  // ==================== LOKI AI OPERATIONAL INTELLIGENCE ====================

  async loadLokiCommands() {
    try {
      const res = await fetch('/api/loki/commands');
      if (res.ok) {
        this.lokiCommands = await res.json();
      }
    } catch (err) {
      console.warn('Could not load LOKI commands:', err);
    }
  }

  toggleLokiWorkspace(forceState) {
    const panel = document.getElementById('loki-workspace-panel');
    if (!panel) return;

    this.isLokiOpen = forceState !== undefined ? forceState : !this.isLokiOpen;
    panel.style.display = this.isLokiOpen ? 'flex' : 'none';

    if (this.isLokiOpen) {
      const input = document.getElementById('loki-user-input');
      if (input) input.focus();
      const dealLabel = document.getElementById('loki-active-deal-label');
      if (dealLabel) {
        const curDeal = this.deals.find(d => d.id === this.currentDealId);
        dealLabel.innerText = curDeal?.company || curDeal?.name || 'ABC Technologies';
      }
    }
  }

  toggleLokiExpand() {
    const panel = document.getElementById('loki-workspace-panel');
    if (!panel) return;
    this.isLokiExpanded = !this.isLokiExpanded;
    panel.classList.toggle('expanded', this.isLokiExpanded);
  }

  setLokiMode(mode) {
    this.lokiMode = mode;
    document.querySelectorAll('.loki-mode-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.mode === mode);
    });
    this.showToast(`LOKI Mode: ${mode.toUpperCase()}`);
  }

  async sendLokiQuery(customQuery) {
    const input = document.getElementById('loki-user-input');
    const query = customQuery || (input ? input.value.trim() : '');
    if (!query) return;

    if (input && !customQuery) input.value = '';
    const dropdown = document.getElementById('loki-slash-dropdown');
    if (dropdown) dropdown.style.display = 'none';

    // 1. Append User Message
    this.appendLokiUserMessage(query);

    // 2. Append Thinking Indicator
    const thinkingId = this.appendLokiThinkingBubble();

    try {
      const res = await fetch('/api/loki/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query,
          deal_id: this.currentDealId,
          mode: this.lokiMode,
          context: this.lokiHistory.slice(-6)
        })
      });

      const thinkingEl = document.getElementById(thinkingId);
      if (thinkingEl) thinkingEl.remove();

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      this.appendLokiAssistantMessage(data);

      this.lokiHistory.push({ role: 'user', content: query });
      this.lokiHistory.push({ role: 'assistant', content: data.answer });
    } catch (err) {
      console.error('LOKI query error:', err);
      const thinkingEl = document.getElementById(thinkingId);
      if (thinkingEl) thinkingEl.remove();

      this.appendLokiAssistantMessage({
        answer: "I apologize, but I encountered an error communicating with the intelligence engine.",
        why: err.message,
        evidence: ["LOKI Gateway Error"],
        recommended_action: "Ensure server is healthy or retry query."
      });
    }
  }

  appendLokiUserMessage(text) {
    const feed = document.getElementById('loki-messages-feed');
    if (!feed) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msg = document.createElement('div');
    msg.className = 'loki-msg-bubble user';
    msg.innerHTML = `
      <div class="loki-msg-header">
        <span class="loki-sender-tag" style="color: #fff;">You</span>
        <span class="loki-msg-time" style="color: rgba(255,255,255,0.7);">${timeStr}</span>
      </div>
      <div class="loki-msg-body">${this.escapeHtml(text)}</div>
    `;
    feed.appendChild(msg);
    feed.scrollTop = feed.scrollHeight;
  }

  appendLokiThinkingBubble() {
    const feed = document.getElementById('loki-messages-feed');
    if (!feed) return null;

    const id = `loki-thinking-${Date.now()}`;
    const msg = document.createElement('div');
    msg.id = id;
    msg.className = 'loki-msg-bubble assistant';
    msg.style.opacity = '0.7';
    msg.innerHTML = `
      <div class="loki-msg-header">
        <span class="loki-sender-tag">🧠 LOKI</span>
        <span class="loki-msg-time">Analyzing deal memory...</span>
      </div>
      <div class="loki-msg-body" style="display: flex; align-items: center; gap: 8px;">
        <span class="pulse-dot" style="display: inline-block;"></span>
        <span>Retrieving cross-tier evidence & synthesizing next actions...</span>
      </div>
    `;
    feed.appendChild(msg);
    feed.scrollTop = feed.scrollHeight;
    return id;
  }

  appendLokiAssistantMessage(data) {
    const feed = document.getElementById('loki-messages-feed');
    if (!feed) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msg = document.createElement('div');
    msg.className = 'loki-msg-bubble assistant';

    let whyBlock = '';
    if (data.why) {
      whyBlock = `
        <div class="loki-section-block why">
          <div class="loki-block-title why">🧠 WHY (Underlying Reasoning)</div>
          <div style="font-size: 0.85rem; color: #cffafe; line-height: 1.45;">${this.renderMarkdown(data.why)}</div>
        </div>
      `;
    }

    let evidenceBlock = '';
    if (data.evidence && data.evidence.length > 0) {
      evidenceBlock = `
        <div class="loki-section-block evidence">
          <div class="loki-block-title evidence">📑 EVIDENCE (Verified Sources)</div>
          <ul class="loki-evidence-list">
            ${data.evidence.map(e => `<li>${this.renderMarkdown(e)}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    let actionBlock = '';
    if (data.recommended_action) {
      actionBlock = `
        <div class="loki-section-block action">
          <div class="loki-block-title action">🎯 RECOMMENDED NEXT ACTION</div>
          <div style="font-size: 0.85rem; color: #a7f3d0; line-height: 1.45;">${this.renderMarkdown(data.recommended_action)}</div>
          <div class="loki-interactive-row">
            <button class="loki-act-btn primary btn-loki-approve-action">✓ Approve & Adopt</button>
            <button class="loki-act-btn btn-loki-create-task">📋 Create Task</button>
          </div>
        </div>
      `;
    }

    let formattedContentBlock = '';
    if (data.formatted_content) {
      formattedContentBlock = `
        <div style="margin-top: 0.75rem; padding: 0.75rem 1rem; background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: 8px; font-size: 0.85rem; line-height: 1.5; color: var(--text-main);">
          ${this.renderMarkdown(data.formatted_content)}
        </div>
      `;
    }

    let quickActionsBlock = '';
    if (data.quick_actions && data.quick_actions.length > 0) {
      quickActionsBlock = `
        <div class="loki-interactive-row" style="margin-top: 0.75rem;">
          ${data.quick_actions.map(qa => `<button class="loki-chip-btn loki-sub-action" data-action="${qa}">${qa}</button>`).join('')}
        </div>
      `;
    }

    msg.innerHTML = `
      <div class="loki-msg-header">
        <span class="loki-sender-tag">🧠 LOKI</span>
        <span class="loki-msg-time">${data.external_intelligence ? '🌐 External Intelligence' : 'Verified Deal Intelligence'} &bull; ${timeStr}</span>
      </div>
      <div class="loki-msg-body">
        <div style="font-size: 0.92rem; color: #fff;">${this.renderMarkdown(data.answer)}</div>
        <div class="loki-structured-box">
          ${whyBlock}
          ${evidenceBlock}
          ${formattedContentBlock}
          ${actionBlock}
        </div>
        ${quickActionsBlock}
      </div>
    `;

    // Bind sub-action buttons
    msg.querySelectorAll('.loki-sub-action').forEach(btn => {
      btn.addEventListener('click', () => {
        this.executeLokiQuickAction(btn.dataset.action);
      });
    });

    msg.querySelector('.btn-loki-approve-action')?.addEventListener('click', (e) => {
      e.target.innerHTML = '✓ Approved & Adopted';
      e.target.style.background = 'var(--emerald)';
      this.showToast('LOKI action approved and added to deal record.');
    });

    msg.querySelector('.btn-loki-create-task')?.addEventListener('click', () => {
      this.createTaskFromLoki(data.recommended_action || data.answer);
    });

    feed.appendChild(msg);
    feed.scrollTop = feed.scrollHeight;
  }

  executeLokiQuickAction(action) {
    if (!action) return;

    if (action.startsWith('/')) {
      this.sendLokiQuery(action);
      return;
    }

    switch (action.toLowerCase()) {
      case 'analyze pricing':
        this.sendLokiQuery('Analyze the pricing history and similar deals for this account.');
        break;
      case 'compare similar deals':
        this.sendLokiQuery('/history');
        break;
      case 'prepare follow-up':
        this.sendLokiQuery('Prepare a strategic follow-up email draft addressing pricing and security.');
        break;
      case 'show stakeholders':
        this.sendLokiQuery('/stakeholders');
        break;
      case 'run deal x-ray':
        this.openDealXRay();
        break;
      case 'loki connect':
        this.openLokiConnect();
        break;
      case 'executive brief':
        this.openLokiBrief();
        break;
      default:
        this.sendLokiQuery(action);
    }
  }

  async askLokiWhy(dealId, topic, text) {
    this.toggleLokiWorkspace(true);
    this.appendLokiUserMessage(`Why was "${topic}" flagged?`);
    const thinkingId = this.appendLokiThinkingBubble();

    try {
      const res = await fetch('/api/loki/why', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deal_id: dealId || this.currentDealId,
          insight_topic: topic || '',
          text: text || ''
        })
      });

      const thinkingEl = document.getElementById(thinkingId);
      if (thinkingEl) thinkingEl.remove();

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      this.appendLokiAssistantMessage(data);
    } catch (err) {
      console.error('Error in askLokiWhy:', err);
      const thinkingEl = document.getElementById(thinkingId);
      if (thinkingEl) thinkingEl.remove();
      this.appendLokiAssistantMessage({
        answer: `Could not retrieve root cause for: ${topic}`,
        why: err.message,
        evidence: ["LOKI Why Engine Error"]
      });
    }
  }

  async openLokiConnect(dealId) {
    const modal = document.getElementById('modal-loki-connect');
    if (!modal) return;
    modal.style.display = 'flex';

    const chainContainer = document.getElementById('loki-connect-chain-nodes');
    if (chainContainer) chainContainer.innerHTML = '<div style="color: var(--text-dim); padding: 1.5rem;">Mapping causal deal links...</div>';

    try {
      const res = await fetch(`/api/loki/connect/${dealId || this.currentDealId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (chainContainer) {
        chainContainer.innerHTML = '';
        data.nodes.forEach((node, idx) => {
          const nodeEl = document.createElement('div');
          nodeEl.className = `loki-chain-node ${idx === 0 ? 'selected' : ''}`;
          nodeEl.dataset.nodeId = node.id;
          nodeEl.innerHTML = `
            <div class="loki-node-top">
              <span class="loki-node-step">STEP ${node.step} OF ${data.nodes.length}</span>
              <span class="loki-node-badge ${node.type}">${node.badge}</span>
            </div>
            <div class="loki-node-title">${node.title}</div>
            <div class="loki-node-summary">${node.summary}</div>
          `;

          nodeEl.addEventListener('click', () => {
            chainContainer.querySelectorAll('.loki-chain-node').forEach(n => n.classList.remove('selected'));
            nodeEl.classList.add('selected');
            this.inspectLokiConnectNode(node);
          });

          chainContainer.appendChild(nodeEl);

          if (idx < data.nodes.length - 1) {
            const arrowEl = document.createElement('div');
            arrowEl.className = 'loki-node-arrow';
            arrowEl.innerText = '↓';
            chainContainer.appendChild(arrowEl);
          }
        });

        if (data.nodes.length > 0) {
          this.inspectLokiConnectNode(data.nodes[0]);
        }
      }
    } catch (err) {
      console.error('Error loading LOKI Connect:', err);
      if (chainContainer) chainContainer.innerHTML = `<div style="color: var(--rose); padding: 1rem;">Failed to load connect graph: ${err.message}</div>`;
    }
  }

  inspectLokiConnectNode(node) {
    const titleEl = document.getElementById('loki-insp-title');
    const catEl = document.getElementById('loki-insp-category');
    const srcEl = document.getElementById('loki-insp-source');
    const factEl = document.getElementById('loki-insp-fact');
    const detailsEl = document.getElementById('loki-insp-details');

    if (titleEl) titleEl.innerText = `${node.badge}: ${node.title}`;
    if (catEl) catEl.innerText = `Step ${node.step} — ${node.type.toUpperCase()}`;
    if (srcEl) srcEl.innerText = node.evidence_source || 'Verified Deal Record';
    if (factEl) factEl.innerText = `[STORED FACT]: ${node.summary}`;
    if (detailsEl) detailsEl.innerText = node.details || 'No additional details.';
  }

  async openDealXRay(dealId) {
    const modal = document.getElementById('modal-deal-xray');
    if (!modal) return;
    modal.style.display = 'flex';

    const grid = document.getElementById('deal-xray-grid');
    if (grid) grid.innerHTML = '<div style="color: var(--text-dim); padding: 2rem;">Scanning all 18 dimensions across 4 persistent memory tiers...</div>';

    try {
      const res = await fetch(`/api/loki/xray/${dealId || this.currentDealId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      const custLabel = document.getElementById('xray-customer-label');
      if (custLabel) custLabel.innerText = data.customer || 'ABC Technologies';
      const healthPill = document.getElementById('xray-health-pill');
      if (healthPill) healthPill.innerText = `Deal Health: ${data.deal_health}/100`;
      const arrLabel = document.getElementById('xray-arr-label');
      if (arrLabel) arrLabel.innerText = data.deal_value || '₹25L ($300k)';

      if (grid) {
        grid.innerHTML = data.xray_sections.map(sec => `
          <div class="xray-dimension-card">
            <div class="xray-dim-top">
              <span class="xray-dim-name">${sec.dimension}</span>
              <span class="xray-dim-badge ${sec.badge || 'emerald'}">${sec.status}</span>
            </div>
            <div class="xray-dim-summary">${sec.summary}</div>
          </div>
        `).join('');
      }
    } catch (err) {
      console.error('Error loading Deal X-Ray:', err);
      if (grid) grid.innerHTML = `<div style="color: var(--rose); padding: 1.5rem;">Failed to run X-Ray: ${err.message}</div>`;
    }
  }

  async openLokiBrief(dealId) {
    const modal = document.getElementById('modal-loki-brief');
    if (!modal) return;
    modal.style.display = 'flex';

    const contentEl = document.getElementById('loki-brief-content');
    if (contentEl) contentEl.innerText = 'Synthesizing executive brief for leadership...';

    try {
      const res = await fetch(`/api/loki/brief/${dealId || this.currentDealId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (contentEl) contentEl.innerText = data.formatted_content || data.answer;
    } catch (err) {
      console.error('Error loading LOKI Brief:', err);
      if (contentEl) contentEl.innerText = `Failed to generate executive brief: ${err.message}`;
    }
  }

  async createTaskFromLoki(taskTitle) {
    try {
      const curDeal = this.deals.find(d => d.id === this.currentDealId) || {};
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deal_id: this.currentDealId,
          customer: curDeal.company || curDeal.name || 'ABC Technologies',
          title: taskTitle.slice(0, 120),
          priority: 'Important',
          badge_color: 'amber',
          due_date: 'Tomorrow',
          assigned_to: 'Sarah Jenkins',
          source: 'LOKI Intelligence Action'
        })
      });
      if (res.ok) {
        this.showToast('Task successfully created and assigned!');
        this.loadTasks();
      }
    } catch (err) {
      console.error('Error creating task from LOKI:', err);
    }
  }

  renderMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color: #67e8f9; text-decoration: underline;">$1</a>')
      .replace(/\n/g, '<br>');
  }

  escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

// Initialize on DOMContentLoaded and expose to window.app & window.nexus
document.addEventListener('DOMContentLoaded', () => {
  window.nexus = new NexusApp();
  window.app = window.nexus;
});
