from django.shortcuts import render, redirect, get_object_or_404

from .forms import TodoForm
from .models import Todo

from django_slack import slack_message

# Create your views here.

def index(request):
    return render(request, "blog/index.html", {})

def todo_list(request):
    todo_list = Todo.objects.all()
    return render(request, "blog/list.html", {"todo_list": todo_list})

def todo_add(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            slack_message('blog/message.slack', {"message": todo.content}) 
            todo.save()
            return redirect('list')
    else:
        form = TodoForm()
    return render(request, "blog/forms.html", {"form": form})

def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'blog/forms.html', {"form": form})


def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('list')

