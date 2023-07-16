PWD := $(shell pwd)

make run_jupyter:
	docker run -d --name jupyter -p 8888:8888 \
		-v $(PWD)/src:/home/jovyan/work/src \
		base-notebook 
	open -n /Applications/Google\ Chrome.app --args --app="http://localhost:8888/lab"




make build_jupyter:
	docker build -t base-notebook --build-arg FILE_NAME=chat.db .

make stop_jupyter:
	docker stop jupyter
	docker rm jupyter


make run_jupyter_with_terminal:
	docker run -d --name jupyter -p 8888:8888 \
		-v $(PWD)/src:/home/jovyan/work/src \
		base-notebook 
	open -n /Applications/Google\ Chrome.app --args --app="http://localhost:8888/lab"
	docker exec -it jupyter bash
