"""Promotion Bureau: household-wide tracking of bank promotions.

deterministic + idempotent — the registry is static; see each module.

The Bureau (a Notion DB) keeps one row per **quota period**: the window a
bank counts a limit over (a calendar month, a statement cycle, or the whole
campaign). The row is named `<year>M<month> — <campaign>`, where the month is
the calendar month, the month of the cycle's closing date, or the campaign's
first month. Every holder's qualifying transactions link to it.

Modules:
  base       BasePromotion (identity, matching, screening, FCFS walk, page)
             and CashbackPromotion (baht shares, trackers, the `% cb` rule)
  ladder     LadderPromotion: steps of pooled spend
  capped     CreditCapPromotion: a per-row rate until a pooled credit cap
  slips      SlipCreditPromotion: a fixed credit per slip until a pooled cap
  rights     DrawRightsPromotion: lucky-draw rights per slip, up to a count per month
  accounts   CardAccount: a quota per primary card account (one Bureau row per card);
             CardNumber: a quota per card number, for two holders' cards with one title
  instant    InstantDiscountPromotion: a discount taken off the charge itself, read back from the net amount
  quota      a campaign's nationwide pool: the bank's page, and `Quotas Exceeded Date` (the day it ran out)
  unionpay_offer  UnionPay International's offer API (the pool left per monthly offer)
  unionpay_qr  UnionPay QR 6% off on KTC UnionPay, monthly from Sep 2026 — per card number
  nw3        Krungsri First Choice NW3 (ladder), Jul–Sep 2026
  on3 / dlv3 / is3   First Choice online shopping, delivery, insurance (Jul/Sep 2026 –)
  bts        BTS draw rights, Aug–Nov 2026: a First Choice pool and a Krungsri Card pool
  onq3 / sup1 / ptt2  Krungsri Card online, supermarket, PTT — per card account
  jdining    Krungsri JCB J Dining 3% per ฿1,000 restaurant slip, Jan–Sep 2026
  eat        Krungsri Card EAT dining ("DN"), ฿100 for the month's 1st and 3rd slip — per card account
  bangchak   Krungsri Card at Bangchak: the card's 1% per cycle, BC3P per slip — per card account
  ttb_campaigns  ttb Caltex (CTG) and Bangchak (BCG) fuel, hypermarket (BMG)
  krungsri_now  Krungsri NOW online ฿25 per ฿500 slip, ฿300 a month
  aeon_unionpay  AEON UnionPay 3% in CNY/HKD/MOP/TWD, ฿2,500 a cycle
  slip_count SlipCountPromotion: a credit for the Nth qualifying slip in a period
  lbs3       Lotus's big-ticket categories (ladder), Sep–Dec 2026
  ttb_so_smart  ttb so smart 1%, ฿2,000 a cycle (credit cap)
  aeon_rabbit / aeon_world / ntw1  AEON Rabbit 5%, AEON World 5% supermarkets, Everyday with AEON
  epw538     UOB e-Commerce & e-Wallet EPW538 (ladder), Jul–Sep 2026
  uob_one    UOB One 10%/5% (monthly) and 1% (per cycle) (credit caps)
  uob_world  UOB World ×5 (a points quota per cycle)
  store      Notion reads/writes for Bureau rows, linked transactions, trackers
  sync       a row's linked rows, candidates and adjustments
  settle     a cashback row's money: shares and trackers
  report     flagged rows, field mismatches, the boundary, drift
  runner     one Bureau row's sync (/sync-promotion's core)
  follow     re-sync the rows a ledger write touched, and apply the split to them

To add a campaign: subclass the shape that fits (or BasePromotion for a new
shape) in a new module, then list it in PROMOTIONS below.
"""

from __future__ import annotations

import datetime as dt

from . import bangchak, bts, eat, jdining, krungsri_now, onq3, ptt2, sup1, unionpay_qr
from .accounts import CardAccount, CardNumber
from .aeon_rabbit import AEONRabbitCashback
from .aeon_unionpay import AEONUnionPayCashback
from .aeon_world import AEONWorldCashback
from .base import (CASHBACK, ELIGIBLE, EXCLUDED, POINTS, RIGHTS, UNCERTAIN, Allocation, BasePromotion,
                   CashbackPromotion, Rule, Tx, TxCredit)
from .bts import BTSDrawPromotion
from .capped import CreditCapPromotion
from .dlv3 import DLV3Promotion
from .epw538 import EPW538Promotion
from .instant import InstantDiscountPromotion
from .is3 import IS3Promotion
from .ladder import LadderPromotion, Tranche
from .lbs3 import LBS3Promotion
from .ntw1 import NTW1Promotion
from .nw3 import NW3Promotion
from .on3 import ON3Promotion
from .rights import DrawRightsPromotion
from .slip_count import SlipCountPromotion
from .slips import SlipCreditPromotion
from .ttb_campaigns import TTBBangchakPromotion, TTBCaltexPromotion, TTBHypermarketPromotion
from .ttb_so_smart import TTBSoSmartCashback
from .uob_one import UOBOneBase, UOBOneBonus
from .uob_world import UOBWorldBonus

PROMOTIONS: tuple[type[BasePromotion], ...] = (
    NW3Promotion, EPW538Promotion, UOBOneBonus, UOBOneBase, UOBWorldBonus,
    ON3Promotion, DLV3Promotion, IS3Promotion, *bts.POOLS,
    *onq3.ACCOUNTS, *sup1.ACCOUNTS, *ptt2.ACCOUNTS, *jdining.ACCOUNTS, *eat.ACCOUNTS, *bangchak.ACCOUNTS,
    *krungsri_now.ACCOUNTS, AEONUnionPayCashback,
    TTBCaltexPromotion, TTBBangchakPromotion, TTBHypermarketPromotion,
    LBS3Promotion, TTBSoSmartCashback, AEONRabbitCashback, AEONWorldCashback, NTW1Promotion,
    *unionpay_qr.ACCOUNTS,
)


def promotion_for(bureau_name: str, start: dt.date, end: dt.date) -> BasePromotion:
    """The campaign a Bureau row belongs to, by its Name and its period."""
    hits = [cls for cls in PROMOTIONS if cls.matches(bureau_name, start, end)]
    if len(hits) != 1:
        known = ", ".join(f"{c.__name__} ({c.name_pattern or c.code})" for c in PROMOTIONS)
        raise LookupError(
            f"{len(hits)} registered promotions match {bureau_name!r} ({start}→{end}); "
            f"known: {known}. Add a BasePromotion subclass in lib/bureau/ for a new campaign.")
    return hits[0]()


__all__ = ["CASHBACK", "ELIGIBLE", "EXCLUDED", "POINTS", "RIGHTS", "UNCERTAIN", "Allocation",
           "AEONRabbitCashback", "AEONUnionPayCashback", "AEONWorldCashback", "BTSDrawPromotion", "BasePromotion", "CardAccount",
           "CardNumber", "CashbackPromotion", "CreditCapPromotion", "DLV3Promotion", "DrawRightsPromotion",
           "EPW538Promotion", "IS3Promotion", "InstantDiscountPromotion", "LBS3Promotion", "LadderPromotion", "NTW1Promotion",
           "NW3Promotion", "ON3Promotion", "PROMOTIONS", "Rule", "SlipCountPromotion", "SlipCreditPromotion", "TTBBangchakPromotion", "TTBCaltexPromotion",
           "TTBHypermarketPromotion",
           "TTBSoSmartCashback", "Tranche", "Tx", "TxCredit", "UOBOneBase", "UOBOneBonus",
           "UOBWorldBonus", "promotion_for"]
