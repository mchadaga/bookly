import openai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from .forms import PromptForm, ImagePromptForm


@login_required
def home(request):
    return TemplateResponse(request, 'openai_example/openai_home.html', {
        'active_tab': 'openai',
    })


@login_required
def chat_demo(request):
    openai.api_key = settings.OPENAI_API_KEY
    prompt_response = ''
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            print(openai_response)
            prompt_response = openai_response.choices[0].message.content.strip()
    else:
        form = PromptForm()
    return TemplateResponse(request, 'openai_example/chat_home.html', {
        'active_tab': 'openai',
        'form': form,
        'prompt_response': prompt_response,
    })


@login_required
def image_demo(request):
    openai.api_key = settings.OPENAI_API_KEY
    image_urls = []
    if request.method == 'POST':
        form = ImagePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            openai_response = openai.Image.create(
                prompt=prompt,
                n=6,
                size="256x256"
            )
            # import pdb; pdb.set_trace()
            print(openai_response)
            image_urls = [data['url'] for data in openai_response.data]
    else:
        form = ImagePromptForm()
    return TemplateResponse(request, 'openai_example/image_home.html', {
        'active_tab': 'openai',
        'form': form,
        'image_urls': image_urls,
    })
