from datetime import timedelta
from worker_app import app  # Importing the Celery app from worker_app.py

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'worker_app.add',  # Reference the task defined in worker_app.py
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
}

SCHEDULED_QUERIES = {
    # This information is collected when the user clicks "Schedule query",
    # and saved into the `extra` field of saved queries.
    # See: https://github.com/mozilla-services/react-jsonschema-form
    'JSONSCHEMA': {
        'title': 'Schedule',
        'description': (
            'In order to schedule a query, you need to specify when it '
            'should start running, when it should stop running, and how '
            'often it should run. You can also optionally specify '
            'dependencies that should be met before the query is '
            'executed. Please read the documentation for best practices '
            'and more information on how to specify dependencies.'
        ),
        'type': 'object',
        'properties': {
            'output_table': {
                'type': 'string',
                'title': 'Output table name',
            },
            'start_date': {
                'type': 'string',
                'title': 'Start date',
                # date-time is parsed using the chrono library, see
                # https://www.npmjs.com/package/chrono-node#usage
                'format': 'date-time',
                'default': 'tomorrow at 9am',
            },
            'end_date': {
                'type': 'string',
                'title': 'End date',
                # date-time is parsed using the chrono library, see
                # https://www.npmjs.com/package/chrono-node#usage
                'format': 'date-time',
                'default': '9am in 30 days',
            },
            'schedule_interval': {
                'type': 'string',
                'title': 'Schedule interval',
            },
            'dependencies': {
                'type': 'array',
                'title': 'Dependencies',
                'items': {
                    'type': 'string',
                },
            },
        },
    },
    'UISCHEMA': {
        'schedule_interval': {
            'ui:placeholder': '@daily, @weekly, etc.',
        },
        'dependencies': {
            'ui:help': (
                'Check the documentation for the correct format when '
                'defining dependencies.'
            ),
        },
    },
    'VALIDATION': [
        # ensure that start_date <= end_date
        {
            'name': 'less_equal',
            'arguments': ['start_date', 'end_date'],
            'message': 'End date cannot be before start date',
            # this is where the error message is shown
            'container': 'end_date',
        },
    ],
    # link to the scheduler; this example links to an Airflow pipeline
    # that uses the query id and the output table as its name
    'linkback': (
        'https://airflow.example.com/admin/airflow/tree?'
        'dag_id=query_${id}_${extra_json.schedule_info.output_table}'
    ),
}

