import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.app.models import TextContent, Hook, Paragraph, Sentence
from nltk.tokenize import sent_tokenize

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes existing TextContents and adds new TextContents with Stories, Paragraphs, Sentences, and Hooks from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='The ID of the user')
        parser.add_argument('csv_filename', type=str, help='The name of the CSV file in the static directory')

    def handle(self, *args, **options):
        user_id = options['user_id']
        csv_filename = options['csv_filename']

        try:
            user = User.objects.get(id=user_id)
            
            # Delete all existing TextContents for the user
            deleted_count, _ = TextContent.objects.filter(user=user).delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing TextContent(s) for user {user.username}'))

            # Read CSV file
            csv_path = os.path.join(settings.STATIC_ROOT, csv_filename)
            with open(csv_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Skip the header row
                next(csv_reader)
                
                total_hooks_created = 0
                total_paragraphs_created = 0
                total_sentences_created = 0
                text_content_count = 0

                for row in csv_reader:
                    if len(row) < 6:
                        raise ValueError("Each row in the CSV file must have at least 6 columns: Story, Prompt, Conflict, Hook1, Hook2, Hook3")

                    # Create new TextContent
                    text_content = TextContent.objects.create(user=user, name=f"textcontent{text_content_count + 1}")
                    text_content_count += 1

                    # Process the story
                    story_text = row[1]  # Second element contains the story
                    paragraphs = story_text.split('\n')
                    for paragraph_text in paragraphs:
                        if paragraph_text.strip():
                            # Create paragraph
                            paragraph = Paragraph.objects.create(
                                textcontent=text_content,
                                paragraph_text=paragraph_text.strip(),
                                user=user
                            )
                            total_paragraphs_created += 1

                            # Create sentences
                            sentences = sent_tokenize(paragraph_text)
                            for sentence_text in sentences:
                                if sentence_text.strip():
                                    Sentence.objects.create(
                                        paragraph=paragraph,
                                        sentence_text=sentence_text.strip(),
                                        user=user
                                    )
                                    total_sentences_created += 1

                    # Create Hooks
                    hooks_created = 0
                    for i in range(4, 7):
                        if row[i]:  # Only create hook if there's content
                            Hook.objects.create(textcontent=text_content, hook_text=row[i])
                            hooks_created += 1
                    
                    total_hooks_created += hooks_created

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {text_content_count} new TextContent(s) with:'
                f'\n- {total_paragraphs_created} Paragraphs'
                f'\n- {total_sentences_created} Sentences'
                f'\n- {total_hooks_created} Hooks'
                f'\nfor user {user.username}'
            ))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with id {user_id} does not exist'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file "{csv_filename}" not found in the static directory'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV file: {str(e)}"))
