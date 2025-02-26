
remove:
	docker rmi tax-agent:latest

build_local:
	docker build -f api.dockerfile -t tax-agent:latest .

run_local:
	docker run --env-file .env --rm --name tax_agent_container \
	-v .:/app -it tax-agent:latest /bin/bash