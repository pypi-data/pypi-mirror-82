# litre-demo

基于Sanic实现的在线视频、音乐
 
# 项目启动

pip install -r requirements.txt

gunicorn -c gunicorn.py main:app

# docker启动项目

docker pull litrewu/demo

docker run -d -p 80:52 --name demo-test litrewu/demo
