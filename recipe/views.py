import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from actions.models import Action
from comments.models import Comment
from .models import recipe_story_list, recipe_detail
from users.models import Detail
# Create your views here.
def homeview(request):
    if request.session.get('username', False):
        try:
            userFK = User.objects.get(username=request.session.get('username'))
            user_id = int(userFK.id)
            # complex filtering for comments left on post
            actions = Action.objects.filter(
                Q(user_id=user_id) |
                Q(target_ct__model='recipe_detail',
                  target_id__in=recipe_detail.objects.filter(user=request.session.get('username')).values_list('id', flat=True))
            ).order_by('-created')
            return render(request,
                          'recipe/recipe_story/dashboard.html',
                          {"actions": actions},
                          )
        except User.DoesNotExist:
            # Handle the case where the username in the session doesn't exist
            return render(request, 'recipe/recipe_story/index.html')
    return render(request,
                  'recipe/recipe_story/index.html')

def listview(request):
    recipe_stories = recipe_story_list.objects.all()[::-1]
    return render(request,
                  'recipe/recipe_story/list.html',
                  {'stories' : recipe_stories}
                  )
def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(recipe_detail, pk=recipe_id)
    comments = Comment.objects.filter(recipe_detail_id=recipe_id).order_by('-created')
    if request.method == 'POST':
        if 'text' in request.POST:
            userFK = User.objects.get(username=request.session.get('username'))
            comment_text = request.POST.get('text')
            new_comment = Comment.objects.create(
                user=userFK,
                recipe_detail_id=recipe.id,
                text=comment_text,
            )
            new_comment.save()
            action = Action(
                user=userFK,
                verb="User commented on this recipe",
                target=recipe,
            )
            action.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
            return redirect('recipe:recipe_detail_view', recipe_id=recipe_id)
        elif 'Edit' in request.POST.get('submit'):
            comment_id = request.POST.get('comment_id')
            if comment_id:
                comment = get_object_or_404(Comment, pk=comment_id)
                print("Edit:", comment)
                return redirect('recipe:recipe_detail_view', recipe_id=recipe_id)
            else:
                print("Error: comment_id is None")
        elif 'Delete' in request.POST.get('submit'):
            comment_id = request.POST.get('comment_id')
            if comment_id:
                comment = get_object_or_404(Comment, pk=comment_id)
                comment.delete()
                userFK = User.objects.get(username=request.session.get('username'))
                action = Action(
                    user=userFK,
                    verb="deleted comment from this recipe",
                    target=recipe,
                )
                action.save()

                messages.add_message(request, messages.WARNING, f'You successfully deleted a comment')
                return redirect('recipe:recipe_detail_view', recipe_id=recipe_id)
            else:
                print("Error: comment_id is None")
    return render(request, 'recipe/recipe_story/recipe_detail.html', {'recipe': recipe, 'comments':comments})

def alt_recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(recipe_detail, pk=recipe_id)
    return render(request, 'recipe/recipe_story/alt_recipe_detail.html', {'recipe': recipe})

# where the ADD message occurs after adding a new message
def uploadview(request):
    if not request.session.get('role') == 'regular' and not request.session.get('role') == 'admin':
        return redirect('recipe:homeview')

    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            user = str(request.session.get('username'))
            userFK = User.objects.get(username=request.session.get('username'))
            date = datetime.datetime.now()
            source = request.POST.get('source')
            ingredients = request.POST.getlist('ingredients')
            nutritionNames = request.POST.getlist('nutritionName')
            nutritionCal = request.POST.getlist('nutritionCal')
            nutritionCarb = request.POST.getlist('nutritionCarb')
            nutritionFat = request.POST.getlist('nutritionFat')
            nutritionProtein = request.POST.getlist('nutritionProtein')
            instructions = request.POST.getlist('instructions')

            nutrition_data = []
            for i in range(len(nutritionNames)):
                nutrition_item = {
                    "name": nutritionNames[i],
                    "calories": nutritionCal[i],
                    "carbs": nutritionCarb[i],
                    "fat": nutritionFat[i],
                    "protein": nutritionProtein[i],
                }
                nutrition_data.append(nutrition_item)

            newrecipedetail = recipe_detail(
                title=title,
                user=user,
                date=date,
                source=source,
                commentsNum=0,
                ingredients=ingredients,
                nutrition=nutrition_data,
                instructions=instructions,
                gallery='',
                userFK=userFK,
            )
            newrecipedetail.save()
            sumProtein = sum(float(i) for i in nutritionProtein if i)

            newrecipelist = recipe_story_list(
                id=newrecipedetail.id,
                source=source,
                name=title,
                protein=sumProtein,
                date=date,
                user=user,
                comments=0,
                userFK=userFK,
            )
            newrecipelist.save()

            # log action
            action = Action(
                user=userFK,
                verb="created the news story",
                target=newrecipedetail,
            )
            action.save()

            messages.add_message(request, messages.SUCCESS, f'You successfully submitted the recipe: {newrecipedetail.title}')
            return redirect('recipe:recipe_detail_view', recipe_id=newrecipedetail.id)

        except Exception as e:
            messages.add_message(request, messages.ERROR, f'An error occurred during upload: {e}')
            return render(request, 'recipe/recipe_story/add.html', {'error': str(e)})

    else:
        return render(request, 'recipe/recipe_story/add.html')

# where the EDIT message occurs for updating a new recipe
def editview(request, recipe_id):
    if not request.session.get('role') == 'regular' and not request.session.get('role') == 'admin':
        return redirect('recipe:homeview')

    storyDetail = get_object_or_404(recipe_detail, pk=recipe_id)
    storyList = get_object_or_404(recipe_story_list, pk=recipe_id)

    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            user = str(request.session.get('username'))
            date = datetime.datetime.now()
            source = request.POST.get('source')
            ingredients = request.POST.getlist('ingredients')
            nutritionNames = request.POST.getlist('nutritionName')
            nutritionCal = request.POST.getlist('nutritionCal')
            nutritionCarb = request.POST.getlist('nutritionCarb')
            nutritionFat = request.POST.getlist('nutritionFat')
            nutritionProtein = request.POST.getlist('nutritionProtein')
            instructions = request.POST.getlist('instructions')
            userFK = User.objects.get(username=request.session.get('username'))

            nutrition_data = []
            for i in range(len(nutritionNames)):
                nutrition_item = {
                    "name": nutritionNames[i],
                    "calories": nutritionCal[i],
                    "carbs": nutritionCarb[i],
                    "fat": nutritionFat[i],
                    "protein": nutritionProtein[i],
                }
                nutrition_data.append(nutrition_item)

            # Update the existing recipe_detail object
            storyDetail.title = title
            storyDetail.user = user
            storyDetail.date = date
            storyDetail.source = source
            storyDetail.ingredients = ingredients
            storyDetail.nutrition = nutrition_data
            storyDetail.instructions = instructions
            storyDetail.userFK = userFK
            storyDetail.save()

            sumProtein = sum(float(i) for i in nutritionProtein if i)

            # Update the existing recipe_story_list object
            storyList.source = source
            storyList.name = title
            storyList.protein = sumProtein
            storyList.date = date
            storyList.user = user
            storyDetail.userFK = userFK
            storyList.save()

            # log action
            action = Action(
                user=userFK,
                verb="created the news story",
                target=storyDetail,
            )
            action.save()

            messages.add_message(request, messages.INFO, f'You successfully updated the recipe: {storyDetail.title}')
            return redirect('recipe:recipe_detail_view', recipe_id=storyDetail.id)

        except Exception as e:
            messages.add_message(request, messages.ERROR, f'An error occurred during update: {e}')
            return render(request, 'recipe/recipe_story/edit.html', {'story': storyDetail, 'error': str(e)})
    else:
        return render(request,
                      'recipe/recipe_story/edit.html',
                      {'story': storyDetail})

def recipe_story_add(request):
    # redirect if not logged in
    if not request.session.get('username', False):
        return redirect('recipe:homeview')
    return render(request,
                  'recipe/recipe_story/add.html', )

def chickencurryview(request):
    story1 = recipe_detail.objects.all().first()
    return render(request,
                  'recipe/recipe_story/chickenCurry.html',
                  {'story' : story1}
                  )

def altchickencurryview(request):
    story1 = recipe_detail.objects.all().first()
    return render(request,
                  'recipe/recipe_story/alternativeChickenCurry.html',
                  {'story' : story1})

# where the DELETE message occurs for deleting something from the listview
def adminview(request):
    if not request.session.get('role') == 'admin':
        return redirect('recipe:homeview')
    recipe_stories = recipe_story_list.objects.all()
    if request.method == 'POST':
        id = request.POST.get('delete_recipe_id')
        if id:
            try:
                recipe_detail_instance = get_object_or_404(recipe_detail, pk=id)
                recipe_story_list_instance = get_object_or_404(recipe_story_list, pk=id)
                title = recipe_detail_instance.title
                recipe_detail_instance.delete()
                recipe_story_list_instance.delete()

                # log action
                userFK = User.objects.get(username=request.session.get('username'))
                action = Action(
                    user=userFK,
                    verb="created the news story",
                    target=title,
                )
                action.save()

                messages.add_message(request, messages.WARNING, f'You successfully deleted the recipe: {title}')
                return redirect('recipe:adminview')
            except Exception as e:
                messages.error(request, f"Error deleting Recipe ID {id}: {e}")
                return redirect('recipe:adminview')
        else:
            messages.warning(request, "No Recipe ID selected for deletion.")
            return redirect('recipe:adminview')
    else:
        return render(request,
                      'recipe/recipe_story/adminlist.html',
                      {'stories' : recipe_stories}
                      )
def adminusersview(request):
    if not request.session.get('role') == 'admin':
        return redirect('recipe:homeview')
    allusers = User.objects.all()
    if request.method == 'POST':
        if 'delete_user_id' in request.POST:
            id = request.POST.get('delete_user_id')
            if id:
                try:
                    user_instance = get_object_or_404(User, pk=id)
                    detail_instance = get_object_or_404(Detail, user_id=id)
                    name = user_instance.username
                    userFK = User.objects.get(username=request.session.get('username'))
                    action = Action(
                        user=userFK,
                        verb="Deleted User",
                        target=user_instance,
                    )
                    action.save()
                    user_instance.delete()
                    detail_instance.delete()
                    messages.add_message(request, messages.WARNING, f'You successfully deleted the user: {name}')
                    return redirect('recipe:adminusersview')
                except Exception as e:
                    messages.error(request, f"Error deleting User {id}: {e}")
                    return redirect('recipe:adminusersview')
        elif 'update_user_id' in request.POST:
            id = request.POST.get('update_user_id')
            if id:
                try:
                    user_instance = get_object_or_404(User, pk=id)
                    detail_instance = get_object_or_404(Detail, user_id=id)
                    name = user_instance.username
                    if detail_instance.role == "admin":
                        detail_instance.role = 'regular'
                    else:
                        detail_instance.role = 'admin'
                    user_instance.save()
                    detail_instance.save()
                    userFK = User.objects.get(username=request.session.get('username'))
                    action = Action(
                        user=userFK,
                        verb="Updated the user role",
                        target=user_instance,
                    )
                    action.save()
                    messages.add_message(request, messages.WARNING, f'You successfully updated the role for the user: {name}')
                    return redirect('recipe:adminusersview')
                except Exception as e:
                    messages.error(request, f"Error deleting User {id}: {e}")
                    return redirect('recipe:adminusersview')
        else:
            messages.warning(request, "No user ID selected for deletion.")
            return redirect('recipe:adminusersview')
    else:
        return render(request,
                      'recipe/recipe_story/adminusers.html',
                      {'users' : allusers}
                      )
def searchview(request):
    return render(request,
                  'recipe/recipe_story/search.html')
