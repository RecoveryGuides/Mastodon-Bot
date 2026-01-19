#!/usr/bin/env python3
"""
🤖 MASTODON SIMPLE BOT
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

print("=" * 50)
print("🤖 MASTODON SIMPLE BOT")
print("=" * 50)

# 1. KONFIGURACJA MASTODON
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

# 2. WCZYTAJ SENTENCJE
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

# 3. WCZYTAJ HISTORIĘ UŻYTYCH SENTENCJI
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

# 4. ZNAJDŹ NIEUŻYTE SENTENCJE
available_sentences = [s for s in all_sentences if s not in used_sentences]

if not available_sentences:
    print("🔄 Wszystkie sentencje użyte dzisiaj, resetuję...")
    used_sentences = set()
    history['used'] = []
    available_sentences = all_sentences

print(f"🎯 Dostępnych sentencji: {len(available_sentences)}")

# 5. WYBIERZ LOSOWĄ SENTENCJĘ
selected_sentence = random.choice(available_sentences)

# Dodaj do użytych
used_sentences.add(selected_sentence)
history['used'] = list(used_sentences)

# Zapisz historię
with open('used_sentences.json', 'w') as f:
    json.dump(history, f, indent=2)

print(f"📝 Wybrana sentencja: {selected_sentence[:80]}...")

# 6. OBSŁUGA LICZNIKA DLA LINKÓW
try:
    with open('counter.txt', 'r') as f:
        counter = int(f.read().strip())
except:
    counter = 0

counter += 1
print(f"📊 Licznik komentarzy: {counter}")

# Co 5 komentarz dodaj link
SHOP_URL = "https://www.payhip.com/daveprime"

if counter % 5 == 0:
    reply = f"{selected_sentence}\n\n🛒 More help: {SHOP_URL}"
    print("🎁 DODAJĘ LINK DO SKLEPU (co 5 komentarz)")
else:
    reply = selected_sentence

# Zapisz licznik
with open('counter.txt', 'w') as f:
    f.write(str(counter))

print(f"📤 Przygotowana odpowiedź: {reply[:100]}...")

# 7. WYSZUKAJ POSTY DO ODPOWIEDZI
print("\n🔍 Szukam postów...")

# Hashtagi związane z Twoimi produktami
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
    "emergency cash"
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
    print(f"   📝 Tekst: {post['content'][:100].replace('<p>', '').replace('</p>', '')}...")
    
    # 8. OPUBLIKUJ ODPOWIEDŹ
    print("\n🔄 Publikuję odpowiedź...")
    
    # Upewnij się że odpowiedź nie jest za długa (Mastodon limit ~500 znaków)
    if len(reply) > 480:
        reply = reply[:475] + "..."
    
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
        
        # Zapisz do historii postów
        try:
            with open('posted_toots.json', 'a') as f:
                data = {
                    'date': datetime.now().isoformat(),
                    'url': response['url'],
                    'sentence': selected_sentence,
                    'to': post['account']['username'],
                    'had_link': (counter % 5 == 0)
                }
                f.write(json.dumps(data) + '\n')
        except:
            pass
            
    else:
        print("❌ Nie udało się opublikować")
    
except Exception as e:
    print(f"❌ Błąd: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("🏁 BOT ZAKOŃCZONY")
print(f"📊 Użyte sentencje: {len(used_sentences)}/{len(all_sentences)}")
print(f"📈 Licznik linków: {counter} (następny link przy {5 - (counter % 5)})")
print("=" * 50)
