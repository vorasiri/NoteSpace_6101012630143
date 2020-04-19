from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Note, Image, Tag, Review
from django.template.loader import get_template


def clear_string_space(input):
    return ' '.join(input.split())
# Clear the too many spaces


def home_page(request):
    notes = Note.objects.order_by('-upload_time')
    return render(request, 'home_page.html', {'notes': notes})
# Render home page with all notes


def upload_page(request):
    return render(request, 'upload_page.html')
# Render upload page


def upload_api(request):
    filetype_list = ['img', 'png', 'jpg', 'jpeg', 'tiff', 'gif', 'bmp']
    if request.POST:
        newnote = Note()
        newnote.name = clear_string_space(request.POST['name'])
        newnote.owner = clear_string_space(request.POST['ownername'])
        newnote.desc = clear_string_space(request.POST['desc'])
        newnote.save()
# Save note name, owner name and description to Note model
        i = 0
        for file in request.FILES.getlist('myfile'):
            if(len(file.name.split('.')) > 1 and
                    file.name.split('.')[-1].lower() in filetype_list):
                newimg = Image()
                newimg.image = file
                newimg.index = i
                newimg.note = newnote
                newimg.save()
                i += 1
# Check file type for all uploaded files and save Image model
        if(i == 0):  # all file is invalid
            newnote.delete()
            return HttpResponse('File Type Error')
# Return 'File Type Error' if none of these files aren't Image File
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


def detail(request, note_index):
    n = get_object_or_404(Note, pk=note_index)
    images = Image.objects.filter(note=n)
    img_url = [i.image.url for i in images]
    return render(request, 'detail.html', {'images_url': img_url, 'note': n})
# Render detail page with all note images


def about(request):
    return render(request, 'about.html')
# Render about page


def help(request):
    return render(request, 'help_main.html')
# Render the main help page showing the list of help topics


def help_detail(request, help_topic):
    try:
        get_template('help/%s.html' % (help_topic))
        return render(request, 'help/%s.html' % (help_topic))
    except:
        return HttpResponseNotFound('<h1>404 Page not found</h1>')
# Render help topic if it exist


def search(request):
    query_word = request.GET.get('q', '')
    searched_notes = Note.objects.filter(
        Q(name__icontains=query_word) |
        Q(desc__icontains=query_word) |
        Q(tags__title__icontains=query_word))
    return render(request, 'search_result.html', {
            'search_key': query_word,
            'searched_notes': searched_notes})
# Searching by name, description, and tag


def tag_query(request, tag_title):
    query_tag = get_object_or_404(Tag, title=tag_title)
    return render(request, 'tag_result.html', {'tag': query_tag})
# Show all notes that has relate tag


def addcomment_api(request):
    note_id = request.POST['note_id']
    n = Note.objects.get(id=note_id)
# Get the current note id
    author = request.POST['author']
    text = request.POST['text']
    score = float(request.POST['score'])
    if request.POST['score'] in ['1', '2', '3', '4', '5'] else 0
    review = Review()
    review.note = n
    review.author = author
    review.text = text
    review.score = score
    review.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# Save the comment, author and score to Review model