import telebot
import requests
from bs4 import BeautifulSoup
import io
b = telebot.TeleBot(input("token: "))
def gd(uid):
    u = f"http://0-0-0-0-0-0-0-0-0-0--0-0-0.work.gd/?uid={uid}"
    r = requests.post(u)
    s = BeautifulSoup(r.text, 'html.parser')
    bs = s.find("div", class_="ban-status")
    bs_text = bs.get_text(strip=True) if bs else "حالة الحظر غير متوفرة"
    ai = s.find("div", class_="result")
    info = ""
    if ai:
        for l in ai.stripped_strings:
            if ":" in l:
                info += l + "\n"
    eq = {}
    ed = s.find("div", class_="equipped-items")
    if ed:
        c = ""
        for ch in ed.children:
            if ch.name in ['h3','h4']:
                c = ch.get_text(strip=True)
                eq[c] = []
            elif ch.name == 'div' and 'equipped-item' in ch.get('class', []):
                im = ch.find('img')
                p = ch.find('p')
                if im and p:
                    eq[c].append({"img": im.get('src'), "alt": im.get('alt'), "desc": p.get_text(strip=True)})
    return bs_text, info, eq

@b.message_handler(commands=['start'])
def st(m):
    b.send_message(m.chat.id, " الايدي:")
    b.register_next_step_handler(m, ex)

def ex(m):
    uid = m.text.strip()
    b.send_message(m.chat.id, "جاري استخراج البيانات")
    bs_text, info, eq = gd(uid)
    txt = f"حالة الحظر:\n{bs_text}\n\nمعلومات الحساب:\n{info}"
    b.send_message(m.chat.id, txt)
    for cat, its in eq.items():
        b.send_message(m.chat.id, f"الفئة: {cat}")
        for it in its:
            cap = f"{it['desc']}\nالنص : {it['alt']}"
            try:
                r = requests.get(it['img'])
                bio = io.BytesIO(r.content)
                bio.name = 'levi.jpg'
                b.send_photo(m.chat.id, bio, caption=cap)
            except Exception as e:
                b.send_message(m.chat.id, f"راسلني: {it['img']}")

b.polling()
##
###
###