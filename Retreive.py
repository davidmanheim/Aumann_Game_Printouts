import requests
import io

# Get data from server via API

URL = "https://opentdb.com/api.php"

number = 50
qtype = "multiple"

# It would be great to have specific categories, but for now, just take anything.

# defining a params dict for the parameters to be sent to the API
PARAMS = {'amount': number, 'type': qtype}

# sending get request and saving the response as response object
r = requests.get(url=URL, params=PARAMS)

# extracting data in json format
data = r.json()

# We have the data, now organize it for the quizmaster sheet and cards sheets.

AnswerSheet=list()
AnswersList=dict()
Number = 0

from random import shuffle
from pylatexenc.latexencode import unicode_to_latex
from w3lib.html import replace_entities

for question in data['results']:
    try:
        question['question'] = replace_entities(question['question'])
        question['correct_answer'] = replace_entities(question['correct_answer'])
        question['incorrect_answers'][0] = replace_entities(question['incorrect_answers'][0])
        question['incorrect_answers'][1] = replace_entities(question['incorrect_answers'][1])
        question['incorrect_answers'][2] = replace_entities(question['incorrect_answers'][2])
    except(UnicodeEncodeError):
        pass
    AnswersList[Number] = list()
    AnswersList[Number].append(question['correct_answer'])
    AnswersList[Number].extend(question['incorrect_answers'])
    shuffle(AnswersList[Number])
    print(AnswersList)
    if max([len(Answer) for Answer in AnswersList[Number]]) >= 20:
        # Does not fit on card. Linebreaks are annoying, so ...
        AnswersList[Number] = None
    else:
        for i in range(0,4):
            AnswersList[Number][i]=AnswersList[Number][i].replace("&", "\&")
            AnswersList[Number][i]=AnswersList[Number][i].replace("#", "\#")
            AnswersList[Number][i]=AnswersList[Number][i].replace("%", "\%")

    # If any answers are too long, skip the question.
    if AnswersList[Number] is not None:
        AnswerSheet.append("Q"+str(Number) + ": " + question['question'] + "\\\\(Correct answer: " +
                           question['correct_answer'] + ")")
        AnswerSheet[Number].replace("&", "\\&")
        AnswerSheet[Number].replace("#", "\\#")
        AnswerSheet[Number].replace("%", "\\%")

        Number = Number + 1

# Now, built the sheets:

# If the output directory doesn't exist, make it.
import os
if not os.path.exists("Output"):
    os.makedirs("Output")

import time
T = str(time.time())

prepend_file = open("Header.tex.part","r")
prepend_data = prepend_file.read()
prepend_file.close

with io.open("Output\Quizmaster_Sheet_v." + T + ".tex", 'w+', encoding="utf-8") as f:

    f.write('\documentclass{article} \n \\usepackage{labels} \n \n')
    f.write('\\begin{document} \n')
    f.write('\section*{Quizmaster\'s Sheet} \n')
    f.write('\\begin{itemize} \n')
    for qa in AnswerSheet:
        f.write('\item ' + qa + '\n')
    f.write('\\end{itemize} \n')

    f.write('\\end{document}')
    f.close()

os.system("pdflatex -interaction=nonstopmode -output-directory=Output " + "\"Output/Quizmaster_Sheet_v." + T + ".tex\"")

    #Now, the answers.

with io.open("Output\Answers_v." + T + ".tex", 'w+', encoding="utf-8") as f:
    f.write(prepend_data)
    f.write('\\begin{document} \n \\newpage')

    for answerset in AnswersList:
        if AnswersList[answerset] is not None:
            for answer in AnswersList[answerset]:
                f.write('\\begin{flashcard}[Q' + str(answerset) + "] {" + answer + '} \\end{flashcard} \n \n')

    f.write('\n \\end{document}')

    f.close()

os.system("pdflatex -interaction=nonstopmode -output-directory=Output " + "\"Output/Answers_v." + T + ".tex\"")