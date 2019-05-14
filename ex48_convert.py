def convert_number(s):
    try:
        return int(s)
    except ValueError:
        return None
first = {'verb', 'go'}
second = {'direction', 'north'}
third = {'direction', 'west'}
sentence = [first, second, third]
print(sentence)