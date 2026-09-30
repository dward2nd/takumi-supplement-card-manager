"""Merchant categories → emoji, for purchase rows in the Transactions DBs.

deterministic + idempotent — declarations and pure functions only.

Matched in order against the merchant string with any `[…]` prefix removed,
so `[บัตรหลัก] TMN 7-11 BANGKOK TH` is a 7-Eleven row. Order matters where
categories overlap: food delivery before rides (Grab Food is food), transit
before wallets (`LINEPAY*BTS` is a BTS fare), flights before hotels (Agoda
sells both), a named category before the foreign-merchant fallback. The
petrol, e-wallet top-up and supermarket tests are the ones the earning rules
use (`lib.promotions`), so an icon never disagrees with how a row earns.
"""

from __future__ import annotations

import re

from .. import promotions
from .base import IconRule, first_match

_CHINA = re.compile(r"\b(CHN|CN)$")
# Airport pairs as Agoda and the airlines print them (`CNX-DMK`); a bare
# three-letter pair would catch shop codes such as `SCT-ONE`.
_AIRPORTS = "BKK|DMK|CNX|CEI|HKT|KBV|USM|HDY|UTH|KKC|UBP|URT|NST|TST|NAW|LPT|PHS|HKG|SIN|NRT|HND|KIX|ICN|TPE"
# Word edges that also split on `_` (`LINEPAY*LP_BTS`, `LP_AIS SERVICE`).
_L, _R = r"(?<![A-Z0-9])", r"(?![A-Z0-9])"


def _china(name: str) -> bool:
    return bool(_CHINA.search(name.strip().upper()))


MERCHANT_RULES: tuple[IconRule, ...] = (
    IconRule("🚆", rf"{_L}(BTS|MRT|SRT|BMTA|BEM){_R}|SMARTCARD|AIRPORT RAIL"),
    IconRule("🛣️", r"EXPRESSW|EASY ?PASS|\bM-?PASS\b"),
    IconRule("👛", r"^LINEPAY\*(LP_)?LINEPAY|^LP_LINEPAY", test=promotions.looks_wallet_top_up),
    IconRule("⛽", r"PTTRM|SUSCO", test=promotions.looks_petrol),
    IconRule("🛵", r"LINE ?MAN|\bLM_|PF_LM|SHOPEEFOOD|FOODPANDA|ROBINHOOD|GRAB ?FOOD"),
    IconRule("🚗", r"GRAB|BOLT|\bRIDE\b|INDRIVE|TAXI|MUVMI"),
    IconRule("🏪", r"7-11|7-ELEVEN|SEVEN ELEVEN|FAMILYMART|LAWSON|MINI BIG|CJ MORE"),
    IconRule("🧾", r"ISERVICE|COUNTER ?SERVICE"),
    IconRule("🧺", r"LAUND|WASH"),
    IconRule("📲", r"PROMPTPAY|PAYANYTHING|PAY ANYTHING"),
    IconRule("🧋", r"CHATRA[MB]UE|CHA TRA MUE|BUBBLE|BOBA|MIXUE|\bTEA\b|JUICE"),
    IconRule("☕", r"^AMZ_|CAFE AMAZON|STARBUCKS|COFFEE|\bCAFE\b|KAFE|BARIST|\bDRIP\b"),
    IconRule("🍦", r"^DQ|DAIRY QUEEN|SWENSEN|YOLE|AFTER YOU|BASKIN|ICE ?CREAM|\bICE\b|SWEET"),
    IconRule("🥐", r"BAKERY|\bBAKE|LOAF|BREAD|CROISSANT|DONUT|DUNKIN"),
    IconRule("🍔", r"\bMCD|MCDONALD|\bKFC|BURGER|PIZZA|SUBWAY|FIVE STAR|CHESTER|BONCHON|CNX BC\b|KEBAB|FAST FOOD"),
    IconRule("🍲", r"HAI ?DI ?LAO|HOT ?POT|SHABU|SUKI"),
    IconRule("🍣", r"SUSHI|RAMEN|IPPUDO|YAYOI|OTOYA|IZAKAYA"),
    IconRule("🍜", r"NOODLE|DUMPLING|CURRY|RESTAURANT|KITCHEN|MOOYIM|JIMJUM|NA-NUA|BISTRO|STEAK|GRILL|"
                   r"BUFFET|SALAD|FRY THANK|SOMTUM|SOUP|PEPPER LUNCH|FOOD AND BE|\bFOOD\b"),
    IconRule("✈️", r"AIR ?ASIA|THAI ?AIRWAYS|NOK ?AIR|VIETJET|THAI ?LION|BANGKOK ?AIR|TRIP\.COM|CTRIP|"
                   rf"EXPEDIA|TRAVELOKA|\b({_AIRPORTS})-({_AIRPORTS})\b"),
    IconRule("🏨", r"AGODA|BOOKING\.COM|HOTEL|RESORT|AIRBNB|HOSTEL|AIRPORTEL"),
    IconRule("🛒", r"MAKRO|LOTUS|BIG ?C\b|\bTOPS\b|GO WHOLESALE|DONKI|DON DON|GROCERY|MARKET|MAX ?VALU|"
                   r"FOODLAND|SAVEMART|RIMPING|CP AXTRA", test=promotions.looks_supermarket),
    IconRule("🛍️", r"SHOPEE|LAZADA|TIKTOK|AMAZON\.|ALIEXPRESS|TEMU|NOCNOC"),
    IconRule("🎬", r"CINEMA|\bSFX\b|MAJOR|CINEPLEX|IMAX"),
    IconRule("🤖", r"ANTHROPIC|CLAUDE|OPENAI|CHATGPT|MIDJOURNEY|CURSOR"),
    IconRule("🎵", r"SPOTIFY|JOOX|APPLE MUSIC"),
    IconRule("📺", r"YOUTUBE|NETFLIX|DISNEY|\bVIU\b|\bHBO\b|PRIME VIDEO|TRUEID|MONOMAX"),
    IconRule("💻", r"APPLE\.COM|ITUNES|GOOGLE|MICROSOFT|ADOBE|CANVA|NGROK|GITHUB|X CORP|DROPBOX|NOTION|"
                   r"STEAM|PLAYSTATION|NINTENDO"),
    IconRule("📶", rf"{_L}AIS{_R}|DTAC|TRUE ?MOVE|REFILL"),
    IconRule("🛡️", r"\bAIA|INSURANCE|ประกัน|MUANG ?THAI ?LIFE|\bFWD\b|ALLIANZ|\bAXA\b"),
    IconRule("🏥", r"CLINIC|HOSPITAL|MEDICAL|\bDENT|HEALTH|SRIPHAT|BUMRUNGRAD|โรงพยาบาล"),
    IconRule("💊", r"WATSON|BOOTS|PHARMA|DRUG|EVEANDBOY|BEAUTRIUM|KONVY|SEPHORA"),
    IconRule("💆", r"MASSAGE|\bSPA\b|WELLNESS|SENTO|ONSEN|SALON|\bNAIL|PANPURI|LET'?S RELAX"),
    IconRule("🏋️", r"FITNESS|\bGYM\b|YOGA|PILATES|CLIMB|BOULDER"),
    IconRule("📱", r"COM7|COMSEVEN|JAYMART|SAMSUNG|BANANA|POWER ?BUY|ISTUDIO|STUDIO7|XIAOMI|HUAWEI|ELECTRONIC"),
    IconRule("📚", r"B2S|KINOKUNIYA|ASIA BOOKS|NAIIN|SE-ED|BOOK"),
    IconRule("👕", r"NIKE|ADIDAS|UNIQLO|ZARA|H&M|\bCDS\b|CENTRAL|ROBINSON|DECATHLON|MUJI|DAISO|MINISO|POP MART"),
    IconRule("🛋️", r"IKEA|IKANO|INDEX LIVING|HOME ?PRO|THAI ?WATSADU|GLOBAL HOUSE|DOHOME"),
    IconRule("🎓", r"UNIVERSITY|COLLEGE|SCHOOL|TUITION"),
    IconRule("🏛️", r"REVENUE|MUSEUM|MUANG BORAN|PASSPORT|IMMIGRATION"),
    IconRule("⛴️", r"BOAT|FERRY|\bPIER\b"),
    IconRule("🇨🇳", r"ALIPAY|UNIONPAY MERCHANT|WECHAT", test=_china),
    IconRule("🌐", test=promotions.looks_foreign_in_thb),
)


def merchant_emoji(bare_name: str) -> str | None:
    """The category emoji for a merchant string, or None when no category fits."""
    return first_match(MERCHANT_RULES, bare_name)
