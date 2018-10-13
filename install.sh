base_image="xavfan/brew-base"
docker container rm hlt-temp-sensor
docker run -ti --name hlt-temp-sensor $base_image
