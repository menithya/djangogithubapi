from django.shortcuts import render, HttpResponse
from datetime import datetime
import requests
import json


def show_view(request):
    items=[]
    if request.method == 'GET':
        search_term=request.GET.get('search_term','')
        if(search_term != ''):
            req = requests.get('https://api.github.com/search/repositories?q='+ search_term)
            search_result_list = req.json(); #store original data in temp
            items=search_result_list['items']
            items.sort(key=lambda n: n['created_at'], reverse=True)
            items=items[:5]
            for indx,data in enumerate(items):
                data['last_commit']={}
                data['order']=indx+1;
                data['created']= datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                try:
                    commit_url = 'https://api.github.com/repos/' + data['owner']['login'] + '/' + data['name'] + '/commits'
                    commit_result = requests.get(commit_url)
                    commit_result = commit_result.json()
                    last_commit = commit_result[0]
                    data['last_commit'] = last_commit
                except:
                    data['last_commit']['sha'] = 'Error in retrieving last commit'

    return render(request, 'template.html',{'items':items,'search_term':search_term})

