import pandas as pd
from google.cloud import bigquery

# 1. अपनी नई मुंबई बकेट और फाइल का नाम सेट करें
BUCKET_NAME = "यहाँ_अपनी_नई_मुंबई_बकेट_का_नाम_लिखें" # <-- यहाँ अपनी नई बकेट का नाम टाइप करें
FILE_NAME = "supply_chain_logistics_data.csv"
csv_file_path = f"gs://{BUCKET_NAME}/{FILE_NAME}"

print(f"नई मुंबई बकेट से डेटा लोड किया जा रहा है: {csv_file_path}")
df = pd.read_csv(csv_file_path)

# 2. डेटा क्लीनिंग (सप्लाई चेन लॉजिक)
df['ActualDeliveryDate'] = df['ActualDeliveryDate'].replace('N/A', None)
df = df[(df['ShippingCost_INR'] >= 0) & (df['Weight_KG'] > 0)]

# 3. GCP वेरिएबल्स
PROJECT_ID = "lofty-proton-512605-u0"
DATASET_ID = "supply_chain_data_mumbai"  # मुंबई के लिए नया डेटासेट नाम
TABLE_ID = "cleaned_shipments_data"

client = bigquery.Client(project=PROJECT_ID)

# 4. फिक्स: डेटासेट की लोकेशन को भी आपकी नई बकेट के हिसाब से 'asia-south1' सेट कर दिया है
dataset_ref = client.dataset(DATASET_ID)
dataset = bigquery.Dataset(dataset_ref)
dataset.location = "asia-south1"  # <-- यह आपकी मुंबई बकेट से मैच करेगा

try:
    client.get_dataset(dataset_ref)
    print(f"डेटासेट '{DATASET_ID}' पहले से मौजूद है।")
except:
    print(f"डेटासेट '{DATASET_ID}' नहीं मिला। नया डेटासेट बनाया जा रहा है...")
    client.create_dataset(dataset)
    print(f"डेटासेट '{DATASET_ID}' सफलतापूर्वक बन गया है।")

# 5. डेटा को BigQuery में लोड करना
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

print("डेटा BigQuery में अपलोड किया जा रहा है...")
job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
job.result()  # अपलोड पूरा होने का इंतजार करें

print(f"बधाई हो भाई! टेबल '{TABLE_ID}' सफलतापूर्वक BigQuery में लोड हो गई है।")
