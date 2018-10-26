from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from taxcalculation.forms import FileUploaderForm
from taxcalculation.models import File, Person
from taxcalculation.output import Output


def home(request):

    files = File.objects.all()
    return render(request, "taxcalculation/home.html", {'section': 'home',
                                                        'files': files})


def upload(request):
    if request.POST:
        form = FileUploaderForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save()
            new_file.populate_person_from_file()

            return HttpResponseRedirect(reverse('taxcalculation:home'))
        else:
            return HttpResponse("something went wrong")

    else:
        form = FileUploaderForm()
        return render(request, "taxcalculation/upload.html", {'section': 'upload',
                                                              'form': form})


def file_detail(request, id):
    file = get_object_or_404(File, id=id)
    persons = Person.objects.filter(file=file)

    return render(request, "taxcalculation/file_detail.html", {'section': 'home',
                                                               'persons': persons,
                                                               'file': file})


def generate_individual_pdf(request, id):
    p = get_object_or_404(Person, id=id)
    person = (Output(p))

    return render(request, "taxcalculation/pdf.html", {'person': person})
