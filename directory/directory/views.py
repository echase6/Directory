from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from directory.logic import update_directory_entry, delete_directory_entry
from directory.logic import get_all_entries, get_entries_by_name
from directory.logic import create_directory_entry
from directory.models import AddressEntry
from directory.settings import API_VERSION


@csrf_exempt
def address_list(request):
    """
    Retrieve all addresses in the database.
    """
    if 'api' in request.GET and request.GET['api'] == API_VERSION:
        if 'name' in request.GET:
            name = request.GET['name']
        else:
            name = ''
        if 'address' in request.GET:
            address = request.GET['address']
        else:
            address = ''
        if request.method == 'GET':
            if name != '':
                entries = get_entries_by_name(name)
            else:
                entries = get_all_entries()
            return JsonResponse(entries, safe=False)
        elif request.method == 'POST':
            if name != '' and address != '':
                try:
                    create_directory_entry(name, address)
                    return HttpResponse(status=200)
                except AddressEntry.AlreadyExists:
                    return HttpResponse(status=403)
        elif request.method == 'PUT':
            if name != '' and address != '':
                try:
                    update_directory_entry(name, address)
                    return HttpResponse(status=200)
                except AddressEntry.DoesNotExist:
                    return HttpResponse(status=404)
        elif request.method == 'DELETE':
            if name != '' and address != '':
                try:
                    delete_directory_entry(name, address)
                    return HttpResponse(status=204)
                except AddressEntry.DoesNotExist:
                    return HttpResponse(status=404)
    return HttpResponse(status=400)


def address_by_key(request, name):
    """
    Retrieve addresses associated with a name.
    """
    if request.method == 'GET' and request.GET['api'] == API_VERSION:
        entries = get_entries_by_name(name)
        return JsonResponse(entries, safe=False)
    return HttpResponse(status=400)


@csrf_exempt
def address_by_key_value(request, name, address):
    """
    Add, Update or Delete an address
    """
    if request.method == 'POST' and request.GET['api'] == API_VERSION:
        try:
            create_directory_entry(name, address)
            return HttpResponse(status=200)
        except AddressEntry.AlreadyExists:
            return HttpResponse(status=403)
    elif request.method == 'PUT' and request.GET['api'] == API_VERSION:
        try:
            update_directory_entry(name, address)
            return HttpResponse(status=200)
        except AddressEntry.DoesNotExist:
            return HttpResponse(status=404)
    elif request.method == 'DELETE' and request.GET['api'] == API_VERSION:
        try:
            delete_directory_entry(name, address)
            return HttpResponse(status=204)
        except AddressEntry.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=400)
