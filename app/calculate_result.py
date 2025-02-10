import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# app = FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def home():
#     return {"Data":"hello world"}

# print("Server started on http://127.0.0.1:8000/")

# print("You can test the model using the following url: http://127.0.0.1:8000/test-model?state=Chhattisgarh&type=rice&area=100")

print("Training.....")

# Load dataset
df = pd.read_csv('production.csv')

# Drop unnecessary columns
df.drop(['Dist Name'], axis=1, inplace=True)  # Assuming 'Dist Name' is not needed for prediction

# Encode categorical variables
label_encoder = LabelEncoder()
label_encoder2 = LabelEncoder()
df['State Code'] = label_encoder.fit_transform(df['State Name'])
df['Type'] = label_encoder2.fit_transform(df['Type'])
# Select relevant features and define target variables for each crop
features = ['State Code', 'Type', 'Area']
Y =  df['Production']
# Define target variables for each crop



  
# Prepare input data for each crop
X = df[features]

# Split data into training and testing sets for each crop
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# Train separate Random Forest models for each crop
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)



# Example input data for prediction
new_data = {
    'State Code': label_encoder.transform(['Chhattisgarh'])[0],
    'Type':label_encoder2.transform(['RICE'])[0],
    'Area': 781   # in hectares
}

# Convert input data to DataFrame
input_df = pd.DataFrame([new_data])

# Make predictions for each crop using Random Forest models
predicted_value = model.predict(input_df[features])



print("Predicted Output", predicted_value[0])

true_values = y_test
predicted_values = model.predict(X_test)

rmse = root_mean_squared_error(true_values, predicted_values)
percentageError = mean_absolute_percentage_error(true_values , predicted_values)

mae = mean_absolute_error(y_test, predicted_values)

# Calculate error in percentage
percentage_error = ( (mae * true_values.shape[0]) / sum(true_values)) * 100

print("rmse", rmse)
print("mae", mae)
print("percentageError", f"{round(percentage_error)}%")


def calculate_result(state:str, type:str, area:float):

    try:
        new_data = {
            'State Code': label_encoder.transform([state.title()])[0],
            'Type':label_encoder2.transform([type.upper()])[0],
            'Area': area
        }
        input_df = pd.DataFrame([new_data])
        predicted_value = model.predict(input_df[features])
        return predicted_value[0]

    except ValueError as ve:
         print(ve)
         print("Invalid state")
         return {"Error": "Invalid State or type or area"}

res = calculate_result("punjab","rice",2000000000)
print("Test Res:")
print(res)

res2 = calculate_result("punjab","rice",200000000000000000000000000000000)
print("Test Res2:")
print(res2)