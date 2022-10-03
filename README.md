# Cache on redis cluster with 1 master and 2 slaves managed by 3 sentinel
Probabilistic cache logic: 
1. We use the same TTL for object
2. App begin analyze probabilistic before 10% of TTL to end
3. Calculate Random probability between (TTL - Last TTL) and (TTL * 0.1)
4. If Random probability higher or equal TTL * 0.05, call source for data
 
 
 
## 1. Run docker container with 3 redis and 3 sentinel container
`docker-compose up` 

## 2. Read app help
`python app.py --help`

## 3. Run few app  paralell in diferent terminals
```
python app.py -i 1 -s 1
python app.py -i 2 -s 1
python app.py -i 3 -s 1
```

## 4. See how probabilistic cache working
App with ID = 1 calculate Random probability but it lower than decision border, and data was taken from cache. 
![image](https://user-images.githubusercontent.com/52753625/193594373-b16fd7a3-60a7-4bca-86d9-24fc62092859.png) 
 
App with ID = 2 get refreshed data by other app, and new data was taken from cache. 
![image](https://user-images.githubusercontent.com/52753625/193594740-95ae3bf0-34e6-492a-9ddb-b5bdd0c8af0c.png) 
 
App with ID = 3 calculate Random probability higher than decision border and get new data from source. 
![image](https://user-images.githubusercontent.com/52753625/193595009-e582e0eb-9ac2-4755-909e-a7985a232a16.png) 
