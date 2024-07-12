import pandas
import collections
import itertools
import re


name_changes = pandas.read_excel(r"C:\Users\ChloeNeil\New Power Names.xlsx")

def is_repeating_string(s):
    return len(s) > len(list(itertools.groupby(s)))


def naiveFindPatrn(mainString, pattern):
   patLen = len(pattern)
   strLen = len(mainString)
   indices = []
   # outer for loop 
   for i in range(strLen - patLen + 1):
      j = 0
      # to check for each character of pattern 
      for j in range(patLen):      
         if mainString[i+j] != pattern[j]:
            break
      # to print the index of the pattern is found
      if j == patLen - 1 and mainString[i+j] == pattern[j]:    
         indices.append(i)
   return indices



def repeat_check(longstring):
    total_repeats = 0
    #grams = [longstring[i: i + 4] for i in range(len(longstring) - 4 + 1)]
    grams = longstring.split()
    joinedstring = ''.join(longstring.split())
    gram_no = len(grams)    
    for gram in grams:
        indices = naiveFindPatrn(joinedstring,gram)
        indices_len = len(indices)
        total_repeats = total_repeats + indices_len
    
    if total_repeats > gram_no:
        return True
    else:
        return False
        

def repeat_detail(longstring):
    total_repeats = 0
    repeated = []
    #grams = [longstring[i: i + 4] for i in range(len(longstring) - 4 + 1)]
    grams = longstring.split()
    joinedstring = ''.join(longstring.split())
    gram_no = len(grams)    
    for gram in grams:
        indices = naiveFindPatrn(joinedstring,gram)
        indices_len = len(indices)
        if indices_len > 1:
            repeated.append(gram)
    
    return repeated        
    
            
    
        

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (re.sub('[\(\[].*?[\)\]]', '', x)))	

name_changes['Repeat_Words'] = name_changes['New Power Plant Name'].apply(lambda x: (repeat_detail(x)))

name_changes.to_excel('New Power Name Check.xlsx')

