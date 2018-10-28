import io
import zipfile

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from taxcalculation import utils
from taxcalculation.forms import FileUploaderForm
from taxcalculation.models import File, Person
from taxcalculation.output import Output


def home(request):
    # File.objects.all().delete()
    files = File.objects.all()
    return render(request, "taxcalculation/home.html", {'section': 'home',
                                                        'files': files})


def upload(request):
    if request.POST:
        form = FileUploaderForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save()
            try:
                new_file.populate_person_from_file()
            except:
                new_file.delete()
                messages.error(request, 'Upload FAIL! Please upload a valid file type with valid formation of data')
                return HttpResponseRedirect(reverse("taxcalculation:upload"))

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


def show_individual_pdf(request, id):
    p = get_object_or_404(Person, id=id)
    try:
        person = Output(p)
    except:
        messages.error(request, 'Something went Wrong. Can not show tax details for' + p.name)
        return HttpResponseRedirect(reverse("taxcalculation:file_detail", args=[p.file_id]))

    return utils.PdfRender.getPdfResponse("taxcalculation/pdf.html", {'person': person})


def download_all_pdf(request, id):
    print('asche')
    file = get_object_or_404(File, id=id)
    ps = Person.objects.filter(file=file)

    b = io.BytesIO()
    zf = zipfile.ZipFile(b, "w")
    for p in ps:
        person = Output(p)
        pdf = utils.PdfRender.getPdf("taxcalculation/pdf.html", {'person': person})
        zf.writestr(person.name + ".pdf", pdf.getvalue())

    print(zf.namelist())
    zf.filename = file.get_filename()
    zf.close()

    resp = HttpResponse(b.getvalue(), content_type="application/x-zip-compressed")

    resp['Content-Disposition'] = 'attachment; filename=%s' % file.get_filename().split(".")[0]+".zip"

    return resp
