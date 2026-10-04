(() => {
  "use strict";
  const guide = JSON.parse(document.getElementById("guide-data").textContent);
  const projects = guide.projects;
  const byId = new Map(projects.map(project => [project.id, project]));
  const detail = document.getElementById("project-detail");
  const search = document.getElementById("project-search");
  const filter = document.getElementById("status-filter");
  const library = document.getElementById("full-review");
  const labels = {idea:"Idea", evidence:"Evidence", scenarios:"Scenarios", controls:"Controls"};
  let selected = projects[0].id;
  let visible = projects;
  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  function badge(assessment) {
    const node = el("span", "badge " + assessment.status);
    const dot = el("span", "dot"); dot.setAttribute("aria-hidden", "true");
    node.append(dot, document.createTextNode(assessment.label));
    return node;
  }
  function listSection(name, heading, values) {
    const section = el("section", "detail-section " + name);
    const title = el("h3");
    const dot = el("span", "section-dot"); dot.setAttribute("aria-hidden", "true");
    title.append(dot, document.createTextNode(heading));
    const list = el("ul"); values.forEach(value => list.append(el("li", "", value)));
    section.append(title, list); return section;
  }
  function showDetail(project) {
    detail.replaceChildren();
    if (!project) {
      detail.append(el("p", "detail-empty", "No project matches these filters. Clear the filters to return to the ten-project overview."));
      return;
    }
    const top = el("div", "detail-topline");
    top.append(el("p", "eyebrow", "THE PROJECT, UNPACKED"), el("span", "detail-number", String(projects.indexOf(project) + 1).padStart(2, "0") + " / 10"));
    const title = el("h2", "", project.name); title.id = "selected-project-title";
    detail.setAttribute("aria-labelledby", title.id);
    detail.append(top, title, el("p", "question", project.question), el("p", "verdict", project.verdict));
    const dimensions = el("div", "dimension-notes");
    Object.entries(labels).forEach(([key, label]) => {
      const assessment = project.assessments[key];
      const card = el("div", "dimension");
      card.append(el("span", "dimension-label", label), badge(assessment), el("p", "", assessment.why));
      dimensions.append(card);
    });
    detail.append(dimensions);
    const columns = el("div", "detail-columns");
    columns.append(listSection("works", "What works", project.works), listSection("limits", "Limits", project.limits), listSection("fixes", "Fix next", project.fixes));
    detail.append(columns);
    const header = el("div", "options-header"); header.append(el("h3", "", "Three ways forward"));
    const options = el("div", "options");
    project.options.forEach(option => {
      const card = el("article", "option-card" + (option.recommended ? " recommended" : ""));
      const heading = el("span", "option-title", option.label);
      if (option.recommended) heading.append(el("span", "recommendation", "Recommended"));
      card.append(heading, el("span", "option-detail", option.detail));
      options.append(card);
    });
    detail.append(header, options);
    detail.append(el("p", "evidence-note", project.evidence_note));
    const links = el("div", "review-links");
    project.review_ids.forEach((id, index) => {
      const link = el("a", "", project.review_ids.length === 1 ? "Read the full assessment →" : "Full assessment " + (index + 1) + " →");
      link.href = "#" + id; links.append(link);
    }); detail.append(links);
  }
  function setSelection(id, updateHash = true) {
    if (!byId.has(id) || !visible.some(project => project.id === id)) return;
    selected = id;
    document.querySelectorAll("tr[data-project]").forEach(row => {
      const active = row.dataset.project === id;
      row.classList.toggle("selected", active);
      row.querySelector("button").setAttribute("aria-pressed", String(active));
    });
    showDetail(byId.get(id));
    if (updateHash) history.replaceState(null, "", "#project-" + id);
  }
  function applyFilters(updateHash = true) {
    const query = search.value.trim().toLocaleLowerCase();
    visible = projects.filter(project => {
      const matchText = !query || JSON.stringify(project).toLocaleLowerCase().includes(query);
      const matchStatus = filter.value === "all" || Object.values(project.assessments).some(value => value.status === filter.value);
      return matchText && matchStatus;
    });
    const ids = new Set(visible.map(project => project.id));
    document.querySelectorAll("tr[data-project]").forEach(row => { row.hidden = !ids.has(row.dataset.project); });
    document.getElementById("project-count").textContent = visible.length + " of " + projects.length + " projects";
    document.getElementById("empty-results").hidden = visible.length > 0;
    if (visible.length) setSelection(ids.has(selected) ? selected : visible[0].id, updateHash);
    else { detail.removeAttribute("aria-labelledby"); showDetail(null); }
  }
  function reset(updateHash = true) { search.value = ""; filter.value = "all"; applyFilters(updateHash); }
  function revealHash(scroll = true) {
    let hash;
    try { hash = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const projectId = hash.startsWith("project-") ? hash.slice(8) : hash;
    if (byId.has(projectId)) {
      if (!visible.some(project => project.id === projectId)) reset(false);
      setSelection(projectId, false); return;
    }
    if (!hash) return;
    const target = document.getElementById(hash);
    if (target && library.contains(target)) {
      library.open = true;
      let node = target;
      while (node && node !== library) {
        if (node.tagName === "DETAILS") node.open = true;
        node = node.parentElement;
      }
      if (scroll) requestAnimationFrame(() => target.scrollIntoView({block:"start"}));
    } else if (target === library) { library.open = true; if (scroll) library.scrollIntoView({block:"start"}); }
  }
  document.getElementById("project-rows").addEventListener("click", event => {
    const row = event.target.closest("tr[data-project]"); if (row) setSelection(row.dataset.project);
  });
  document.getElementById("open-full").addEventListener("click", () => { library.open = true; history.replaceState(null, "", "#full-review"); library.scrollIntoView({block:"start"}); library.querySelector("summary").focus({preventScroll:true}); });
  document.getElementById("reset-filters").addEventListener("click", () => reset());
  document.querySelectorAll("[data-reset]").forEach(button => button.addEventListener("click", () => reset()));
  search.addEventListener("input", () => applyFilters()); filter.addEventListener("change", () => applyFilters());
  window.addEventListener("hashchange", () => revealHash());
  document.addEventListener("click", event => {
    const link = event.target.closest('a[href^="#"]');
    if (link && location.hash === link.hash) revealHash();
  });
  applyFilters(false); revealHash();
})();
