# Aumann_Game_Printouts

This is a simple tool to generate latex files that are automatically compiled to PDF via latexpdf, and can then be printed, and cut out to play the Aumann Agreement Game, described here: https://www.lesswrong.com/posts/nmwog5hGidZniDDpR/aumann-agreement-game (The rules and scoring PDF is from the google doc linked there.)

This is a very simple version, and several improvements are possible if anyone wants to help;

- Allow the user to pick the question category/ies and difficulty/ies using the API. This is farily simple, see https://opentdb.com/api_config.php
- Change to allow more than 4 player games by making more cards. This should be done by inserting multiples of the incorrect answers. (This requires making sure you have that many players, to make sure someone gets the right answer. Or after printing, duplicates could be removed by the game master.)
- Format the latex cards better. For now I just throw out any that have answers that are too long to fit on the card, and the layout is not great.
- Modify and compile the script along with a latex layout engine in python so that it automatically creates pdfs without needing latexpdf installed on the system. (Not sure how to do this.)
