.PHONY: help api clean lint

.DEFAULT: help

help:
	@echo "\nUsage:"
	@echo "make <command>"
	@echo "\nAvailable Commands:"
	@echo "- api\t\t\t Run the local API"
	@echo "- clean\t\t\t Run clean project"
	@echo "- lint\t\t\t Check python code against some of the style conventions in PEP 8\n\n"


api:
	@echo "\n> Run the local API\n";\
	uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload

clean:
	@echo "\n> Cleaning project\n";\
	find . -name '*.pyc' -exec rm --force {} +;\
	find . -name '*.pyo' -exec rm --force {} +;\
	find . | grep -E "__pycache__|.pyc" | xargs rm -rf;\
	rm -f logs/grace_service.log;\

lint:
	@echo "\n> Check python code PEP 8\n";\
	black app/ & flake8 app/ & bandit -r -lll app/;\