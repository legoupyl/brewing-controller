base_image="xavfan/brew-base"
docker build --tag $base_image .
docker push $base_image
