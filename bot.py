# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 22:11:22 2018

@author: HossamEldeen
"""

import numpy as np
import tensorflow as tf
import re
import time

lines = open('movie_lines.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')

linesDict = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        linesDict[_line[0]] = _line[4]

conversationsIds = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    _conversation = _conversation.split(',')
    conversationsIds.append(_conversation)
    
questions = []
answers = []
for conversation in conversationsIds:
    for i in range(len(conversation) - 1):
        questions.append(linesDict[conversation[i]])
        answers.append(linesDict[conversation[i+1]])


#clean text
#everything in lowercase
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"don't", "do not", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", "will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    #text = re.sub(r"[-()\"#/@;:<>{}+=-|.?,]", "", text)
    text = re.sub(r"\.", "", text)
    return text

clean_questions = []
for question in questions:
    question = clean_text(question)
    clean_questions.append(question)


clean_answers = []
for answer in answers:
    answer = clean_text(answer)
    clean_answers.append(answer)
    

#removing non freuquent words
wordCount = {}
for question in clean_questions:
    for word in question.split():
        if word not in wordCount:
            wordCount[word] = 1
        else:
            wordCount[word] += 1

for answer in clean_answers:
    for word in answer.split():
        if word not in wordCount:
            wordCount[word] = 1
        else:
            wordCount[word] += 1


threshold = 20
questionWordsInt = {}
wordNumber = 0
for word, count in wordCount.items():
    if count >= threshold:
        questionWordsInt[word] = wordNumber
        wordNumber += 1

answerWordsInt = {}
wordNumber = 0
for word, count in wordCount.items():
    if count >= threshold:
        answerWordsInt[word] = wordNumber
        wordNumber += 1
        


tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
for token in tokens:
    questionWordsInt[token] = len(questionWordsInt) + 1
    answerWordsInt[token] = len(answerWordsInt) + 1


#create inverse dictionary
answerIntWords = {w_i: w for w, w_i in answerWordsInt.items()}

for i in range(len(clean_answers)):
    clean_answers[i] += '<EOS>'
    

questionsToInt = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionWordsInt:
            ints.append(questionWordsInt['<OUT>'])
        else:
            ints.append(questionWordsInt[word])
    questionsToInt.append(ints)


answersToInt = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word in answerWordsInt:
            ints.append(answerWordsInt[word])
        else:
            ints.append(answerWordsInt['<OUT>'])
    answersToInt.append(ints)
    
    
sortedCleanQuestions = []
sortedCleanAnswers = []
for length in range(1, 25+1):
    for i in enumerate(questionsToInt):
        if len(i[1]) == length:
                sortedCleanQuestions.append(questionsToInt[i[0]])
                sortedCleanAnswers.append(answersToInt[i[0]])
    
