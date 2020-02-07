docker stop app_h
docker rm app_h
docker rmi app_h_img
docker build -t app_h_img .
docker run -p 5001:5001 --name app_h --restart always -d app_h_img