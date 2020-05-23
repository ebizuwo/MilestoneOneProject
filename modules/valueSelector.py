from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style


class ValueDropper():
    def __init__(self, q):
        self.q = q

    def initiate_selection(self):
        vals = []
        try:
            for v in self.q:
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
        return vals


class ValueSelector():
    def __init__(self, q):
        self.q = q

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
        return f'class:text', text






class ValueClassifier():
    def __init__(self, q, c):
        self.q = q
        self.c = c
        self.autocompleter = WordCompleter(self.c)
        # style dict for each word
        self.Styler = Styler([], '#ff0000')
        self.style = self.Styler.style


    def initiate_classifier(self):
        vals = []
        print(self.style)
        try:
            count = 0
            num = len(self.q)
            for v in self.q:
                # for word v create colored text 'object' to print
                text = self.Styler.create_text(v)
                count+=1
                while True:
                    #TODO message constructor class
                    message = [
                        ('class:all', f"\nHere is the comparison list {self.c}"),
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
                        vals.append((v, resp))
                        break
                    else:
                        print(f"{resp} is invalid try again")
                print(f"you have completed classifying all {num} items")
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
