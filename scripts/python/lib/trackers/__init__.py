"""Cashback trackers: settling a `รายการติดตามเครดิตเงินคืนของ<name>` row.

deterministic + idempotent — see each module.

A tracker row expects a credit for one promotion period. It is settled when
the credit has reached the holder: the ledger row(s) that carry it go in
`Slip Transaction`, and the unnamed checkbox is ticked. The Bureau sync
(`lib.bureau.settle`) only writes `Expected Cashback`; nothing here touches it.

Modules:
  model   the tracker page, its Bureau row, the ledger rows it links (read side)
  basis   Basis: one class per way a credit settles a tracker
          (ExactCredit, PooledCredit, CycleCredits, ZeroShare)
  settle  plan the writes for a spec, refuse a ticked (frozen) row, apply

Rules: docs/databases/cashback-trackers.md.
"""
