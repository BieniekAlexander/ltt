#%% decorators
def capitalize_string_args(method):
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
      return method(*processed_args, **processed_kwargs)
    return wrapper


#%% main
def main():
  @capitalize_string_args
  def printArgs(one, two, *args, **kwargs):
    print(one)
    print(two)

    for arg in args:
      print(arg)

    for key in kwargs:
      print(kwargs[key])

  
  printArgs("one", "tWo", "Three", {"not a": "string"}, potato="FOUR", tomato="fIVE")


if __name__ == "__main__":
  main()