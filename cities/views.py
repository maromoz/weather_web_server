# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
from audioop import reverse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        if city_temperature <= 9:
            image = "../static/images/cloud-37011_640.png"
        elif city_temperature >= 10 and city_temperature <= 19:
            image = "../static/images/weather-157114_640.png"
        elif city_temperature >= 20:
            image = "../static/images/sun-159392_640.png"
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+name+'&key=AIzaSyDeJsN1m7f1gmun0G3NZedinAaAJLBwZkE'
        weather = urllib2.urlopen(url)
        wjson = weather.read()
        wjdata = json.loads(wjson)
        lat = wjdata['results'][0]['geometry']['location']['lat']
        lng = wjdata['results'][0]['geometry']['location']['lng']

    template = loader.get_template('city_weather.html')
    context = Context({
        'c': city_list[0],
        "weather": {'image': image},
        "geocoding": {'lat': lat, 'lng': lng},
    })
    return HttpResponse(template.render(context))

@csrf_exempt
def get_favorite(request):
    favorite_list = Favorite.objects.all()
    city_list = []
    degree_system = request.GET.get('degree')
    for favorite in favorite_list:
        filtered_cities = Cities.objects.filter(id=favorite.city_id)
        if len(filtered_cities) == 0:
            print "Warning: no cities found for id %d " % favorite.city_id
        if len(filtered_cities) > 1:
            print "Warning: more than 1 city found for id %d, using the first city" % favorite.city_id
        city_temperature = filtered_cities[0].temperature
        if city_temperature <= 9:
            image = "../static/images/cloud-37011_640.png"
        elif city_temperature >= 10 and city_temperature <= 19:
            image = "../static/images/weather-157114_640.png"
        elif city_temperature >= 20:
            image = "../static/images/sun-159392_640.png"
        else:
            image = "../static/images/cloud-37011_640.png"
        filtered_cities[0].image = image
        city_list.append(filtered_cities[0])
        if degree_system == "Fahrenheit":
            filtered_cities[0].temperature = filtered_cities[0].temperature * 1.8 + 32

    degree = "℃"
    if degree_system == "Fahrenheit":
        degree = "°F"
    template = loader.get_template('get_favorite.html')
    context = Context({
        'favorite_list': city_list,
        "stuff": {'degree': degree},
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
    for item in city_list:
        city_list_id = item.id
    favorite_list = Favorite.objects.filter(city_id=city_list_id)
    if len(favorite_list) >= 1:
        return HttpResponse("The city already exists in the favorite list")
    f = Favorite(city_id=city_list_id)
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
    city_list = Cities.objects.filter(name=name)
    for item in city_list:
        city_list_id = item.id
    favorite_list = Favorite.objects.filter(city_id=city_list_id)
    if len(favorite_list) == 0:
        return HttpResponse("The city does not exists in the favorite list")
    favorite_list.delete()
    return HttpResponse("The city was removed from your favorite list (:")


@csrf_exempt
def delete_id_from_db(request):
    favorite = Favorite.objects.filter(city_id=request.POST.get('id'))
    favorite.delete()
    return HttpResponse()

@csrf_exempt
def get_auto_complete_cities(request):
    start_of_city_name = request.GET.get('text')
    possible_cities = Cities.objects.filter(name__istartswith=start_of_city_name)
    possible_cities_names = []
    for city in possible_cities:
        possible_cities_names.append(city.name)

    return JsonResponse({'possible_cities':possible_cities_names})

@csrf_exempt
def add_id_to_db(request):
    # write the new city to the favorite table
    name_to_add = request.POST.get('city')
    city_to_add = Cities.objects.get(name=name_to_add)
    new_favorite = Favorite(city_id=city_to_add.id)
    new_favorite.save()

    #render html element for js
    degree_system = request.GET.get('degree')
    degree = "℃"
    if degree_system == "Fahrenheit":
        degree = "°F"
        city_to_add.temperature = city_to_add.temperature * 1.8 + 32

    city_temperature = city_to_add.temperature
    if city_temperature <= 9:
        image = "../static/images/cloud-37011_640.png"
    elif city_temperature >= 10 and city_temperature <= 19:
        image = "../static/images/weather-157114_640.png"
    elif city_temperature >= 20:
        image = "../static/images/sun-159392_640.png"
    else:
        image = "../static/images/cloud-37011_640.png"
    city_to_add.image = image


    context = Context({
        'favorite': city_to_add,
        "stuff": {'degree': degree},
    })
    return render_to_response('single_city.html', context)

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
