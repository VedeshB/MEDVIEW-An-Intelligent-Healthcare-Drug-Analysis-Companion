import string
def filter_word(n):
    print(n, 'input')
    res = []
    for i in [n]:
        t, st = [], ''
        for j in i:
            if j in string.punctuation or j.isspace():
                if not st.strip().isspace():
                    t.append(st.strip())
                st = ''
            else:
                st += j
        t.append(st.strip())
        res.append('-'.join(list(filter(lambda x: x != '', t))))
    print(res)
    return res

def t_ex(text):
        text2 = []
        s = ''
        for i in text:
            if i != '.':
                s += i
            elif i == '.':
                text2.append(s)
                s = ''
        if s:
            text2.append(s)
        print(text2)
        return text2

def processedtext(response):
    l=[]
    s=''
    for i in range(len(response)-1):
        if response[i]=='\n':
            continue
        if response[i]!='*':
            s+=response[i]
        
        elif (response[i]=='*' and response[i+1]=='*') or (response[i]=='*') :
            if response[i]!='':
                l.append(s)
            s=''
    print(l)
    return l