
import openai
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


API_KEY = "sk-cgdX71bullQIykhX6APFT3BlbkFJwRvGJJnU"
openai.api_key = API_KEY
model_engine = "gpt-3.5-turbo-16k"

def get_pdf_to_text(pdffileobj):
    pdfreader = PyPDF2.PdfReader(pdffileobj)
    final_text = ""
    for iter in pdfreader.pages:
        final_text += str(iter.extract_text())
    return final_text

pdffileobj = open(r"C:\Users\pagal\OneDrive\Desktop\Akaike\chapter-3.pdf", 'rb')
pdf_data = get_pdf_to_text(pdffileobj)

def summarizer(text):
    if(len(text)<16385):
        return text
    stopword = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqtable = dict()
    for word in words:
        word = word.lower()
        if word in stopword:
            continue
        if word in freqtable:
            freqtable[word] = freqtable[word]+1
        else:
            freqtable[word] = 1
    sentences = sent_tokenize(text)
    sentencevalue = dict()
    for sentence in sentences:
        for word, freq in freqtable.items():
            if word in sentence.lower():
                if sentence in sentencevalue:
                    sentencevalue[sentence] = freq + sentencevalue[sentence]
                else:
                    sentencevalue[sentence] = freq
    sumvalues = 0
    for sentence in sentencevalue:
        sumvalues = sentencevalue[sentence] + sumvalues
    average = int(sumvalues / len(sentencevalue))
    summary = ''
    for sentence in sentences:
        if (sentence in sentencevalue) and (sentencevalue[sentence] > (1.2 * average)):
            summary = summary + " " + sentence
    return summarizer(summary)

def get_chatgpt_response(content):
    messages = [
        {"role": "system",
         "content": "You are now a MCQ generator.Your questions must have two correct answers among the 4 options you are going to provide . Strictly frame mcq questions according to this. You have generate 10 mcq from the text given. The question compulsorily have two correct answers among the four choices. For Example, QUESTION : orange is what? Options : a)Fruit b)Color c)Animal d)bird.You can see both a and b are the correct answers.Just frame questions like this.Dont give options and answers"  },
        {"role": "user", "content": content},
        {"role": "assistant", "content": "Give correct mcq generated with 2 correct answers among the 4 options."}
    ]
    response = openai.ChatCompletion.create(
    model=model_engine,
    messages=messages
    )
    generated_text = response['choices'][0]['message']['content']
    return  generated_text

def get_mca_questions(context: str):
    mca_questions = []
    summarized_context = summarizer(context)
    all_mca = get_chatgpt_response(summarized_context)
    mcas = str(all_mca).split('\n')
    for iter in mcas:
        try:
            serialnumber = iter[0]
            if(serialnumber in '0123456789'):
                mca_questions.append(iter)
        except:
            continue
    return mca_questions
