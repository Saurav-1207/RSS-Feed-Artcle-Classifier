import spacy

nlp = spacy.load('en_core_web_sm')

def classify_article(title, content):
    title_doc = nlp(title)
    content_doc = nlp(content)
    
    political_crisis_keywords = [
        'protest', 'terror', 'riot', 'violence', 'uprising', 'demonstration',
        'rebellion', 'civil unrest', 'conflict', 'attack', 'insurrection', 
        'politics', 'militant', 'activism', 'disorder', 'turmoil', 'strife', 
        'provocation', 'hostility', 'assault', 'crisis', 'activist', 'situation',
        'rebellious', 'aggression', 'intimidation', 'mobilization', 'turmoil', 
        'disruption', 'skirmish', 'outcry', 'resistance', 'confrontation', 
        'terrorist', 'fanaticism', 'anarchy', 'coup', 'violence', 'opposition',
        'provocateur', 'disturbance', 'lawsuit', 'defamation', 'charges', 
        'criminal', 'shooting', 'settlement', 'debt', 'bipartisan', 'reform', 
        'political', 'GOP', 'election', 'scandal', 'senate', 'democrat', 'republican',
        'rally', 'administration', 'president', 'vice president', 'governor',
        'endorsing', 'voters', 'debate', 'troops', 'fighting', 'defense minister',
        'jailbreak', 'court', 'secret service', 'infiltrated', 'racist', 'remarks', 
        'resign', 'navy', 'criticism', 'defense', 'arrest', 'revolution', 
        'overthrowing', 'dictator', 'collapse', 'chaos',
        # New words from news text
        'strike', 'union', 'negotiations', 'machinist', 'deal', 'false claims',
        'controversy', 'dispute', 'withdrawal', 'labor'
    ]
    
    natural_disaster_keywords = [
        'earthquake', 'flood', 'tsunami', 'hurricane', 'disaster', 
        'natural disaster', 'wildfire', 'avalanche', 'landslide', 'storm',
        'drought', 'tornado', 'cyclone', 'blizzard', 'catastrophe', 
        'seismic', 'cataclysm', 'extreme weather', 'natural phenomenon',
        'hazard', 'devastation', 'volcano', 'epicenter', 'dislocation', 
        'weather event', 'famine', 'disruption', 'inundation', 
        'tsunami', 'aftershock', 'severe', 'destruction', 'emergency',
        'rescue', 'relief', 'recovery', 'contingency', 'rainfall', 'collapses'
    ]
    
    positive_lifestyle_keywords = [
        'happy', 'success', 'achievement', 'celebrate', 'joy', 'positive', 
        'inspiration', 'uplifting', 'victory', 'triumph', 'growth', 
        'progress', 'celebration', 'optimism', 'prosperity', 'satisfaction', 
        'well-being', 'gratitude', 'encouragement', 'hope', 'milestone',
        'love', 'kindness', 'support', 'achievement', 'happiness', 
        'wonder', 'bliss', 'delight', 'excitement', 'fellowship', 
        'friendship', 'community', 'achievement', 'appreciation', 
        'enthusiasm', 'motivation', 'euphoria', 'wellness', 
        'cheerful', 'fulfillment', 'congratulations', 'victorious', 
        'celebratory', 'mother', 'gift', 'thoughtful', 'travel', 
        'pharmacy', 'savings', 'taxes', 'filing', 'compost', 'waste', 
        'cooking', 'dryers', 'sale', 'deals', 'medical', 'health', 
        'retail', 'support', 'financial', 'AI', 'weight loss', 'insurance',
        'healthcare', 'food', 'market', 'technology', 'event', 'community',
        'impact', 'expenses', 'streaming', 'subscription', 'grocery',
        'bitcoin', 'cryptocurrency', 'startup', 'entrepreneur', 'business',
        'tycoon', 'conglomerate', 'artist', 'music', 'concert', 'record',
        'film', 'movie', 'entertainment', 'culture', 'artificial intelligence', 
        'economy', 'innovation', 'chips', 'recalled', 'rebrand', 'nostalgia', 
        'heritage', 'cycling', 'intimacy', 'photography', 'award', 'sports', 
        'football', 'airlines', 'tourism',
        # New words from news text
        'cricket', 'holy', 'temple', 'blessing', 'icon', 'megastar', 'tour',
        'pilot', 'history', 'high speed trains', 'credit card', 'medicare',
        'generic drugs', 'investment', 'stocks', 'electric vehicles'
    ]
    
    def check_keywords(text, keywords):
        return any(word in text.lower() for word in keywords)
    
    if (check_keywords(title_doc.text, political_crisis_keywords) or 
        check_keywords(content_doc.text, political_crisis_keywords)):
        return 'Terrorism / protest / political unrest / riot'
    
    elif (check_keywords(title_doc.text, natural_disaster_keywords) or 
          check_keywords(content_doc.text, natural_disaster_keywords)):
        return 'Natural Disasters'
    
    elif (check_keywords(title_doc.text, positive_lifestyle_keywords) or 
          check_keywords(content_doc.text, positive_lifestyle_keywords)):
        return 'Positive/Lifestyle'
    
    else:
        return 'Others'
