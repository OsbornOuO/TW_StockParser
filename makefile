APP=tw_stock_parser
IMAGE=asia.gcr.io/tw-stock-241407/${APP}:dev

default:
	@echo subcommands: docker-push docker-clean

docker-build:
	docker build -t ${IMAGE} .

docker-push: docker-build
	docker push ${IMAGE}

docker-clean:
	-docker rm -f ${APP}
	docker images | grep none | awk '{print $3}' | xargs docker rmi