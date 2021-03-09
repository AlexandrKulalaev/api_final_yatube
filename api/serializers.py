from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title')
        read_only_fields = ('id', )


class FollowSerializer(serializers.ModelSerializer):
    pass
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].username)
        follow = Follow.objects.filter(
            user=self.context['request'].user, following=user).exists()
        if user == self.context['request'].user:
            raise serializers.ValidationError(
                'Вы не можете подписаться сам на себя')
        if follow is True:
            raise serializers.ValidationError(
                'Вы уже подписаны на пользователя')
        return data

    class Meta:
        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('id', 'user')
