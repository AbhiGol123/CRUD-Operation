from django.shortcuts import render, redirect, get_object_or_404
import json
from .models import Questionnaire, QuestionnaireQuestion, QuestionnaireOption
from .forms import QuestionnaireForm

def save_questionnaire_questions(questionnaire, questions_json):
    if not questions_json:
        return
    
    try:
        data = json.loads(questions_json)
        # Clear existing
        questionnaire.questions.all().delete()

        for q_data in data:
            if not q_data.get('text'):
                continue
            question = QuestionnaireQuestion.objects.create(
                questionnaire=questionnaire, 
                text=q_data.get('text'),
                emoji=q_data.get('emoji', '❓')
            )
            for opt_data in q_data.get('options', []):
                if isinstance(opt_data, dict):
                    if opt_data.get('text'):
                        QuestionnaireOption.objects.create(
                            question=question, 
                            text=opt_data['text'], 
                            emoji=opt_data.get('emoji', '😊')
                        )
    except json.JSONDecodeError:
        pass

def questionnaire_create(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, request.FILES)

        if form.is_valid():
            questionnaire = form.save(commit=False)
            
            # Use 'active' as published and logic for drafts if buttons used
            if 'save_draft' in request.POST:
                questionnaire.status = 'inactive'
            else:
                questionnaire.status = 'active'
                
            questionnaire.save()

            save_questionnaire_questions(questionnaire, request.POST.get('questions_json'))
            
            return redirect('questionnaire_list') 
    else:
        form = QuestionnaireForm()
    
    return render(request, 'questionnaire/questionnaire_form.html', {
        'form': form,
        'questions_data': '[]'
    })

def questionnaire_list(request):
    queryset = Questionnaire.objects.all().order_by('-created_at')
    
    # Search
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(title__icontains=search)
    
    # Status
    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)
        
    # Date filters
    date_from = request.GET.get('date_from')
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
        
    date_to = request.GET.get('date_to')
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'oldest':
        queryset = queryset.order_by('created_at')
    elif sort == 'newest':
        queryset = queryset.order_by('-created_at')

    return render(request, 'questionnaire/questionnaire_list.html', {'questionnaires': queryset})

def questionnaire_update(request, pk):
    questionnaire = get_object_or_404(Questionnaire, pk=pk)
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, request.FILES, instance=questionnaire)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            if 'save_draft' in request.POST:
                questionnaire.status = 'inactive'
            else:
                questionnaire.status = 'active'
            questionnaire.save()
            save_questionnaire_questions(questionnaire, request.POST.get('questions_json'))
            
            return redirect('questionnaire_list')
    else:
        form = QuestionnaireForm(instance=questionnaire)
    
    # Serialize questions for frontend
    questions = questionnaire.questions.all()
    questions_data = []
    for q in questions:
        questions_data.append({
            'text': q.text,
            'emoji': q.emoji,
            'options': [
                {'text': opt.text, 'emoji': opt.emoji} 
                for opt in q.options.all()
            ]
        })
    
    return render(request, 'questionnaire/questionnaire_form.html', {
        'form': form,
        'questions_data': json.dumps(questions_data)
    })

def questionnaire_delete(request, pk):
    questionnaire = get_object_or_404(Questionnaire, pk=pk)
    if request.method == 'POST':
        questionnaire.delete()
        return redirect('questionnaire_list')
    return render(request, 'questionnaire/questionnaire_confirm_delete.html', {'questionnaire': questionnaire})
