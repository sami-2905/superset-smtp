from celery import Celery

class MyCelery(Celery):
    key_prefix = 'celery{mytag}:'

    def gen_task_name(self, name, module):
        # Apply a hash tag to ensure all keys related to this task map to the same slot
        return f'{self.key_prefix}{super().gen_task_name(name, module)}'

app = MyCelery('worker_app', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def add(x, y):
    return x + y



# Ensure that tasks are discovered by celery
app.autodiscover_tasks(['worker_app'])
