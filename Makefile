DIPLOMA_BACKEND_IMAGE ?= diploma-backend:local

.EXPORT_ALL_VARIABLES:
.DEFAULT_GOAL := run

docker-build:
	@docker rmi $(DIPLOMA_BACKEND_IMAGE) 2> /dev/null || true
	@docker build --target=local -t $(DIPLOMA_BACKEND_IMAGE) .

# Start an app with its services on local machine in debug mode
run: docker-build
	@docker compose up

# The same as run command but in daemon mode
rund: docker-build
	@docker compose up -d

# Stop and remove Photo awards containers
rm:
	@docker compose stop
	@docker compose rm -f

down:
	@docker compose down --remove-orphans -v

# Run linting and mypy checks
check: docker-build
	@docker compose run --rm backend sh -c 'flake8 && mypy .'

# Go inside application running container. Note that the app should be after stared via `make run`
sh:
	@docker compose exec backend bash

# Stop all running services that run by the make run command
stop:
	@docker compose stop
