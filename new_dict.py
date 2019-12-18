words_dict = []
with open('dict.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        word = line.split(' ')
        words_dict.append(word[0])
        
with open('new_dict.txt', 'w') as f:
    for word in words_dict:
        f.write(word + '\n')
