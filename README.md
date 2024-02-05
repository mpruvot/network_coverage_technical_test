# network_coverage_technical_test

- This is a network coverage tool for French telecom operators. It uses an address to fetch network coverage data. 
It can also do revese search by searching for gps data and retrieve an adress from it.

- This project also contain csv_converter CLI to convert the .csv with Lamber93 data into GPS data.

## Installation
### without Docker
  
- ```pip install -r requirements.txt```

- ```./run.sh```

### with Docker
- ```docker build -t coverage-app .```
- ```docker run -p 4000:80 coverage-app ```

- Then you can access the app on http://localhost:4000