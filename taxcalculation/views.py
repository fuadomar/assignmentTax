import datetime
import io
import zipfile

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from taxcalculation import utils
from taxcalculation.forms import FileUploaderForm
from taxcalculation.models import File, Person
from taxcalculation.output import Output


def home(request):
    #File.objects.all().delete()
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
            except Exception as e:
                print("exception"+str(e))
                new_file.delete()
                messages.error(request, 'Upload FAIL! Please upload a valid file type with valid formation of data')
                return HttpResponseRedirect(reverse("taxcalculation:upload"))

            return HttpResponseRedirect(reverse('taxcalculation:home'))
        else:
            messages.error(request, 'Upload FAIL! Please upload a valid file type with valid formation of data')
            return HttpResponseRedirect(reverse("taxcalculation:upload"))

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

    #pdf=utils.PdfRender.getPdf_xhtml2pdf("taxcalculation/pdf.html", {'person': person})
    #pdf=pdf.getvalue()
    pdf=utils.PdfRender.getPdf_weasyprint("taxcalculation/pdf.html", {'person': person})

    return  HttpResponse(pdf, content_type='application/pdf')



def download_all_pdf(request, id):
    file = get_object_or_404(File, id=id)
    ps = Person.objects.filter(file=file)

    b = io.BytesIO()
    zf = zipfile.ZipFile(b, "w")

    try:
        for p in ps:
            person = Output(p)
            a = datetime.datetime.now()
            #pdf = utils.PdfRender.getPdf_xhtml2pdf("taxcalculation/pdf.html", {'person': person})
            #pdf=pdf.getvalue()
            pdf = utils.PdfRender.getPdf_weasyprint("taxcalculation/pdf.html", {'person': person})
            print("pdf" + str(datetime.datetime.now() - a))
            zf.writestr(person.name + ".pdf", pdf)
    except:
        messages.error(request, 'Something went Wrong. Could not build the zip')
        return HttpResponseRedirect(reverse("taxcalculation:file_detail", args=[p.file_id]))

    #print(zf.namelist())
    zf.filename = file.get_filename()
    zf.close()

    resp = HttpResponse(b.getvalue(), content_type="application/x-zip-compressed")

    resp['Content-Disposition'] = 'attachment; filename=%s' % file.get_filename().split(".")[0]+".zip"

    return resp
