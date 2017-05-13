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


class Relations(models.Model):

    wid = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        related_name = 'r_wid',
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


class TopRelations(models.Model):

    wid = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        related_name = 'tr_wid',
    )

    top1 = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'tr_top1',
    )

    top2 = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'tr_top2',
    )

    top3 = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'tr_top3',
    )

    top4 = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'tr_top4',
    )

    top5 = models.ForeignKey(
        Words,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'tr_top5',
    )

    class Meta:

        db_table = 'top_relations'

    def __str__(self):
        return '%s:%s' % (self.wid.value, self.top1.value)
