"""directory Models."""

from django.db import models
import datetime


class AddressEntry(models.Model):
    """Individual Address Entry.

    name is the name of the addressee
    address is the email (or whatever) address associated with the name
    date_created is when the entry was originally stored
    date_updated is when the entry was last stored
    version is the number of times the entry was stored
    """
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    date_created = models.DateField()
    date_updated = models.DateField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        r"""String function

        >>> str(AddressEntry(name='Eric', address='example',
        ... date_created=datetime.date(2017, 8, 1),
        ... date_updated=datetime.date(2017, 8, 2), version=5))
        'Eric, example, 2017-08-01, 2017-08-02, 5'
        """
        return ', '.join([
            str(self.name),
            str(self.address),
            str(self.date_created),
            str(self.date_updated),
            str(self.version),
        ])

    def __repr__(self):
        r"""Repr function

        >>> repr(AddressEntry(name='Eric', address='example',
        ... date_created=datetime.date(2017, 8, 1),
        ... date_updated=datetime.date(2017, 8, 2), version=5))
        ... # doctest: +NORMALIZE_WHITESPACE
        "AddressEntry(name='Eric', address='example',
        date_created=datetime.date(2017, 8, 1),
        date_updated=datetime.date(2017, 8, 2), version=5"
        """
        return 'AddressEntry(name={!r}, address={!r}, date_created={!r}, ' \
               'date_updated={!r}, version={!r}'.format(self.name,
                                                        self.address,
                                                        self.date_created,
                                                        self.date_updated,
                                                        self.version)

