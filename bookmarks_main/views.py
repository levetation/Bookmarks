from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Saved_Bookmarks

# Create your views here.
def home(request):
    context = {}
    bookmarks = Saved_Bookmarks.objects.order_by('-bookmark_save_date') # display in decending order
    context['bookmarks'] = bookmarks

    if request.method == 'POST' and 'submit_new_bookmark' in request.POST:
        
        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']
        
        new_bookmark = Saved_Bookmarks(
            bookmark_title = new_bookmark_title, 
            bookmark_address = new_bookmark_address,
            bookmark_notes = new_bookmark_notes
        )

        new_bookmark.save()
        return HttpResponseRedirect('')

    if request.method == 'POST' and 'delete_bookmark' in request.POST:
        delete_bookmark(request, request.POST['bookmark_id'])
        return HttpResponseRedirect('')
    
    return render(request, 'bookmarks_main/index.html', context)

def delete_bookmark(request, id):
    bookmark_checked = Saved_Bookmarks.objects.get(pk=id)
    bookmark_checked.delete()
    return redirect('home-page')