- use dotenv and .env file to keep secrets
- the CSV files in this directory contain Spanish characters that exist outside English á, é, í, ó, ú, *always use utf-8 encoding for everything*
- there are some headaches that are caused by the special characters that are hard to work around, in some cases I just had to deal with them manually
- the most import table is in 'cards.csv', the text used for every flashcard is stored here
    - each card has a unique id which is a combination of verb_id, tense_id, and person_id
- You can also add to the discussion on Discord https://discordapp.com/channels/1373077048146264166/1373081089349783753


|               field              |                         description                           |             example             |
| -------------------------------- | ------------------------------------------------------------- | ------------------------------- |
| verb                             | infinitive form of the verb                                   | ser                             |
| form                             | grammatical tense/mood of the conjugation                     | indicativo_presente             | 
| person                           | grammatical person/number of the conjugation                  | 1st_singular                    |
| hypothetical_regular_conjugation | what the conjugation would be if the conjugation were regular | so                              |
| conjugation                      | actual conjugation given verb/form/person                     | soy                             |
| regular                          | hypotehtical_regular_conjugation == conjugation (true/false)  | false                           | 
| sentence                         | example sentence using the verb in context                    | Soy capaz de correr un maratón. |
| audio_path                       | file path to the audio recording of the sentence              | audio/1_3_11.mp3                |
