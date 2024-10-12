from django import forms


class PromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={"rows":"3"}),
        help_text="E.g. 'Can you write me a poem about the Django web framework in the style of a pirate?'"
    )


class ImagePromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={"rows":"3"}),
        help_text="E.g. 'A pegasus in space in the style of tron'"
    )
