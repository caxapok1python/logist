init:
	echo "inited"

grab:
	touch ./tmp/1
	rm ./tmp/*
	python3 grab_image.py

download:
	touch ./tmp/1
	rm ./tmp/*
	scp pi@192.168.2.121:/home/pi/Desktop/tmp/* ./tmp/

line:
	touch ./tmp/1
	rm ./tmp/*
	python3 main.py
