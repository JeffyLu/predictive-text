from django.db import models


class Words(models.Model):

    value = models.CharField(
        max_length = 26,
    )

    counts = models.IntegerField(
        default = 0,
    )

    class Meta:

        db_table = 'words'

    def __str__(self):
        return '%s:%d' % (self.value, self.counts)


