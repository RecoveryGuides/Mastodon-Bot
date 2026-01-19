# 🤖 Mastodon Financial Helper Bot

Bot który pomaga osobom w trudnej sytuacji finansowej na Mastodon.

## ✨ Funkcje
- 2 posty dziennie (14-15 UTC i 22-23 UTC)
- Losowe godziny publikacji
- Wyszukuje posty z hashtagami o trudnościach finansowych
- Odpowiada pomocnymi radami
- Co 5 post link do sklepu
- Darmowe i bez limitów!

## 🚀 Jak uruchomić

### 1. Załóż konto na Mastodon
1. Wejdź na: **https://mastodon.social**
2. Kliknij **"Create account"**
3. Wpisz nazwę: `FinancialHelperBot`
4. Potwierdź email

### 2. Utwórz aplikację i token
1. Po zalogowaniu: **Preferences** → **Development**
2. Kliknij **"New application"**
3. Wpisz:
   - Name: `Financial Helper Bot`
   - Website: `https://github.com/yourusername/mastodon-bot`
   - Scopes: **read:statuses, write:statuses**
4. Kliknij **"Submit"**
5. Skopiuj **Your access token**

### 3. Skonfiguruj GitHub
1. W GitHub repo: **Settings** → **Secrets and variables** → **Actions**
2. Dodaj 2 sekrety:
   - `MASTODON_TOKEN` - twój access token
   - `MASTODON_URL` - `https://mastodon.social`

### 4. Wrzuć kod na GitHub
Utwórz 5 plików:
- `.github/workflows/bot.yml`
- `bot.py`
- `sentences.txt`
- `requirements.txt`
- `README.md`

### 5. Uruchom bota
1. Idź do **Actions**
2. Kliknij **"🤖 Mastodon Bot"**
3. Kliknij **"Run workflow"**

## ⏰ Godziny działania
- **14:15-14:45 UTC** - pierwszy post (losowa minuta)
- **22:15-22:45 UTC** - drugi post (losowa minuta)

## 📊 Statystyki
- 2 posty dziennie
- 60 postów miesięcznie
- Bez limitu API
- Całkowicie darmowe

## 🔧 Edycja sentencji
Edytuj plik `sentences.txt` aby dodać swoje sentencje.
