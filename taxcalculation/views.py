
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from taxcalculation.forms import FileUploaderForm
from taxcalculation.models import File

STARTING_ROW_INDEX = 15
NAME_COL_INDEX = 0
GENDER_COL_INDEX = 1
FEST_BONUS_COL_INDEX = 67
PF_COL_INDEX = 70
TOTAL_INCOME_COL_INDEX = 71


def file_detail(request, id):
    file = get_object_or_404(File,id=id)

    import openpyxl

    book = openpyxl.load_workbook(file.upload.file, data_only=True)
    sheet = book.active

    for row in sheet.iter_rows(min_row=15):
        if row[0].value is None:
            break
        print(row[0].value)




    return HttpResponse(str(file.filename()))

def home(request):
    files = File.objects.all()
    file = File.objects.get(id=1)
    print(file.filename())
    return render(request, "taxcalculation/home.html", {'section': 'home',
                                                        'files': files})

def upload(request):
    if request.POST:
        form= FileUploaderForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save()
            print(new_file.upload.name)
            print(new_file.upload.url)
            return HttpResponseRedirect(reverse('taxcalculation:home'))
        else:
            return HttpResponse("something went wrong")

    else:
        form = FileUploaderForm()
        return render(request,"taxcalculation/upload.html",{'section':'upload',
                                                            'form': form})
