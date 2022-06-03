

import curses
from time import sleep

from storage.datastore_client import DatastoreClient
from training.training_session import TrainingSession
from training.recall import Recall


##### CONSTANTS #####
# connectivity
MONGODB_URL = "mongodb://localhost:27017/"

# display
# TODO revisit sizes, I think this crashes when it's too small, this is quite hardcoded
PANEL_HEIGHT = 10
PANEL_WIDTH = 50
Y_PADDING = 3
X_PADDING = 10

# training evaluation
recall_dict = dict(zip(range(1, len(Recall)+1), Recall))

def main(stdscr: curses.window):
  # initialize training session
  datastore_client = DatastoreClient(MONGODB_URL)
  training_session = TrainingSession('a'*24, 'polish', datastore_client)
  training_session.load_study_terms()

  # initialize things for TUI
  SCREEN_HEIGHT, SCREEN_WIDTH = stdscr.getmaxyx()
  curses.curs_set(False)
  question_window = curses.newwin(PANEL_HEIGHT, PANEL_WIDTH, Y_PADDING, X_PADDING)
  answer_window = curses.newwin(PANEL_HEIGHT, PANEL_WIDTH, Y_PADDING, 2*X_PADDING+PANEL_WIDTH)
  recall_window = curses.newwin(PANEL_HEIGHT, PANEL_WIDTH, 2*Y_PADDING+PANEL_HEIGHT, X_PADDING)
  term = None
  get_next_term = True

  # main loop
  while True:
    # update term
    if get_next_term:
      term = training_session.get_study_term()
      show_hint = False
      get_next_term = False

    # render
    question_window.clear()
    answer_window.clear()
    recall_window.clear()
    question_window.addstr(2, 2, "Term")
    question_window.addstr(4, 2, term['term']['lemma'])
    answer_window.addstr(2, 2, "Answer")
    
    for index, recall in recall_dict.items():
      recall_window.addstr(index, 5, f"{index} - {recall.name.title()}")

    if show_hint:
      answer_window.addstr(4, 2, term['term']['definitions'][0][:40])

    answer_window.refresh()
    question_window.refresh()
    recall_window.refresh()
    
    # get input
    curses.flushinp()
    c = answer_window.getch()

    if c == 27: # alt or escape
      # TODO this method takes a long time to abort with ESC
      answer_window.nodelay(True)
      if answer_window.getch()==-1:
        stdscr.addstr(10, 15, "Saving study session, please wait...")
        stdscr.refresh()
        break
      answer_window.nodelay(False)
    elif c == ord(' '): # toggle hint
      show_hint = show_hint==False
    elif c in list(map(ord, '12345')):
      recall = recall_dict[list(map(ord, '12345')).index(c)+1]
      training_session.update_study_term_stats(term, recall)
      get_next_term = True


if __name__ == "__main__":
  curses.wrapper(main)