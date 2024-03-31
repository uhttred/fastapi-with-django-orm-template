msg := ''

test:
	# testing all application
	@export ENV_MODE=test
	@pytest

serve:
	@uvicorn cliver.main:app --reload	
