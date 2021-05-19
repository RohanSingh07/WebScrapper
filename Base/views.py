from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen
from . import  models
# Create your views here.
def Homeview(request):
    return render(request,'index.html',{})

def Frequency(request):
    return render(request,'Frequency.html',{})

# List of common words
common_words = ['the', 'at', 'there', 'some', 'my', 'of', 'be', 'use', 'her', 'than', 'and', 'this', 'an', 'would',
                'first', 'a', 'have', 'each', 'make', 'water',
                'to', 'from', 'which', 'like', 'been', 'in', 'or', 'she', 'him', 'call', 'is', 'one', 'do', 'into',
                'who', 'you', 'had', 'how', 'time', 'oil', 'that'
                , 'by', 'their', 'has', 'its', 'it', 'word', 'if', 'look', 'now', 'he', 'but', 'will', 'two', 'find', 'was',
                'not', 'up', 'more', 'long', 'for', 'what',
                'other', 'write', 'down', 'on', 'all', 'about', 'go', 'day', 'are', 'were', 'out', 'see', 'did',
                'as', 'we', 'many', 'number', 'get', 'with', 'when', 'then',
                'no', 'come', 'his', 'your', 'them', 'way', 'made', 'they', 'can', 'these', 'could', 'may', 'i',
                'said', 'so', 'people', 'part', 'should','again','{','}','(',')','+','-','=','}}','{{','%','{%','%}']
def Result(request):
    url = request.POST['URL']
    DB = models.Urlword.objects.filter(url = url)
    # if the url is already processed
    if DB.exists():
        Url = DB[0]
        fresh = 0
    else:
        # Open the page
        page = urlopen(url)
        # Decode the html
        html = page.read().decode("utf-8")
        # Parse the html elements
        soup = BeautifulSoup(html, "html.parser")
        # Extract the text
        text= soup.get_text()
        # Remove all the new lines
        final_text = str(text).replace('\n','')
        # Make list of words
        word_list = list(final_text.split())
        countlist=[]
        fresh=1
        # remove the common words
        for words in word_list:
            if words.lower() not in common_words and {'word':words,'count':word_list.count(words)} not in countlist:
                countlist.append(
                    {'word':words,'count':word_list.count(words)}
                )
        # Sort the result is ascending order
        sorted_words = sorted(countlist, key=lambda k: k['count'],reverse=True)
        # Save the top 10 words with url
        Url = models.Urlword(
            url=url
        )
        Url.save()
        for i in range(10):
            word,count = sorted_words[i]['word'],sorted_words[i]['count']
            new_word = models.Word(
                word= word,
                frequency = count
            )
            new_word.save()
            Url.words.add(new_word)
    return render(request, 'Result.html', {
    'Urlword':Url,
    'Freshprep': fresh
    })