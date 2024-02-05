# network_coverage_technical_test

- This is a network coverage tool for French telecom operators. It uses an address to fetch network coverage data. 
It can also do revese search by searching for gps data and retrieve an adress from it.

- This project also contain csv_converter CLI which  Convert a CSV file with Lambert93 coordinates to a new file with GPS coordinates.    

  - Usage :                                                      
     - ```cd data```
     - ```csv_converter.py SOURCE DEST   ```

## Installation
### without Docker
  
- ```pip install -r requirements.txt```

- ```./run_app.sh```

### with Docker
- ```docker build -t coverage-app .```
- ```docker run -p 4000:80 coverage-app ```

- Then you can access the app on http://localhost:4000

## Tests
- ```./run_tests.sh```


### Swagger 

<img width="1382" alt="Screenshot 2024-02-05 at 07 57 11" src="https://github.com/mpruvot/network_coverage_technical_test/assets/132161864/ee4d558b-45b2-4ccb-8b47-22831290cac0">

<img width="1378" alt="Screenshot 2024-02-05 at 07 57 25" src="https://github.com/mpruvot/network_coverage_technical_test/assets/132161864/d0974875-d4da-4f67-9c17-2ca83254de7a">


