base_image="xavfan/brew-base"
dockerd build --tag $base_image .
docker push $base_image
