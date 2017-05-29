from django.db import models


class Words(models.Model):

    value = models.CharField(
        max_length = 26,
        unique = True,
    )

    counts = models.IntegerField(
        default = 0,
    )

    class Meta:

        db_table = 'words'

    def __str__(self):
        return '%s:%d' % (self.value, self.counts)


class Relations(models.Model):

    wid = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        related_name = 'r_wid',
        db_index = True,
    )

    next_wid = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        related_name = 'r_next_wid',
    )

    counts = models.IntegerField(
       default = 1,
   )

    class Meta:

        db_table = 'relations'

    def __str__(self):
        return '%s->%s:%d' % (self.wid.value, self.next_wid.value, self.counts)


class UserHabits(models.Model):

    uid = models.IntegerField()

    value = models.CharField(
        max_length = 26,
    )

    counts = models.IntegerField(
        default = 0,
    )

    class Meta:

        unique_together = ('value', 'uid')
        db_table = 'user_habits'

    def __str__(self):
        return '[%d]%s:%d' % (self.uid, self.value, self.counts)


class DailyLanguages(models.Model):

    wid = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        db_index = True,
    )

    next_words = models.CharField(
        max_length = 50,
    )

    class Meta:

        db_table = 'daily_languages'

    def __str__(self):
        return '%s %s' % (self.wid.value, self.next_words)


