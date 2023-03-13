# 
FROM python:3.10

# 
WORKDIR /model_pricing_apartment_v2/

# 
COPY requirements.txt ./requirements.txt
COPY ./model/ ./model/
COPY ./vectorize/  ./vectorize/
COPY ./data/ ./data/


# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY ./app/main.py ./app/
COPY ./modules/*.py ./modules/

# 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
