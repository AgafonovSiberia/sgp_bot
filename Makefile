run:
	docker-compose up --build

stop:
	docker-compose stop

reload:
	make stop
	make clear_data
	make run


clear_data:
	docker-compose down -v

run_dev:
	python -m app
