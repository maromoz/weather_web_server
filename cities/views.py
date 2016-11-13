# -*- coding: utf-8 -*-
from audioop import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
# Create your views here.
from django.db import connection
from django.http import HttpResponse
from django.template import RequestContext

from cities.models import Cities, Favorite
from django.template import Context
from django.template import loader
from django.utils.encoding import smart_str, smart_unicode
import math
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def get_cities(request):
    cities = Cities.objects.all()
    response = ""
    for item in cities:
        city_name = item.name
        response += "%s<br>" % city_name

    template = loader.get_template('get_cities.html')
    context = Context({
        'cities': cities
    })
    return HttpResponse(template.render(context))


def get_city_temp(request):
    params = request.GET
    if 'name' not in request.GET:
        template = loader.get_template('get_city_temp.html')
        return HttpResponse(template.render())

    if params["name"] == "":
        response = "Please enter a city and press enter"
        return HttpResponse(response)

    name = request.GET.get('name')
    city_list = Cities.objects.filter(name=name)
    if len(city_list) == 0:
        return HttpResponse("Oops, the city you have asked is not available")
    for item in city_list:
        city_temperature = item.temperature
        if city_temperature >= 0 and city_temperature<=9:
            image = "../static/images/cloud-37011_640.png"
        elif city_temperature >= 10 and city_temperature<= 19:
            image = "../static/images/weather-157114_640.png"
        elif city_temperature >= 20:
            image = "../static/images/sun-159392_640.png"


    template = loader.get_template('city_weather.html')
    context = Context({
        'c': city_list[0],
        "weather": {'image': image}
    })
    return HttpResponse(template.render(context))


def get_favorite(request):
    print request.GET
    favorite_list = Favorite.objects.all()
    response = ""
    for item in favorite_list:
        favorite_name = item.name
        city_temperature = item.temperature
        response += "%s - %s" % (favorite_name, city_temperature)

    degree = "℃"
    template = loader.get_template('get_favorite.html')
    context = Context({
        'favorite': favorite_list,
        "stuff": {'degree': degree}
    })
    return HttpResponse(template.render(context))


def add_city_to_favorite(request):
    params = request.GET
    if 'add' not in request.GET:
        template = loader.get_template('add_city_to_favorite.html')
        return HttpResponse(template.render())

    if params["add"] == "":
        response = "Please enter a city and press enter"
        return HttpResponse(response)

    name = request.GET.get('add')
    city_list = Cities.objects.filter(name=name)
    if len(city_list) == 0:
        return HttpResponse("The city does not exists please choose a different city from the cities list")
    favorite_list = Favorite.objects.filter(name=name)
    if len(favorite_list) >= 1:
        return HttpResponse("The city already exists in the favorite list")
    city_temperature = city_list[0].temperature
    f = Favorite(name=name, temperature=city_temperature)
    f.save()
    return HttpResponse("The city was added to your favorite list (:")


def remove_city_from_favorite(request):
    params = request.GET
    if 'remove' not in request.GET:
        template = loader.get_template('remove_city_from_favorite.html')
        return HttpResponse(template.render())

    if params["remove"] == "":
        response = "Please enter a city and press enter"
        return HttpResponse(response)

    name = request.GET.get('remove')
    favorite_list = Favorite.objects.filter(name=name)
    if len(favorite_list) == 0:
        return HttpResponse("The city does not exists in the favorite list")
    favorite_list.delete()
    return HttpResponse("The city was removed from your favorite list (:")


#############################################OLD############################################


def cities(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM cities")
        row = cursor.fetchall()
        result = list()
        for city in row:
            city = city[0]
            result.append(city)
            result.append("\n")
    if request.GET.get('name', ''):
        name = request.GET.get('name')
        if name not in result:
            return HttpResponse("Oops, the city you have asked is not available")
        with connection.cursor() as cursor:
            cursor.execute('SELECT cities.temprature FROM cities where cities.name = "%s"' % name)
            query = cursor.fetchone()
        return HttpResponse(query)
    return HttpResponse(result)


def favorite(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT name FROM favorite')
        row = cursor.fetchall()
        favorite_list = list()
        for city in row:
            cursor.execute('SELECT name,temprature,last_updated from cities WHERE name = "%s"' % city)
            city_forecast = cursor.fetchone()
            favorite_list.append(city_forecast)
    return HttpResponse(favorite_list)


def add_to_favorite(request):
    if request.GET.get('add', ''):
        city_name = request.GET.get('add')
        with connection.cursor() as cursor:
            cursor.execute('SELECT count(*) FROM cities WHERE name = "%s"' % city_name)
            test = cursor.fetchone()[0]
            if test == 0:
                not_exists = "The city does not exists please choose a different city from the cities list"
                return HttpResponse(not_exists)
            cursor.execute('SELECT count(*) FROM favorite WHERE name = "%s"' % city_name)
            test = cursor.fetchone()[0]
            if test == 1:
                already_in_table = "The city already exists in the favorite list"
                return HttpResponse(already_in_table)
            cursor.execute('INSERT INTO favorite (favorite.name) VALUES ("%s")' % city_name)
            success = "The city was added to your favorite list (:"
            return HttpResponse(success)


def remove_from_favorite(request):
    if request.GET.get('remove', ''):
        city_name = request.GET.get('remove')
        with connection.cursor() as cursor:
            cursor.execute('SELECT count(*) FROM favorite WHERE name = "%s"' % city_name)
            test = cursor.fetchone()[0]
            if test == 0:
                not_exists = "The city does not exists please choose a different city from the favorite list"
                return HttpResponse(not_exists)
            cursor.execute('DELETE FROM favorite WHERE name = "%s"' % city_name)
            success = "The city was removed from your favorite list (:"
        return HttpResponse(success)
