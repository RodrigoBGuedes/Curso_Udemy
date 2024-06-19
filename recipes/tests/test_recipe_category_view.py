import re
from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipesCategoryViewsTest(RecipeTestBase):
    def  test_recipe_category_view_function_is_corret(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)
        
    def  test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100})
            )
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_category_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', args=(1, )))        
        response_content = response.content.decode('utf-8')
        
        # Check if one recipe exists
        self.assertIn(needed_title, response_content)
    
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':recipe.category.id}))
        
        self.assertEqual(response.status_code, 404)
 