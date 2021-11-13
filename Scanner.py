import io

res_Words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
special_Chars = ['+', '-', '*', '/', '=', ';', '<', '>', '<=', '>=']


def get_token(code):
    token_list = []
    for tiny in io.StringIO(code):
        token = ""
        token_type = ""

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

    output = []

    for j in token_list:
        if j in res_Words:
            output.append(j+", reserved")

        elif j in special_Chars:
            output.append(j+", special char")

        elif j == ":=":
            output.append(j+", assign")

        elif j.isdigit():
            output.append(j+", number")

        elif j.isalpha():
            output.append(j+", identifer")

        else:
            pass


    return output


        
                



"""
if __name__ == '__main__':
    code =  { Sample program in TINY language – computes factorial}
     read x;   {input an integer }
     if  0 < x   then     {  don’t compute if x <= 0 }
        fact  := 1;
        repeat 
           fact  := fact *  x;
            x  := x  -  1
        until  x  =  0;
        write  fact   {  output  factorial of x }
     end 
    print(get_token(code))"""
   
