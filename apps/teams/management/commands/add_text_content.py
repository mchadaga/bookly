import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.app.models import TextContent, Hook

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes all existing TextContents and adds a new TextContent with Hooks from a CSV file'

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
                # Get the data row
                data_row = next(csv_reader)

                if len(data_row) < 6:
                    raise ValueError("CSV file must have at least 6 columns: Story, Prompt, Conflict, Hook1, Hook2, Hook3")

                # Create new TextContent
                text_content = TextContent.objects.create(user=user, name="textcontent1")

                # Create Hooks
                for i in range(3, 6):
                    Hook.objects.create(textcontent=text_content, hook_text=data_row[i])

            self.stdout.write(self.style.SUCCESS(f'Successfully created new TextContent "textcontent1" with 3 Hooks for user {user.username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with id {user_id} does not exist'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file "{csv_filename}" not found in the static directory'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
        except StopIteration:
            self.stdout.write(self.style.ERROR("CSV file is empty or has only a header row"))
