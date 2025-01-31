from retrying import retry

def retry_if_exception(exception):
    return isinstance(exception, Exception)

retry_config = retry(
    stop_max_attempt_number=3,
    wait_random_min=1000,
    wait_random_max=2000,
    retry_on_exception=retry_if_exception
)