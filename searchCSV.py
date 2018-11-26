# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 19:37:40 2018

@author: Afnan
"""
import csv

def searchCSV(term_list):
    count = 0
    weight = 0
    file = open("./sampleDir/file2.csv", "r")
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        for column in row:
            for term in term_list:
                if term in column:
                    count += 1
            weight += 1
    weighted_count = count/weight
    return weighted_count

def getMedWords(source):
    return [word for line in open(source, 'r') for word in line.split()]

if __name__ == "__main__":
    terms = "lib/medTerms.txt"
    term_list = getMedWords(terms)
    print(str(searchCSV(term_list)))