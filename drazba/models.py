from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

PSC_REGEX = RegexValidator(r'^\d{5}$', 'Nesprávně zadané poštovní směrovací číslo')
TELEFON_REGEX = RegexValidator(r'^[+]\d{3}( \d{3}){3}$', 'Nesprávně zadané telefonní číslo')


class Misto(models.Model):
    jmeno = models.CharField(max_length=50, verbose_name='Jméno města/obce', help_text='Zadejte jméno města/obce',
                             error_messages={'blank': 'Jméno města/obce musí být vyplněno'})
    psc = models.PositiveIntegerField(verbose_name='PSČ', help_text='Zadejte poštovní směrovací číslo (bez mezery)', validators=[PSC_REGEX])

    class Meta:
        ordering = ['jmeno']
        verbose_name = 'Město/obec'
        verbose_name_plural = 'Místa'

    def __str__(self):
        return f'{self.jmeno}, {self.psc}'


class Urad(models.Model):
    nazev = models.CharField(max_length=100, verbose_name='Název úřadu', help_text='Zadejte úplný název exekutorského úřadu',
                             error_messages={'blank': 'Název úřadu musí být vyplněn'})
    adresa = models.CharField(max_length=100, verbose_name='Adresa úřadu', help_text='Zadejte adresu exekutorského úřadu včetně čísla popisného/orientačního',
                             error_messages={'blank': 'Adresa úřadu musí být vyplněna'})
    mesto = models.ForeignKey('Misto', on_delete=models.CASCADE, verbose_name='Město')

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Exekutorský úřad'
        verbose_name_plural = 'Exekutorské úřady'

    def __str__(self):
        return f'{self.nazev}'


class Exekutor(models.Model):
    jmeno = models.CharField(max_length=50, verbose_name='Jméno exekutora', help_text='Zadejte jméno exekutora',
                             error_messages={'blank': 'Jméno exekutora musí být vyplněno'})
    prijmeni = models.CharField(max_length=50, verbose_name='Příjmení exekutora', help_text='Zadejte příjmení exekutora',
                                error_messages={'blank': 'Příjmení exekutora musí být vyplněno'})
    TITULY = (
        ('Bc.', 'Bc.'),
        ('Ing.', 'Ing.'),
        ('Mgr.', 'Mgr.'),
        ('JUDr.', 'JUDr.'),
    )
    titul = models.CharField(max_length=5, choices=TITULY, verbose_name='Titul', help_text='Zvolte titul exekutora', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Email exekutora', help_text='Zadejte e-mail exekutora',
                              error_messages={'unique': 'E-mailová adresa musí být jedinečná', 'invalid': 'Neplatná e-mailová adresa',
                                              'blank': 'Pole nesmí být prázdné'})
    telefon = models.CharField(max_length=16, verbose_name='Telefon exekutora', help_text='Zadejte telefon v podobě: +420 777 777 777',
                               blank=True, validators=[TELEFON_REGEX])
    urad = models.ForeignKey('Urad', on_delete=models.CASCADE, verbose_name='Exekutorský úřad')

    class Meta:
        ordering = ['prijmeni', 'jmeno']
        verbose_name = 'Exekutor'
        verbose_name_plural = 'Exekutoři'

    def __str__(self):
        return f'{self.prijmeni}, {self.jmeno}'


class Predmet(models.Model):
    oznaceni = models.CharField(max_length=200, verbose_name='Označení předmětu exekuce', help_text='Zadejte vhodné označení předmětu exekuce')
    cislo_jednaci = models.CharField(max_length=20, verbose_name='Číslo jednací', help_text='Zadejte přesné číslo jednací')
    popis = models.TextField(verbose_name='Popis předmětu dražby', help_text='Zadejte podrobnější popis předmětu dražby')
    foto = models.ImageField(blank=True, null=True, upload_to='fota', verbose_name='Fotografie')
    pocatecni_cena = models.PositiveIntegerField(verbose_name='Počáteční cena v Kč')
    zacatek_drazby = models.DateTimeField(verbose_name='Datum a čas začátku dražby')
    konec_drazby = models.DateTimeField(verbose_name='Datum a čas konce dražby')
    misto = models.ForeignKey('Misto', on_delete=models.CASCADE, verbose_name='Místo')
    exekutor = models.ForeignKey('Exekutor', on_delete=models.CASCADE, verbose_name='Exekutor', null=True, blank=True)

    class Meta:
        ordering = ['zacatek_drazby']
        verbose_name = 'Předmět dražby'
        verbose_name_plural = 'Předměty dražby'

    def __str__(self):
        return f'{self.oznaceni} ({self.misto})'


class Zajemce(models.Model):
    TYPY_ZAJEMCU = (
        ('FO', 'Fyzická osoba'),
        ('PO', 'Právnická osoba'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Uživatel')
    telefon = models.CharField(max_length=16, verbose_name='Telefon', validators=[TELEFON_REGEX],
                               help_text='Telefonní číslo ve tvaru: +420 123 456 789',
                               error_messages={'invalid': 'Neplatné telefonní číslo', 'blank': 'Pole nesmí být prázdné'})
    datum_registrace = models.DateTimeField(auto_now_add=True, verbose_name='Datum registrace')
    typ = models.CharField(max_length=2, choices=TYPY_ZAJEMCU, verbose_name='Typ zájemce')
    poznamka = models.TextField(blank=True, null=True, verbose_name='Poznámka')
    predmety = models.ManyToManyField('Predmet', related_name='zajemci', verbose_name='Předměty zájmu')

    class Meta:
        verbose_name = 'Zájemce'
        verbose_name_plural = 'Zájemci'
        ordering = ['datum_registrace']

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.get_typ_display()})'