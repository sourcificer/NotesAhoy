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
    editingEntry = request.GET.get('text',None)
    print(editingEntry)
    if editingEntry is not None:
        editingEntry = (editingEntry.split(' '))[1]
        editObject = get_object_or_404(Entry,id=editingEntry)
        print(editObject)
    else:
        editObject = ''
    
    if request.method == "POST":
        if editObject:
            print(editObject)
            print("[+] EDITING ENTRY")
            form = EntryForm(request.POST,instance=editObject)
            if form.is_valid():
                print("[+] FORM VALID")
                form.save()
                print(form)
                # return redirect('home')
    
    return render(request,'entries/add.html',{'form':form})

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