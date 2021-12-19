#%% imports
from bson.objectid import ObjectId


#%% utils
def generate_query(**kwargs):
  """
  Create a query 
  """
  query = {}

  for key, value in kwargs.items():
    if any(isinstance(value, t) for t in [str, int, float, bool, ObjectId]):
      query[key] = value
    elif isinstance(value, list):
      query[key] = {"$in": value} 
    elif value is None:
      pass
    else:
      # TODO create exception type
      raise Exception("Unhandled value type for datastore query")

  return query


#%% implementation
def cast_object_id(id):
  if isinstance(id, str):
    return ObjectId(id)
  elif isinstance(id, ObjectId):
    return id
  else:
    raise TypeError("id should be a [str] or an [ObjectId]")
    

if __name__ == "__main__":
  print(generate_query(lemma=100, _id=[1,2,3]))