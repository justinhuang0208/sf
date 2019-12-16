from ckiptagger import WS, POS, NER

text = '傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。'
ws = WS("./data")
pos = POS("./data")
ner = NER("./data")

ws_results = ws([text])
pos_results = pos([text])
ner_results = ner([text], pos_results)

print(ws_results)
print(pos_results)
for name in ner_results[0]:
    print(name)
