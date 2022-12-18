import curses
import os

from pymongo import MongoClient
from training.sm2_anki.recall import Recall
from training.sm2_anki.training_session import (get_study_entries, push_study_entry,
                                       put_studied_entries)

##### CONSTANTS #####
# connectivity
MONGODB_URI = os.environ['MONGODB_URI']
USER_ID = "62a57d5bfa96028f59ac1d75"

# display
# TODO revisit sizes, I think this crashes when it's too small, this is quite hardcoded
PANEL_HEIGHT = 10
PANEL_WIDTH = 50
Y_PADDING = 3
X_PADDING = 10

# training evaluation
recall_dict = dict(list(enumerate(Recall)))


def add_linebreaks(string: str, line_length: int) -> str:
    """
    Add linebreaks to a string before words that would break the line

    Args:
        string (str): the string to which we'll add line breaks
        line_length (int): the length of the line

    Returns:
        str: the line with new linebreaks
    """
    idx = line_length
    ret_string = string

    while idx < len(ret_string):
        while ret_string[idx] != ' ':
            idx -= 1

        ret_string = f'{ret_string[:idx]}\n{ret_string[idx:]}'
        idx += line_length+1

    return ret_string


def main(stdscr: curses.window):
    # initialize training session
    datastore_client = MongoClient(MONGODB_URI)
    vocabulary = get_study_entries(
        USER_ID, 'polish', datastore_client, interval=1, count=10)
    study_queue = vocabulary.copy()

    # initialize things for TUI
    SCREEN_HEIGHT, SCREEN_WIDTH = stdscr.getmaxyx()
    curses.curs_set(False)
    question_window = curses.newwin(
        PANEL_HEIGHT, PANEL_WIDTH, Y_PADDING, X_PADDING)
    answer_window = curses.newwin(
        PANEL_HEIGHT, PANEL_WIDTH, Y_PADDING, 2*X_PADDING+PANEL_WIDTH)
    recall_window = curses.newwin(
        PANEL_HEIGHT, PANEL_WIDTH, 2*Y_PADDING+PANEL_HEIGHT, X_PADDING)
    get_next_entry = True

    # study loop
    while True:
        # if we're pulling the next term and the study queue has entries in it, get the next one
        if get_next_entry:
            if study_queue:
                entry = study_queue.pop(0)
                show_hint = False
                get_next_entry = False
            else:
                break

        # render
        question_window.clear()
        answer_window.clear()
        recall_window.clear()

        term_string = add_linebreaks(
            f"{entry['lexeme']['lemma']}\n\n{entry['lexeme']['pos'].lower()}", PANEL_WIDTH)
        answer_string = add_linebreaks(
            f"{entry['lexeme']['definitions'][0]}", PANEL_WIDTH)

        question_window.addstr(0, 0, "Term")
        question_window.addstr(2, 0, term_string)
        answer_window.addstr(0, 0, "Answer")

        for index, recall in list(enumerate(Recall)):
            recall_window.addstr(index, 5, f"{index} - {recall.name.title()}")

        if show_hint:
            answer_window.addstr(2, 0, answer_string)

        answer_window.refresh()
        question_window.refresh()
        recall_window.refresh()

        # get input
        curses.flushinp()
        c = answer_window.getch()

        if c == 27:  # alt or escape
            answer_window.nodelay(True)
            if answer_window.getch() == -1:
                stdscr.addstr(10, 15, "Saving study session, please wait...")
                stdscr.refresh()
                break
            answer_window.nodelay(False)
        elif c == ord(' '):  # toggle hint
            show_hint = show_hint == False
        elif c in list(map(ord, '0123')):
            recall = recall_dict[list(map(ord, '0123')).index(c)]
            entry['stats']['definition'].update(recall)
            push_study_entry(study_queue, entry)
            get_next_entry = True

    # update the terms and persist them in the backend
    put_studied_entries(USER_ID, 'polish', datastore_client, vocabulary)


if __name__ == "__main__":
    curses.wrapper(main)
