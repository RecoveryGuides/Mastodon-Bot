#!/usr/bin/env python3
"""
🤖 MASTODON SIMPLE BOT (24/7 SMART VERSION)
- Sam decyduje czy odpowiadać (max 8 postów dziennie)
- DZIAŁA 24/7 (w tym w nocy dla międzynarodowej publiczności)
- Tylko sentencje z sentences.txt
- Co 5 komentarz link do sklepu
- Nigdy nie powtarza sentencji
"""

from mastodon import Mastodon
import os
import json
import random
import time
from datetime import datetime, date
import sys

print("=" * 50)
print("🤖 MASTODON SMART BOT 24/7")
print(f"⏰ Godzina: {datetime.now().strftime('%H:%M')}")
print("=" * 50)

# ==================== NOWA LOGIKA DECYZYJNA (24/7) ====================

def should_i_post_now():
    """INTELIGENTNA decyzja czy teraz postować (24/7)"""
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0=poniedziałek, 6=niedziela
    
    # 1. Sprawdź dzienny limit (zwiększony do 8)
    MAX_POSTS_PER_DAY = 8
    LIMIT_FILE = "daily_limit.json"
    
    try:
        with open(LIMIT_FILE, 'r') as f:
            limit_data = json.load(f)
    except:
        limit_data = {"date": None, "posts_today": 0}
    
    today = date.today().isoformat()
    
    # Reset jeśli nowy dzień
    if limit_data.get("date") != today:
        limit_data = {"date": today, "posts_today": 0}
        with open(LIMIT_FILE, 'w') as f:
            json.dump(limit_data, f, indent=2)
    
    # Sprawdź limit
    if limit_data["posts_today"] >= MAX_POSTS_PER_DAY:
        print(f"⏭️ Dzisiejszy limit: {limit_data['posts_today']}/{MAX_POSTS_PER_DAY}")
        return False
    
    # 2. RÓŻNE SZANSE W ZALEŻNOŚCI OD PORY (24/7):
    chance = random.random()
    
    # WIĘKSZE SZANSE W NOCY dla międzynarodowej publiczności!
    if 0 <= hour < 6:    # Noc głęboka (0-6): 40% szans - DOBRY CZAS!
        print(f"🌙 Nocna zmiana (0-6) - celuję w USA/Azje")
        if chance > 0.40:
            print(f"   🎲 Losowo pomijam (szansa: {chance:.2f})")
            return False
    
    elif 6 <= hour < 9:   # Poranek (6-9): 30% szans - Europa budzi się
        print(f"🌅 Poranek (6-9) - Europa wschodzi")
        if chance > 0.30:
            print(f"   🎲 Losowo pomijam (szansa: {chance:.2f})")
            return False
    
    elif 9 <= hour < 12:  # Przedpołudnie (9-12): 35% szans
        print(f"☀️ Przedpołudnie (9-12) - Europa aktywna")
        if chance > 0.35:
            print(f"   🎲 Losowo pomijam (szansa: {chance:.2f})")
            return False
    
    elif 12 <= hour < 17: # Południe (12-17): 45% szans - NAJLEPSZY CZAS dla Europy
        print(f"🌞 Południe (12-17) - szczyt aktywności Europy")
        if chance > 0.45:
            print(f"   🎲 Losowo pomijam (szansa: {chance:.2f})")
            return False
    
    elif 17 <= hour < 21: # Wieczór (17-21): 40% szans - USA rano/południe
        print(f"🌆 Wieczór (17-21) - USA budzi się")
        if chance > 0.40:
            print(f"   🎲 Losowo pomijam (szansa: {chance:.2f})")
            return False
    
    else:  # Późny wieczór/noc (21-24): 35% szans - USA aktywna
        print(f"🌃 Późny wieczór (21-24) - USA w pełni")
        if chance > 0.35:
            print(f"   🎲 Losowo pomijam (szansa: {chance:.2f})")
            return False
    
    # 3. Weekend vs weekday (mniejsza aktywność w weekendy)
    if weekday >= 5:  # Weekend
        weekend_chance = random.random()
        if weekend_chance > 0.6:  # 40% mniej postów w weekend
            print(f"🎪 Weekend - zmniejszam aktywność")
            return False
    
    # 4. Zaktualizuj licznik
    limit_data["posts_today"] += 1
    with open(LIMIT_FILE, 'w') as f:
        json.dump(limit_data, f, indent=2)
    
    time_of_day = ["noc", "rano", "przedpołudnie", "południe", "wieczór", "noc"][hour // 4]
    print(f"✅ DECYZJA: POSTUJĘ o {now.strftime('%H:%M')} ({time_of_day})!")
    print(f"   📊 {limit_data['posts_today']}/{MAX_POSTS_PER_DAY} postów dzisiaj")
    return True

# ==================== GŁÓWNA DECYZJA ====================
if not should_i_post_now():
    print("💤 Kończę pracę - nie postuję teraz")
    sys.exit(0)

# ==================== RESZTA TWOJEGO KODU (BEZ ZMIAN) ====================
print("\n" + "=" * 50)
print("🚀 ROZPOCZYNAM POSTOWANIE")
print("=" * 50)

# 1. INICJALIZUJ PLIKI (ŻEBY NA PEWNO ISTNIAŁY)
print("📁 Inicjalizuję pliki...")
def init_files():
    if not os.path.exists("counter.txt"):
        with open("counter.txt", "w") as f:
            f.write("0")
        print("✅ counter.txt created")
    
    if not os.path.exists("used_sentences.json"):
        with open("used_sentences.json", "w") as f:
            json.dump({"used": [], "reset_date": date.today().isoformat()}, f)
        print("✅ used_sentences.json created")
    
    if not os.path.exists("posted_toots.json"):
        with open("posted_toots.json", "w") as f:
            f.write("")
        print("✅ posted_toots.json created")
    
    if not os.path.exists("daily_limit.json"):
        with open("daily_limit.json", "w") as f:
            json.dump({"date": date.today().isoformat(), "posts_today": 1}, f)
        print("✅ daily_limit.json created")
    
    if not os.path.exists("sentences.txt"):
        print("❌ BRAK sentences.txt!")
        print("Tworzę przykładowy plik...")
        with open("sentences.txt", "w") as f:
            f.write("Every day is a new chance to change.\n")
            f.write("Small steps lead to big results.\n")
            f.write("You're stronger than you think.\n")
        print("✅ sentences.txt created (example)")

init_files()

# 2. KONFIGURACJA MASTODON
ACCESS_TOKEN = os.environ.get('MASTODON_ACCESS_TOKEN')
BASE_URL = os.environ.get('MASTODON_BASE_URL', 'https://mastodon.social')

if not ACCESS_TOKEN:
    print("❌ BRAK MASTODON_ACCESS_TOKEN!")
    print("Dodaj w GitHub: Settings → Secrets → Actions")
    exit(1)

print(f"🔗 Server: {BASE_URL}")

try:
    mastodon = Mastodon(access_token=ACCESS_TOKEN, api_base_url=BASE_URL)
    
    # Sprawdź połączenie
    account = mastodon.account_verify_credentials()
    print(f"✅ Połączono jako: @{account['username']}")
    print(f"   👥 Followers: {account['followers_count']}")
    
except Exception as e:
    print(f"❌ Błąd połączenia: {e}")
    exit(1)

# 3. WCZYTAJ SENTENCJE
print("\n📚 Wczytywanie sentencji...")
try:
    with open('sentences.txt', 'r', encoding='utf-8') as f:
        all_sentences = [line.strip() for line in f if line.strip()]
    
    if not all_sentences:
        print("❌ Brak sentencji w sentences.txt!")
        exit(1)
    
    print(f"✅ Załadowano {len(all_sentences)} sentencji")
    
except Exception as e:
    print(f"❌ Błąd wczytywania sentencji: {e}")
    exit(1)

# 4. WCZYTAJ HISTORIĘ UŻYTYCH SENTENCJI
print("\n📖 Sprawdzam historię sentencji...")
try:
    with open('used_sentences.json', 'r') as f:
        history = json.load(f)
    
    # Sprawdź czy trzeba zresetować (nowy dzień)
    today = date.today().isoformat()
    
    if history.get('reset_date') != today:
        print("🆕 NOWY DZIEŃ - resetuję historię sentencji")
        history = {'used': [], 'reset_date': today}
    
    used_sentences = set(history.get('used', []))
    print(f"📊 Dzisiaj użyto: {len(used_sentences)}/{len(all_sentences)} sentencji")
    
except Exception as e:
    print(f"⚠️  Błąd historii, zaczynam od nowa: {e}")
    history = {'used': [], 'reset_date': date.today().isoformat()}
    used_sentences = set()

# 5. ZNAJDŹ NIEUŻYTE SENTENCJE
available_sentences = [s for s in all_sentences if s not in used_sentences]

if not available_sentences:
    print("🔄 Wszystkie sentencje użyte dzisiaj, resetuję...")
    used_sentences = set()
    history['used'] = []
    available_sentences = all_sentences

print(f"🎯 Dostępnych sentencji: {len(available_sentences)}")

# 6. WYBIERZ LOSOWĄ SENTENCJĘ
selected_sentence = random.choice(available_sentences)

# Dodaj do użytych
used_sentences.add(selected_sentence)
history['used'] = list(used_sentences)

# Zapisz historię
with open('used_sentences.json', 'w') as f:
    json.dump(history, f, indent=2)

print(f"📝 Wybrana sentencja: {selected_sentence[:80]}...")

# 7. OBSŁUGA LICZNIKA DLA LINKÓW
try:
    with open('counter.txt', 'r') as f:
        counter = int(f.read().strip())
except:
    counter = 0

counter += 1
print(f"📊 Licznik komentarzy: {counter}")

# ZAPISZ LICZNIK OD RAZU
with open('counter.txt', 'w') as f:
    f.write(str(counter))

# Co 5 komentarz dodaj link
SHOP_URL = "https://www.payhip.com/daveprime"

if counter % 5 == 0:
    reply = f"{selected_sentence}\n\n🛒 More help: {SHOP_URL}"
    print("🎁 DODAJĘ LINK DO SKLEPU (co 5 komentarz)")
else:
    reply = selected_sentence

print(f"📤 Przygotowana odpowiedź: {reply[:100]}...")

# 8. WYSZUKAJ POSTY DO ODPOWIEDZI
print("\n🔍 Szukam postów...")

# Hashtagi związane z problemami finansowymi (teraz międzynarodowe)
keywords = [
    "debt",
    "creditor", 
    "collection",
    "broke",
    "medical bills",
    "homeless",
    "eviction",
    "food stamps",
    "SNAP",
    "financial help",
    "money stress",
    "emergency cash",
    "unemployed",
    "bill help",
    "rent help",
    "financial crisis",
    "collectors",
    "low income",
    "survival",
    "poverty",
    "medical",
    "bill",
    "bills",
    "cash",
    "money",
    "guide",
    "struggling"
]

selected_keyword = random.choice(keywords)
print(f"   Szukam: #{selected_keyword}")

try:
    # Szukaj postów z hashtagiem
    posts = mastodon.timeline_hashtag(
        hashtag=selected_keyword,
        limit=20
    )
    
    if not posts:
        print("❌ Nie znaleziono postów, próbuję inny hashtag...")
        # Fallback - szukaj po prostu "help"
        posts = mastodon.timeline_hashtag(hashtag="help", limit=15)
    
    if not posts:
        print("❌ Nie znaleziono żadnych postów")
        exit(0)
    
    print(f"✅ Znaleziono {len(posts)} postów")
    
    # Filtruj posty - znajdź z engagement
    good_posts = []
    for post in posts:
        # Pomiń swoje własne posty
        if post['account']['username'] == account['username']:
            continue
        
        # Szukaj postów z engagement
        if post['favourites_count'] > 0 or post['reblogs_count'] > 0:
            good_posts.append(post)
    
    if not good_posts:
        good_posts = posts[:5]  # Weź pierwsze 5
    
    # Wybierz losowy post
    post = random.choice(good_posts)
    
    print(f"\n🎯 Wybrany post od: @{post['account']['username']}")
    print(f"   👍 Polubienia: {post['favourites_count']}")
    print(f"   🔁 Boosty: {post['reblogs_count']}")
    print(f"   💬 Odpowiedzi: {post['replies_count']}")
    content_preview = post['content'].replace('<p>', '').replace('</p>', '')[:80]
    print(f"   📝 Tekst: {content_preview}...")
    
except Exception as e:
    print(f"❌ Błąd wyszukiwania postów: {type(e).__name__}: {e}")
    exit(1)

# 9. OPUBLIKUJ ODPOWIEDŹ
print("\n🔄 Publikuję odpowiedź...")

# Upewnij się że odpowiedź nie jest za długa
if len(reply) > 480:
    reply = reply[:475] + "..."

try:
    # Publikuj
    response = mastodon.status_post(
        status=reply,
        in_reply_to_id=post['id'],
        visibility='public'
    )
    
    if response:
        print(f"✅ OPUBLIKOWANO!")
        print(f"🔗 Link: {response['url']}")
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ZAPISZ DO HISTORII - WAŻNE!
        try:
            with open('posted_toots.json', 'a', encoding='utf-8') as f:
                data = {
                    'date': datetime.now().isoformat(),
                    'url': response['url'],
                    'sentence': selected_sentence,
                    'to': post['account']['username'],
                    'had_link': (counter % 5 == 0),
                    'counter': counter
                }
                f.write(json.dumps(data) + '\n')
                print("📁 Zapisano w posted_toots.json")
        except Exception as e:
            print(f"⚠️  Błąd zapisu historii: {e}")
            
    else:
        print("❌ Nie udało się opublikować")
    
except Exception as e:
    print(f"❌ Błąd publikacji: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("🏁 BOT ZAKOŃCZONY")

# NA KONIEC ZAPISZ UŻYTE SENTENCJE PONOWNIE (na wypadek błędu)
try:
    with open('used_sentences.json', 'w') as f:
        json.dump(history, f, indent=2)
    print("💾 Zapisano użyte sentencje")
except:
    pass

print(f"📊 Użyte sentencje: {len(used_sentences)}/{len(all_sentences)}")
print(f"📈 Licznik: {counter} (następny link za {5 - (counter % 5)})")
print(f"📆 Posty dzisiaj: {limit_data['posts_today'] if 'limit_data' in locals() else '?'}/8")
print("=" * 50)
