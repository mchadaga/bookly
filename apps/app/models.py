# Create your models here.
from django.db import models
from zenlearner.settings import AUTH_USER_MODEL
from django.core.validators import MaxLengthValidator
from apps.teams.models import Team
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.

class Hook(models.Model):
    hook_text = models.CharField(max_length=10000, null=True)
    textcontent = models.ForeignKey('TextContent', on_delete=models.CASCADE, related_name='hooks')

class TextContent(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, null=True)
    completed = models.IntegerField(default=0)
    # enrichments = GenericRelation(Enrichment)

class Assignment(models.Model):
    teacher = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_assignments')
    textcontent = models.ForeignKey(TextContent, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    linked_class = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL,  # Change CASCADE to SET_NULL
        related_name='assignments',
        null=True,  # Allow null values
        blank=True,  # Allow blank in forms
        default=None  # Set default to None
    )

    def __str__(self):
        return f"{self.name} - {self.textcontent.name} - {self.team.name}"

class Paragraph(models.Model):
    textcontent = models.ForeignKey(TextContent, on_delete = models.CASCADE, null=True)
    paragraph_text = models.CharField(max_length=10000, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null=True) 
    # enrichments = GenericRelation(Enrichment)

class Sentence(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete = models.CASCADE, null=True, related_name='sentences')
    sentence_text = models.CharField(max_length=10000, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)    
    # enrichments = GenericRelation(Enrichment)

class StudentAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='student_assignments')
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')
    textcontent = models.ForeignKey(TextContent, on_delete=models.CASCADE, related_name='student_assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # New fields for tracking progress
    current_sentence = models.ForeignKey(Sentence, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_for_assignments')
    completed_questions_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['student', 'assignment']

    def __str__(self):
        return f"{self.student.username} - {self.assignment.name}"

    def update_progress(self, sentence):
        self.current_sentence = sentence
        self.save()

    def increment_completed_questions(self):
        self.completed_questions_count += 1
        self.save()

class Support(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete = models.CASCADE, null=True, related_name='supports')
    support_text = models.CharField(max_length=10000, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)    
    
class ParagraphImage(models.Model):
    paragraph = models.ForeignKey(
        'Paragraph', 
        on_delete=models.CASCADE, 
        related_name='images'  # This allows you to access images using paragraph.images
    )
    image_url = models.URLField(max_length=2000)  # Storing the URL of the image
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Image for Paragraph ID {self.paragraph.id}"
    
class EnrichmentTemplate(models.Model):
    textcontent = models.ForeignKey(TextContent, on_delete=models.CASCADE, related_name="%(class)ss")
    content = models.CharField(max_length=1000)
    explanation = models.TextField()
    reference_sentence = models.ForeignKey(Sentence, on_delete=models.SET_NULL, null=True, related_name="%(class)ss")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Quiz(EnrichmentTemplate):
    def __str__(self):
        return f"Quiz: {self.content[:50]}..."

class Debate(EnrichmentTemplate):
    def __str__(self):
        return f"Debate: {self.content[:50]}..."

class ThoughtExperiment(EnrichmentTemplate):
    def __str__(self):
        return f"Thought Experiment: {self.content[:50]}..."

class LearnMore(EnrichmentTemplate):
    def __str__(self):
        return f"Learn More: {self.content[:50]}..."
    
class Question(models.Model):
    CATEGORY_CHOICES = [
        ('remember', 'Remember'),
        ('understand', 'Understand'),
        ('apply', 'Apply'),
        ('analyze', 'Analyze'),
        ('evaluate', 'Evaluate'),
        ('create', 'Create'),
    ]
    textcontent = models.ForeignKey(TextContent, on_delete=models.CASCADE, null=True, related_name="questions")
    question = models.CharField(max_length=300, null=True) 
    answer = models.CharField(max_length=3000, null=True) 
    completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='remember')
    opinion = models.BooleanField(default=False)
    reference_sentence = models.ForeignKey(Sentence, on_delete=models.SET_NULL, null=True, related_name="questions")

class QuestionMessage(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE, null=True, related_name="question_messages")
    text = models.CharField(max_length=300, null=True) 
    from_bot = models.BooleanField(default=False)

class Enrichment(models.Model):
    ENRICHMENT_TYPES = [
        ('translation', 'Translation'),
        ('pronunciation', 'Pronunciation'),
        ('explanation', 'Explanation'),
        ('note', 'Note'),
        ('question', 'Question'),
        # Add other types as needed
    ]
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name='enrichments', default=None)
    student_assignment = models.ForeignKey(StudentAssignment, on_delete=models.CASCADE, related_name='enrichments', null=True, blank=True)
    enrichment_type = models.CharField(max_length=20, choices=ENRICHMENT_TYPES, default='explanation')
    initial_content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    archived = models.BooleanField(default=False)
    current_mode = models.CharField(max_length=50, default='quiz_me')

class EnrichmentMode(models.Model):
    enrichment = models.ForeignKey(Enrichment, on_delete=models.CASCADE, related_name='modes')
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ['enrichment', 'name']

    def __str__(self):
        return f"{self.enrichment.id} - {self.name}"

class EnrichmentMessage(models.Model):
    enrichment = models.ForeignKey(Enrichment, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    llm_response = models.TextField(blank=True, null=True)
    complete_flag = models.BooleanField(default=False)
    is_user_message = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(null=True, default=False)
    mode = models.ForeignKey(EnrichmentMode, on_delete=models.CASCADE, related_name='messages', null=True)

    class Meta:
        ordering = ['created_at']