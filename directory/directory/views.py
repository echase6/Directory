"""directory views"""

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from directory.logic import create_directory_entry
from directory.logic_async import get_all_entries, get_entries_by_name
from directory.logic import update_directory_entry, delete_directory_entry
from directory.models import AddressEntry
from directory.settings import API_VERSION


@csrf_exempt
def address_list(request):
    """
    Retrieve all addresses in the database.
    """
    if 'api' in request.GET and request.GET['api'] == API_VERSION:
        name = get_name(request)
        address = get_address(request)

        if request.method == 'GET':
            return respond_to_get(name)

        if name == '' or address == '':
            return HttpResponse(status=400)

        if request.method == 'POST':
            return respond_to_post(name, address)

        if request.method == 'PUT':
            return respond_to_put(name, address)

        if request.method == 'DELETE':
            return respond_to_delete(name, address)

    return HttpResponse(status=400)


@csrf_exempt
def address_by_key(request, name):
    """
    Retrieve addresses associated with a name.
    """
    if 'api' in request.GET and request.GET['api'] == API_VERSION:
        if request.method == 'GET':
            return respond_to_get(name)

    return HttpResponse(status=400)


@csrf_exempt
def address_by_key_value(request, name, address):
    """
    Add, Update or Delete an address
    """
    if 'api' in request.GET and request.GET['api'] == API_VERSION:
        if name == '' or address == '':
            return HttpResponse(status=400)

        if request.method == 'POST':
            return respond_to_post(name, address)

        if request.method == 'PUT':
            return respond_to_put(name, address)

        if request.method == 'DELETE':
            return respond_to_delete(name, address)

    return HttpResponse(status=400)


def get_name(request):
    """
    Get the name string from the request. Return empty string if not found
    :param request:
    :return:
    """
    if 'name' in request.GET:
        return request.GET['name']
    else:
        return ''


def get_address(request):
    """
    Get the address string from the request. Return empty string if not found
    :param request:
    :return:
    """
    if 'address' in request.GET:
        return request.GET['address']
    else:
        return ''


def respond_to_get(name):
    """
    Return the appropriate response to GET, depending on whether the name
      parameter was provided, i.e., w/o a name, return all entries
    :param name:
    :return:
    """
    if name == '':
        entries = get_all_entries()
    else:
        entries = get_entries_by_name(name)
    return JsonResponse(entries, safe=False)


def respond_to_post(name, address):
    """
    Process a POST request
    Return the appropriate response to POST, i.e., respond OK only if the
      entry does not already exist
    :param name:
    :param address:
    :return:
    """
    try:
        create_directory_entry(name, address)
        return HttpResponse(status=200)
    except AddressEntry.AlreadyExists:
        return HttpResponse(status=403)


def respond_to_put(name, address):
    """
    Process a PUT request
    Return the appropriate response to PUT, i.e., respond OK only if the
      entry does already exist
    :param name:
    :param address:
    :return:
    """
    try:
        update_directory_entry(name, address)
        return HttpResponse(status=200)
    except AddressEntry.DoesNotExist:
        return HttpResponse(status=404)


def respond_to_delete(name, address):
    """
    Process a DELETE
    Return the appropriate response to DELETE, i.e., respond OK only if the
      entry does already exist
    :param name:
    :param address:
    :return:
    """
    try:
        delete_directory_entry(name, address)
        return HttpResponse(status=204)
    except AddressEntry.DoesNotExist:
        return HttpResponse(status=404)
