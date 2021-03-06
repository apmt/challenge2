```
git clone https://github.com/apmt/challenge2
```
# How to run with docker
Copy the **input csv file** into **challenge2/INPUT** and go to **challenge2** directory:
```
cd challenge2
mv <csv_path> challenge2/INPUT
```
Start docker (on ubuntu):
```
sudo dockerd
```
Build and run image iteratively:
```
docker image build -t ana .
docker container run -it ana
```

Run the script on docker image **cli**:
```
sudo python main.py
rm -f INPUT/*.csv
```
Check database on docker image **cli**:
```
sqlite3 anapaula.db
> select * from trips;
> select * from trip_clusters;
```
Insights
```
python insights.py -r "<region_name>"
python insights.py -bb "<lat_min>,<long_min>;<lat_max>,<long_max>
python insights.py -bb "-90,-180;90,180"
```

**WARNING:** Kill all process/containers and delete all images
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```
# How to setup and run without docker on linux/ubuntu/WSL

## Requirements

#### How to install requirements on linux/ubuntu/WSL

python:3.8
```
sudo apt install python3
sudo apt install python-is-python3
```
sqlite3
```
sudo apt install sqlite3
```

## Run on linux/ubuntu/WSL

Go to the **challenge2** directory and copy the input csv file into **challenge2/INPUT**
```
cd challenge2
python -m venv env
source env/bin/activate
pip install -r requirements.txt
mv <csv_path> challenge2/INPUT
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
