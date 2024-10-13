from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Prefetch, Q
from apps.app.models import TextContent, Hook, Paragraph, Sentence, UserTextContent, TextContentSimilarity
from apps.teams.decorators import login_and_team_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
import os
import requests
from django.views.decorators.csrf import csrf_exempt

@login_and_team_required
def get_random_textcontent(request):
    user = request.user
    clicked_textcontents = UserTextContent.objects.filter(user=user).values_list('textcontent_id', flat=True)
    
    recent_textcontent = UserTextContent.objects.filter(user=user).order_by('-id').first()
    
    # Get the 'entered' parameter from the request
    entered = request.GET.get('entered', 'false').lower() == 'true'
    
    selection_method = "random"
    similarity_score = None
    
    if recent_textcontent and entered:
        # User entered the previous story, find the most similar one
        similar_textcontent = TextContentSimilarity.objects.filter(
            Q(text_content_1=recent_textcontent.textcontent) | Q(text_content_2=recent_textcontent.textcontent)
        ).exclude(
            Q(text_content_1__in=clicked_textcontents) & Q(text_content_2__in=clicked_textcontents)
        ).order_by('-similarity_score').first()
        
        if similar_textcontent:
            if similar_textcontent.text_content_1 != recent_textcontent.textcontent:
                textcontent = similar_textcontent.text_content_1
            else:
                textcontent = similar_textcontent.text_content_2
            selection_method = "similarity"
            similarity_score = similar_textcontent.similarity_score
        else:
            textcontent = TextContent.objects.exclude(id__in=clicked_textcontents).order_by('?').first()
    else:
        # User skipped the previous story or there's no recent story, select a random one
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
            ],
            'selection_method': selection_method,
            'similarity_score': similarity_score,
            'recent_textcontent_id': recent_textcontent.textcontent.id if recent_textcontent else None
        }
        print(f"Returning TextContent: ID {textcontent.id}, Name: {textcontent.name}")
        print(f"Selection method: {selection_method}")
        return JsonResponse(data)
    else:
        print("No new TextContent found")
        return JsonResponse({'error': 'No new TextContent found'}, status=404)

# Add this at the end of your views.py file
from django.db import connection
from django.db import reset_queries

def print_query_count():
    print(f"Number of queries: {len(connection.queries)}")
    reset_queries()

# Call this function at the end of get_random_textcontent
print_query_count()

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

# def mask(user, similarity):
#     binary_array = np.array(user)
#     data_array = np.array(similarity)
#     selected_elements = data_array[binary_array == 1]
#     return selected_elements


# def recommend_story(story_id, cosine_sim, df):
#     idx = df[df['Filename'] == story_id].index[0]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores_unseen = mask(user_unseen, sim_scores)
#     sim_scores_unseen = sorted(sim_scores_unseen, key=lambda x: x[1], reverse=True)
#     top_similar_story = [df['Filename'][sim_scores_unseen[1][0]]]
#     return top_similar_story

# def next_story(click, story_id, cosine_sim, df):
#     if(click):
#         return recommend_story(story_id, cosine_sim, df)
#     else:
#         return random.choice(mask{user_unseen, df['Filename'].to_list()})

@csrf_exempt
@require_POST
def ask_ai_about_story(request):
    textcontent_id = request.POST.get('textcontent_id')
    current_sentence_index = int(request.POST.get('current_sentence_index', 0))
    user_question = request.POST.get('user_question')

    if not all([textcontent_id, user_question]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    try:
        textcontent = TextContent.objects.get(id=textcontent_id)
        sentences = Sentence.objects.filter(paragraph__textcontent=textcontent)[:current_sentence_index + 1]
        story_context = " ".join([sentence.sentence_text for sentence in sentences])

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": 'Write all your responses in 1-2 sentences, in the simplest language possible.'
                },
                {
                    "role": "user",
                    "content": f"Context: {story_context}\n\nQuestion: {user_question}"
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
        }

        url = 'https://api.openai.com/v1/chat/completions'

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()

        if response.status_code == 200:
            ai_response = response_json['choices'][0]['message']['content'].strip()
            return JsonResponse({'ai_response': ai_response})
        else:
            return JsonResponse({'error': 'Failed to get response from AI'}, status=500)

    except TextContent.DoesNotExist:
        return JsonResponse({'error': 'TextContent not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
