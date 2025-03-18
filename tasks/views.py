from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Manager').exists()


@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get('type','all')
    
   

    counts = Task.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='PENDING')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        completed=Count('id', filter=Q(status='COMPLETED'))
    )

    base_query = Task.objects.select_related("details").prefetch_related("assigned_to")
    if type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    else:
        tasks = base_query.all()



    context = {
        'tasks': tasks,
        'counts': counts
    }
    return render(request, 'dashboard/manager-dashboard.html', context)

@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')


@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            """ For django model form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request,"Task created successfully")
            return redirect("create-task")
            """ For django form """
           
            
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, 'task_form.html', context)


@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task deleted successfully")
        return redirect("manager-dashboard")
    else:
        messages.success(request,"Something went wrong")
        return redirect("manager-dashboard")

@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)
    
    
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            """ For django model form """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            
            messages.success(request,"Task updated successfully")
            return redirect("update-task", id )
            """ For django form """
           
            
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, 'task_form.html', context)

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def view_task(request):
    
    tasks_count = Project.objects.annotate(num_tasks=Count('task'))
   
    return render(request, "show_task.html", {"tasks_count": tasks_count})

