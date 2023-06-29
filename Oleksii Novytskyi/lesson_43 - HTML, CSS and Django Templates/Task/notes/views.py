from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import Notes, Categories
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NotesForm
from django_filters.views import FilterView
from .filters import ProductFilter


# def index(request):
#     latest_notes_list = Categories.objects.order_by('id')[:5]
#     context = {'latest_notes_list': latest_notes_list}
#     return render(request, 'notes/.html', context)


def notes(request):
    notes = Notes.objects.select_related('categories').all()
    # form = SearchForm(request.POST)
    # if form.is_valid():
    #     form.save()
    #         # Редирект або інші дії після збереження форми
    # else:
    #     form = SearchForm()

    return render(request, 'notes/index.html', {'data': notes})


def create_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            # form.save()
            q = Notes(categories=form.cleaned_data['categories'], title=form.cleaned_data['title'],
                         text=form.cleaned_data['text'], reminder=form.cleaned_data['reminder'])
            q.save()

            # return redirect('notes/index.html')  # Перенаправлення на сторінку зі списком нотаток
            return HttpResponseRedirect('/notes/')
    else:
        form = NotesForm()

    return render(request, 'notes/create_note.html', {'form': form})


def delete_note(request, note_id):
        if request.method == 'POST':
            note = Notes.objects.get(pk=note_id)
            note.delete()
            return redirect('/notes/')  # Перенаправлення на сторінку зі списком нотаток
        else:
            return HttpResponseRedirect('/notes/')  # Перенаправлення на головну сторінку, якщо метод не є POST


def correct_note(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/notes/')
    else:
        form = NotesForm(instance=note)

    return render(request, 'notes/correct_note.html', {'form': form})


def filter_notes(request):

    category = request.GET.get('category').capitalize()
    title = request.GET.get('title').capitalize()
    reminder = request.GET.get('reminder').capitalize()
    # search_staff = {'form': SearchForm()}
    filtered_notes = Notes.objects.all()

    # if search_staff:
    #     filtered_notes = filtered_notes.filter(categories__title=SearchForm.categories)
        # filtered_notes = filtered_notes.filter(categories__title=SearchForm.title)
        # filtered_notes = filtered_notes.filter(categories__title=SearchForm.reminder)

    if category:
        filtered_notes = filtered_notes.filter(categories__title=category)
    if title:
        filtered_notes = filtered_notes.filter(title__icontains=title)
    if reminder:
        filtered_notes = filtered_notes.filter(reminder__icontains=reminder)

    return render(request, 'notes/filter_notes.html', {'notes': filtered_notes})


def find_notes(request):

    title = request.GET.get('title').capitalize()
    filtered_notes = Notes.objects.all()
    if title:
        filtered_notes = filtered_notes.filter(title__icontains=title)
    return render(request, 'notes/find_notes.html', {'notes': filtered_notes})


def search(request):
    query = request.GET.get('searching_text')
    results = Notes.Notes.objects.all()
    if query:
        results = Notes.objects.filter(title__icontains=query)

    context = {
        'results': results,
    }
    return render(request, 'notes/search.html', context)

