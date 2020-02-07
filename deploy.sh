sudo docker stop app_h
sudo docker rm app_h
sudo docker rmi app_h_img
sudo docker build -t app_h_img .
sudo docker run -p 5001:5001 --name app_h --restart always -d app_h_img