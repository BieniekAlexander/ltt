#%% imports
import time
from random import randint

# constants
CRAWL_DELAY = 5


#%% decorators
def capitalize_string_args(function):
  """
  Capitalizes all string arguments used in the given function
  """
  def wrapper(*args, **kwargs):
    processed_args = []
    for arg in args:
      if isinstance(arg, str):
        processed_args.append(arg.capitalize())
      else:
        processed_args.append(arg)
    
    processed_kwargs = {}
    for key, val in kwargs.items():
      if isinstance(val, str):
        processed_kwargs[key] = val.capitalize()
      else:
        processed_kwargs[key] = val

    # change new_args here
    return function(*processed_args, **processed_kwargs)
  return wrapper


def delay(seconds=CRAWL_DELAY):
  """
  Delay the calling of a function by [seconds]
  """
  def decorator(func):
    def wrapper(*args, **kwargs):
      time.sleep(randint(CRAWL_DELAY-1, CRAWL_DELAY+1))
      return func(*args, **kwargs)
    return wrapper
  return decorator


#%% main
def main():
  @delay(3)
  def foo():
    print("foo")

  foo()


if __name__ == "__main__":
  main()