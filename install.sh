base_image="xavfan/brew-base"
docker container rm hlt-temp-sensor
docker run -ti --name hlt-temp-sensor -v /brewing-controller:/brewing-controller $base_image /brewing-controller/hlt-temp-sensor.py
