import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title('Consultation de Prédiction de Crédit Client')

# Récupération de la liste des identifiants SK_ID_CURR depuis l'API Flask
response = requests.get("http://127.0.0.1:5000/get_ids")
if response.status_code == 200:
    ids = response.json()
    sk_id_curr = st.selectbox('Choisissez SK_ID_CURR pour obtenir des informations détaillées et une prédiction:', ids)
else:
    st.error("Impossible de charger la liste des identifiants SK_ID_CURR.")
    ids = []
    sk_id_curr = None

if st.button('Obtenir la prédiction') and sk_id_curr:
    data = {'SK_ID_CURR': sk_id_curr}
    response = requests.post("http://127.0.0.1:5000/prediction", json=data)
    
    if response.status_code == 200:
        prediction_data = response.json()
        
        # Affichage des informations et des prédictions
        st.write(f"Prédiction : {prediction_data['prediction']}, Probabilité : {prediction_data['probability']}")
        st.write(f"Décision basée sur le seuil de 0.39 : {prediction_data['decision']}")
        
        st.write(f"Nombre d'enfants du client : {prediction_data['client_children']}")
        st.write(f"Revenu total du client : {prediction_data['client_income']}")
        st.write(f"Montant du crédit du client : {prediction_data['client_credit']}")
        st.write(f"Montant de l'annuité du client : {prediction_data['client_annuity']}")
        
        st.write(f"Moyenne du nombre d'enfants parmi tous les clients : {prediction_data['mean_children']:.2f}")
        st.write(f"Moyenne du revenu total parmi tous les clients : {prediction_data['mean_income']:.2f}")
        st.write(f"Moyenne du montant du crédit parmi tous les clients : {prediction_data['mean_credit']:.2f}")
        st.write(f"Moyenne du montant de l'annuité parmi tous les clients : {prediction_data['mean_annuity']:.2f}")
        
        # Création de la visualisation
        fig, ax = plt.subplots()
        labels = ["Enfants", "Revenu", "Crédit", "Annuité"]
        client_values = [prediction_data['client_children'], prediction_data['client_income'], prediction_data['client_credit'], prediction_data['client_annuity']]
        mean_values = [prediction_data['mean_children'], prediction_data['mean_income'], prediction_data['mean_credit'], prediction_data['mean_annuity']]
        
        x = range(len(labels))  # les labels de l'axe x
        
        ax.bar(x, client_values, width=0.4, label='Client', align='center')
        ax.bar(x, mean_values, width=0.4, label='Moyenne', align='edge')
        
        ax.set_xlabel('Caractéristiques')
        ax.set_ylabel('Valeurs')
        ax.set_title('Comparaison des caractéristiques du client avec les moyennes')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        
        st.pyplot(fig)
    else:
        st.error("Une erreur s'est produite lors de l'obtention de la prédiction.")
