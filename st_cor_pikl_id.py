import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
from sklearn.model_selection import train_test_split
import joblib

# Chargement du modèle
model_path = 'best_model.joblib'
pipeline = joblib.load(model_path)
classifier_model = pipeline.named_steps['classifier']

# Chargement et préparation des données
df = pd.read_csv('df_final.csv')  # Assurez-vous que 'SK_ID_CURR' est une colonne dans 'df_final.csv'
X = df.drop(columns=['TARGET'])
y = df['TARGET']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation de l'explainer SHAP
explainer = shap.Explainer(classifier_model, X_train)
shap_values = explainer(X_train)

# Interface Streamlit
st.title("Prédiction de Non-Paiement de Prêt avec le Meilleur Modèle")

# Sélection de l'ID du client
client_id = st.number_input("Entrez l'ID du client pour l'explication", min_value=int(X['SK_ID_CURR'].min()), max_value=int(X['SK_ID_CURR'].max()), value=int(X['SK_ID_CURR'].min()))

# Trouver l'observation correspondant à l'ID du client
observation_to_explain = X_test[X_test['SK_ID_CURR'] == client_id]
if not observation_to_explain.empty:
    index_to_explain = observation_to_explain.index[0]  # Récupération de l'indice pour affichage

    # Prédiction et probabilité
    predicted_class = classifier_model.predict(observation_to_explain)[0]
    probability_of_default = classifier_model.predict_proba(observation_to_explain)[0, 1]

    # Affichage des résultats
    st.write(f"Prédiction pour l'ID client {client_id}: {'Non-Paiement' if predicted_class else 'Paiement'}")
    st.write(f"Probabilité de non-paiement: {probability_of_default:.4f}")

    # Décision de prêt
    decision_threshold = 0.428
    loan_decision = "Prêt Accordé" if probability_of_default < decision_threshold else "Prêt Refusé"
    st.write(f"Décision de prêt basée sur le seuil de {decision_threshold}: {loan_decision}")

    # Explications SHAP pour l'observation sélectionnée
    st.header(f"Explications SHAP pour l'ID client {client_id}")
    shap_values_observation = explainer(observation_to_explain)
    fig, ax = plt.subplots()
    shap.plots.waterfall(shap_values_observation[0], max_display=10)
    st.pyplot(fig)
else:
    st.write("ID client non trouvé. Veuillez entrer un ID valide.")
