base_image="xavfan/brew-base"
wd="/brewing-controller"


create_container () {
local objname=$1
local objscript="$1"."py"
docker container rm $objname -f
docker run -d -it --privileged --name $objname -w $wd -v $wd:$wd $base_image python $objscript
#docker run -ti --privileged --name $objname -w $wd -v $wd:$wd $base_image python $objscript $objargs

}


#create_container "hlt-temp-sensor" "sensor_pt100" "22"
#create_container "hlt-heater" "actor" "12 1"
create_container "hlt_temp_sensor"
create_container "hlt_temp_controller"
