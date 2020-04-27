import datetime
from django.db import models
from django.db.models import Q
from sorl.thumbnail import ImageField, get_thumbnail
from notes.field import RatingField


class Tag(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True) 

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['title']
# An inner class change singular or plural versions of the tag name

    def get_absolute_url(self):
        return '/tags/%s/' % self.slug
# A slug is a short label for tag in URL

    def __str__(self):
        return self.title


def note_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<>/<filename>
    return '{0}/{1}'.format(instance.note.id, filename)


class Note(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=30)
    desc = models.CharField(default='', max_length=1000)
# Create attribute fields to save note ID, name, owner, description
    upload_time = models.DateTimeField(
        'upload_time',
        null=True,
        default=datetime.datetime.now)
# Save date and time when publish the note
    tags = models.ManyToManyField(Tag, related_name='notes')
# Create many-to-many relationship  subject tag to note
# A note can have more than one tag
    mean_score = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
# Create to save score and comments from reader

    def __str__(self):
        return self.name

    def get_thumb(self):
        try:
            i = Image.objects.filter(note=self)[0].get_thumb()
            return i
            # remember that sorl objects have url/width/height attributes
        except:
            return '/media/loading.jpg'
# Get the thumbnail from first note image


class Image(models.Model):
    index = models.IntegerField()
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='images')
    image = ImageField(upload_to=note_directory_path)
# Create relation note images to note with ForeignKey
# ForeignKey is a many-to-one relation
    def get_thumb(self):
        im = get_thumbnail(self.image, '500x500', crop='center', quality=99)
        return im.url
        # remember that sorl objects have url/width/height attributes
# Make a thumbnail for note


class Review(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='reviews')
    author = models.CharField(max_length=30)
    datetime = models.DateTimeField(
        'reviewed_time',
        null=True,
        default=datetime.datetime.now)
    score = models.FloatField(default=0)
    text = models.TextField(max_length=1000)

    def save(self, *args, **kwargs):
        if self.score != 0:
            self.note.mean_score = (
                self.note.mean_score*self.note.review_count
                + self.score) / (self.note.review_count + 1)
            self.note.review_count += 1
            self.note.save()
        super(Review, self).save(*args, **kwargs)