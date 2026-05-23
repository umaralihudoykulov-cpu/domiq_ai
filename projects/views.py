"""Projects - Views"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm


@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/list.html', {'projects': projects, 'page_title': 'Loyihalarim'})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f"'{project.title}' loyihasi yaratildi! 🏗️")
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form, 'page_title': 'Yangi Loyiha'})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    designs = project.designs.all().order_by('-created_at')[:6]
    estimates = project.estimates.all()
    electrical_plans = project.electrical_plans.all()
    
    context = {
        'project': project,
        'designs': designs,
        'estimates': estimates,
        'electrical_plans': electrical_plans,
        'page_title': f'{project.title} — DomIQ',
    }
    return render(request, 'projects/detail.html', context)


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Loyiha yangilandi!")
            return redirect('projects:detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit.html', {'form': form, 'project': project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Loyiha o'chirildi.")
        return redirect('projects:list')
    return render(request, 'projects/confirm_delete.html', {'project': project})
