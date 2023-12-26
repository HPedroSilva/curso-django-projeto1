import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView, DetailView

from utils.pagination import make_pagination
from recipes.models import Recipe

PER_PAGE = int(os.environ.get("PER_PAGE", 6))


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        pk=id,
        is_published=True,
    )

    return render(
        request,
        "recipes/pages/recipe-view.html",
        context={
            "recipe": recipe,
            "is_detail_page": True,
        },
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = ["-id"]
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get("recipes"), PER_PAGE
        )
        context.update(
            {
                "recipes": page_obj,
                "pagination_range": pagination_range,
            }
        )

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()

        if not search_term:
            raise Http404()

        queryset = Recipe.objects.filter(
            Q(
                Q(title__icontains=search_term) | Q(description__icontains=search_term),
            ),
            is_published=True,
        ).order_by("-id")

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()
        context.update(
            {
                "page_title": f'Search for "{search_term}" |',
                "search_term": search_term,
                "additional_url_query": f"&q={search_term}",
            }
        )
        return context


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = get_list_or_404(
            queryset.filter(
                category__id=self.kwargs.get("category_id"),
                is_published=True,
            ).order_by("-id")
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_name = context.get("recipes")[0].category.name
        context.update(
            {
                "title": f"{category_name} - Category | ",
            }
        )
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe-view.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                "is_detail_page": True,
            }
        )
        return context
