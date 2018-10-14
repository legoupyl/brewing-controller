base_image="xavfan/brew-base"
wd="/brewing-controller"

objname="hlt-temp-sensor"
objtype="sensor_pt100"
objargs="$objname 13"


objscript="$objtype"".py"
docker container rm hlt-temp-sensor
docker run -ti --privileged --name $objname -w $wd -v $wd:$wd $base_image python $objscript $objargs
