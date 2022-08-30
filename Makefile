build:
	docker build -t flask-app .

run:
	docker run -it --rm -p 5000:5000 -v `pwd`/flaskr:/flaskr/ flask-app
