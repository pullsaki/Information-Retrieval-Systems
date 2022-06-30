# Boolean Retrieval System

A software to search for documents in the corpus with boolean queries.

## Procedure
First, run all the cells in the notebook file. In the main function, a prompt to enter query is given.
Enter the query in the required format.

Format:
1. In the query, there should be one space between any two tokens.
2. Every logical operation (AND, OR, NOT) must be enclosed within parentheses.
3. The operators should be given in capital letters
4. To do a wildcard search, ‘ * ’ should be specified in the word.
5. In case of an invalid query, the program will return a message saying “Invalid Query”

##### Stopword Removal
`remove_stopwords` function is used

The following stopwords are removed from all the documents: "a","about","above","after","again","against","all","am","an","and","any","are","as","at","be","because","been","before","being","below","between","both","but","by","can","did","do","does","doing","down","during","each","few","for","from","further","had","has","have","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","it","its","itself","let","me","more","most","my","myself","nor","of","on","once","only","or","other","our","ours","ourselves","out","over","own","same","she","should","so","some","such","than","that","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","very","was","we","were","what","when","where","which","while","who","whom","why","with","would","you","your","yours","yourself","yourselves"

Eg:- my name is brutus -> name brutus

##### Stemming
`PorterStemmer` class functions are used to do this task
Porter Stemmer principles are used:
sses -> ss
ies -> i
ational -> ate
tional -> tion

Eg:- carpenter -> carpent, marriage -> marri

##### Building Index
`preprocessing` function is used to build the index for the processed data
Inverted Index is created for the documents
Permuterm Index is created for wildcard searches by matchin each rotation of the word with itself.

##### Querying
`main` function is used to give results of the inputted query
We have to enter a valid query in the above mentioned format for a successful retrieval.
1. Initially we check if a single token is entered in the query and if so it is proccessed accordingly(either a wildcard search or a normal query)
2. The query is split based on whitespace and we start pushing each element into the stack.
3. If a ")" is encountered we pop elements out of the stack until a "(" is encountered to get a single logical operation.
4. Now accordingly the operation is performed and the list of documents is pushed into the stack.
5. The process is repeated until there is only one element in the stack which is a list of documents.
6. Finally we print the list of documents

Eg:- `( befal AND ( NOT ( thes*u OR godspe ) ) )`
Output:- 

the-taming-of-the-shrew_TXT_FolgerShakespeare.txt
antony-and-cleopatra_TXT_FolgerShakespeare.txt
cymbeline_TXT_FolgerShakespeare.txt
titus-andronicus_TXT_FolgerShakespeare.txt
twelfth-night_TXT_FolgerShakespeare.txt
henry-vi-part-1_TXT_FolgerShakespeare.txt
henry-vi-part-2_TXT_FolgerShakespeare.txt
henry-vi-part-3_TXT_FolgerShakespeare.txt
julius-caesar_TXT_FolgerShakespeare.txt
loves-labors-lost_TXT_FolgerShakespeare.txt
measure-for-measure_TXT_FolgerShakespeare.txt
richard-iii_TXT_FolgerShakespeare.txt
richard-ii_TXT_FolgerShakespeare.txt
the-comedy-of-errors_TXT_FolgerShakespeare.txt