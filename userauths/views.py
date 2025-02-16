from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauths.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Profile
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404
from api.models import TransactionData
from django.db import IntegrityError
from api.forms import TransactionUploadForm


User = get_user_model()


def RegisterView(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already signed in.")
        return redirect("api:index")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            try:
                # Attempt to save the new user
                new_user = form.save()

                email = form.cleaned_data.get("email")
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")

                messages.success(request, f"Welcome, {username.title()}! Your account has been created successfully. You are now logged in as {username}.")

                # Authenticate and login the user
                authenticated_user = authenticate(username=email, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect("api:index")
                else:
                    messages.warning(request, "Your account was created, but there was an issue logging you in. Please sign in manually.")
                    return redirect("userauths:sign-in")

            except IntegrityError as e:
                # Check if the error is related to unique constraint violation
                if 'username' in str(e):
                    messages.error(request, "The USERNAME you have chosen is already taken. Please choose a different username!.")
                elif 'email' in str(e):
                    messages.error(request, "The EMAIL address is already associated with an existing account.")
                else:
                    messages.error(request, "There was an error creating your account. Please try again.")
                return redirect("userauths:sign-up")
        
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")

            full_error_message = "There was an error creating your account:\n" + "\n".join(error_messages)
            messages.error(request, full_error_message)

    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-up.html", context)
    
def LoginView(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already signed in.")
        return redirect("api:index")

    next_url = request.GET.get('next')  # Get the 'next' parameter

    if next_url:
        messages.warning(request, "You need to sign in to view that page.")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, "User does not exist, create an account.")
            return redirect('userauths:sign-in')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in successfully.")

            # Ensure the next URL is safe before redirecting
            if next_url:
                return redirect(next_url)

            return redirect("api:index")

        else:
            messages.warning(request, "Username or password is incorrect.")

    return render(request, "userauths/sign-in.html", {"next": next_url})


def LogoutView(request):
    logout(request)
    return redirect("userauths:sign-in")



@login_required
def my_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)  # Ensure profile exists

    # Fetch transactions (if needed)
    transactions = TransactionData.objects.filter(user=user).first()  # Assuming you have this model
    form = TransactionUploadForm()
    context = {
        "user": user,
        "profile": profile,
        "transactions": transactions,  # Pass transactions to the template
        "form": form,
    }

    return render(request, "userauths/profile.html", context)



@login_required
def settings(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)  
            profile.save()

            # Update User Model Fields
            user.first_name = request.POST.get("first_name", user.first_name)
            user.last_name = request.POST.get("last_name", user.last_name)
            user.save()

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("userauths:settings")

    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        "form": form,
        "user": user,
        "profile": profile,
    }
    
    return render(request, "userauths/settings.html", context)



def change_password(request):
    user = request.user  

    if request.method == "POST":
        form = CustomPasswordChangeForm(user, request.POST)  
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            messages.success(request, "Your password has been updated successfully.")
            return redirect("userauths:change_password")
        else:
            # Pass form errors to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomPasswordChangeForm(user)

    return render(request, "userauths/change-password.html", {"form": form})




@login_required
def delete_account(request):
    user = request.user  # Get logged-in user
    
    if request.method == "POST":
        confirm_delete = request.POST.get("confirm_delete")  # Get checkbox value
        
        if confirm_delete:  # Ensure the checkbox is checked
            user.delete()  # Delete the user account
            logout(request)  # Log out the user
            messages.success(request, "Your account has been deleted successfully.")
            return redirect("userauths:sign-in")  # Redirect to homepage or login page
        else:
            messages.error(request, "Please confirm that you want to delete your account.")

    return render(request, "userauths/delete-account.html")