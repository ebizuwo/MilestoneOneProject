from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
import json
from collections import defaultdict
import pandas as pd


class ValueDropper():
    def __init__(self, q):
        self.q = q
        self.selected_vals = self.read_drop()
        self.selected_keep = self.read_kept()

    def store_selected(self, vals):
        with open('data_selected/selectedDrop.json', 'w') as fp:
            json.dump(vals, fp)
            fp.close()

    def read_drop(self):
        with open('data_selected/selectedDrop.json', 'r') as fp:
            return json.load(fp)

    def read_kept(self):
        with open('data_selected/selectedKeep.json', 'r') as fp:
            return json.load(fp)

    def initiate_selection(self):
        vals = []
        try:
            for v in self.q:
                if v in self.selected_vals:
                    vals.append(v)
                    continue
                if v in self.selected_keep:
                    continue
                while True:
                    resp = input(f"\nDo you want to drop {v} "
                                 f"\nPlease type n for no or y for yes: ")
                    if resp == 'n':
                        print(f"keeping value {v}")
                        break
                    if resp == 'y':
                        print(f"adding {v} to drop list")
                        vals.append(v)
                        break
                    else:
                        print(f"{resp} is invalid try again")
        except KeyboardInterrupt:
            while True:
                key_resp = input(f"Would you like to send {vals}"
                                 f"Press y or n "
                                 )
                if key_resp == 'y':
                    print(f"sending {vals}")
                    return vals
                if key_resp == 'n':
                    print('aborting')
                    return
        print('finish selecting values to drop')
        self.store_selected(vals)
        return vals


class ValueSelector():
    def __init__(self, q):
        self.q = q

    # def store_classified(self, vals):
    #     d = {x:1 for x in vals}
    #     json.dump('data_selected/selected.json', d)
    #     return d
    def initiate_selection(self):
        vals = []
        try:
            for v in self.q:
                while True:
                    resp = prompt(f"\nDo you want to keep {v} "
                                 f"\nPlease type n for no or y for yes: ")
                    if resp == 'y':
                        print(f"keeping value {v}")
                        vals.append(v)
                        break
                    if resp == 'n':
                        print(f"removing value {v}")
                        break
                    elif resp:
                        print(f"{resp} is invalid try again")
        except KeyboardInterrupt:
            while True:
                key_resp = input(f"Would you like to send {vals}"
                                 f"Press y or n "
                                 )
                if key_resp == 'y':
                    print(f"sending {vals}")
                    return vals
                if key_resp == 'n':
                    print('aborting')
                    return
        return vals


class Styler():
    #TODO could be better at this
    def __init__(self, keys, color_value):
        self.style = self.create_style(keys, color_value)


    def create_style(self, keys, color_value):

        my_style_dict = {f'{k}': color_value for k in keys}

        return Style.from_dict({f'text': color_value,
                                f'all': 'white'})

    def create_text(self, text):
        return f'class:text', str(text)






class ValueClassifier():
    value_store = defaultdict(str)
    map_store = ''
    jsonclassifieds = {}

    def __init__(self, q, c):
        self.q = q
        self.c = c
        self.autocompleter = WordCompleter(self.c)
        # style dict for each word
        self.Styler = Styler([], '#ff0000')
        self.style = self.Styler.style
        self.jsonclassifieds = self.read_classified()

    def store_classified(self):
        with open('data_classified/classified.json', 'w') as fp:
            json.dump(dict(self.value_store), fp)

    def set_value(self, val):
        # set value in dictionary
        self.value_store[val[0]] = val[1]
        # update object
        self.map_store.add_map(val)

    def read_classified(self):
        with open('data_classified/classified.json', 'r') as fp:
            return json.load(fp)

    def initiate_classifier(self, map_rec_raw_obj):
        # store object
        self.map_store = map_rec_raw_obj
        try:
            count = 0
            num = len(self.q)
            for v in self.q:
                # logic to handle reading and updating from file
                # will not enter for loop if it sees value in dict
                if v in self.jsonclassifieds.keys():
                    self.set_value((v, self.jsonclassifieds[v]))
                    continue
                # for word v create colored text 'object' to print
                text = self.Styler.create_text(v)
                count+=1
                while True:
                    #TODO message constructor class
                    message = [
                        ('class:all', f"\nClassifying {count} of {num} things"),
                        ('class:all', f"\nHere is a value "),
                        text,
                        ('class:all', f"\nPress tab to autocomplete or see values\n")
                    ]
                    # prompt for message
                    resp = prompt(message, completer=self.autocompleter, style=self.style)

                    # response handling
                    if resp in self.c:
                        print(f"classifying {text} as {resp}")
                        self.set_value((v, resp))
                        break
                    if resp == '':
                        self.set_value((v, None))
                        print('adding a None match')
                        break
                    else:
                        print(f"{resp} is invalid try again")
            print(f"you have completed classifying {num} items")
        except KeyboardInterrupt:
            while True:
                #TODO: Modif handling here
                key_resp = input(f"Would you like to send {self.value_store}"
                                 f"Press y or n "
                                 )
                if key_resp == 'y':
                    print(f"sending {self.value_store}")
                    self.store_classified()
                    return self.value_store, self.map_store
                if key_resp == 'n':
                    print('aborting')
                    return
        self.store_classified()
        return self.value_store, self.map_store
# classifier = ValueClassifier([1,2,3,4], ['a','b','c','d']).initiate_classifier()