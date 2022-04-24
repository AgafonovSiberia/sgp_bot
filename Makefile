build:
	docker build -t 811022626/sgp_bot .

run:
	docker run --env-file=.env_dev 811022626/sgp_bot

