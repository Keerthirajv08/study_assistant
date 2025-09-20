from django.core.management.base import BaseCommand
from base.models import StudyTopic

class Command(BaseCommand):
    help = 'Set up initial study topics and sample data'

    def handle(self, *args, **options):
        #Create initial study topics
        topics_data = [
            {
                'name': 'Mathematics',
                'description': 'Algebra, Geometry, Calculus, Statistics, Trigonometry, and more mathematical concepts.',
                'icon': '🧮'
            },
            {
                'name': 'Science', 
                'description': 'Biology, Chemistry, Physics, Astronomy, and more scientific concepts.',
                'icon': '🔬'
            },
            {
                'name': 'History', 
                'description': 'Ancient History, Modern History, World History, and more historical events and figures.',
                'icon': '📜'
            },
            {
                'name': 'English', 
                'description': 'Grammar, Vocabulary, Literature, and more language learning resources.',
                'icon': '📖'
            },
            {
                'name': 'Computer Science', 
                'description': 'Programming, Data Structures, Algorithms, and more computer science concepts.',
                'icon': '🖥️'
            },
            {
                'name': 'Languages', 
                'description': 'Spanish, French, German, Italian, and more language learning resources.',
                'icon': '🌐'
            },
            {
                'name': 'Arts', 
                'description': 'Painting, Drawing, Sculpture, Photography, and more creative arts.',
                'icon': '🎨'
            },
            {
                'name': 'Study Skills', 
                'description': 'Time management, organization, study strategies, and more study tips.',
                'icon': '📚'
            }
        ]

        created_count = 0

        for topic_data in topics_data: 
            topic, created = StudyTopic.objects.get_or_create(
                name=topic_data['name'],
                defaults={
                    'description': topic_data['description'],
                    'icon': topic_data['icon'],
                    'is_active': True
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created topic: {topic.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Topic already exists: {topic.name}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set up initial data. Created {created_count} new topics."
            )
        )

