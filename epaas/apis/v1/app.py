# -*- coding: utf-8 -*-
from epaas.models import App


def applist_schema(title, sort, page: int, limit: int, author):
    page = int(page)
    limit = int(limit)
    applist = []
    items = App.query.all()
    if title:
        filter(lambda item: item['title'] == title, items)
    if author != '' and not author:
        filter(lambda item: item['name'] == author, items)
    if sort == '-id':
        items = items.reverse()
    start = (page - 1) * limit
    end = limit * page
    apps = items[start:end]
    for app in apps:
        app_json = {
            'id': app.id,
            'title': app.name,
            'author': app.author,
            'description': app.description,
            'docker_images': app.docker_images,
            'module_env': app.module_env,
            'modulename': app.modulename
        }
        applist.append(app_json)
    return applist, len(items)
