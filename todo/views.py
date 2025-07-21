from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task

# Create your views here.

def index(request):
    if request.method == 'POST':
        task = Task(title = request.POST['title'], due_at = make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    priority = request.GET.get('priority')
    if priority in ['low', 'medium', 'high']:
        tasks = Task.objects.filter(priority=priority)
    elif request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')
    
    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks':tasks,
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

  
def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id) 
    except Task.DoesNotExist:
        raise Http404("Task does not exist") 
    task.delete()
    return redirect(index)

  
def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect('index')

    context = {
        'task': task,
    }
    return render(request, 'todo/edit.html', context)

def priority(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        priority_value = request.POST.get('priority')
        if priority_value is not None:
            task.priority = priority_value
            task.save()
            return redirect('index')

    context = {
        'task': task,
    }
    return render(request, 'todo/priority.html', context)
  