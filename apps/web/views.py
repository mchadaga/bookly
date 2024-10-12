from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.app.models import TextContent, Hook, Paragraph, Sentence

from apps.teams.decorators import login_and_team_required


def home(request):
    if request.user.is_authenticated:
        team = request.team
        if team:
            return HttpResponseRedirect(reverse('web_team:home', args=[team.slug]))
        else:
            messages.info(request, _(
                'Teams are enabled but you have no teams. '
                'Create a team below to access the rest of the dashboard.'
            ))
            return HttpResponseRedirect(reverse('teams:manage_teams'))
    else:
        return render(request, 'web/landing_page.html')


@login_and_team_required
def team_home(request, team_slug):
    assert request.team.slug == team_slug
    
    hooks = Hook.objects.filter(textcontent__user=request.user).select_related('textcontent')
    
    hook_data = []
    for hook in hooks:
        paragraphs = Paragraph.objects.filter(textcontent=hook.textcontent)
        paragraph_data = []
        for paragraph in paragraphs:
            sentences = Sentence.objects.filter(paragraph=paragraph)
            paragraph_data.append({
                'paragraph': paragraph,
                'sentences': sentences
            })
        
        hook_data.append({
            'hook': hook,
            'paragraphs': paragraph_data
        })
    
    return render(request, 'web/fyp.html', context={'hook_data': hook_data})


def simulate_error(request):
    raise Exception('This is a simulated error.')
