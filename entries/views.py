from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm

# Create your views here.
def home(request):
    # entries = Entry.objects.all()
    entries = Entry.objects.order_by('-date_posted') #orders the date in "ascending" order


    if request.method == 'POST':
        # print(request.POST)
        if 'entryDelete' in request.POST:
            selectedEntry = request.POST['entryDelete']
            selectedEntry = (selectedEntry.split(' '))[1]
            # print(selectedEntry)
            entry = Entry.objects.get(id=selectedEntry)
            entry.delete()


    return render(request,'entries/home.html',{'entries':entries})


def edit(request):
    print(request.method)
    
    if request.method == "GET":
        editingEntry = request.GET.get('text',None)
    else:
        editingEntry = request.POST.get('text',None)
    
    print(editingEntry)
    # print(editObject)
    if editingEntry is not None:
        editingEntry = (editingEntry.split(' '))[1]
        editObject = get_object_or_404(Entry,id=editingEntry)
        print(editObject)
    else:
        editObject = ''
    
    if request.method == "POST":
        # if editObject:
        print(editObject)
        print("[+] EDITING ENTRY")
        form = EntryForm(request.POST,instance=editObject)
        print(form)
        if form.is_valid():
            print("[+] FORM VALID")
            form.save()
            # print(form)
            return redirect('home')
    else:
        form = EntryForm(instance=editObject)
    
    # print(editObject.id)
    return render(request,'entries/edit.html',{'form':form,'editObject':editObject})

def add(request):
    print(request)
    form = EntryForm(request.POST)
    if request.method == "POST":              
        if form.is_valid():
            print("[+] VALID FORM")
            print(form)
            form.save()
            return redirect('home')
        else:
            form = EntryForm()
    
    return render(request,'entries/add.html',{'form':form})