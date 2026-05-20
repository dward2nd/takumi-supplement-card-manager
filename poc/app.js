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
    aliases:         byId(data.aliases || []),
  };

  const cardQuotas    = data.cardQuotas    || [];
  const accountQuotas = data.accountQuotas || [];

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

  // Aggregate balance + shared quotas on a PrimaryAccount, including the slice
  // visible to a given holder. Supplement holders see only "their card's" share
  // of the cards list but the full account-level outstanding and quota progress
  // — that's the cross-holder visibility rule from product-shape.md.
  const accountsForPerson = (personId) => {
    const ownCards = cardsForPerson(personId);
    const accountIds = new Set(ownCards.map((c) => c.primaryAccountId));
    return data.primaryAccounts
      .filter((pa) => accountIds.has(pa.id))
      .map((pa) => {
        const allCards = data.cards.filter((c) => c.primaryAccountId === pa.id);
        const allCardIds = new Set(allCards.map((c) => c.id));
        const outstanding = data.transactions
          .filter((t) => allCardIds.has(t.cardId) && (t.status === "processed" || t.status === "pending"))
          .reduce((sum, t) => sum + t.amountBaht, 0);
        const accountQuota = accountQuotas.find((q) => q.primaryAccountId === pa.id);
        return { primaryAccount: pa, allCards, outstanding, accountQuota };
      });
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
      tbody.appendChild(el("tr", {}, el("td", { colspan: "10", class: "empty-row" }, "No transactions.")));
      return;
    }
    for (const tx of rows) {
      const rewardChips = el("span", { class: "chips" });
      for (const rule of tx.rewardRules || []) {
        rewardChips.appendChild(el("span", { class: `chip chip--${rule.type}` }, rewardLabel(rule)));
      }
      if (tx.aliasMatchedId && idx.aliases[tx.aliasMatchedId]) {
        rewardChips.appendChild(el("span", { class: "chip chip--alias", title: "Matched alias rule" }, `↪ ${idx.aliases[tx.aliasMatchedId].canonicalMerchant}`));
      }
      if (tx.refundOfTxId) {
        rewardChips.appendChild(el("span", { class: "chip chip--adjustment", title: `Refund of ${tx.refundOfTxId}` }, "refund row"));
      }
      const isAdjustment = (tx.amountBaht || 0) < 0;
      const trClass = isAdjustment ? "tx-row tx-row--adjustment" : "tx-row";
      tbody.appendChild(
        el("tr", { class: trClass }, [
          el("td", {}, tx.swipedAt),
          el("td", {}, tx.processedDate || "—"),
          el("td", {}, tx.billCycleDate || "—"),
          el("td", {}, tx.dueDate || "—"),
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

  // ---- progress bar ---------------------------------------------------------

  const progressBar = (used, cap, label) => {
    const pct = Math.max(0, Math.min(100, (used / cap) * 100));
    return el("div", { class: "progress" }, [
      el("div", { class: "progress__label" }, [
        el("span", {}, label),
        el("span", { class: "progress__num" }, `฿${fmtBaht(used)} / ฿${fmtBaht(cap)} (${pct.toFixed(0)}%)`),
      ]),
      el("div", { class: "progress__track" }, [
        el("div", { class: `progress__fill ${pct >= 80 ? "progress__fill--high" : ""}`, style: `width: ${pct}%` }),
      ]),
    ]);
  };

  const renderAccounts = (personId) => {
    const wrap = document.querySelector('[data-rows="accounts"]');
    wrap.replaceChildren();
    const accounts = accountsForPerson(personId);
    if (accounts.length === 0) {
      wrap.appendChild(el("p", { class: "empty-state" }, "No primary accounts."));
      return;
    }
    for (const { primaryAccount, allCards, outstanding, accountQuota } of accounts) {
      const issuer = idx.issuers[primaryAccount.issuerId];
      const card = el("article", { class: "account" }, [
        el("header", { class: "account__head" }, [
          el("h3", { class: "account__title" }, issuer ? issuer.name : "—"),
          el("span", { class: "account__limit" }, `credit limit: ฿${fmtBaht(primaryAccount.creditLimit)}`),
        ]),
        el("div", { class: "account__stats" }, [
          el("div", {}, [
            el("span", { class: "stat__label" }, "Outstanding (processed + pending)"),
            el("span", { class: "stat__value" }, `฿${fmtBaht(outstanding)}`),
          ]),
          el("div", {}, [
            el("span", { class: "stat__label" }, "Cards on this account"),
            el("span", { class: "stat__value" }, String(allCards.length)),
          ]),
        ]),
      ]);
      if (accountQuota) {
        card.appendChild(progressBar(accountQuota.usedThisCycleBaht, accountQuota.capBaht, accountQuota.label));
      }
      // Per-card quotas attached to cards on this account
      const localCardQuotas = cardQuotas.filter((q) => allCards.some((c) => c.id === q.cardId));
      for (const q of localCardQuotas) {
        const c = idx.cards[q.cardId];
        card.appendChild(progressBar(q.usedThisCycleBaht, q.capBaht, `${q.label} — ${c.nickname}`));
      }
      wrap.appendChild(card);
    }
  };

  const renderBills = (personId) => {
    const tbody = document.querySelector('[data-rows="bills"]');
    const empty = document.querySelector('[data-empty="bills"]');
    tbody.replaceChildren();
    const rows = billsForPerson(personId);
    empty.hidden = rows.length > 0;
    for (const bill of rows) {
      const card    = idx.cards[bill.cardId];
      const product = card ? idx.cardProducts[card.productId] : null;
      // Reconciliation: sum all transactions for this card on this billCycleDate,
      // including adjustment rows (negative). Cross-cycle refund adjustments contribute
      // to the cycle their billCycleDate names, which is what we want.
      const txSum = data.transactions
        .filter((t) => t.cardId === bill.cardId && t.billCycleDate === bill.cycleDate)
        .reduce((s, t) => s + (t.amountBaht || 0), 0);
      const delta = +(txSum - bill.amountBaht).toFixed(2);
      const reconCell = delta === 0
        ? el("span", { class: "recon recon--ok",   title: `tx sum ฿${fmtBaht(txSum)} matches bill` }, "✓ matches")
        : el("span", { class: "recon recon--diff", title: `tx sum ฿${fmtBaht(txSum)} vs bill ฿${fmtBaht(bill.amountBaht)}` }, `⚠ Δ ${delta > 0 ? "+" : ""}${fmtBaht(delta)}`);

      const paidPill = el("button", {
        type: "button",
        class: `pill pill--${bill.paid ? "paid" : "unpaid"} pill--clickable`,
        title: "Click to toggle paid (demo only — in-memory)",
        "data-toggle-paid": bill.id,
      }, bill.paid ? "paid" : "unpaid");

      tbody.appendChild(
        el("tr", {}, [
          el("td", {}, bill.cycleDate),
          el("td", {}, productLabel(bill.cardId)),
          el("td", {}, networkName(product?.networkId)),
          el("td", { class: "num" }, fmtBaht(bill.amountBaht)),
          el("td", {}, reconCell),
          el("td", {}, paidPill),
          el("td", {}, bill.paymentEvidence || "—"),
        ])
      );
    }
    // Re-attach click handlers for the toggle-paid pills (idempotent — pills are recreated each render).
    for (const btn of tbody.querySelectorAll("[data-toggle-paid]")) {
      btn.addEventListener("click", () => {
        const bill = data.bills.find((b) => b.id === btn.dataset.togglePaid);
        if (!bill) return;
        bill.paid = !bill.paid;
        if (bill.paid && !bill.paymentEvidence) bill.paymentEvidence = "slip-demo.jpg";
        renderAll();
      });
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
    // Phase 2: every holder gets every tab (Bills is symmetric now).
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
    renderAccounts(state.personId);
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
        document.dispatchEvent(new CustomEvent("poc:holder-changed", { detail: { personId: state.personId } }));
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

    wireThemeToggle();
    wireEntryForm();
  };

  // ---- entry form: live alias match + add to in-memory transactions ----------

  const matchAlias = (merchant) => {
    if (!merchant) return null;
    return (data.aliases || []).find((a) => {
      const p = a.pattern || {};
      if (p.type === "contains") return merchant.toLowerCase().includes((p.text || "").toLowerCase());
      if (p.type === "exact")    return merchant === p.text;
      return false;
    }) || null;
  };

  const wireEntryForm = () => {
    const form = document.querySelector("[data-entry-form-body]");
    if (!form) return;
    const cardSel     = form.querySelector("[data-entry-card]");
    const merchantInp = form.querySelector("[data-entry-merchant]");
    const categorySel = form.querySelector("[data-entry-category]");
    const aliasNote   = form.querySelector("[data-entry-alias]");

    const populateCards = () => {
      cardSel.replaceChildren();
      for (const c of cardsForPerson(state.personId)) {
        const product = idx.cardProducts[c.productId];
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.textContent = `${product ? product.name : "—"} (••${c.last4 || "----"}, ${c.nickname || ""})`;
        cardSel.appendChild(opt);
      }
    };
    const populateCategories = () => {
      categorySel.replaceChildren();
      for (const cat of data.categories) {
        const opt = document.createElement("option");
        opt.value = cat.id;
        opt.textContent = cat.name;
        categorySel.appendChild(opt);
      }
      // Default to "Other / Uncategorized" if it exists.
      const other = data.categories.find((c) => c.id === "cat-other");
      if (other) categorySel.value = other.id;
    };

    const refreshAlias = () => {
      const merchant = merchantInp.value.trim();
      const a = matchAlias(merchant);
      if (a) {
        aliasNote.hidden = false;
        aliasNote.textContent = `Matched alias “${a.canonicalMerchant}” — category auto-set to “${idx.categories[a.categoryId]?.name || a.categoryId}”.`;
        categorySel.value = a.categoryId;
      } else {
        aliasNote.hidden = true;
        aliasNote.textContent = "";
      }
    };

    merchantInp.addEventListener("input", refreshAlias);

    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const fd = new FormData(form);
      const cardId    = fd.get("cardId");
      const merchant  = String(fd.get("merchant") || "").trim();
      const amount    = parseFloat(fd.get("amount"));
      const categoryId= fd.get("categoryId") || "cat-other";
      const note      = String(fd.get("note") || "").trim() || merchant;
      if (!cardId || !merchant || !Number.isFinite(amount)) return;
      const today = new Date().toISOString().slice(0, 10);
      const matched = matchAlias(merchant);
      const newTx = {
        id: `t-poc-${Date.now()}`,
        cardId, categoryId,
        amountBaht: amount,
        swipedAt: today,
        processedDate: null,
        billCycleDate: today,
        dueDate: today,
        status: "pending",
        rewardRules: [{ type: "multiplier", value: 1 }],
        note,
        ...(matched ? { aliasMatchedId: matched.id } : {}),
      };
      data.transactions.unshift(newTx);
      form.reset();
      aliasNote.hidden = true;
      renderAll();
    });

    // Re-populate when the holder switches (cards available differ per holder).
    // Also at first render.
    populateCards();
    populateCategories();
    document.addEventListener("poc:holder-changed", () => {
      populateCards();
    });
  };

  // ---- theme toggle: system → light → dark → system, persisted in localStorage --

  const THEMES = ["system", "light", "dark"];
  const themeLabel = { system: "System", light: "Light", dark: "Dark" };
  const themeIcon  = { system: "🌗", light: "☀️", dark: "🌙" };

  const applyTheme = (choice) => {
    const root = document.documentElement;
    if (choice === "system") {
      root.removeAttribute("data-theme");
    } else {
      root.setAttribute("data-theme", choice);
    }
    const btn = document.querySelector("[data-theme-toggle]");
    if (btn) {
      btn.querySelector("[data-theme-icon]").textContent  = themeIcon[choice];
      btn.querySelector("[data-theme-label]").textContent = themeLabel[choice];
      btn.setAttribute("aria-label", `Theme: ${themeLabel[choice]} (click to cycle)`);
    }
  };

  const wireThemeToggle = () => {
    const stored = (() => { try { return localStorage.getItem("poc-theme") || "system"; } catch { return "system"; } })();
    state.theme = THEMES.includes(stored) ? stored : "system";
    applyTheme(state.theme);
    const btn = document.querySelector("[data-theme-toggle]");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const i = THEMES.indexOf(state.theme);
      state.theme = THEMES[(i + 1) % THEMES.length];
      try { localStorage.setItem("poc-theme", state.theme); } catch { /* ignore */ }
      applyTheme(state.theme);
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    wireEvents();
    renderAll();
  });
})();
