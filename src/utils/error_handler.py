import traceback

def catch_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"⛔ Error in {func.__name__}: {str(e)}")
            print(traceback.format_exc())
            return None
    return wrapper
