import django_filters
from django import forms
from Institute.models import Exam
from django_filters import DateFilter
from django.forms import DateInput

CLASS=(
    ("1st","1st"),
    ("2nd","2nd"),
    ("3rd","3rd"),
    ("4th","4th"),
    ("5th","5th"),
    ("6th","6th"),
    ("7th","7th"),
    ("8th","8th"),
    ("9th","9th"),
    ("10th","10th"),
)

class Exam_List_Filter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='exam_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='exam_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    )
    class_name = django_filters.ChoiceFilter(choices=CLASS)
    subject = django_filters.CharFilter()
    def __init__(self, *args, **kwargs):
        super(Exam_List_Filter, self).__init__(*args, **kwargs)
        self.filters['exam_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['exam_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = Exam
        fields = ['exam_date','class_name','subject']
        widgets = {
            'exam_date': DateInput(attrs={'type': 'date'})
        }

