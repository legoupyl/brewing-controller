base_image="xavfan/brew-base"
dockerd build --name $base_image .
docker push $base_image
