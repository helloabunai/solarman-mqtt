build-and-push-pi: ## not updated/tested arm V7
	docker buildx build --platform linux/arm/v7 --push -t helloabunai/solarman-mqtt .

build-mac: ## developed on M2 mac
	docker buildx build --platform linux/arm64/v8 --push -t helloabunai/solarman-mqtt .

build-synology: ## will run on synology NAS
	docker buildx build --platform linux/amd64 --push -t helloabunai/solarman-mqtt .

local-dev:
	docker build -t solarman-mqtt ./ && docker run solarman-mqtt:latest

run:
	python3 run.py