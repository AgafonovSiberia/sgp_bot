
build:
	docker build -t sgp_bot .

run:
	docker run --env-file=.env_dev sgp_bot


