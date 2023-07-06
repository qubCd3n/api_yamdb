import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils import timezone
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api_yamdb.settings import BASE_DIR

data_folder = os.path.join(BASE_DIR, 'static/data/')
titles_file = 'titles.csv'
genre_title_file = 'genre_title.csv'
comments_file = 'comments.csv'
reviews_file = 'review.csv'
file_name_dict = {
    'category.csv': Category,
    'genre.csv': Genre,
    'users.csv': User,
}


class Command(BaseCommand):
    """Загрузка данных CSV в БД."""

    help = 'Import data from CSV files'

    def import_norelatedfield_models(self, *args, **options):
        """
        Загрузка моделей без связанных полей.
        При загрузке цифр преобразовывает их в int
        """
        for file_name in file_name_dict:
            file_path = os.path.join(data_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                obj = file_name_dict[file_name]
                obj_count = 0
                for row in csv_reader:
                    for key, value in row.items():
                        if value.isdigit():
                            row[key] = int(value)
                    obj.objects.get_or_create(**row)
                    obj_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"Количество созданных записей {file_name}: {obj_count} "
            ))

    def import_title_csv(self, *args, **options):
        """Загрузка произведений."""
        file_path = os.path.join(data_folder, titles_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            obj_count = 0
            for row in csv_reader:
                row['year'] = int(row['year'])
                category = row.pop('category', None)
                genre_ids = row.pop('genre', None)
                title_instance, _ = Title.objects.get_or_create(**row)
                if category:
                    category = Category.objects.get(id=category)
                    title_instance.category = category
                title_instance.genre.clear()
                if genre_ids:
                    for genre in genre_ids:
                        genre = Genre.objects.get(id=genre)
                        title_instance.genre.add(genre)
                title_instance.save()
                obj_count += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Количество созданных записей titles.csv: {obj_count} "
            ))

    def import_genre_title_csv(self, *args, **options):
        """Загрузка связей Жанр-Произведение."""
        file_path = os.path.join(data_folder, genre_title_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            obj_count = 0
            for row in csv_reader:
                id = row.pop('id')
                genre_id = row.pop('genre_id')
                title_id = row.pop('title_id')
                genre = Genre.objects.get(id=genre_id)
                title = Title.objects.get(id=title_id)
                if genre and title:
                    title_genre_instance, _ = Title.objects.get_or_create(
                        id=id,
                        genre=genre,
                    )
                    obj_count += 1
        self.stdout.write(
            self.style.SUCCESS(
                f'Количество созданных записей genre_title.csv: {obj_count}'
            ))

    def import_review(self, *args, **options):
        """Загрузка отзывов."""
        file_path = os.path.join(data_folder, reviews_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            obj_count = 0
            for row in csv_reader:

                row['score'] = int(row['score'])

                title_id = row.pop('title_id')
                author_id = row.pop('author')
                pub_date_str = row.get('pub_date', '')

                try:
                    pub_date = datetime.strptime(
                        pub_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
                row['pub_date'] = pub_date

                if author_id is None or title_id is None:
                    continue

                try:
                    author = User.objects.get(id=author_id)
                    title = Title.objects.get(id=title_id)
                except User.DoesNotExist or Title.DoesNotExist:
                    continue

                try:
                    review_instance, _ = Review.objects.get_or_create(
                        title=title,
                        author=author,
                        **row
                    )
                    obj_count += 1
                except IntegrityError:
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'Количество вновь созданных записей {reviews_file}: {obj_count}'
        ))

    def import_comments_csv(self, *args, **options):
        """Загрузка комментариев."""
        file_path = os.path.join(data_folder, comments_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            obj_count = 0
            for row in csv_reader:
                review_id = row.pop('review_id')
                author_id = row.pop('author')
                pub_date_str = row.get('pub_date', '')

                try:
                    pub_date = datetime.strptime(
                        pub_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
                row['pub_date'] = pub_date

                if author_id is None or review_id is None:
                    continue

                try:
                    author = User.objects.get(id=author_id)
                    review = Review.objects.get(id=review_id)
                except User.DoesNotExist or Review.DoesNotExist:
                    continue

                try:
                    comment_instance, _ = Comment.objects.get_or_create(
                        review=review,
                        author=author,
                        **row
                    )
                    obj_count += 1
                except IntegrityError:
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'Количество вновь созданных записей {comments_file}: {obj_count}'
        ))

    def handle(self, *args, **options):
        """Главная функция."""
        self.import_norelatedfield_models(self, *args, **options)
        self.import_title_csv(self, *args, **options)
        self.import_genre_title_csv(self, *args, **options)
        self.import_review(self, *args, **options)
        self.import_comments_csv(self, *args, **options)
