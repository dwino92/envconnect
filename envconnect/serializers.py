# Copyright (c) 2018, DjaoDjin inc.
# see LICENSE.

#pylint: disable=old-style-class,no-init

from rest_framework import serializers

from pages.models import PageElement
from pages.serializers import PageElementSerializer as BasePageElementSerializer
from survey.models import EnumeratedQuestions

from .models import ColumnHeader, Consumption


class ColumnHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ColumnHeader
        fields = ('slug', 'hidden',)
        read_only_fields = ('slug',)


class ConsumptionSerializer(serializers.ModelSerializer):

    path = serializers.CharField(required=False)
    rank = serializers.SerializerMethodField()
    nb_respondents = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    opportunity = serializers.SerializerMethodField()
    implemented = serializers.SerializerMethodField()
    planned = serializers.SerializerMethodField()

    class Meta:
        model = Consumption
        fields = (
            "path",
            # description
            #XXX "text",
            #XXX "avg_energy_saving", "avg_fuel_saving",
            #XXX "capital_cost", "payback_period",
            # value summary
            "environmental_value", "business_value", "profitability",
            "implementation_ease", "avg_value",
            # benchmarks
            "nb_respondents", "rate", "opportunity",
            "rank", "implemented", "planned", "requires_measurements")

    @staticmethod
    def get_nb_respondents(obj):
        return obj.nb_respondents if hasattr(obj, 'nb_respondents') else 0

    def get_rank(self, obj):
        if hasattr(obj, 'rank') and obj.rank:
            return obj.rank
        return EnumeratedQuestions.objects.filter(
            campaign=self.context['campaign'],
            question_id=obj.id).first().rank

    @staticmethod
    def get_rate(obj):
        return obj.rate if hasattr(obj, 'rate') else 0

    @staticmethod
    def get_implemented(obj):
        return obj.implemented if hasattr(obj, 'implemented') else (
            obj.measured if hasattr(obj, 'measured') else "")

    def get_planned(self, obj):
        return (hasattr(obj, 'is_planned') and bool(obj.is_planned)
            or self.context.get('is_planned', False))

    def get_opportunity(self, obj):
        if hasattr(obj, 'opportunity'):
            return obj.opportunity
        # XXX This is used in ``ImprovementListAPIView``.
        opportunities = self.context.get('opportunities', None)
        if opportunities is not None:
            return opportunities.get(obj.pk, 0) * 3
        return 0


class AccountSerializer(serializers.Serializer):
    """
    Used to list accessible suppliers
    """
    slug = serializers.CharField()
    printable_name = serializers.CharField()
    email = serializers.EmailField()
    normalized_score = serializers.IntegerField(required=False)
    last_activity_at = serializers.DateTimeField(required=False)
    nb_questions = serializers.IntegerField(required=False)
    nb_answers = serializers.IntegerField(required=False)
    improvement_score = serializers.IntegerField(required=False)
    request_key = serializers.CharField(required=False)

    def create(self, validated_data):
        raise NotImplementedError('This serializer is read-only')

    def update(self, instance, validated_data):
        raise NotImplementedError('This serializer is read-only')


class MoveRankSerializer(serializers.Serializer):
    """
    Move a best practice into the tree of best practices.
    """
    source = serializers.CharField(write_only=True)

    def create(self, validated_data):
        raise NotImplementedError('This serializer is read-only')

    def update(self, instance, validated_data):
        raise NotImplementedError('This serializer is read-only')


class PageElementSerializer(BasePageElementSerializer):

    consumption = ConsumptionSerializer(required=False)
    is_empty = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = PageElement
        fields = ('slug', 'path', 'title', 'tag',
            'rank', 'is_empty', 'consumption')

    @staticmethod
    def get_rank(obj):
        return obj.rank if hasattr(obj, 'rank') else None

    @staticmethod
    def get_is_empty(obj):
        return not obj.text


class ScoreWeightSerializer(serializers.Serializer):

    weight = serializers.DecimalField(decimal_places=2, max_digits=3,
        required=True)

    class Meta:
        fields = ('weight',)

    def create(self, validated_data):
        raise NotImplementedError('done is APIView')

    def update(self, instance, validated_data):
        raise NotImplementedError('done is APIView')
