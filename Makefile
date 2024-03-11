build-and-push-pi: ## not updated/tested arm V7
	docker buildx build --platform linux/arm/v7 --push -t helloabunai/solarman-mqtt .

build-synology: ## my main dev target
	docker buildx build --platform linux/amd64 --push -t helloabunai/solarman-mqtt .

run:
	python run.py