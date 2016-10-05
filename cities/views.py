from django.shortcuts import render

# Create your views here.
from django.db import connection
from django.http import HttpResponse
from cities.models import Cities, Favorite


def get_cities(request):
    cities = Cities.objects.all()
    response = ""
    for item in cities:
        city_name = item.name
        response += "%s<br>" % (city_name)
    return HttpResponse(response)


def get_city_temp(request):
    if 'name' not in request.GET:
        return HttpResponse("please specify name of city")
    name = request.GET.get('name')
    city_list = Cities.objects.filter(name=name)
    if len(city_list) == 0:
        return HttpResponse("Oops, the city you have asked is not available")
    city_temperature = city_list[0].temprature
    temp_response = "%s<br>" % city_temperature
    return HttpResponse(temp_response)


def get_favorite(request):
    favorite_list = Favorite.objects.all()
    response = ""
    for item in favorite_list:
        favorite_name = item.name
        response += "%s<br>" % favorite_name
    return HttpResponse(response)


def add_city_to_favorite(request):
    if 'add' not in request.GET:
        return HttpResponse("please write the word add before the name of the city")
    name = request.GET.get('add')
    city_list = Cities.objects.filter(name=name)
    if len(city_list) == 0:
        return HttpResponse("The city does not exists please choose a different city from the cities list")
    favorite_list = Favorite.objects.filter(name=name)
    if len(favorite_list) >= 1:
        return HttpResponse("The city already exists in the favorite list")
    f = Favorite(name=name)
    f.save()
    return HttpResponse("The city was added to your favorite list (:")


def remove_city_from_favorite(request):
    if 'remove' not in request.GET:
        return HttpResponse("please write the word remove before the name of the city")
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
