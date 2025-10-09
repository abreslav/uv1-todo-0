from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo
import json

def todo_list(request):
    """Main view showing todos with add form - requires authentication"""
    if not request.user.is_authenticated:
        return render(request, 'django_app/login.html')

    todos = Todo.objects.filter(user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Todo.objects.create(content=content, user=request.user)
            messages.success(request, 'Todo added successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Todo content cannot be empty!')

    return render(request, 'django_app/todo_list.html', {'todos': todos})

@require_http_methods(["POST"])
@login_required
def toggle_todo(request, todo_id):
    """Toggle the done status of a todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    if todo.is_done:
        todo.marked_as_done_at = None
        messages.success(request, 'Todo marked as not done!')
    else:
        todo.marked_as_done_at = timezone.now()
        messages.success(request, 'Todo marked as done!')

    todo.save()
    return redirect('todo_list')

@require_http_methods(["POST"])
@login_required
def delete_todo(request, todo_id):
    """Delete a todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return redirect('todo_list')

@require_http_methods(["POST"])
@login_required
def edit_todo(request, todo_id):
    """Edit a todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    content = request.POST.get('content', '').strip()
    if content:
        todo.content = content
        todo.save()
        messages.success(request, 'Todo updated successfully!')
    else:
        messages.error(request, 'Todo content cannot be empty!')

    return redirect('todo_list')
