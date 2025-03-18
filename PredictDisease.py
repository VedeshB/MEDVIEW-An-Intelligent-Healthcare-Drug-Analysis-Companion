import numpy as np
import pandas as pd
import joblib
from sklearn.impute import SimpleImputer










def predictdisease(symptoms):

    def predict_disease(symptoms_list):
        # Convert input symptoms into a feature vector
        user_input = np.zeros(len(feature_columns))  # Initialize all features as 0
        
        for symptom in symptoms_list:
            if symptom in feature_columns:
                user_input[list(feature_columns).index(symptom)] = 1  # Mark symptom as present

        # Reshape input for prediction
        user_input = user_input.reshape(1, -1)

        # Predict the prognosis
        predicted_label = model.predict(user_input)[0]
        predicted_disease = le.inverse_transform([predicted_label])[0]

        return predicted_disease

# Load the saved model
    model = joblib.load('best_model.pkl')

    # Load the label encoder used during training
    train = pd.read_csv("dataset/Training.csv")  # Load training data
    train = train.loc[:, ~train.columns.str.contains('^Unnamed')]  # Remove unnamed columns

    # Recreate LabelEncoder
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    train['prognosis'] = le.fit_transform(train['prognosis'])  # Fit with training labels

    # Get the list of symptoms (features used for training)
    feature_columns = train.drop(columns=['prognosis']).columns

    user_symptoms = symptoms  # Example symptoms

    predicted_disease = predict_disease(user_symptoms)
    print(f"Predicted Disease: {predicted_disease}")
    return predicted_disease

    