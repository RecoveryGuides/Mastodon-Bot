# 🤖 Mastodon Simple Bot

Bot który odpowiada na posty na Mastodon.

## 📋 Wymagania
1. Konto na Mastodon (np. mastodon.social)
2. Access token z uprawnieniami: read:statuses, write:statuses
3. GitHub account

## 🚀 Szybki start
1. Utwórz nowe repo na GitHub
2. Dodaj 5 plików z tej struktury
3. W GitHub Secrets dodaj:
   - `MASTODON_ACCESS_TOKEN` - twój token
   - `MASTODON_BASE_URL` - np. `https://mastodon.social`
4. Bot zacznie działać automatycznie co 30 minut

## ⚙️ Konfiguracja
- Edytuj `sentences.txt` aby dodać swoje sentencje
- Bot NIGDY nie powtarza sentencji w ciągu dnia
- Co 5 komentarz dodaje link do sklepu

## 📊 Pliki generowane automatycznie
- `used_sentences.json` - śledzi użyte sentencje
- `counter.txt` - licznik komentarzy
- `posted_toots.json` - historia opublikowanych odpowiedzi
