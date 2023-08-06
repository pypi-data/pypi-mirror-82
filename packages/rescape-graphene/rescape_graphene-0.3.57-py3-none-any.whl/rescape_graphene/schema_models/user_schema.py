import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from graphene import InputObjectType
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from rescape_python_helpers import ramda as R

from .django_object_type_revisioned_mixin import reversion_types, DjangoObjectTypeRevisionedMixin
from ..django_helpers.write_helpers import increment_prop_until_unique
from ..graphql_helpers.schema_helpers import input_type_fields, REQUIRE, DENY, CREATE, \
    merge_with_django_properties, input_type_parameters_for_update_or_create, UPDATE, \
    guess_update_or_create, graphql_update_or_create, graphql_query, update_or_create_with_revision


class UserType(DjangoObjectType, DjangoObjectTypeRevisionedMixin):
    id = graphene.Int(source='pk')

    class Meta:
        model = get_user_model()


user_fields = merge_with_django_properties(UserType, dict(
    id=dict(create=DENY, update=[REQUIRE]),
    username=dict(create=[REQUIRE], unique_with=increment_prop_until_unique(get_user_model(), None, 'username', {})),
    password=dict(create=[REQUIRE], read=DENY),
    email=dict(create=[REQUIRE]),
    is_superuser=dict(),
    first_name=dict(create=REQUIRE),
    last_name=dict(create=REQUIRE),
    is_staff=dict(),
    is_active=dict(),
    date_joined=dict(create=DENY, update=DENY),
    **reversion_types
))

user_mutation_config = dict(
    class_name='User',
    crud={
        CREATE: 'createUser',
        UPDATE: 'updateUser'
    },
    resolve=guess_update_or_create
)


class UpsertUser(graphene.Mutation):
    """
        Abstract base class for mutation
    """
    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, user_data=None):
        user_model = get_user_model()
        data = R.merge(user_data, dict(password=make_password(R.prop('password', user_data), salt='not_random')) if
        R.prop_or(False, 'password', user_data) else
        {})
        update_or_create_values = input_type_parameters_for_update_or_create(user_fields, data)
        user, created = update_or_create_with_revision(user_model, update_or_create_values)
        return UpsertUser(user=user)


class CreateUser(UpsertUser):
    """
        Create User mutation class
    """

    class Arguments:
        user_data = type('CreateUserInputType', (InputObjectType,), input_type_fields(user_fields, CREATE, UserType))(
            required=True)


class UpdateUser(UpsertUser):
    """
        Update User mutation class
    """

    class Arguments:
        user_data = type('UpdateUserInputType', (InputObjectType,), input_type_fields(user_fields, UPDATE, UserType))(
            required=True)


graphql_update_or_create_user = graphql_update_or_create(user_mutation_config, user_fields)
graphql_query_users = graphql_query(UserType, user_fields, 'users')

