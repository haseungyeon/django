from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextId = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Rountind is ..'},
    {'id': 2, 'title': 'views', 'body': 'View is ..'},
    {'id': 3, 'title': 'Model', 'body': 'Model is ..'},
]


def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''<form action="/delete/" method="POST">
            <input type="hidden" name="id" value={id}>
            <input type="submit" value="delete">
        </form>'''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return HttpResponse(f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ul>
                {ol}
            </ul>
            {articleTag}
            <h2><a href="/create">create</a></h2>
            {contextUI}
        </body>
    </html>
    ''')


def index(requeset):
    article = '''
        <h2>Welcome</h2>
        Hello, Django'''
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    global nextId
    article = ''''''
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        print("pppppost", request.POST)
        # article = f'''
        # <h2>{request.POST["title"]}</h2>
        # <p>{request.POST["body"]}</p>
        # '''
        title = request.POST["title"]
        body = request.POST["body"]
        newTopic = {"id":nextId,"title":title, "body":body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)
        nextId += 1
        return redirect(url)


def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if str(topic["id"]) == id:
            article = f'<h2>{str(topic["title"])}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST["id"]
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        print("id:", id)
        # del topics[id+1]
        return redirect('/')
        