from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Todo
import json

def todo_list(request):
    """Main view showing all todos with add form"""
    todos = Todo.objects.all()

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Todo.objects.create(content=content)
            messages.success(request, 'Todo added successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Todo content cannot be empty!')

    return render(request, 'django_app/todo_list.html', {'todos': todos})

@require_http_methods(["POST"])
def toggle_todo(request, todo_id):
    """Toggle the done status of a todo"""
    todo = get_object_or_404(Todo, id=todo_id)

    if todo.is_done:
        todo.marked_as_done_at = None
        messages.success(request, 'Todo marked as not done!')
    else:
        todo.marked_as_done_at = timezone.now()
        messages.success(request, 'Todo marked as done!')

    todo.save()
    return redirect('todo_list')

@require_http_methods(["POST"])
def delete_todo(request, todo_id):
    """Delete a todo"""
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return redirect('todo_list')
