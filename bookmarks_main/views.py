from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Saved_Bookmarks
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def userhome(request):
    context = {}
    #bookmarks = Saved_Bookmarks.objects.order_by('-bookmark_save_date') # display in decending order
    bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id).order_by('-bookmark_save_date')
    context['bookmarks'] = bookmarks

    # get all unique catagories from user bookmarks
    bookmark_list = [bookmark for bookmark in bookmarks]
    catagories = list(set([entry.bookmark_catagory for entry in bookmark_list]))
    context['catagories'] = catagories

    if request.method =='POST' and 'select_catagory' in request.POST:
        bookmarks = Saved_Bookmarks.objects.filter(
            bookmark_catagory=request.POST['selected_bookmark_catagory'],
            author=request.user.id
        ).order_by('-bookmark_save_date')
        context['bookmarks'] = bookmarks
        return render(request, 'bookmarks_main/index.html', context)
    elif request.method =='POST' and 'view_all' in request.POST:
        return redirect(request.META['HTTP_REFERER'])

    if request.method == 'POST' and 'submit_new_bookmark' in request.POST:
        
        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']
        new_bookmark_catagory = request.POST['new_bookmark_catagory']
        
        new_bookmark = Saved_Bookmarks(
            bookmark_title = new_bookmark_title, 
            bookmark_address = new_bookmark_address,
            bookmark_notes = new_bookmark_notes,
            bookmark_catagory = new_bookmark_catagory,
            author = request.user,
        )

        new_bookmark.save()
        # return HttpResponseRedirect('')
        return redirect(request.META['HTTP_REFERER'])

    if request.method == 'POST' and 'delete_bookmark' in request.POST:
        delete_bookmark(request, request.POST['bookmark_id'])
        return HttpResponseRedirect('')
    
    return render(request, 'bookmarks_main/index.html', context)

def delete_bookmark(request, id):
    bookmark_checked = Saved_Bookmarks.objects.get(pk=id)
    bookmark_checked.delete()
    return redirect('home-page')

def edit_bookmark(request, id):
    bookmark_to_edit = Saved_Bookmarks.objects.get(pk=id)

    if request.method == 'POST' and 'submit_edit_selected_bookmark' in request.POST:
    
        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']
        new_bookmark_catagory = request.POST['new_bookmark_catagory']

        bookmark_update = Saved_Bookmarks.objects.filter(pk=id).update(
            bookmark_title=new_bookmark_title, 
            bookmark_address=new_bookmark_address, 
            bookmark_notes=new_bookmark_notes,
            bookmark_catagory=new_bookmark_catagory
            )

        messages.success(request, ("Bookmark updated"))

        return redirect(request.META['HTTP_REFERER'])
    
    return render(request, 'bookmarks_main/edit.html', {'bookmark_to_edit':bookmark_to_edit})

def home(request):
    return render(request, 'bookmarks_main/welcome.html', {})