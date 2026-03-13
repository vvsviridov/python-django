from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
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
        allowed_size = 1 * 1024 * 1024  # 1MB
        if myfile.size > allowed_size:
            return HttpResponse(f'File "{myfile.name}" too big!')
        storage_path = settings.BASE_DIR / "uploads"
        fs = FileSystemStorage(location=str(storage_path))
        file_name = fs.save(myfile.name, myfile)
        print(f'File saved: {file_name}')
    return render(request, 'requestdataapp/file-upload.html')
