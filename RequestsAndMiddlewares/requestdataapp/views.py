from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context)


def user_bio_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')


def upload_file_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('file'):
        myfile = request.FILES['file']
        max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024  # 1MB
        if myfile.size > max_size_bytes:
            return HttpResponseBadRequest(f'File "{myfile.name}" too big!')
        if myfile.content_type not in settings.ALLOWED_MIME_TYPES:
            return HttpResponseBadRequest("Недопустимый тип файла.")
        fs = FileSystemStorage(location=str(settings.MEDIA_ROOT))
        file_name = fs.save(fs.get_valid_name(myfile.name), myfile)
        print(f'File saved: {file_name}')
    return render(request, 'requestdataapp/file-upload.html')
