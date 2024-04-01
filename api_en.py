from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Charger le DataFrame
df = pd.read_csv("df_pred.csv")  # Assurez-vous que le chemin vers votre fichier est correct

@app.route('/get_ids', methods=['GET'])
def get_ids():
    # Renvoyer une liste unique de tous les SK_ID_CURR disponibles
    ids = df['SK_ID_CURR'].unique().tolist()
    return jsonify(ids)

@app.route('/prediction', methods=['POST'])
def get_prediction():
    data = request.json
    sk_id_curr = data['SK_ID_CURR']
    
    if sk_id_curr not in df['SK_ID_CURR'].values:
        return jsonify({'error': 'SK_ID_CURR non trouvé'}), 404
    
    prediction_row = df.loc[df['SK_ID_CURR'] == sk_id_curr].iloc[0]
    
    decision = "Prêt approuvé" if prediction_row['probability'] > 0.39 else "Prêt refusé"
    
    client_children = prediction_row['CNT_CHILDREN']
    mean_children = df['CNT_CHILDREN'].mean()
    
    client_income = prediction_row['AMT_INCOME_TOTAL']
    mean_income = df['AMT_INCOME_TOTAL'].mean()
    
    client_credit = prediction_row['AMT_CREDIT']
    mean_credit = df['AMT_CREDIT'].mean()
    
    client_annuity = prediction_row['AMT_ANNUITY']
    mean_annuity = df['AMT_ANNUITY'].mean()
    
    return jsonify({
        'prediction': prediction_row['prediction'], 
        'probability': prediction_row['probability'], 
        'decision': decision,
        'client_children': int(client_children),
        'mean_children': float(mean_children),
        'client_income': float(client_income),
        'mean_income': float(mean_income),
        'client_credit': float(client_credit),
        'mean_credit': float(mean_credit),
        'client_annuity': float(client_annuity),
        'mean_annuity': float(mean_annuity),
        'comparison': {
            'children': f"Le nombre d'enfants du client est {'au-dessus' if client_children > mean_children else 'en dessous' if client_children < mean_children else 'égal à'} la moyenne.",
            'income': f"Le revenu total du client est {'au-dessus' if client_income > mean_income else 'en dessous' if client_income < mean_income else 'égal à'} la moyenne.",
            'credit': f"Le montant du crédit du client est {'au-dessus' if client_credit > mean_credit else 'en dessous' if client_credit < mean_credit else 'égal à'} la moyenne.",
            'annuity': f"Le montant de l'annuité du client est {'au-dessus' if client_annuity > mean_annuity else 'en dessous' if client_annuity < mean_annuity else 'égal à'} la moyenne."
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
