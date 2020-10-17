'''
Coding interview examples

Reverse words in a sentence

Write a program that takes input of an interger N, followed by N lines of input sentences.
  For each sentence, reverse each individual word in the sentence. The order of the words
  are not reversed.
  Note: Your output lines should not have any trailing or leading whitespaces

Input:
3
RemoteIo is awesome
Candidates give interview
best candidates are selected

Output
oIetomeR si emosewa
setadidnaC evig weivretni
tseb setadidnac era detceles


def answer(line):
    #TODO: Implement your logic here
    return line

N = int(input())
for _ in range(N):
    line = input()
    print(answer(line))
'''

def answer(line):
    return (' ').join([word[::-1] for word in line.split(' ')])

N = int(input())
for _ in range(N):
    line = input()
    print(answer(line))

assert answer('Testing this string') == 'gnitseT siht gnirts'
assert answer('') == ''
