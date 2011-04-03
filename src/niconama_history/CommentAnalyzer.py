#-*- coding:utf-8

def analyze(dateCommentList, analyzer, methodName):
    history = []
    for date, rows in dateCommentList:
        messages = analyzer.__getattribute__(methodName)(rows)
        if messages:
            if isinstance(messages, str):
                history.append((date, [messages]))
            elif isinstance(messages, list):
                history.append((date, messages))

    return history

if __name__ == '__main__':
    pass