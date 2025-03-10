
remove:
	docker rmi tax-agent:latest

build_local:
	docker build -f api.dockerfile -t tax-agent:latest .

run_local:
	docker run --env-file .env --rm --name tax_agent_container \
	-v .:/app -it tax-agent:latest /bin/bash

run_api:
	docker run --env-file .env --rm --name tax_agent_container \
	-v .:/app -p 8086:8086 -it tax-agent:latest \
	uvicorn api.main:app --host 0.0.0.0 --port 8086 --reload --log-config=log_config.yaml

compose_up:
	docker compose build && docker compose up