from rest_framework.status import HTTP_400_BAD_REQUEST

from drf_openapi.entities import VersionedSerializers
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class LanguageSerializer(serializers.Serializer):
    name = serializers.ChoiceField(
        choices=LANGUAGE_CHOICES, default='python', help_text='The name of the programming language')


class SnippetSerializerV1(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = LanguageSerializer()
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    lines = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, allow_null=True, required=False)

    class Meta:
        error_status_codes = {
            HTTP_400_BAD_REQUEST: 'Bad Request'
        }

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class SnippetSerializerV2(SnippetSerializerV1):
    title = serializers.CharField(required=True, max_length=100)


class SnippetSerializer(VersionedSerializers):
    """
    Changelog:

    * **v1.0**: `title` is optional
    * **v2.0**: `title` is required
    """

    VERSION_MAP = (
        ('>=1.0, <2.0', SnippetSerializerV1),
        ('>=2.0', SnippetSerializerV2),
    )
