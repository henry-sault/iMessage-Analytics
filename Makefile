PWD := $(shell pwd)

make run_jupyter:
	docker run -d --name jupyter -p 8888:8888 \
		-v $(PWD)/src:/home/jovyan/work/src \
		base-notebook 
	open -n /Applications/Google\ Chrome.app --args --app="http://localhost:8888/lab"
	docker exec -it jupyter bash



make build_jupyter:
	docker build -t base-notebook --build-arg FILE_NAME=chat.db .