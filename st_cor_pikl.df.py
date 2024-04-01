import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
from sklearn.model_selection import train_test_split
import joblib  # Pour charger le modèle

# Chargement du modèle sérialisé
model_path = 'best_model.joblib'
pipeline = joblib.load(model_path)

# Extraire le modèle de classification du pipeline
classifier_model = pipeline.named_steps['classifier']

# Préparation des données (comme précédemment)
df = pd.read_csv('df_final.csv')  # Remplacez par votre chemin de fichier correct
X = df.drop(columns=['TARGET'])
y = df['TARGET']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialiser l'explainer SHAP avec le modèle extrait
explainer = shap.Explainer(classifier_model, X_train)
# Calcul des valeurs SHAP pour l'ensemble d'entraînement (pour les explications globales)
shap_values = explainer(X_train)

# Prédictions et probabilités pour tout le jeu de données X_test
predictions = classifier_model.predict(X_test)
probabilities = classifier_model.predict_proba(X_test)[:, 1]  # Probabilités de la classe positive

# Ajouter les prédictions et probabilités au dataframe X_test pour visualisation
X_test_with_predictions = X_test.copy()
X_test_with_predictions['Prediction'] = predictions
X_test_with_predictions['Probability_of_default'] = probabilities

# Si vous voulez travailler avec le dataframe original incluant les prédictions:
df_test_with_predictions = df.iloc[X_test.index].copy()
df_test_with_predictions['Prediction'] = predictions
df_test_with_predictions['Probability_of_default'] = probabilities

# Maintenant, vous pouvez afficher le dataframe avec les prédictions et probabilités ajoutées
st.write(df_test_with_predictions)
