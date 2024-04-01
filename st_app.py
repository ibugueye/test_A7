import streamlit as st
import requests

st.title('Consultation de Prédiction de Crédit Client')

# Récupérer la liste des identifiants SK_ID_CURR depuis l'API Flask
response = requests.get("http://127.0.0.1:5000/get_ids")
if response.status_code == 200:
    ids = response.json()
    # Permettre à l'utilisateur de choisir un identifiant depuis un selectbox
    sk_id_curr = st.selectbox('Choisissez SK_ID_CURR pour obtenir la prédiction et la probabilité:', ids)
else:
    st.error("Impossible de charger la liste des identifiants SK_ID_CURR.")
    ids = []
    sk_id_curr = None

# Bouton pour obtenir la prédiction
if st.button('Obtenir la prédiction') and sk_id_curr:
    # Préparer les données pour la requête API
    data = {'SK_ID_CURR': sk_id_curr}
    
    # Envoyer une requête à l'API Flask pour obtenir la prédiction
    response = requests.post("http://127.0.0.1:5000/prediction", json=data)
    
    if response.status_code == 200:
        prediction_data = response.json()
        decision = "Prêt approuvé"  if prediction_data['probability'] > 0.39 else "Prêt refusé"
        st.write(f"Prédiction : {prediction_data['prediction']}, Probabilité : {prediction_data['probability']}")
        st.write(f"Décision basée sur le seuil de 0.39 : {decision}")
    else:
        st.error("Une erreur s'est produite lors de l'obtention de la prédiction.")
