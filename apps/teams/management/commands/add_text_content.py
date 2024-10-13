import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.app.models import TextContent, Hook, Paragraph, Sentence, UserTextContent, Question, TextContentSimilarity
from nltk.tokenize import sent_tokenize

class Command(BaseCommand):
    help = 'Deletes existing TextContents, associated UserTextContents, and adds new TextContents with Stories, Paragraphs, Sentences, Hooks, Questions, and TextContentSimilarities from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='The name of the CSV file in the static directory')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']

        try:
            # Delete existing data (same as before)
            user_text_content_deleted, _ = UserTextContent.objects.filter(textcontent__isnull=False).delete()
            self.stdout.write(self.style.WARNING(f'Deleted {user_text_content_deleted} existing UserTextContent(s)'))

            deleted_count, _ = TextContent.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing TextContent(s)'))

            text_contents = []
            similarity_data = []  # Store similarity data temporarily

            # Read CSV file
            csv_path = os.path.join(settings.STATIC_ROOT, csv_filename)
            with open(csv_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                total_hooks_created = 0
                total_paragraphs_created = 0
                total_sentences_created = 0
                total_questions_created = 0
                total_similarities_created = 0
                text_content_count = 0

                for row in csv_reader:
                    # Create new TextContent
                    text_content = TextContent.objects.create(user=None, name=row['Filename'])
                    text_contents.append(text_content)
                    text_content_count += 1

                    # Process the story (same as before)
                    story_text = row['Story']
                    paragraphs = story_text.split('\n')
                    for paragraph_text in paragraphs:
                        if paragraph_text.strip():
                            paragraph = Paragraph.objects.create(
                                textcontent=text_content,
                                paragraph_text=paragraph_text.strip(),
                                user=None
                            )
                            total_paragraphs_created += 1

                            sentences = sent_tokenize(paragraph_text)
                            for sentence_text in sentences:
                                if sentence_text.strip():
                                    Sentence.objects.create(
                                        paragraph=paragraph,
                                        sentence_text=sentence_text.strip(),
                                        user=None
                                    )
                                    total_sentences_created += 1

                    # Create Hooks
                    for i in range(1, 4):
                        hook_text = row[f'Hook{i}']
                        if hook_text:
                            Hook.objects.create(textcontent=text_content, hook_text=hook_text, hook_audio=row[f'HookAudio{i}'], voice=row[f'Voice{i}'], hook_timestamps=row[f'HookTimestamps{i}'])
                            total_hooks_created += 1

                    # Create Questions
                    question_types = ['Recall', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create']
                    for q_type in question_types:
                        csv_key = 'ImagineQuestion' if q_type == 'Create' else f'{q_type}Question'
                        csv_answer_key = 'ImagineAnswerKey' if q_type == 'Create' else f'{q_type}AnswerKey'
                        
                        question_text = row[csv_key]
                        answer_text = row[csv_answer_key]
                        if question_text and answer_text:
                            Question.objects.create(
                                textcontent=text_content,
                                question=question_text,
                                answer=answer_text,
                                category=q_type.lower()
                            )
                            total_questions_created += 1

                    # Store similarity data for later processing
                    current_similarities = {}
                    for key, value in row.items():
                        if key.isdigit():
                            current_similarities[int(key)] = value
                    similarity_data.append(current_similarities)

            # Now create TextContentSimilarity objects after all TextContents are created
            for i, similarities in enumerate(similarity_data):
                for j, score in similarities.items():
                    if j < i:  # Ensure we're only creating similarities with previous TextContents
                        try:
                            similarity_score = float(score)
                            print(f"Creating similarity for {i}, {j} with score {similarity_score}")
                            TextContentSimilarity.objects.create(
                                text_content_1=text_contents[i],
                                text_content_2=text_contents[j],
                                similarity_score=similarity_score
                            )
                            total_similarities_created += 1
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Invalid similarity score for pair {i}, {j}"))

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {text_content_count} new TextContent(s) with:'
                f'\n- {total_paragraphs_created} Paragraphs'
                f'\n- {total_sentences_created} Sentences'
                f'\n- {total_hooks_created} Hooks'
                f'\n- {total_questions_created} Questions'
                f'\n- {total_similarities_created} TextContentSimilarities'
            ))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file "{csv_filename}" not found in the static directory'))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV file: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))
