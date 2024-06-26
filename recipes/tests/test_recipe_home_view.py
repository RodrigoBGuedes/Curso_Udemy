from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipesHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_corret(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "No recipes found here",
            response.content.decode("utf-8"),
        )

        # # Tenho que escrever mais algumas coisa sobre o test
        # self.fail('Para que eu termine de digitá-lo')

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse("recipes:home"))
        response_content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]

        # Check if one recipe exists
        self.assertIn("Recipe Title", response_content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))

        # Check if one recipe exists
        self.assertIn(
            "No recipes found here ",
            response.content.decode("utf-8"),
        )

    # @patch("recipes.views.PER_PAGE", new=3)
    def test_recipe_home_is_paginated(self):
        for i in range(9):
            kwargs = {"slug": f"r{i}", "author_data": {"username": f"u{i}"}}
            self.make_recipe(**kwargs)

        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 3)
