base_image="xavfan/brew-base"
wd="/brewing-controller"

objname="hlt-temp-sensor"
objscript="$objname"".py"
docker container rm hlt-temp-sensor
docker run -ti --name $objname -w $wd -v $wd:$wd $base_image python $objscript
