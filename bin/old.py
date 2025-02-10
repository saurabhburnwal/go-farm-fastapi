import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('old.csv')

# Drop unnecessary columns
df.drop(['Dist Name'], axis=1, inplace=True)  # Assuming 'Dist Name' is not needed for prediction

# Encode categorical variables
label_encoder = LabelEncoder()
df['State Code'] = label_encoder.fit_transform(df['State Name'])

# Select relevant features and define target variables for each crop
features = ['State Code', 'RICE AREA (1000 ha)', 'WHEAT AREA (1000 ha)', 'MAIZE AREA (1000 ha)', 'BARLEY AREA (1000 ha)']

# Define target variables for each crop
y_rice = df['RICE PRODUCTION (1000 tons)']
y_wheat = df['WHEAT PRODUCTION (1000 tons)']
y_maize = df['MAIZE PRODUCTION (1000 tons)']
y_barley = df['BARLEY PRODUCTION (1000 tons)']

# Prepare input data for each crop
X = df[features]

# Split data into training and testing sets for each crop
X_train_rice, X_test_rice, y_train_rice, y_test_rice = train_test_split(X, y_rice, test_size=0.2, random_state=42)
X_train_wheat, X_test_wheat, y_train_wheat, y_test_wheat = train_test_split(X, y_wheat, test_size=0.2, random_state=42)
X_train_maize, X_test_maize, y_train_maize, y_test_maize = train_test_split(X, y_maize, test_size=0.2, random_state=42)
X_train_barley, X_test_barley, y_train_barley, y_test_barley = train_test_split(X, y_barley, test_size=0.2, random_state=42)

# Train separate Random Forest models for each crop
model_rice = RandomForestRegressor(n_estimators=100, random_state=42)
model_rice.fit(X_train_rice, y_train_rice)

model_wheat = RandomForestRegressor(n_estimators=100, random_state=42)
model_wheat.fit(X_train_wheat, y_train_wheat)

model_maize = RandomForestRegressor(n_estimators=100, random_state=42)
model_maize.fit(X_train_maize, y_train_maize)

model_barley = RandomForestRegressor(n_estimators=100, random_state=42)
model_barley.fit(X_train_barley, y_train_barley)

# Example input data for prediction
new_data = {
    'State Code': label_encoder.transform(['Rajasthan'])[0],
    'RICE AREA (1000 ha)': 100,   # in hectares
    'WHEAT AREA (1000 ha)': 100,  # in hectares
    'MAIZE AREA (1000 ha)': 100,  # in hectares
    'BARLEY AREA (1000 ha)': 100   # in hectares
}

# Convert input data to DataFrame
input_df = pd.DataFrame([new_data])

# Make predictions for each crop using Random Forest models
predicted_rice_yield = model_rice.predict(input_df[features])
predicted_wheat_yield = model_wheat.predict(input_df[features])
predicted_maize_yield = model_maize.predict(input_df[features])
predicted_barley_yield = model_barley.predict(input_df[features])

# Display predicted yields for each crop
print("Predicted Rice Yield (1000 tons):", predicted_rice_yield[0])
print("Predicted Wheat Yield (1000 tons):", predicted_wheat_yield[0])
print("Predicted Maize Yield (1000 tons):", predicted_maize_yield[0])
print("Predicted Barley Yield (1000 tons):", predicted_barley_yield[0])

# Evaluate the Random Forest models using RMSE on the test set
rice_rmse = mean_squared_error(y_test_rice, model_rice.predict(X_test_rice), squared=False)
wheat_rmse = mean_squared_error(y_test_wheat, model_wheat.predict(X_test_wheat), squared=False)
maize_rmse = mean_squared_error(y_test_maize, model_maize.predict(X_test_maize), squared=False)
barley_rmse = mean_squared_error(y_test_barley, model_barley.predict(X_test_barley), squared=False)

print("Rice RMSE:", rice_rmse)
print("Wheat RMSE:", wheat_rmse)
print("Maize RMSE:", maize_rmse)
print("Barley RMSE:", barley_rmse)