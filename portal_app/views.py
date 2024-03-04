from datetime import timedelta

from django.contrib import messages
from django.db.models import ProtectedError, Q, ExpressionWrapper, F, fields
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django_tables2 import RequestConfig

from dogs_app.forms import (OwnerForm, CameraForm, KennelForm, KennelEditForm, TreatmentPortalForm,
                            ExaminationPortalForm, PlacementPortalForm, ObservesPortalForm,
                            ObservationPortalForm, DogStancePortalForm)
from dogs_app.models import (Owner, Camera, Kennel, Treatment, EntranceExamination,
                             DogPlacement, Observes, Observation, DogStance, Branch)
from portal_app.tables import (OwnerTable, CameraTable, KennelTable, TreatmentTable, ExaminationTable,
                               DogPlacementTable, ObservesTable, ObservationTable, DogStanceTable)


# Helper function to get the user's current branch object (Israel/Italy)
def get_current_branch(request):
    # Get the current Branch (Israel/Italy)
    branch_name = request.session.get('branch', 'Israel')  # Default to Israel
    branch = Branch.objects.get(branchName=branch_name)  # Get the branch object

    return branch


# Display a list of all Owners
def owner_list_portal(request):
    branch = get_current_branch(request)
    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = Owner.objects.filter(branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:
            queryset = queryset.filter(
                Q(firstName__icontains=term) |
                Q(lastName__icontains=term) |
                Q(ownerID__icontains=term) |
                Q(ownerAddress__icontains=term) |
                Q(city__icontains=term) |
                Q(phoneNum__icontains=term) |
                Q(cellphoneNum__icontains=term) |
                Q(comments__icontains=term)
            )
        table = OwnerTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/owners.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Owner
def add_owner_portal(request):
    branch = get_current_branch(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OwnerForm(request.POST)
            if form.is_valid():
                try:
                    # Create Owner instance but don't save to DB yet
                    owner_instance = form.save(commit=False)
                    # Assign the current branch to the owner
                    owner_instance.branch = branch
                    # Save the owner instance to the database
                    owner_instance.save()
                    messages.success(request, "Owner added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Owner: {str(e)}")
                return redirect('portal_app:list-owners')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Owner",
                    'list_page': reverse('portal_app:list-owners')
                })
        else:
            form = OwnerForm()
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Owner",
            'list_page': reverse('portal_app:list-owners')
        })
    else:
        messages.error(request, "You must be logged in to add an Owner.")
        return redirect('dogs_app:home')


# Handle deleting an Owner
def delete_owner_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        owner = get_object_or_404(Owner, pk=pk)

        # Delete the owner
        try:
            owner.delete()
            messages.success(request, "Owner deleted successfully.")
        except ProtectedError:
            messages.error(request, "Owner can't be deleted because it is associated with one or more dogs.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Owner: {str(e)}")

        # Redirect to the owners list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-owners')
                                    + '?page=' + page + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete an Owner.")
        return redirect('dogs_app:home')


# Handle editing an Owner
def edit_owner_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        owner = get_object_or_404(Owner, pk=pk)

        if request.method == 'POST':
            form = OwnerForm(request.POST, instance=owner)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Owner updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Owner: {str(e)}")
                return HttpResponseRedirect(reverse('portal_app:list-owners')
                                            + '?page=' + page + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = OwnerForm(instance=owner)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Owner",
            'list_page': reverse('portal_app:list-owners'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit an Owner.")
        return redirect('dogs_app:home')


# Display a list of all Cameras
def camera_list_portal(request):
    branch = get_current_branch(request)

    # Check if user is logged in
    if request.user.is_authenticated:

        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = Camera.objects.filter(branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:
            queryset = queryset.filter(
                Q(camID__icontains=term)
            )

        table = CameraTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/cameras.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Camera
def add_camera_portal(request):
    branch = get_current_branch(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CameraForm(request.POST)
            if form.is_valid():
                try:
                    # Create Camera instance but don't save to DB yet
                    camera_instance = form.save(commit=False)
                    # Assign the current branch to the Camera
                    camera_instance.branch = branch
                    # Save the kennel instance to the database
                    camera_instance.save()
                    messages.success(request, "Camera added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Camera: {str(e)}")
                return redirect('portal_app:list-cameras')
            else:
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Camera",
                    'list_page': reverse('portal_app:list-cameras')
                })
        else:
            form = CameraForm()
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Camera",
            'list_page': reverse('portal_app:list-cameras')
        })
    else:
        messages.error(request, "You must be logged in to add a Camera.")
        return redirect('dogs_app:home')


# Handle deleting a Camera
def delete_camera_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        camera = get_object_or_404(Camera, pk=pk)

        # Delete the camera
        try:
            camera.delete()
            messages.success(request, "Camera deleted successfully.")
        except ProtectedError:
            messages.error(request, "Camera can't be deleted because it is associated with Sessions.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Camera: {str(e)}")

        # Redirect to the cameras list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-cameras') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete a Camera.")
        return redirect('dogs_app:home')


# Handle editing a Camera
def edit_camera_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        camera = get_object_or_404(Camera, pk=pk)

        if request.method == 'POST':

            form = CameraForm(request.POST, request.FILES, instance=camera)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Camera updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Camera: {str(e)}")
                return HttpResponseRedirect(reverse('portal_app:list-cameras') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = CameraForm(instance=camera)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Camera",
            'list_page': reverse('portal_app:list-cameras'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit a Camera.")
        return redirect('dogs_app:home')


# Display a list of all Kennels
def kennel_list_portal(request):
    branch = get_current_branch(request)

    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = Kennel.objects.filter(branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:

            queryset = queryset.filter(
                Q(kennelNum__icontains=term) |
                Q(kennelImage__icontains=term)
            )

        table = KennelTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/kennels.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Kennel
def add_kennel_portal(request):
    branch = get_current_branch(request)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = KennelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    # Create Kennel instance but don't save to DB yet
                    kennel_instance = form.save(commit=False)
                    # Assign the current branch to the kennel
                    kennel_instance.branch = branch
                    # Save the kennel instance to the database
                    kennel_instance.save()
                    messages.success(request, "Kennel added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Kennel: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Kennel",
                        'list_page': reverse('portal_app:list-kennels')
                    })
                return redirect('portal_app:list-kennels')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Kennel",
                    'list_page': reverse('portal_app:list-kennels')
                })
        else:
            form = KennelForm()
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Kennel",
            'list_page': reverse('portal_app:list-kennels')
        })
    else:
        messages.error(request, "You must be logged in to add a Kennel.")
        return redirect('dogs_app:home')


# Handle deleting a Kennel
def delete_kennel_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        kennel = get_object_or_404(Kennel, pk=pk)

        # Delete the kennel
        try:
            kennel.delete()
            messages.success(request, "Kennel deleted successfully.")
        except ProtectedError:
            messages.error(request, "Kennel can't be deleted because it is associated with one or more Placements.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Kennel: {str(e)}")

        # Redirect to the kennels list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-kennels') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete a Kennel.")
        return redirect('dogs_app:home')


# Handle editing a Kennel
def edit_kennel_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        kennel = get_object_or_404(Kennel, pk=pk)

        if request.method == 'POST':

            form = KennelEditForm(request.POST, request.FILES, instance=kennel)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Kennel updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Kennel: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "kennel",
                        'list_page': reverse('portal_app:list-kennels'),
                        'page': page, 'sort': sort, 'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-kennels') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = KennelEditForm(instance=kennel)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "kennel",
            'list_page': reverse('portal_app:list-kennels'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit a Kennel.")
        return redirect('dogs_app:home')


# Display a list of all Treatments
def treatment_list_portal(request):
    branch = get_current_branch(request)
    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = Treatment.objects.filter(dog__branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:

            # Account for date searches
            if '/' in term:
                date_parts = term.split('/')
                date_search = ''
                if len(date_parts) == 3:
                    date_search = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
                elif len(date_parts) == 2:
                    date_search = date_parts[1] + '-' + date_parts[0]

                if date_search:
                    queryset = queryset.filter(
                        Q(treatmentName__icontains=term) |
                        Q(treatmentDate__icontains=date_search) |
                        Q(treatmentDate__icontains=term) |
                        Q(treatedBy__icontains=term) |
                        Q(comments__icontains=term) |
                        Q(dog__dogName__icontains=term)
                    )
            else:
                queryset = queryset.filter(
                    Q(treatmentName__icontains=term) |
                    Q(treatmentDate__icontains=term) |
                    Q(treatedBy__icontains=term) |
                    Q(comments__icontains=term) |
                    Q(dog__dogName__icontains=term)
                )

        table = TreatmentTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/treatments.html', {'table': table,
                                                               'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Treatment
def add_treatment_portal(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TreatmentPortalForm(request.POST, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Treatment added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Treatment: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Treatment",
                        'list_page': reverse('portal_app:list-treatments')
                    })
                return redirect('portal_app:list-treatments')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Treatment",
                    'list_page': reverse('portal_app:list-treatments')
                })
        else:
            form = TreatmentPortalForm(request=request)
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Treatment",
            'list_page': reverse('portal_app:list-treatments')
        })
    else:
        messages.error(request, "You must be logged in to add a Treatment.")
        return redirect('dogs_app:home')


# Handle deleting a Treatment
def delete_treatment_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        treatment = get_object_or_404(Treatment, pk=pk)

        # Delete the treatment
        try:
            treatment.delete()
            messages.success(request, "Treatment deleted successfully.")
        except ProtectedError:
            messages.error(request, "Treatment can't be deleted because it is associated with one or more dogs.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Treatment: {str(e)}")

        # Redirect to the treatments list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-treatments') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete a Treatment.")
        return redirect('dogs_app:home')


# Handle editing a Treatment
def edit_treatment_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        treatment = get_object_or_404(Treatment, pk=pk)

        if request.method == 'POST':
            form = TreatmentPortalForm(request.POST, instance=treatment, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Treatment updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Treatment: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "Treatment",
                        'list_page': reverse('portal_app:list-treatments'),
                        'page': page, 'sort': sort, 'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-treatments') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = TreatmentPortalForm(instance=treatment, request=request)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Treatment",
            'list_page': reverse('portal_app:list-treatments'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit a Treatment.")
        return redirect('dogs_app:home')


# Display a list of all Examinations
def examination_list_portal(request):
    branch = get_current_branch(request)
    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = EntranceExamination.objects.filter(dog__branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:

            # Account for date searches
            if '/' in term:
                date_parts = term.split('/')
                date_search = ''
                if len(date_parts) == 3:
                    date_search = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
                elif len(date_parts) == 2:
                    date_search = date_parts[1] + '-' + date_parts[0]

                if date_search:
                    queryset = queryset.filter(
                        Q(examinationDate__icontains=date_search) |
                        Q(examinedBy__icontains=term) |
                        Q(results__icontains=term) |
                        Q(dogWeight__icontains=term) |
                        Q(dogTemperature__icontains=term) |
                        Q(dogPulse__icontains=term) |
                        Q(comments__icontains=term) |
                        Q(dog__dogName__icontains=term)
                    )
            else:
                queryset = queryset.filter(
                    Q(examinationDate__icontains=term) |
                    Q(examinedBy__icontains=term) |
                    Q(results__icontains=term) |
                    Q(dogWeight__icontains=term) |
                    Q(dogTemperature__icontains=term) |
                    Q(dogPulse__icontains=term) |
                    Q(comments__icontains=term) |
                    Q(dog__dogName__icontains=term)
                )

        table = ExaminationTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/examinations.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Examination
def add_examination_portal(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ExaminationPortalForm(request.POST, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Examination added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Examination: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Examination",
                        'list_page': reverse('portal_app:list-examinations')
                    })
                return redirect('portal_app:list-examinations')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Examination",
                    'list_page': reverse('portal_app:list-examinations')
                })
        else:
            form = ExaminationPortalForm(request=request)
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Examination",
            'list_page': reverse('portal_app:list-examinations')
        })
    else:
        messages.error(request, "You must be logged in to add an Examination.")
        return redirect('dogs_app:home')


# Handle deleting an Examination
def delete_examination_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        examination = get_object_or_404(EntranceExamination, pk=pk)

        # Delete the examination
        try:
            examination.delete()
            messages.success(request, "Examination deleted successfully.")
        except ProtectedError:
            messages.error(request, "Examination can't be deleted because it is associated with one or more dogs.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Examination: {str(e)}")

        # Redirect to the examinations list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-examinations') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete an Examination.")
        return redirect('dogs_app:home')


# Handle editing an Examination
def edit_examination_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        examination = get_object_or_404(EntranceExamination, pk=pk)

        if request.method == 'POST':
            form = ExaminationPortalForm(request.POST, instance=examination, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Examination updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Examination: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "Examination",
                        'list_page': reverse('portal_app:list-examinations'),
                        'page': page, 'sort': sort, 'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-examinations') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = ExaminationPortalForm(instance=examination, request=request)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Examination",
            'list_page': reverse('portal_app:list-examinations'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit an Examination.")
        return redirect('dogs_app:home')


# Display a list of all Dog Placements
def placement_list_portal(request):
    branch = get_current_branch(request)

    # Check if user is logged in
    if request.user.is_authenticated:
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = DogPlacement.objects.filter(kennel__branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:
            # Account for date searches
            if '/' in term:
                date_parts = term.split('/')
                date_search = ''
                if len(date_parts) == 3:
                    date_search = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
                elif len(date_parts) == 2:
                    date_search = date_parts[1] + '-' + date_parts[0]

                if date_search:
                    queryset = queryset.filter(
                        Q(dog__dogName__icontains=term) |
                        Q(kennel__kennelNum__icontains=term) |
                        Q(kennel__branch__branchName__icontains=term) |
                        Q(entranceDate__icontains=date_search) |
                        Q(expirationDate__icontains=date_search) |
                        Q(placementReason__icontains=term)
                    )
            # If "branch" is in the search term, exclude it from the search
            elif term.lower() == "branch":
                continue
            else:
                queryset = queryset.filter(
                    Q(dog__dogName__icontains=term) |
                    Q(kennel__kennelNum__icontains=term) |
                    Q(kennel__branch__branchName__icontains=term) |
                    Q(entranceDate__icontains=term) |
                    Q(expirationDate__icontains=term) |
                    Q(placementReason__icontains=term)
                )
            # Numeric term - calculate and filter based on duration
            if term.isdigit():
                # Calculate the difference in days
                duration = ExpressionWrapper(F('expirationDate') - F('entranceDate'),
                                             output_field=fields.DurationField())
                # Filter where duration matches the numeric term
                duration_query = DogPlacement.objects.annotate(duration_days=duration).filter(
                    duration_days=timedelta(days=int(term)))
                queryset = queryset | duration_query  # Combine with the main queryset

        table = DogPlacementTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/placements.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Placement
def add_placement_portal(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PlacementPortalForm(request.POST, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Placement added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Placement: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Placement",
                        'list_page': reverse('portal_app:list-placements')
                    })
                return redirect('portal_app:list-placements')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Placement",
                    'list_page': reverse('portal_app:list-placements')
                })
        else:
            form = PlacementPortalForm(request=request)
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Placement",
            'list_page': reverse('portal_app:list-placements')
        })
    else:
        messages.error(request, "You must be logged in to add a Placement.")
        return redirect('dogs_app:home')


# Handle deleting a Placement
def delete_placement_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        placement = get_object_or_404(DogPlacement, pk=pk)

        # Delete the placement
        try:
            placement.delete()
            messages.success(request, "Placement deleted successfully.")
        except ProtectedError:
            messages.error(request, "Placement can't be deleted because "
                                    "it is associated with one or more dogs/kennels.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Placement: {str(e)}")

        # Redirect to the placements list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-placements') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete a Placement.")
        return redirect('dogs_app:home')


# Handle editing a Placement
def edit_placement_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        placement = get_object_or_404(DogPlacement, pk=pk)

        if request.method == 'POST':
            form = PlacementPortalForm(request.POST, instance=placement, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Placement updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Placement: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "Placement",
                        'list_page': reverse('portal_app:list-placements'),
                        'page': page, 'sort': sort, 'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-placements') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = PlacementPortalForm(instance=placement, request=request)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Placement",
            'list_page': reverse('portal_app:list-placements'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit a Placement.")
        return redirect('dogs_app:home')


# Display a list of all Sessions (Observes)
def observes_list_portal(request):
    branch = get_current_branch(request)
    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = Observes.objects.filter(dog__branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:

            # Account for date searches
            if '/' in term:
                date_parts = term.split('/')
                date_search = ''
                if len(date_parts) == 3:
                    date_search = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
                elif len(date_parts) == 2:
                    date_search = date_parts[1] + '-' + date_parts[0]

                if date_search:
                    queryset = queryset.filter(
                        Q(dog__dogName__icontains=term) |
                        Q(camera__camID__icontains=term) |
                        Q(sessionDate__icontains=date_search) |
                        Q(comments__icontains=term)
                    )
            else:
                queryset = queryset.filter(
                    Q(dog__dogName__icontains=term) |
                    Q(camera__camID__icontains=term) |
                    Q(sessionDate__icontains=term) |
                    Q(comments__icontains=term)
                )

        table = ObservesTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/observes.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Session
def add_observes_portal(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ObservesPortalForm(request.POST, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Session added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Session: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Camera Session",
                        'list_page': reverse('portal_app:list-observes')
                    })
                return redirect('portal_app:list-observes')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Camera Session",
                    'list_page': reverse('portal_app:list-observes')
                })
        else:
            form = ObservesPortalForm(request=request)
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Camera Session",
            'list_page': reverse('portal_app:list-observes')
        })
    else:
        messages.error(request, "You must be logged in to add a Session.")
        return redirect('dogs_app:home')


# Handle deleting a Session
def delete_observes_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        observes = get_object_or_404(Observes, pk=pk)

        # Delete the Session
        try:
            observes.delete()
            messages.success(request, "Session deleted successfully.")
        except ProtectedError:
            messages.error(request, "Session can't be deleted because it is associated with one or more dogs/cameras.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Session: {str(e)}")

        # Redirect to the sessions list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-observes') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete a Session.")
        return redirect('dogs_app:home')


# Handle editing a Session
def edit_observes_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        observes = get_object_or_404(Observes, pk=pk)

        if request.method == 'POST':
            form = ObservesPortalForm(request.POST, instance=observes, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Session updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Session: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "Camera Session",
                        'list_page': reverse('portal_app:list-observes'),
                        'page': page, 'sort': sort, 'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-observes') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = ObservesPortalForm(instance=observes, request=request)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Camera Session",
            'list_page': reverse('portal_app:list-observes'),
            'page': page, 'sort': sort, 'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit a Session.")
        return redirect('dogs_app:home')


# Display a list of all Observations
def observations_list_portal(request):
    branch = get_current_branch(request)
    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = Observation.objects.filter(observes__dog__branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:

            # Account for date searches
            if '/' in term:
                date_parts = term.split('/')
                date_search = ''
                if len(date_parts) == 3:
                    date_search = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
                elif len(date_parts) == 2:
                    date_search = date_parts[1] + '-' + date_parts[0]

                if date_search:
                    queryset = queryset.filter(
                        Q(observes__dog__dogName__icontains=term) |
                        Q(observes__camera__camID__icontains=term) |
                        Q(observes__sessionDate__icontains=date_search) |
                        Q(obsDateTime__icontains=date_search) |
                        Q(sessionDurationInMins__icontains=term) |
                        Q(isKong__icontains=term)
                    )
            elif term.lower() in ['yes', 'no']:
                queryset = queryset.filter(
                    Q(isKong__icontains=term[0])
                )
            else:
                queryset = queryset.filter(
                    Q(observes__dog__dogName__icontains=term) |
                    Q(observes__camera__camID__icontains=term) |
                    Q(observes__sessionDate__icontains=term) |
                    Q(obsDateTime__icontains=term) |
                    Q(sessionDurationInMins__icontains=term) |
                    Q(isKong__icontains=term)
                )

        table = ObservationTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/observations.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new Observation
def add_observation_portal(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ObservationPortalForm(request.POST, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Observation added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Observation: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Observation",
                        'list_page': reverse('portal_app:list-observations'),
                        'flatpicker_col': "obsDateTime"
                    })
                return redirect('portal_app:list-observations')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/add/__add_template.html', {
                    'form': form,
                    'title': "Observation",
                    'list_page': reverse('portal_app:list-observations'),
                    'flatpicker_col': "obsDateTime"
                })
        else:
            form = ObservationPortalForm(request=request)
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Observation",
            'list_page': reverse('portal_app:list-observations'),
            'flatpicker_col': "obsDateTime"
        })
    else:
        messages.error(request, "You must be logged in to add an Observation.")
        return redirect('dogs_app:home')


# Handle deleting an Observation
def delete_observation_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        observation = get_object_or_404(Observation, pk=pk)

        # Delete the observation
        try:
            observation.delete()
            messages.success(request, "Observation deleted successfully.")
        except ProtectedError:
            messages.error(request, "Observation can't be deleted because it is associated with one or more Sessions.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Observation: {str(e)}")

        # Redirect to the observations list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-observations') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete an Observation.")
        return redirect('dogs_app:home')


# Handle editing an Observation
def edit_observation_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        observation = get_object_or_404(Observation, pk=pk)

        if request.method == 'POST':
            form = ObservationPortalForm(request.POST, instance=observation, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Observation updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Observation: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "Observation",
                        'list_page': reverse('portal_app:list-observations'),
                        'flatpicker_col': "obsDateTime",
                        'page': page,
                        'sort': sort,
                        'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-observations') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
        else:
            form = ObservationPortalForm(instance=observation, request=request)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Observation",
            'list_page': reverse('portal_app:list-observations'),
            'flatpicker_col': "obsDateTime",
            'page': page,
            'sort': sort,
            'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit an Observation.")
        return redirect('dogs_app:home')


# Display a list of all DogStances
def stances_list_portal(request):
    branch = get_current_branch(request)
    # Check if user is logged in
    if request.user.is_authenticated:
        # Capture the search term
        search_query = request.GET.get('search', '')
        # Split the search query into individual terms
        search_terms = search_query.split()
        # Initialize the base query
        queryset = DogStance.objects.filter(observation__observes__dog__branch=branch)

        # Apply filters for each search term across all relevant fields
        for term in search_terms:
            # Account for date searches
            if '/' in term:
                date_parts = term.split('/')
                date_search = ''
                if len(date_parts) == 3:
                    date_search = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
                elif len(date_parts) == 2:
                    date_search = date_parts[1] + '-' + date_parts[0]

                if date_search:
                    queryset = queryset.filter(
                        Q(observation__observes__dog__dogName__icontains=term) |
                        Q(observation__observes__camera__camID__icontains=term) |
                        Q(observation__observes__sessionDate__icontains=date_search) |
                        Q(observation__obsDateTime__icontains=date_search) |
                        Q(stanceStartTime__icontains=term) |
                        Q(dogStance__icontains=term) |
                        Q(dogLocation__icontains=term)
                    )
            else:
                queryset = queryset.filter(
                    Q(observation__observes__dog__dogName__icontains=term) |
                    Q(observation__observes__camera__camID__icontains=term) |
                    Q(observation__observes__sessionDate__icontains=term) |
                    # Q(observation__obsDateTime__icontains=term) | # Needs to account for timezone first, currently displays results two hours ahead
                    Q(stanceStartTime__icontains=term) |
                    Q(dogStance__icontains=term) |
                    Q(dogLocation__icontains=term)
                )

        table = DogStanceTable(queryset, request=request)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'portal/list/dogstances.html', {'table': table, 'search_query': search_query})
    else:
        # If user is not logged in/authenticated, show an error message and redirect to home.
        messages.error(request, "You Must Be Logged In To Access The Portal...")
        return redirect('dogs_app:home')


# Handle adding a new DogStance
def add_stance_portal(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DogStancePortalForm(request.POST, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Stance added successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while adding Stance: {str(e)}")
                    return render(request, 'portal/add/__add_template.html', {
                        'form': form,
                        'title': "Stance",
                        'list_page': reverse('portal_app:list-stances'),
                        'flatpicker_col': "stanceStartTime"
                    })
                return redirect('portal_app:list-stances')
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
            return render(request, 'portal/add/__add_template.html', {
                'form': form,
                'title': "Stance",
                'list_page': reverse('portal_app:list-stances'),
                'flatpicker_col': "stanceStartTime"
            })
        else:
            form = DogStancePortalForm(request=request)
        # Render the add page
        return render(request, 'portal/add/__add_template.html', {
            'form': form,
            'title': "Stance",
            'list_page': reverse('portal_app:list-stances'),
            'flatpicker_col': "stanceStartTime"
        })
    else:
        messages.error(request, "You must be logged in to add a Stance.")
        return redirect('dogs_app:home')


# Handle deleting a DogStance
def delete_stance_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        dogstance = get_object_or_404(DogStance, pk=pk)

        # Delete the stance
        try:
            dogstance.delete()
            messages.success(request, "Stance deleted successfully.")
        except ProtectedError:
            messages.error(request, "Stance can't be deleted because it is associated with one or more Observations.")
        except Exception as e:
            messages.error(request, f"Error occurred while deleting Stance: {str(e)}")

        # Redirect to the stances list page with the captured parameters
        return HttpResponseRedirect(reverse('portal_app:list-stances') + '?page=' + page
                                    + '&sort=' + sort + '&search=' + search)
    else:
        messages.error(request, "You must be logged in to delete a Stance.")
        return redirect('dogs_app:home')


# Handle editing a DogStance
def edit_stance_portal(request, pk):
    if request.user.is_authenticated:
        # Capture the 'page' and 'sort' and 'search' GET parameters
        page = request.GET.get('page', '1')
        sort = request.GET.get('sort', '')
        search = request.GET.get('search', '')
        dogstance = get_object_or_404(DogStance, pk=pk)

        if request.method == 'POST':
            form = DogStancePortalForm(request.POST, instance=dogstance, request=request)
            if form.is_valid():
                # Save the form
                try:
                    form.save()
                    messages.success(request, "Stance updated successfully.")
                except Exception as e:
                    messages.error(request, f"Error occurred while updating Stance: {str(e)}")
                    return render(request, 'portal/edit/__edit_template.html', {
                        'form': form,
                        'title': "Stance",
                        'list_page': reverse('portal_app:list-stances'),
                        'flatpicker_col': "stanceStartTime",
                        'page': page,
                        'sort': sort,
                        'search': search
                    })
                return HttpResponseRedirect(reverse('portal_app:list-stances') + '?page=' + page
                                            + '&sort=' + sort + '&search=' + search)
            else:
                messages.error(request, "Invalid form data. Please correct the listed errors.")
                return render(request, 'portal/edit/dogstance.html', {'form': form,
                                                                      'page': page,
                                                                      'sort': sort,
                                                                      'search': search})
        else:
            form = DogStancePortalForm(instance=dogstance, request=request)
        # Render the edit page with the captured parameters
        return render(request, 'portal/edit/__edit_template.html', {
            'form': form,
            'title': "Stance",
            'list_page': reverse('portal_app:list-stances'),
            'flatpicker_col': "stanceStartTime",
            'page': page,
            'sort': sort,
            'search': search
        })
    else:
        messages.error(request, "You must be logged in to edit a Stance.")
        return redirect('dogs_app:home')
