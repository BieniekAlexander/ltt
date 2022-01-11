from bs4 import BeautifulSoup


class ScrapingError(Exception):
  """
  Base class for exceptions related to Web Scraping
  
  Attributes:
    soup: the [BeautifulSoup] object that we're scraping from
    message: the message held by the exception
  """
  pass


class ScrapingFindError(ScrapingError):
  """
  Exception raised when data of interest was not found in the webpage being scraped

  Attributes:
      soup: the [BeautifulSoup] object that we're scraping from
      query_args: the arguments used in the search
      message: the message held by the exception
  """
  def __init__(self, soup, query_args, message=None):
    self.soup = soup
    self.query_args = query_args

    if message:
      self.message = message
    else:
      self.message = f"Failed to find the following contents in the BeautifulSoup object: {query_args}"

    super().__init__(self.message)


class ScrapingFormatError(ScrapingError):
  """
  Exception raised when an assumption of the webpage's HTML format was violated

  Attributes:
      soup: the [BeautifulSoup] object that we're scraping from
      query_args: the arguments used in the search
      message: the message held by the exception
  """
  def __init__(self, soup, query_args, message=None):
    self.soup = soup
    self.query_args = query_args

    if message:
      self.message = message
    else:
      self.message = f"An assertion about the format of the webpage was violated: {query_args}"

    super().__init__(self.message)


class ScrapingValueError(ScrapingError):
  """
  Exception raised when we find an unexpected value while scraping

  Attributes:
      soup: the [BeautifulSoup] object that we're scraping from
      property: the name of the property we're scraping
      value: the unexpected value that we found
      message: the message held by the exception
  """
  def __init__(self, soup, property, value, message=None):
    self.soup = soup
    self.property = property
    self.value = value

    if message:
      self.message = message
    else:
      self.message = f"Found an unexpected value for the following property: {property}={value}"

    super().__init__(self.message)