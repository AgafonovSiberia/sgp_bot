import asyncio
from functools import wraps


def asyncio_celery_task_runner(celery_task):
	"""
	Декоратора для запуска задач, использующих asyncio
	:param celery_task: декорируемая таска
	:return:
	"""
	@wraps(celery_task)
	def async_wrapper(*args):
		result = asyncio.run(celery_task(*args))
		return result
	return async_wrapper


