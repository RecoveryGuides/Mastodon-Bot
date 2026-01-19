#!/usr/bin/env python3
"""
🤖 MASTODON FINANCIAL HELPER BOT
Darmowy, bez limitów, 2 posty dziennie
"""

from mastodon import Mastodon
import os
import json
import random
import time
from datetime import datetime, date
import logging

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='🤖 %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class MastodonBot:
    def __init__(self):
        """Inicjalizacja bota Mastodon"""
        print("=" * 50)
        print("🤖 MASTODON FINANCIAL HELPER BOT")
        print("=" * 50)
        
        # Pobierz token i URL z environment variables
        self.access_token = os.environ.get('MASTODON_TOKEN', '')
        self.api_base_url = os.environ.get('MASTODON_URL', 'https://mastodon.social')
        
        if not self.access_token:
            logger.error("❌ BRAK TOKENU MASTODON!")
            logger.error("🔗 Utwórz token na: https://mastodon.social/settings/applications")
            raise ValueError("Missing MASTODON_TOKEN")
        
        # Połącz z Mastodon
        try:
            self.mastodon = Mastodon(
                access_token=self.access_token,
                api_base_url=self.api_base_url
            )
            
            # Sprawdź połączenie
            account = self.mastodon.account_verify_credentials()
            logger.info(f"✅ Połączono jako: @{account['username']}")
            logger.info(f"   📊 Followers: {account['followers_count']}")
            logger.info(f"   🔗 Server: {self.api_base_url}")
            
        except Exception as e:
            logger.error(f"❌ Błąd połączenia z Mastodon: {e}")
            raise
        
        # Inicjalizacja
        self.shop_url = "https://payhip.daveprime"
        self.load_sentences()
        self.load_history()
        
        logger.info("🤖 Bot gotowy do działania!")
    
    def load_sentences(self):
        """Wczytuje sentencje z pliku"""
        try:
            with open('sentences.txt', 'r', encoding='utf-8') as f:
                self.sentences = [line.strip() for line in f if line.strip()]
            logger.info(f"📚 Wczytano {len(self.sentences)} sentencji")
        except FileNotFoundError:
            # Domyślne sentencje
            self.sentences = [
                "When you're broke, track every dollar. It adds up fast.",
                "Call hospital billing TODAY for payment plans.",
                "Food banks exist for a reason. Use them without shame.",
                "Sell plasma - immediate cash when you have nothing.",
                "Cancel ALL subscriptions. Netflix won't feed you.",
                "Rice and beans = $0.50 per meal. Learn to cook them.",
                "Call 211 for emergency help with bills and food.",
                "Your library has free internet, AC, and job resources.",
                "Apply for SNAP benefits online - takes 20 minutes.",
                "Avoid payday loans at ALL costs. 400% interest kills.",
                "Walk or bike everywhere. Cancel car insurance if needed.",
                "Collect aluminum cans. Honest money when desperate.",
                "Learn basic handyman skills. Offer services on Craigslist.",
                "Check church bulletin boards for odd jobs paying cash.",
                "Use food pantry finder: feedingamerica.org/find-food",
                "Medicaid expansion saved millions. Check your eligibility.",
                "Section 8 waiting lists are long. Apply TODAY anyway.",
                "Learn about 'adverse possession' laws in your state.",
                "Homeless shelters often have job placement resources.",
                "Sell old clothes on Poshmark. Every $5 helps."
            ]
            logger.info(f"📚 Używam domyślnych {len(self.sentences)} sentencji")
    
    def load_history(self):
        """Wczytuje historię z pliku"""
        try:
            with open('history.json', 'r') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = {
                'daily_count': 0,
                'last_date': '2000-01-01',
                'used_sentences': [],
                'posted_toots': []
            }
    
    def save_history(self):
        """Zapisuje historię"""
        with open('history.json', 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def check_daily_limit(self):
        """Sprawdza czy można postować dzisiaj"""
        today = date.today().isoformat()
        
        # Jeśli nowy dzień, zresetuj licznik
        if self.history.get('last_date') != today:
            self.history['daily_count'] = 0
            self.history['last_date'] = today
            self.history['used_sentences'] = []
            logger.info("🆕 NOWY DZIEŃ - reset licznika")
        
        # Sprawdź limit (2 posty dziennie)
        if self.history.get('daily_count', 0) >= 2:
            logger.info(f"⏸️ Limit osiągnięty: {self.history['daily_count']}/2")
            return False
        
        return True
    
    def get_fresh_sentence(self):
        """Zwraca świeżą sentencję"""
        # Sprawdź użyte sentencje
        used = set(self.history.get('used_sentences', []))
        available = [s for s in self.sentences if s not in used]
        
        # Jeśli wszystkie użyte, zacznij od nowa
        if not available:
            available = self.sentences
            self.history['used_sentences'] = []
        
        # Wybierz losową sentencję
        sentence = random.choice(available)
        
        # Zapisz jako użyta
        self.history['used_sentences'] = self.history.get('used_sentences', []) + [sentence]
        
        # Ogranicz do 100 ostatnich
        if len(self.history['used_sentences']) > 100:
            self.history['used_sentences'] = self.history['used_sentences'][-100:]
        
        return sentence
    
    def search_posts(self):
        """Wyszukuje posty na Mastodon"""
        # Hashtagi związane z trudnościami finansowymi
        hashtags = [
            'poverty',
            'homeless',
            'unemployment',
            'broke',
            'debt',
            'medicaldebt',
            'foodinsecurity',
            'eviction',
            'financialhelp',
            'survival'
        ]
        
        hashtag = random.choice(hashtags)
        logger.info(f"🔍 Szukam hashtagu: #{hashtag}")
        
        try:
            # Wyszukaj najnowsze posty z hashtagiem
            posts = self.mastodon.timeline_hashtag(
                hashtag=hashtag,
                limit=20
            )
            
            if not posts:
                logger.warning(f"❌ Nie znaleziono postów z #{hashtag}")
                return None
            
            # Filtruj posty z engagement
            good_posts = []
            for post in posts:
                # Pomiń swoje własne posty
                if post['account']['username'] == self.mastodon.account_verify_credentials()['username']:
                    continue
                
                # Pomiń posty z dużą ilością odpowiedzi (może być spam)
                if post['replies_count'] > 10:
                    continue
                
                # Preferuj posty z jakimś engagement
                if post['favourites_count'] > 0 or post['reblogs_count'] > 0:
                    good_posts.append(post)
            
            if not good_posts:
                good_posts = posts[:5]  # Weź pierwsze 5
            
            # Wybierz losowy post
            post = random.choice(good_posts)
            
            logger.info(f"🎯 Znaleziono post od: @{post['account']['username']}")
            logger.info(f"   👍 Polubienia: {post['favourites_count']}")
            logger.info(f"   🔁 Boosty: {post['reblogs_count']}")
            logger.info(f"   💬 Odpowiedzi: {post['replies_count']}")
            
            return post
            
        except Exception as e:
            logger.error(f"❌ Błąd wyszukiwania: {e}")
            return None
    
    def create_reply(self, post):
        """Tworzy odpowiedź na post"""
        # Pobierz świeżą sentencję
        sentence = self.get_fresh_sentence()
        
        # Zwiększ licznik
        self.history['daily_count'] = self.history.get('daily_count', 0) + 1
        current_count = self.history['daily_count']
        
        # Dodaj link co 5 post
        if current_count % 5 == 0:
            reply = f"@{post['account']['acct']} {sentence}\n\n📚 Free survival guide: {self.shop_url}"
        else:
            reply = f"@{post['account']['acct']} {sentence}"
        
        # Sprawdź długość (Mastodon ma limit 500 znaków)
        if len(reply) > 490:
            reply = reply[:485] + "..."
        
        logger.info(f"📝 Odpowiedź ({len(reply)}/500 znaków)")
        logger.info(f"📊 Post #{current_count}/2 dzisiaj")
        
        return reply
    
    def post_reply(self, post, reply):
        """Publikuje odpowiedź na Mastodon"""
        try:
            logger.info("🔄 Publikuję odpowiedź...")
            
            # Opublikuj odpowiedź
            response = self.mastodon.status_post(
                status=reply,
                in_reply_to_id=post['id'],
                visibility='public'
            )
            
            if response:
                # Zapisz w historii
                self.history.setdefault('posted_toots', []).append({
                    'id': response['id'],
                    'url': response['url'],
                    'date': datetime.now().isoformat(),
                    'to': post['account']['username']
                })
                
                # Ogranicz historię do 50 ostatnich
                if len(self.history['posted_toots']) > 50:
                    self.history['posted_toots'] = self.history['posted_toots'][-50:]
                
                logger.info(f"✅ OPUBLIKOWANO!")
                logger.info(f"🔗 {response['url']}")
                
                # Zapisz historię
                self.save_history()
                
                return True
            
        except Exception as e:
            logger.error(f"❌ Błąd publikacji: {e}")
        
        return False
    
    def run(self):
        """Główna funkcja bota"""
        # Sprawdź godzinę
        current_hour = datetime.utcnow().hour
        logger.info(f"🕐 Godzina UTC: {current_hour}:00")
        
        # Bot działa tylko o 14-15 i 22-23 UTC
        if current_hour not in [14, 22]:
            logger.warning(f"⏸️ Nie teraz (wymagane 14 lub 22 UTC)")
            return
        
        # Sprawdź dzienny limit
        if not self.check_daily_limit():
            return
        
        # Wyszukaj post
        post = self.search_posts()
        if not post:
            logger.error("❌ Nie znaleziono odpowiedniego postu")
            return
        
        # Stwórz odpowiedź
        reply = self.create_reply(post)
        
        # Opublikuj odpowiedź
        success = self.post_reply(post, reply)
        
        if success:
            logger.info("🎉 Sukces! Bot zakończył pracę pomyślnie")
        else:
            logger.error("💥 Nie udało się opublikować")

if __name__ == "__main__":
    try:
        bot = MastodonBot()
        bot.run()
    except Exception as e:
        logger.error(f"💥 Krytyczny błąd bota: {e}")
    
    print("=" * 50)
    print("🏁 BOT ZAKOŃCZONY")
    print("=" * 50)
