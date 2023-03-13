# Load the libraries
import boto3
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from joblib import load

from modules import extract
from modules.instant import CanHo

# FastAPI instance
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download file from aws s3 bucket
session = boto3.Session(
    aws_access_key_id='AKIAUAIYXGJKKVVPD45I',
    aws_secret_access_key='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',
)
s3 = session.resource(service_name='s3')
bucket = s3.Bucket('htdf-model-pricing-apartment')

# key_on_s3_model = 'model-2022-11-04 1507/'
# key_on_s3_model = 'model-2022-11-10-1628/'
key_on_s3_model = 'model-2022-12-07-1154/'
bucket.download_file(key_on_s3_model + 'model.sav', './model/model.sav')

# key_on_s3_vec = 'vectorize-2022-11-04 1507/'
# key_on_s3_vec = 'vectorize-2022-11-10-1628/'
key_on_s3_vec = 'vectorize-2022-12-07-1154/'
bucket.download_file(key_on_s3_vec + 'vectorize.sav', './vectorize/vectorize.sav')

# key_on_s3_data = 'data-2022-11-04 1506/'
key_on_s3_data = 'data-2022-12-07-1154/'
bucket.download_file(key_on_s3_data + 'data.csv', './data/data.csv')

model = load('./model/model.sav')
vectorize = load('./vectorize/vectorize.sav')
data = pd.read_csv('./data/data.csv')
########################################################################

# Default route
@app.get("/")
async def root():
    return {"message": "Welcome to Model Pricing Apartment"}


# Define the route to the price predictor
@app.post("/predict_price")
async def predict_price(ch: CanHo):

    if(not ch):
        raise HTTPException(status_code=400, 
                            detail = "Please Provide a valid apartment's information")
    
    try:
        vectorize.transform(extract.json_to_input(ch))
    except:
        raise HTTPException(status_code=404,
                            detail="Not found result, please check your input.")
    else:
        input = vectorize.transform(extract.json_to_input(ch))
        
        output = model.predict(input)[0]
        
        output = output * ( 1 + extract.consider_floor(ch) )
        output = output * ( 1 + extract.consider_direction(ch) )
        output = output * ( 1 + extract.consider_corner(ch) )

        return {
            'suggested price (tr/m2)': output / ch.area,
            'suggested price (tr)': output 
        }
