test:
	pytest

run: build 
	echo starting
	docker compose -f ./docker-compose.yml up

build:
	echo building
	docker build -t investment-tracker .
	docker compose -f ./docker-compose.yml build 
	echo building finished


run-dev: build-dev
	echo starting development
	docker compose -f ./docker-compose.dev.yml up

build-dev:
	echo building development
	docker build -t investment-tracker-dev .
	docker compose -f ./docker-compose.dev.yml build 
	echo building finished
