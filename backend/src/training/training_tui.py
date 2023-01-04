import curses
import os
import argparse
from enforce_typing import enforce_types
from bson.objectid import ObjectId
from pymongo import MongoClient

from training.tui.repr_polish import (
    definition_answer_repr as definition_answer_repr_pl,
    definition_hint_repr as definition_hint_repr_pl
)
from training.tui.repr_chinese import (
    written_answer_repr as definition_answer_repr_zh,
    written_hint_repr as definition_hint_repr_zh
)

from training.tui.utils import add_linebreaks
from training.sm2_anki.recall import Recall
from training.sm2_anki.training_session import (get_study_entries, push_study_entry,
                                       put_studied_entries)

##### CONSTANTS #####
# connectivity
MONGODB_URI = os.environ['MONGODB_URI']
USER_ID = ObjectId("62a57d5bfa96028f59ac1d75")

# display
# TODO revisit sizes, I think this crashes when it's too small, this is quite hardcoded
PANEL_HEIGHT = 20
PANEL_WIDTH = 50
Y_PADDING = 3
X_PADDING = 10

# training evaluation
recall_dict = dict(list(enumerate(Recall)))

repr_dict = {
    "polish":  {
        "definition": (definition_hint_repr_pl, definition_answer_repr_pl)
    },
    "chinese": {
        "written": (definition_hint_repr_zh, definition_answer_repr_zh),
        "spoken": (definition_hint_repr_zh, definition_answer_repr_zh)
    }
}


@enforce_types
def main(stdscr: curses.window, language: str, fact: str, card_count: int):
    # initialize training session
    datastore_client = MongoClient(MONGODB_URI)
    vocabulary = get_study_entries(USER_ID, language, datastore_client, fact=fact, interval=1, count=card_count)
    study_queue = vocabulary.copy()

    get_hint, get_answer = repr_dict[language][fact]

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

        term_string = add_linebreaks(get_hint(entry), PANEL_WIDTH)
        answer_string = add_linebreaks(get_answer(entry), PANEL_WIDTH)

        question_window.addstr(0, 0, "Hint")
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
            entry['stats'][fact].update(recall)
            push_study_entry(study_queue, entry, fact)
            get_next_entry = True

    # update the terms and persist them in the backend
    put_studied_entries(USER_ID, language, datastore_client, fact, vocabulary)
    with open('out.json', 'w') as file:
        file.write(str(vocabulary))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'training_tui',
                    description = 'text interface utility for studying',)
    
    parser.add_argument('-l', '--language', default="polish", help="the language to study terms from", type=str)
    parser.add_argument('-f', '--fact', default="definition", help="the fact to study", type=str)
    parser.add_argument('-c', '--count', default=10, help="the number of cards to retrieve for studying", type=int)
    args = parser.parse_args()

    curses.wrapper(main, language=args.language, fact=args.fact, card_count=args.count)
