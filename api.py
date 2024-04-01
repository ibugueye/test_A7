from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Charger le DataFrame
df = pd.read_csv("df_pred.csv")

@app.route('/prediction', methods=['POST'])
def get_prediction():
    data = request.json
    sk_id_curr = data['SK_ID_CURR']  # Utiliser SK_ID_CURR comme identifiant
    
    # Trouver la prédiction et la probabilité pour SK_ID_CURR
    prediction_row = df.loc[df['SK_ID_CURR'] == sk_id_curr, ['prediction', 'probability']].iloc[0]
    
    # Appliquer le seuil pour décider du résultat
    decision = "Prêt approuvé" if prediction_row['probability'] > 0.39 else "Prêt refusé"
    
    return jsonify({'prediction': prediction_row['prediction'], 'probability': prediction_row['probability'], 'decision': decision})
    Prediction,Probability_of_default

if __name__ == '__main__':
    app.run(debug=True)
