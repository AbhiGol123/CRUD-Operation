from django.shortcuts import render, redirect, get_object_or_404

import json
from .models import Item, Question, Option
from .forms import ItemForm

def save_questions(item, questions_json, db_alias='default'):
    if not questions_json:
        return
    
    try:
        data = json.loads(questions_json)
        # Clear existing questions (simple approach for now)
        Question.objects.using(db_alias).filter(item=item).delete()

        for q_data in data:
            if not q_data.get('text'):
                continue
            question = Question.objects.using(db_alias).create(item=item, text=q_data['text'])
            for opt_text in q_data.get('options', []):
                if opt_text:
                    Option.objects.using(db_alias).create(question=question, text=opt_text)
    except json.JSONDecodeError:
        pass

def item_list(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'items/item_list.html', {'items': items})

def item_list1(request):
    items = Item.objects.using('postgresql').all().order_by('-created_at')
    return render(request, 'items/item_list.html', {'items': items})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            if 'draft' in request.POST:
                item.status = 'draft'
            else:
                item.status = 'published'
            item.save()
            save_questions(item, request.POST.get('questions_json'))
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'title': 'Create Item', 'questions_data': '[]'})

def item_create1(request):
    print(request.POST)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            if 'draft' in request.POST:
                item.status = 'draft1'
            else:
                item.status = 'published'
            item.save(using='postgresql')
            save_questions(item, request.POST.get('questions_json'), 'postgresql')
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'title': 'Create Item', 'questions_data': '[]'})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if 'draft' in request.POST:
                item.status = 'draft'
            else:
                item.status = 'published'
            item.save()
            save_questions(item, request.POST.get('questions_json'))
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    
    # Serialize questions for frontend
    questions = item.questions.all()
    questions_data = []
    for q in questions:
        questions_data.append({
            'text': q.text,
            'options': [opt.text for opt in q.options.all()]
        })
    
    return render(request, 'items/item_form.html', {
        'form': form, 
        'title': 'Update Item',
        'questions_data': json.dumps(questions_data)
    })

def item_update1(request, pk):
    item = get_object_or_404(Item.objects.using('postgresql'), pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if 'draft' in request.POST:
                item.status = 'draft'
            else:
                item.status = 'published'
            item.save(using='postgresql')
            save_questions(item, request.POST.get('questions_json'), 'postgresql')
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)

    # Serialize questions from second DB
    questions = item.questions.all().using('postgresql') # Since item is from postgresql, simple access might imply default db if not careful
    # Safest to query explicitly
    questions = Question.objects.using('postgresql').filter(item=item)
    questions_data = []
    for q in questions:
        # Fetch options for this question
        options = Option.objects.using('postgresql').filter(question=q)
        questions_data.append({
            'text': q.text,
            'options': [opt.text for opt in options]
        })

    return render(request, 'items/item_form.html', {
        'form': form, 
        'title': 'Update Item',
        'questions_data': json.dumps(questions_data)
    })

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})

def item_delete1(request, pk):
    item = get_object_or_404(Item.objects.using('postgresql'), pk=pk)
    if request.method == 'POST':
        item.delete(using='postgresql')
        return redirect('item_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})
