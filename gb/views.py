from django.shortcuts import render, redirect
from gb.models import mesage
# Create your views here.
def gb (request):
    mes = mesage.objects.all()
    args = {'mes': mes}
    return render(request, 'gb.html', args)
def send (request):
    m_tema = None
    m_otzyv = None

    if 'tema' in request.POST:
        m_tema = request.POST['tema']

    if 'otzyv' in request.POST:
        m_otzyv = request.POST['otzyv']

    if m_tema and m_otzyv:
        new_mesage = mesage(tema=m_tema, otzyv=m_otzyv)
        new_mesage.save()

    #return redirect('/gb/')



    mes = mesage.objects.all()
    args = {'mes': mes}
    return render(request, 'gb.html', args)