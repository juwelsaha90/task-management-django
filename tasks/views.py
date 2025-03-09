from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task


def manager_dashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')

def test(request):
    context = {
        'names': ['Mahmud', 'Ahmed', 'John'],
        'age': [20, 30, 40]
        
        
    }
    return render(request, 'test.html', context)

def create_task(request):
    
    form = TaskModelForm()
    
    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():
            
            """ For django model form """
            form.save()

            return render(request, 'task_form.html', {'form': form, 'message': 'Task created successfully'})
            """ For django form """
           
            
    context = {"form": form}
    return render(request, 'task_form.html', context)

def view_task(request):
    tasks = Task.objects.all()
    
    task_3 = Task.objects.get(id=1)
    return render(request, "show_task.html", {"tasks": tasks, "task3": task_3})

