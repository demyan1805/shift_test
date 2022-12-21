.PHONY: docker_build docker_run docker_test

docker_build:
	@docker build . -t shift_test

docker_run: docker_build
	@docker run --rm -p 8000:8000 shift_test

docker_test: docker_build
	@docker run --rm -it shift_test pytest -vv
