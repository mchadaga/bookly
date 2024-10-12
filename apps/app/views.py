from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Prefetch
from apps.app.models import TextContent, Hook, Paragraph, Sentence, UserTextContent
from apps.teams.decorators import login_and_team_required
from django.views.decorators.http import require_POST

@login_and_team_required
def get_random_textcontent(request):
    user = request.user
    clicked_textcontents = UserTextContent.objects.filter(user=user).values_list('textcontent_id', flat=True)
    textcontent = TextContent.objects.exclude(id__in=clicked_textcontents).order_by('?').first()
    
    if textcontent:
        hook = Hook.objects.filter(textcontent=textcontent).first()
        paragraphs = Paragraph.objects.filter(textcontent=textcontent).prefetch_related(
            Prefetch('sentences', queryset=Sentence.objects.all())
        )
        data = {
            'id': textcontent.id,
            'hook': hook.hook_text if hook else '',
            'paragraphs': [
                {
                    'sentences': [
                        {'sentence_text': sentence.sentence_text}
                        for sentence in paragraph.sentences.all()
                    ]
                }
                for paragraph in paragraphs
            ]
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'No new TextContent found'}, status=404)

@login_and_team_required
@require_POST
def track_textcontent_click(request):
    textcontent_id = request.POST.get('textcontent_id')
    if textcontent_id:
        UserTextContent.objects.get_or_create(
            user=request.user,
            textcontent_id=textcontent_id
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid textcontent_id'}, status=400)

@login_and_team_required
def get_user_textcontents(request):
    user_textcontents = UserTextContent.objects.filter(user=request.user).select_related('textcontent')
    data = [{'id': utc.textcontent.id, 'name': utc.textcontent.name} for utc in user_textcontents]
    return JsonResponse(data, safe=False)
