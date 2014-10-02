.PHONY: test coverage

test:
	DJANGO_SETTINGS_MODULE=activated_mixin.tests.settings django-admin.py test activated_mixin.tests

coverage:
	DJANGO_SETTINGS_MODULE=activated_mixin.tests.settings coverage run `which django-admin.py` test activated_mixin.tests
	coverage html
