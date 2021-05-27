from kassabon_project_create_db_sqalchemy import *
from kassabon_project_create_plots import *
from PIL import Image
import re
from nltk.tokenize import word_tokenize
import pytesseract as tess

#extracts a string from a png file and saves it in variable text
tess.pytesseract.tesseract_cmd=r'C:/Program Files/Tesseract-OCR/tesseract.exe'
img=Image.open('bon_2258.png')
text = tess.image_to_string(img)

#create an empty list for categories
cat_labels = []

#list of all possible supermarkets for this project
supermarkets =['BILA','SPAR','EUROSPAR','INTERSPAR','HOFER','PENNI','LIDL','MERKUR']
#list of words that can be discarded right away
out = ['Rabatt','EUR','SUMME','MAESTRO','WIEN','TELEFON', 'KARTE']

#user enters categories to popoulate a dictionary with categories as keys,
#when user is done entering categories, press 'x' to see a selection of categories
#and confirm with 'Y' or keep updating with 'N'
def define_categories():
    while True:
        cat = input('Please enter category name, \nEnter \'x\' when ready: ')
        if cat != 'x':
            cat_labels.append(cat) #populates th elist cat_labels
        else:
            print('you have selected the following categories: ')
            print(cat_labels)
            x = input ('confirm choice with \'Y\', keep updating with \'N\'')
            if x.capitalize() == 'Y':
                # return a dictionary with categories (taken from the list cat_labels) as keys
                return {k: [] for k in cat_labels}
            #keep updating when pressing 'N'
            elif x.capitalize() == 'N':
                continue

#extract a date with regex and save in variable date
def extract_date(text_receipt):
    date_pattern='\d\d\.\d\d\.\d\d\d\d'
    date=re.findall(date_pattern,text_receipt)
    return date[0]

#identify the type of super market supermarket:
def extract_supermarket(text_receipt):
    for i in text_receipt:
        if i in supermarkets:
            return i
        else:
            superm_input = input("unknown supermarket, please enter supermarket name is known")
            return superm_input

def assign_cat_to_item(text_receipt):
    #words getting assigned to the dict1 for each category
    for w in text_receipt:
        if len(w)>3 and w.isalpha() and w not in out and w.capitalize() not in supermarkets:
            print(w)
            print(dict1.keys())
            while True:
                x = input("Select category from keys: ")
                if x in dict1.keys(): #if the category exists leave the while loop
                    break
                elif x == "": #if the enter is pressed break
                    break
                else:
                    print("Wrong category given!") #if wrong category is put, ask for new input
                    continue
            if x == "":
                pass #if enter was pressed keep iterating through the list of words
            else: #otherwise append the word to the dictionary
                dict1[x].append(w)

def count_items_per_cat(dict_):
    cat_count = []
    for list in dict_.values():
        cat_count.append(len(list))
    return cat_count

#extract words with nltk
words = word_tokenize(text)
dict1 = define_categories()
assign_cat_to_item(words)
supermarket = extract_supermarket(words)
date = extract_date(text)

#populate database
enter_data(dict1,date,supermarket)
#create pie plot
create_plot(count_items_per_cat(dict1),cat_labels)
