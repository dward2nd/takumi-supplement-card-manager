// Vanilla JS application logic for the POC.
// All state is in-memory and derived from window.POC_DATA (see data.js).
// No build step, no framework, no network calls.

(function () {
  "use strict";

  const data = window.POC_DATA;

  // ---- lookup helpers -------------------------------------------------------

  const byId = (rows) => Object.fromEntries(rows.map((r) => [r.id, r]));
  const idx = {
    people:          byId(data.people),
    primaryAccounts: byId(data.primaryAccounts),
    cards:           byId(data.cards),
    issuers:         byId(data.issuers),
    networks:        byId(data.networks),
    cardProducts:    byId(data.cardProducts),
    categories:      byId(data.categories),
  };

  const personLabel  = (id) => {
    const p = idx.people[id];
    return p ? `${p.displayName} (${p.notionName})` : "—";
  };
  const productLabel = (cardId) => {
    const card = idx.cards[cardId];
    if (!card) return "—";
    const product = idx.cardProducts[card.productId];
    return product ? product.name : "—";
  };
  const issuerName   = (id) => (idx.issuers[id]   ? idx.issuers[id].name   : "—");
  const networkName  = (id) => (idx.networks[id]  ? idx.networks[id].name  : "—");
  const categoryName = (id) => (idx.categories[id] ? idx.categories[id].name : "—");

  const fmtBaht = (n) =>
    typeof n === "number"
      ? n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : "—";

  const rewardLabel = (rule) => {
    if (rule.type === "multiplier") return `×${rule.value}`;
    if (rule.type === "cashback")   return `${rule.percent}% cb`;
    return JSON.stringify(rule);
  };

  // ---- filtering ------------------------------------------------------------

  const cardsForPerson = (personId) =>
    data.cards.filter((c) => c.holderPersonId === personId);

  const transactionsForPerson = (personId) => {
    const cardIds = new Set(cardsForPerson(personId).map((c) => c.id));
    return data.transactions
      .filter((t) => cardIds.has(t.cardId))
      .sort((a, b) => b.swipedAt.localeCompare(a.swipedAt));
  };

  const billsForPerson = (personId) => {
    const cardIds = new Set(cardsForPerson(personId).map((c) => c.id));
    return data.bills
      .filter((b) => cardIds.has(b.cardId))
      .sort((a, b) => b.cycleDate.localeCompare(a.cycleDate));
  };

  // ---- rendering ------------------------------------------------------------

  const el = (tag, attrs = {}, children = []) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k === "html") node.innerHTML = v;
      else node.setAttribute(k, v);
    }
    for (const child of [].concat(children)) {
      if (child == null) continue;
      node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    }
    return node;
  };

  const renderCards = (personId) => {
    const tbody = document.querySelector('[data-rows="cards"]');
    tbody.replaceChildren();
    const rows = cardsForPerson(personId);
    if (rows.length === 0) {
      tbody.appendChild(el("tr", {}, el("td", { colspan: "6", class: "empty-row" }, "No cards.")));
      return;
    }
    for (const card of rows) {
      const product = idx.cardProducts[card.productId];
      const pa      = idx.primaryAccounts[card.primaryAccountId];
      tbody.appendChild(
        el("tr", {}, [
          el("td", {}, product ? product.name : "—"),
          el("td", {}, issuerName(product?.issuerId)),
          el("td", {}, networkName(product?.networkId)),
          el("td", {}, card.premiumTier || "—"),
          el("td", { class: "num" }, fmtBaht(card.allocatedLimit)),
          el("td", {}, pa ? personLabel(pa.holderPersonId) : "—"),
        ])
      );
    }
  };

  const renderTransactions = (personId) => {
    const tbody = document.querySelector('[data-rows="transactions"]');
    tbody.replaceChildren();
    const rows = transactionsForPerson(personId);
    if (rows.length === 0) {
      tbody.appendChild(el("tr", {}, el("td", { colspan: "7", class: "empty-row" }, "No transactions.")));
      return;
    }
    for (const tx of rows) {
      const rewardChips = el("span", { class: "chips" });
      for (const rule of tx.rewardRules || []) {
        rewardChips.appendChild(el("span", { class: `chip chip--${rule.type}` }, rewardLabel(rule)));
      }
      tbody.appendChild(
        el("tr", {}, [
          el("td", {}, tx.swipedAt),
          el("td", {}, productLabel(tx.cardId)),
          el("td", {}, tx.categoryId ? categoryName(tx.categoryId) : "—"),
          el("td", {}, tx.note || "—"),
          el("td", { class: "num" }, fmtBaht(tx.amountBaht)),
          el("td", {}, rewardChips),
          el("td", {}, el("span", { class: `status status--${tx.status}` }, tx.status)),
        ])
      );
    }
  };

  const renderBills = (personId) => {
    const tbody = document.querySelector('[data-rows="bills"]');
    const empty = document.querySelector('[data-empty="bills"]');
    tbody.replaceChildren();
    const rows = billsForPerson(personId);
    empty.hidden = rows.length > 0;
    for (const bill of rows) {
      tbody.appendChild(
        el("tr", {}, [
          el("td", {}, bill.cycleDate),
          el("td", {}, productLabel(bill.cardId)),
          el("td", { class: "num" }, fmtBaht(bill.amountBaht)),
          el("td", {}, el("span", { class: `pill pill--${bill.paid ? "paid" : "unpaid"}` }, bill.paid ? "paid" : "unpaid")),
          el("td", {}, bill.paymentEvidence || "—"),
        ])
      );
    }
  };

  const renderSummary = (personId) => {
    const cards = cardsForPerson(personId);
    const txs   = transactionsForPerson(personId);
    const outstanding = billsForPerson(personId)
      .filter((b) => !b.paid)
      .reduce((sum, b) => sum + b.amountBaht, 0);

    document.querySelector('[data-summary="card-count"]').textContent  = String(cards.length);
    document.querySelector('[data-summary="tx-count"]').textContent    = String(txs.length);
    document.querySelector('[data-summary="outstanding"]').textContent = `฿${fmtBaht(outstanding)}`;
  };

  // ---- tab + holder switching ----------------------------------------------

  const state = { personId: "p-takumi", tab: "cards" };

  const applyTabVisibility = () => {
    const person = idx.people[state.personId];
    const isPrimary = person && person.role === "primary";

    // Primary holders (Takumi) have no Bills view — matches Notion-as-built.
    const billsTabBtn = document.querySelector('.tab[data-tab="bills"]');
    billsTabBtn.hidden = isPrimary;

    // If the bills tab was active but is now hidden, fall back to cards.
    if (isPrimary && state.tab === "bills") state.tab = "cards";

    for (const btn of document.querySelectorAll(".tab")) {
      btn.setAttribute("aria-selected", btn.dataset.tab === state.tab ? "true" : "false");
    }
    for (const panel of document.querySelectorAll(".panel")) {
      panel.hidden = panel.dataset.panel !== state.tab;
    }
  };

  const renderAll = () => {
    applyTabVisibility();
    renderSummary(state.personId);
    renderCards(state.personId);
    renderTransactions(state.personId);
    renderBills(state.personId);
  };

  const wireEvents = () => {
    for (const btn of document.querySelectorAll(".holder-btn")) {
      btn.addEventListener("click", () => {
        state.personId = btn.dataset.personId;
        for (const b of document.querySelectorAll(".holder-btn")) {
          b.setAttribute("aria-selected", b === btn ? "true" : "false");
        }
        renderAll();
      });
    }

    for (const btn of document.querySelectorAll(".tab")) {
      btn.addEventListener("click", () => {
        if (btn.hidden) return;
        state.tab = btn.dataset.tab;
        applyTabVisibility();
      });
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    wireEvents();
    renderAll();
  });
})();
