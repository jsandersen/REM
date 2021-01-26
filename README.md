# REM: Efficient Real-time Moderation of Online Forums  
  
## Technologies  
- Flask  
- Vue.js  
- D3.js  
- MongoDB  
- Docker  
  
## Local Deployment  
  
### 1. Setup REM  
  
REM is dockerized, for local deployment run:  
````  
docker-compose up  
````  
  
#### Ports  
- REM UI: http://localhost:8080/  
- Swagger UI: http://localhost:5050/db/  
- MongoDB: http://localhost:27017  
  
### 2. Data Import  
  
Run the data import script to initialize the database and import dummy data. 
The Script can be used as a starting point, to import other data sources. 
````  
python ./data_import/mongo_dummy_import.py  
````  
#### Requirements  
- pymongo

### 3. Login

- usr: testuser
- pwd: testuser
