from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Galery, Category, Objects, Movement
from .forms import GallaryAddForm, AddCategory, AddObject, AuthUserForm, AddMovement
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

# Create your views here.
# def index(request):
#     data = Galery.objects.all()
#     search = request.POST.get('search')
#     sr = []
#     nal = False
    # try:
    #     search = search.lower().split()
    #     counter=0
    #     for i in data:
    #         tmp = i.name.lower().split()
    #         for j in search:
    #             for y in tmp:
    #                 if y==j:
    #                     sr.append(i)
    #                     nal = True
    #                     break
    #             break
    #         nal = False
    #         counter=0
    #     if len(sr)==0:
    #         sr=None
    # except Exception:
    #     pass
#     category = Category.objects.all() #получаем объекты бд категории
#     for i in data: #цикл по объектам бд карточек
#        for j in category: #цикл по объектам бд категории
#             nal = True if i.category==j.category else False #наличие равно правде только если категория из бд карточек есть в бд категорий
#        if nal==False and i.category!='': #проверяем что наличия нет
#             newCat=Category.objects.create(category=i.category) #добавляем категорию
#             newCat.save()#сохраняем
#     objects = Objects.objects.all()
#     for i in data:
#         for j in objects:
#             nal = True if i.obj==j.object else False
#         if nal == False and i.obj!='':
#             newObj=Objects.objects.create(object=i.obj)
#             newObj.save()
#     if search!=None:
#         context = {
#             'search' : search,
#             'data': data,
#             'category' : Category.objects.all(),
#             'objects' : Objects.objects.all(),
#             'sr' : sr,
#             'search_past' : ' '.join(search)
#         }
#     else:
#         context = {
#             'search' : search,
#             'data': data,
#             'category' : Category.objects.all(),
#             'objects' : Objects.objects.all(),
#             'sr' : sr,
#             'search_past' : None
#         }
#     return render(request, 'main/index.html', context)
@login_required(login_url='/login/')
def redirect_to_home (request):
    return HttpResponseRedirect('/pictures/')

def search_task(request):
    fast_search = request.GET.get('fast_search', '')
    cards = Galery.objects.filter(
                                Q(author__iregex=fast_search) | Q(name__iregex=fast_search) |
                                Q(description__iregex=fast_search) | Q(dir__iregex=fast_search) |
                                Q(id__iregex=fast_search)
                                    )
    return render(request, 'main/cards.html', {'data': cards})
@login_required(login_url='/login/')
def index(request):
    search_query = request.GET.get('search_name', '')
    search_cat = request.GET.get('search_cat', '')
    search_obj = request.GET.get('search_obj', '')

    if search_query:
        if search_cat and search_obj:
            cards = Galery.objects.filter(Q(author__iregex=search_query) | Q(name__iregex=search_query) | Q(
                description__iregex=search_query) | Q(category=search_cat) | Q(obj=search_obj) | Q(id__iregex=search_query))
        elif search_cat:
            cards = Galery.objects.filter(Q(author__iregex=search_query) | Q(name__iregex=search_query) | Q(
                description__iregex=search_query) | Q(id__iregex=search_query) | Q(category=search_cat))
        elif search_obj:
            cards = Galery.objects.filter(Q(author__iregex=search_query) | Q(name__iregex=search_query) | Q(
                description__iregex=search_query) | Q(id__iregex=search_query) | Q(obj=search_obj))
        else:
            cards = Galery.objects.filter(Q(author__iregex=search_query) | Q(name__iregex=search_query) | Q(
                description__iregex=search_query) | Q(id__iregex=search_query))
    elif search_cat and search_obj:
        cards = Galery.objects.filter(Q(category=search_cat) | Q(obj=search_obj))
    elif search_cat:
        cards = Galery.objects.filter(Q(category=search_cat))
    elif search_obj:
        cards = Galery.objects.filter(Q(obj=search_obj))
    else:
        cards = Galery.objects.all()




    objects = Objects.objects.all()
    categories = Category.objects.all()
    error = ''


    if request.method == 'POST' and 'addcard' in request.POST:
        form = GallaryAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        form = GallaryAddForm()

    if request.method == 'POST' and 'addcat' in request.POST:
        add_category_form = AddCategory(request.POST)
        if add_category_form.is_valid():
            add_category_form.save()
            return HttpResponseRedirect('/pictures')
        else:
            return HttpResponseRedirect('/')
    else:
        add_category_form = AddCategory()

    if request.method == 'POST' and 'addobj' in request.POST:
        add_object_form = AddObject(request.POST)
        if add_object_form.is_valid():
            add_object_form.save()
            return HttpResponseRedirect('/pictures')
        else:
            return HttpResponseRedirect('/')
    else:
        add_object_form = AddObject()

    data = {
        'form': form,
        'error': error,
        'objects': objects,
        'categories': categories,
        'data': cards,
        'add_category_form': add_category_form,
        'add_object_form': add_object_form,
    }
    return render(request, 'main/index.html', data)



@login_required(login_url='/login/')
def add_card(request):

    if request.method == 'POST' and 'addcard' in request.POST:
        form = GallaryAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pictures')
        else:
            return HttpResponseRedirect('/')
    else:
        form = GallaryAddForm()

    data = {
        'form': form,

    }
    return render(request, 'main/add_card.html', data)


def edit(request, pk):
    post = get_object_or_404(Galery, pk=pk)
    if request.method == 'POST':
        form = GallaryAddForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        form = GallaryAddForm(instance=post)
    return render(request, 'main/add_card.html', {'form': form})


def view(request, pk):
    obj = Galery.objects.get(id=pk)
    return render(request, 'main/view_card.html', {'obj': obj})
class PictureView(LoginRequiredMixin, DetailView):
    model = Galery
    template_name = 'main/view_card.html'
    context_object_name = 'obj'

class PictureUpdate(LoginRequiredMixin, UpdateView):
    model = Galery
    template_name = 'main/add_card.html'
    form_class = GallaryAddForm

class PictureDelete(LoginRequiredMixin, DeleteView):
    model = Galery
    success_url = '/pictures'
    template_name = 'main/delete.html'



class MyprojectLoginView(LoginView):
    template_name = 'main/login.html'
    form_class = AuthUserForm
    success_url = '/pictures'
    def get_success_url(self):
        return self.success_url

# class AddMovements(CreateView):
#     model = Movements
#     template_name = 'main/add_movements.html'
#     success_url = '/pictures'


# class AddMovement(CreateView):
#     model = Movement
#     success_url = '/pictures'
#     form_class = AddMovement
#
#     template_name = 'main/add_movements.html'


def add_movement(request, pk):
    if request.method == 'POST':
        picture = Galery.objects.get(id=pk)
        form = AddMovement(request.POST)
        if form.is_valid():
            obj = form.save()
            picture.movements.add(obj.id)
            picture.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        form = AddMovement()

    data = {
        'form': form
    }
    return render(request, 'main/add_movements.html', data)