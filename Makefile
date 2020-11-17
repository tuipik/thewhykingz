build:
	@docker build -t tuipik/thewhykingz:latest .
run:
	@docker-compose up
test:
	@docker-compose run app sh -c "python -m pytest"