import io


class scanner(object):
    def __init__(self, code=""):
        code.encode(encoding="utf-8")
        code = code.translate(str.maketrans({"-":  r"\-",
                                                       "]":  r"\]",
                                                       "\\": r"\\",
                                                       "^":  r"\^",
                                                       "$":  r"\$",
                                                       "*":  r"\*",
                                                       ".":  r"\.",
                                                       ":":  r"\:"}))
        self.code = code
        self.token_list = []
        self.code_list = []
        self.scan_out = []

    def set_code(self, code):
        code.encode(encoding="utf-8")
        self.code = code

    def scan(self):
        token_list = []
        res_Words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        special_Chars = ['(', ')', '+', '-', '*', '/', '=', ';', '<', '>', '<=', '>=']
        for tiny in io.StringIO(self.code):
            token = ""
            

            state = "START"
            i=0
            while i<len(tiny):
                if tiny[i] in special_Chars and state != "INASSIGN" and state != "INCOMMENT":
                    if token !="":
                        token_list.append(token)
                        token = ""

                    token_list.append(tiny[i])
                    state = "START"

                elif state == "START":
                    if tiny[i] == " ":
                        state = "START"

                    elif tiny[i].isalpha():
                        token += tiny[i]
                        state = "INID"
                    
                    elif tiny[i].isdigit():
                        token += tiny[i]
                        state = "INNUM"

                    elif tiny[i] == ':':
                        token += tiny[i]
                        state = "INASSIGN"

                    elif tiny[i]=='{':
                        token += tiny[i]
                        state = "INCOMMENT"

                    else:
                        state = "DONE"

                elif state == "INID":
                    if tiny[i].isalpha():
                        token += tiny[i]
                        state = "INID"  #same state

                    else:
                        state = "DONE"

                elif state == "INNUM":
                    if tiny[i].isdigit():
                        token += tiny[i]
                        state = "INNUM"
                    
                    else:
                        state = "DONE"

                elif state == "INASSIGN":
                    if tiny[i] == '=':
                        token += tiny[i]
                        state = "DONE"

                    else:
                        state = "DONE"

                elif state == "INCOMMENT":
                    if tiny[i] == '{':
                        token += tiny[i]
                        state = "START"

                    else:
                        token += tiny[i]

                elif state == "DONE":
                    token_list.append(token)
                    token = ""
                    state = "START"
                    i-=1

                i+=1

            if token !="":
                token_list.append(token)
                token = ""

        code_list = []
        output = []
        for j in token_list:
            if j in res_Words:
                code_list.append(j)
                output.append(j+", reserved")
            elif j in special_Chars:
                code_list.append(j)
                output.append(j+", special char")
            elif j == ":=":
                code_list.append(j)
                output.append(j+", assign")
            elif j.isdigit():
                code_list.append("number")
                output.append(j+", number")
            elif j.isalpha():
                code_list.append("identifier")
                output.append(j+", identifer")
            else:
                pass
               
        self.code_list = token_list
        self.token_list = code_list
        self.scan_out = output

    