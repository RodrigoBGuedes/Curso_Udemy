from os import name

from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes.views import recipe

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='teste_default_category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='recipe Description',
            slug='recipe-slug-for_no_defaults',
            preparation_time=10 ,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='Recipe Preparations Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
         
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_steps_is_html, 
                         msg='Recipe preparation_steps_html is not false')
    
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published, 
                         msg='Recipe is published is not false')
    
    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed,
                         msg=f'Recipe string representation must be "{needed}" but '
                         f'"{str(self.recipe)}" was received'
                         ) 
            