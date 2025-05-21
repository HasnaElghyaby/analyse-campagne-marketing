# Bibliothèques nécessaires
# pip install pandas nltk pyodbc sqlalchemy

import pandas as pd
import pyodbc
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download le lexique VADER si ce n'est pas déjà fait
nltk.download('vader_lexicon', quiet=True)

def obtenir_connexion_sql():
    #Créer et retourner une connexion à la base de données.
    conn_str = (
        "Driver={SQL Server};"
        r"Server=your-server-name;"
        "Database=your-database-name;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def recuperer_avis_clients():
    #Récupérer les avis clients depuis la base de données SQL sous forme de DataFrame.
    requete = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM fact_customer_reviews"
    with obtenir_connexion_sql() as conn:
        df = pd.read_sql(requete, conn)
    return df

# Initialiser l'analyseur de sentiment VADER une seule fois
sia = SentimentIntensityAnalyzer()

def calculer_score_sentiment(texte):
    #Retourner le score composé de sentiment pour un texte donné.
    return sia.polarity_scores(texte)['compound']

def categoriser_sentiment(score, note):
    if score > 0.05:
        if note >= 4:
            return 'Positif'
        elif note == 3:
            return 'Positif Mixte'
        else:
            return 'Négatif Mixte'
    elif score < -0.05:
        if note <= 2:
            return 'Négatif'
        elif note == 3:
            return 'Négatif Mixte'
        else:
            return 'Positif Mixte'
    else:
        if note >= 4:
            return 'Positif'
        elif note <= 2:
            return 'Négatif'
        else:
            return 'Neutre'

def categoriser_score(score):
    #Classer le score de sentiment dans des intervalles descriptifs.
    if score >= 0.5:
        return '0.5 à 1.0'
    elif 0.0 <= score < 0.5:
        return '0.0 à 0.49'
    elif -0.5 <= score < 0.0:
        return '-0.49 à 0.0'
    else:
        return '-1.0 à -0.5'

def main():
    # Charger les données
    df = recuperer_avis_clients()
    
    # Calculer les scores de sentiment pour chaque avis
    df['ScoreSentiment'] = df['ReviewText'].apply(calculer_score_sentiment)
    
    # Catégoriser le sentiment en fonction du score et de la note
    df['CategorieSentiment'] = df.apply(
        lambda ligne: categoriser_sentiment(ligne['ScoreSentiment'], ligne['Rating']), axis=1
    )
    
    # Classer les scores dans des buckets
    df['BucketSentiment'] = df['ScoreSentiment'].apply(categoriser_score)
    
    # Afficher un aperçu des résultats
    print(df.head())
    
    # Enregistrer les résultats dans un fichier CSV
    df.to_csv('fact_customer_reviews_with_sentiment.csv', index=False)
    
if __name__ == "__main__":
    main()
