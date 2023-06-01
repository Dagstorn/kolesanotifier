from django.db import models

class Filter(models.Model):
    BODY_TYPES = (
        ('clear', 'не указывать'),
        ('sedan', 'седан'),
        ('station-wagon', 'универсал'),
        ('hatchback', 'хэтчбек'),
        ('limousine', 'лимузин'),
        ('body-coupe', 'купе'),
        ('body-roadster', 'родстер'),
        ('cabriolet', 'кабриолет'),
        ('suv', 'внедорожник'),
        ('crossover-suv', 'внедорожник'),
        ('microvan', 'микровэн'),
        ('minivan', 'минивэн'),
        ('van', 'микроавтобус'),
        ('wagon', 'фургон'),
        ('body-pickup', 'пикап'),
        ('targa', 'тарга'),
        ('fastback', 'фастбек'),
        ('liftback', 'лифтбек'),
        ('hardtop', 'хардтоп')
    )
    ENGINE_TYPES = (
        ('clear', 'не указывать'),
        ('1', 'бензин'),
        ('2', 'дизель'),
        ('3', 'газ-бензин'),
        ('4', 'газ'),
        ('5', 'гибрид'),
        ('6', 'электричество')
    )
    TRANSMISSION_TYPES = (
        ('clear', 'не указывать'),
        ('1', 'механика'),
        ('2', 'АКПП'),
        ('3', 'автомат'),
        ('4', 'типтроник'),
        ('5', 'вариатор'),
        ('6', 'робот')
    )
    CHEAPERCHOICES = (
        ('15', '15%'),
        ('20', '20%'),
        ('25', '25%'),
        ('30', '30%')
    )
    title = models.CharField('Название фильтра', max_length=100)
    year_from = models.CharField('Год с', blank=True, null=True, max_length=100) 
    year_to = models.CharField('Год до', blank=True, null=True, max_length=100) 
    price_from = models.CharField('Цена с', blank=True, null=True, max_length=100) 
    price_to = models.CharField('Цена до', blank=True, null=True, max_length=100) 
    body = models.CharField('Кузов', choices=BODY_TYPES, default=BODY_TYPES[1][0],  max_length=120)
    engine_fuel = models.CharField('Тип двигателя', choices=ENGINE_TYPES, default=ENGINE_TYPES[1][0],max_length=120)
    transmission_type = models.CharField('КПП', choices=TRANSMISSION_TYPES, default=TRANSMISSION_TYPES[1][0],max_length=120)
    engine_volume_from = models.DecimalField('Объем двигателя от', max_digits=3, decimal_places=2, blank=True, null=True)
    engine_volume_to = models.DecimalField('Объем двигателя до', max_digits=3, decimal_places=2, blank=True, null=True)
    text = models.CharField('Текст поиска', max_length=200, blank=True, null=True)
    url = models.CharField('Сслыка поиска', max_length=1000, default='https://kolesa.kz/cars/?auto-custom=2')
    lastcar = models.CharField('lastacar id', max_length=100, default=1)
    cheaper_perc = models.CharField('Дешевле на', max_length=100, choices=CHEAPERCHOICES)
    view_count = models.PositiveIntegerField('Кол. просмотров', default='1')
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"

    def save(self, *args, **kwargs):
        url = 'https://kolesa.kz/cars/?auto-custom=2'

        if self.body != 'clear':
            url = 'https://kolesa.kz/cars/' + self.body + '/?auto-custom=2'

        if self.year_from:
            url += '&year[from]=' + str(self.year_from)
        if self.year_to:
            url += '&year[to]=' + str(self.year_to)
        if self.price_from:
            url += '&price[from]=' + str(self.price_from)
        if self.price_to:
            url += '&price[to]=' + str(self.price_to)
        if self.engine_fuel != 'clear':
            url += '&auto-fuel=' + str(self.engine_fuel)
        if self.transmission_type != 'clear':
            url += '&auto-car-transm=' + str(self.transmission_type)
        if self.engine_volume_from:
            url += '&auto-car-volume[from]=' + str(self.engine_volume_from)
        if self.engine_volume_to:
            url += '&auto-car-volume[to]=' + str(self.engine_volume_to)
        if self.text:
            url += '&_txt_=' + str(self.text)
        self.url = url
        super(Filter, self).save(*args, **kwargs)


class Client(models.Model):
    tgid = models.PositiveIntegerField('Телеграм ID')
    name = models.CharField('Имя', max_length=120)

    def __str__(self):
        return self.name
            
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

