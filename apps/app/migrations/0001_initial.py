# Generated by Django 4.1.7 on 2024-10-12 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0003_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('linked_class', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to='teams.team')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_assignments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enrichment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrichment_type', models.CharField(choices=[('translation', 'Translation'), ('pronunciation', 'Pronunciation'), ('explanation', 'Explanation'), ('note', 'Note'), ('question', 'Question')], default='explanation', max_length=20)),
                ('initial_content', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('current_mode', models.CharField(default='quiz_me', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragraph_text', models.CharField(max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300, null=True)),
                ('answer', models.CharField(max_length=3000, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('remember', 'Remember'), ('understand', 'Understand'), ('apply', 'Apply'), ('analyze', 'Analyze'), ('evaluate', 'Evaluate'), ('create', 'Create')], default='remember', max_length=20)),
                ('opinion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_text', models.CharField(max_length=10000, null=True)),
                ('paragraph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sentences', to='app.paragraph')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('completed', models.IntegerField(default=0)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThoughtExperiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('explanation', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference_sentence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.sentence')),
                ('textcontent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.textcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_text', models.CharField(max_length=10000, null=True)),
                ('paragraph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supports', to='app.paragraph')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('completed_questions_count', models.IntegerField(default=0)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_assignments', to='app.assignment')),
                ('current_sentence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_for_assignments', to='app.sentence')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to=settings.AUTH_USER_MODEL)),
                ('textcontent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_assignments', to='app.textcontent')),
            ],
            options={
                'unique_together': {('student', 'assignment')},
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('explanation', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference_sentence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.sentence')),
                ('textcontent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.textcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, null=True)),
                ('from_bot', models.BooleanField(default=False)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_messages', to='app.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='reference_sentence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='app.sentence'),
        ),
        migrations.AddField(
            model_name='question',
            name='textcontent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='app.textcontent'),
        ),
        migrations.CreateModel(
            name='ParagraphImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
                ('caption', models.TextField(blank=True)),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.paragraph')),
            ],
        ),
        migrations.AddField(
            model_name='paragraph',
            name='textcontent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.textcontent'),
        ),
        migrations.AddField(
            model_name='paragraph',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='LearnMore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('explanation', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference_sentence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.sentence')),
                ('textcontent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.textcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnrichmentMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('enrichment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modes', to='app.enrichment')),
            ],
            options={
                'unique_together': {('enrichment', 'name')},
            },
        ),
        migrations.CreateModel(
            name='EnrichmentMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('llm_response', models.TextField(blank=True, null=True)),
                ('complete_flag', models.BooleanField(default=False)),
                ('is_user_message', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hidden', models.BooleanField(default=False, null=True)),
                ('enrichment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app.enrichment')),
                ('mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app.enrichmentmode')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='enrichment',
            name='sentence',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='enrichments', to='app.sentence'),
        ),
        migrations.AddField(
            model_name='enrichment',
            name='student_assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrichments', to='app.studentassignment'),
        ),
        migrations.AddField(
            model_name='enrichment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('explanation', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference_sentence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)ss', to='app.sentence')),
                ('textcontent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='app.textcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='textcontent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='app.textcontent'),
        ),
    ]
