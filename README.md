# Requirements

### How to install requirements on linux/ubuntu/WSL

python:3.8
```
sudo apt install python3
sudo apt install python-is-python3
```
sqlite3
```
sudo apt install sqlite3
```

# How to run without docker on linux/ubuntu/WSL

Go to the jobsity_2 directory and copy the input csv file into jobsity_2/INPUT
```
cd jobsity_2
python -m venv env
source env/bin/activate
pip install -r requirements.txt
mv <csv_path> jobsity_2/INPUT
```
Run main.py and delete the input files
```
sudo python main.py
rm -f INPUT/*.csv
```
Check the database
```
sqlite3 anapaula.db
> select * from trips;
> select * from trip_clusters;
```

# How to run with docker
Start docker (on ubuntu):
```
sudo dockerd
```
Build and run image iteratively:
```
docker image build -t ana .
docker container run -it ana
```

Run the script on image cli:
```
sudo python main.py
rm -f INPUT/*.csv
sqlite3 anapaula.db
> select * from trips;
> select * from trip_clusters;
```


**WARNING:** Kill all process/containers and delete all images
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```