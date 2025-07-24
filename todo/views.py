from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task, Tag
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    if request.method == 'POST':
        due_input = request.POST.get('due_at')
        parsed_due = parse_datetime(due_input) if due_input else None
        due_at = make_aware(parsed_due) if parsed_due else None

        task = Task(
            title=request.POST['title'],
            due_at=due_at,
            priority=request.POST.get('priority', 'medium')
        )
        task.save()

        tag_input = request.POST.get('tags', '')
        tag_names = [t.strip() for t in tag_input.split(',') if t.strip()]
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            task.tags.add(tag)

    priority = request.GET.get('priority')
    order = request.GET.get('order')

    if priority in ['low', 'medium', 'high']:
        tasks = Task.objects.filter(priority=priority)
    else:
        tasks = Task.objects.all()

    if order == 'due':
        tasks = tasks.order_by('due_at')
    elif order == 'post':
        tasks = tasks.order_by('-posted_at')
    else:
        tasks = tasks.order_by('order')

    context = {
        'tasks': tasks,
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

        task.tags.clear()
        tag_input = request.POST.get('tags', '')
        tag_names = [t.strip() for t in tag_input.split(',') if t.strip()]
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            task.tags.add(tag)

        return redirect('index')

    context = {
        'task': task,
    }
    return render(request, 'todo/edit.html', context)

@csrf_exempt
def reorder_tasks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_ids = data.get("task_ids", [])
            for idx, task_id in enumerate(task_ids):
                Task.objects.filter(id=task_id).update(order=idx)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=400)
