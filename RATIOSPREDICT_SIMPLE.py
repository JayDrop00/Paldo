import pandas as pd
import joblib

# 1️⃣ Load the trained model and feature names
rf_model = joblib.load("Bankruptcy_Simple.pkl")
feature_columns = joblib.load("bankruptcy_features_69rows.pkl")  # your saved feature order

# 2️⃣ Prepare new data with the same feature names
new_data = pd.DataFrame([[
    0.475698337639546,0.540503706934147,0.840500058715579,0.0108879535477268,0.0085129265976865,0.146264776128428,0.565473497723891
]], columns=feature_columns)  # ✅ match names exactly

# 3️⃣ Predict bankruptcy
prediction = rf_model.predict(new_data)
prediction_proba = rf_model.predict_proba(new_data)

print("Predicted Bankruptcy:", int(prediction[0]))  # 0 = safe, 1 = bankrupt
print("Probability of Bankruptcy:", round(prediction_proba[0][1], 2))
