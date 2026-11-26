"""Beylikdüzü demo sitelerini üretir: python3 tools/build_sites.py"""
import json, os, re, html, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "prospects", "businesses.json"), encoding="utf-8"))

ICONS = {
 "paw": '<path d="M12 13c-3 0-5.5 2.6-5.5 4.8 0 1.5 1.3 2.2 2.8 2.2 1.2 0 1.8-.6 2.7-.6s1.5.6 2.7.6c1.5 0 2.8-.7 2.8-2.2C17.5 15.6 15 13 12 13zM6 12.5a2 2.5 0 1 0 0-.1zM9.5 8.5a2 2.6 0 1 0 0-.1zM14.5 8.5a2 2.6 0 1 0 0-.1zM18 12.5a2 2.5 0 1 0 0-.1z"/>',
 "steth": '<path d="M6 3v6a4 4 0 0 0 8 0V3M10 13v2a5 5 0 0 0 10 0v-2" fill="none" stroke-width="2"/><circle cx="20" cy="11" r="2" fill="none" stroke-width="2"/>',
 "syringe": '<path d="M18 2l4 4M15 5l4 4M17 7L7 17l-3 1 1-3L15 5M9 11l2 2M12 8l2 2M4 20l-2 2" fill="none" stroke-width="2"/>',
 "heart": '<path d="M12 21s-8-5.3-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.7-8 11-8 11z"/>',
 "scissors": '<circle cx="6" cy="6" r="3" fill="none" stroke-width="2"/><circle cx="6" cy="18" r="3" fill="none" stroke-width="2"/><path d="M8.5 8L20 19M8.5 16L20 5" fill="none" stroke-width="2"/>',
 "bag": '<path d="M5 8h14l-1 13H6L5 8zM9 8V6a3 3 0 0 1 6 0v2" fill="none" stroke-width="2"/>',
 "bone": '<path d="M7 10a2.5 2.5 0 1 1 2-4l6 6a2.5 2.5 0 1 1 4 2 2.5 2.5 0 1 1-2 4l-6-6a2.5 2.5 0 1 1-4-2z" fill="none" stroke-width="2"/>',
 "bath": '<path d="M3 12h18v3a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5v-3zM6 12V5a2 2 0 0 1 4 0" fill="none" stroke-width="2"/>',
 "fish": '<path d="M3 12c4-6 11-6 15 0-4 6-11 6-15 0zM18 12l3-3v6z" fill="none" stroke-width="2"/>',
 "clock": '<circle cx="12" cy="12" r="9" fill="none" stroke-width="2"/><path d="M12 7v5l3 2" fill="none" stroke-width="2"/>',
 "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z" fill="none" stroke-width="2"/>',
 "pin": '<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z" fill="none" stroke-width="2"/><circle cx="12" cy="10" r="2.5" fill="none" stroke-width="2"/>',
 "wa": '<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7L4 20z" fill="none" stroke-width="2"/><path d="M9 9.5c.5 2 2 3.5 4 4l1-1 1.5.8c-.3 1-1 1.5-2 1.2-2.5-.7-4.3-2.5-5-5-.3-1 .2-1.7 1.2-2l.8 1.5-1 1z"/>',
}
def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def e(s): return html.escape(s, quote=True)

def tel_link(p): return "tel:+90" + "".join(c for c in p if c.isdigit()).lstrip("0")
def wa_link(p): return "https://wa.me/90" + "".join(c for c in p if c.isdigit()).lstrip("0")

TEMPLATE = open(os.path.join(ROOT, "tools", "template.html"), encoding="utf-8").read()

for b in data:
    t = b["theme"]
    services = "\n".join(
        f'<article class="card">{icon(s["icon"], "ic big")}<h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></article>'
        for s in b["services"])
    why = "\n".join(f'<li>{icon("paw")}<span>{e(w)}</span></li>' for w in b["why"])
    phone = b.get("phone")
    if phone:
        cta = (f'<a class="btn primary" href="{tel_link(phone)}">{icon("phone")} Hemen Ara</a>'
               f'<a class="btn ghost" href="{wa_link(phone)}" target="_blank" rel="noopener">{icon("wa")} WhatsApp</a>')
        phone_row = f'<li>{icon("phone")}<a href="{tel_link(phone)}">{e(phone)}</a></li>'
        float_btn = f'<a class="float" href="{wa_link(phone)}" target="_blank" rel="noopener" aria-label="WhatsApp ile yazın">{icon("wa")}</a>'
    else:
        cta = f'<a class="btn primary" href="#iletisim">{icon("pin")} Bize Ulaşın</a>'
        phone_row = '<li>{}<span>Telefon: [işletme numarası eklenecek]</span></li>'.format(icon("phone"))
        float_btn = ""
    q = urllib.parse.quote(b["name"] + " " + b["address"])
    out = TEMPLATE
    for k, v in {
        "NAME": e(b["name"]), "SHORT": e(b["short"]), "KIND": e(b["kind"]),
        "TAGLINE": b["tagline"], "INTRO": e(b["intro"]), "ABOUT": e(b["about"]),
        "ADDRESS": e(b["address"]), "HOURS": e(b["hours"]), "SERVICES": services, "WHY": why,
        "CTA": cta, "PHONE_ROW": phone_row, "FLOAT": float_btn,
        "MAP_Q": q, "HERO_ICON": icon(b["hero_icon"], "heroic"),
        "PIN": icon("pin"), "CLOCK": icon("clock"), "LOGO": icon("paw", "logo"),
        "C1": t["c1"], "C2": t["c2"], "BG": t["bg"], "INK": t["ink"],
        "DESC": e(re.sub("<[^>]+>", "", b["tagline"]) + " – " + b["address"]),
    }.items():
        out = out.replace("{{" + k + "}}", v)
    d = os.path.join(ROOT, "sites", b["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    print("ok", b["slug"])
