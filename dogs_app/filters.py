import django_filters
from .models import Dog
from django.db.models import Q


# Used for Advanced Filtering of dogs in view_dogs page
class DogFilter(django_filters.FilterSet):
    dogName = django_filters.CharFilter(field_name='dogName',
                                        label='Dog Name',
                                        lookup_expr='icontains')
    dateOfArrival = django_filters.DateFromToRangeFilter(field_name='dateOfArrival',
                                                         label='Date of Arrival (Range)',
                                                         lookup_expr=('gte', 'lte'))
    breed = django_filters.CharFilter(field_name='breed',
                                      label='Breed',
                                      method='filter_breed')
    gender = django_filters.ChoiceFilter(field_name='gender',
                                         label='Gender',
                                         choices=Dog.GENDER_CHOICES)
    furColor = django_filters.CharFilter(field_name='furColor',
                                         label='Fur Color',
                                         method='filter_furColor')
    dateOfVaccination = django_filters.DateFromToRangeFilter(field_name='dateOfVaccination',
                                                             label='Date of Vaccination (Range)',
                                                             lookup_expr=('gte', 'lte'))
    isNeutered = django_filters.ChoiceFilter(field_name='isNeutered',
                                             label='Neutered',
                                             choices=Dog.IS_NEUTERED_CHOICES)
    isDangerous = django_filters.ChoiceFilter(field_name='isDangerous',
                                              label='Dangerous',
                                              choices=Dog.IS_DANGEROUS_CHOICES)
    kongDateAdded = django_filters.DateFromToRangeFilter(field_name='kongDateAdded',
                                                         label='Date given last Kong (Range)',
                                                         lookup_expr=('gte', 'lte'))
    owner = django_filters.CharFilter(field_name='owner__ownerSerialNum',
                                      label='Owner',
                                      method='filter_owner')

    # Ensures that values of "Unspecified" return all results with an empty field
    def filter_breed(self, queryset, name, value):
        if value.lower() == 'unspecified':
            return queryset.filter(Q(breed__exact='') | Q(breed__isnull=True))
        else:
            return queryset.filter(Q(breed__icontains=value))

    # Ensures that values of "Unspecified" return all results with an empty field
    def filter_furColor(self, queryset, name, value):
        if value.lower() == 'unspecified':
            return queryset.filter(Q(furColor__exact='') | Q(furColor__isnull=True))
        else:
            return queryset.filter(Q(furColor__icontains=value))

    # Ensures that values of "Unspecified" return all results with an empty field
    def filter_owner(self, queryset, name, value):
        if value.lower() == 'unspecified':
            return queryset.filter(owner__isnull=True)
        else:
            # Convert the string name back to the owner's serial number
            return queryset.filter(owner__ownerSerialNum=value)

    class Meta:
        model = Dog
        fields = ['dogName', 'dateOfArrival', 'breed', 'gender', 'furColor', 'dateOfVaccination', 'isNeutered', 'isDangerous', 'kongDateAdded', 'owner']
