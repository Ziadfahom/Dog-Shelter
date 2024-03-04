import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from dogs_app.models import (Owner, Camera, Kennel, Treatment, EntranceExamination,
                             DogPlacement, Observes, Observation, DogStance, Branch)


# Helper function to get the user's current branch object (Israel/Italy)
def get_current_branch(request):
    # Get the current Branch (Israel/Italy)
    branch_name = request.session.get('branch', 'Israel')  # Default to Israel
    branch = Branch.objects.get(branchName=branch_name)  # Get the branch object

    return branch


# Owner Table
class OwnerTable(tables.Table):
    # Add columns for deleting and editing Owner
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OwnerTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-owner',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" onclick="return confirm(\'Are you sure you want '
                               'to delete this owner?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-owner',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    class Meta:
        model = Owner
        template_name = 'django_tables2/bootstrap.html'
        fields = ('firstName', 'lastName', 'ownerID', 'ownerAddress', 'city',
                  'phoneNum', 'cellphoneNum', 'comments', 'edit', 'delete')
        order_by = ('firstName', 'lastName')


# Camera Table
class CameraTable(tables.Table):
    # Add columns for deleting and editing a Camera
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CameraTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-camera',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" title="Delete" onclick="return confirm(\'Are you sure you want '
                               'to delete this camera?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-camera',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    class Meta:
        model = Camera
        template_name = 'django_tables2/bootstrap.html'
        fields = ('camID', 'edit', 'delete')


# Kennel Table
class KennelTable(tables.Table):
    # Add columns for deleting and editing Kennel
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(KennelTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-kennel',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" title="Delete" onclick="return confirm(\'Are you sure you want '
                               'to delete this kennel?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-kennel',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    class Meta:
        model = Kennel
        template_name = 'django_tables2/bootstrap.html'
        fields = ('kennelNum', 'kennelImage', 'edit', 'delete')
        pagination_template = 'tables/pagination.html'


# Treatments Table
class TreatmentTable(tables.Table):
    # Add columns for deleting and editing Treatment
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TreatmentTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-treatment',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" onclick="return confirm(\'Are you sure you want '
                               'to delete this treatment?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-treatment',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    # Format date in DD/MM/YYYY format
    def render_treatmentDate(self, record):
        # Format date in DD/MM/YYYY format if it's not None
        if record.treatmentDate:
            return record.treatmentDate.strftime('%d/%m/%Y')
        return '—'

    class Meta:
        model = Treatment
        template_name = 'django_tables2/bootstrap.html'
        fields = ('treatmentName', 'treatmentDate', 'treatedBy', 'comments', 'dog', 'edit', 'delete')
        order_by = '-treatmentDate'


# Examinations Table
class ExaminationTable(tables.Table):
    # Add columns for deleting and editing Examination
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ExaminationTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-examination',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" onclick="return confirm(\'Are you sure you want '
                               'to delete this examination?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return '—'

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-examination',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    # Format date in DD/MM/YYYY format
    def render_examinationDate(self, record):
        # Format date in DD/MM/YYYY format if it's not None
        if record.examinationDate:
            return record.examinationDate.strftime('%d/%m/%Y')
        return '—'

    class Meta:
        model = EntranceExamination
        template_name = 'django_tables2/bootstrap.html'
        fields = ('examinationDate', 'examinedBy', 'results', 'dogWeight', 'dogTemperature',
                  'dogPulse', 'comments', 'dog', 'edit', 'delete')
        order_by = '-examinationDate'


# Dog Placements Table
class DogPlacementTable(tables.Table):
    # Add columns for deleting and editing DogPlacement as well as calculating the duration of stay
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)
    duration = tables.Column(empty_values=(), orderable=False, verbose_name='Duration (Days)')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DogPlacementTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-placement',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" title="Delete" onclick="return confirm(\'Are you sure you want '
                               'to delete this placement?\');"><span class="icon-delete text-white"></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-placement',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    # Retrieve the duration of stay
    def render_duration(self, record):
        return record.duration()  # Calls the duration method from DogPlacement model

    # Format dates in DD/MM/YYYY format
    def render_entranceDate(self, record):
        # Format date in DD/MM/YYYY format if it's not None
        if record.entranceDate:
            return record.entranceDate.strftime('%d/%m/%Y')
        return '—'

    def render_expirationDate(self, record):
        # Format date in DD/MM/YYYY format if it's not None
        if record.expirationDate:
            return record.expirationDate.strftime('%d/%m/%Y')
        return '—'

    def render_kennel(self, record):
        if record.kennel:
            return f"Kennel #{record.kennel.kennelNum}"
        else:
            return '—'

    class Meta:
        model = DogPlacement
        template_name = 'django_tables2/bootstrap.html'
        fields = ('dog', 'kennel', 'duration', 'entranceDate', 'expirationDate', 'placementReason', 'edit', 'delete')
        order_by = ['-entranceDate', 'expirationDate']


# Session (Observes) Table
class ObservesTable(tables.Table):
    # Add columns for deleting and editing Observes
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ObservesTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-observes',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" onclick="return confirm(\'Are you sure you want '
                               'to delete this session?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-observes',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    # Format dates in DD/MM/YYYY format
    def render_sessionDate(self, record):
        # Format date in DD/MM/YYYY format if it's not None
        if record.sessionDate:
            return record.sessionDate.strftime('%d/%m/%Y')
        return '—'

    def render_camera(self, record):
        if record.camera:
            return f"Camera #{record.camera.camID}"
        else:
            return '—'

    class Meta:
        model = Observes
        template_name = 'django_tables2/bootstrap.html'
        fields = ('dog', 'camera', 'sessionDate', 'comments', 'edit', 'delete')
        order_by = '-sessionDate'


# Observation Table
class ObservationTable(tables.Table):
    # Add columns for deleting and editing Observation
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)
    jsonFile = tables.Column(empty_values=(), orderable=False)
    rawVideo = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ObservationTable, self).__init__(*args, **kwargs)

        # Only display isHuman and isDog if the current branch is Italy
        if get_current_branch(self.request).branchName != 'Italy':
            self.exclude = ('isHuman', 'isDog')


    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-observation',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" title="Delete" onclick="return confirm(\'Are you sure you want '
                               'to delete this observation?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-observation',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    # Format DateTime in DD/MM/YYYY HH:MM:SS format and convert to local time
    def render_obsDateTime(self, record):
        # Convert to local time
        record.obsDateTime = record.obsDateTime.astimezone()
        # Format DateTime in DD/MM/YYYY HH:MM:SS format if it's not None
        if record.obsDateTime:
            return record.obsDateTime.strftime('%d/%m/%Y %H:%M:%S')

        return '—'

    class Meta:
        model = Observation
        template_name = 'django_tables2/bootstrap.html'
        fields = ('observes', 'obsDateTime', 'sessionDurationInMins', 'isKong', 'isDog', 'isHuman', 'jsonFile', 'rawVideo', 'edit', 'delete')
        order_by = '-obsDateTime'


# DogStances Table
class DogStanceTable(tables.Table):
    # Add columns for deleting and editing ٍStances
    delete = tables.Column(empty_values=(), orderable=False)
    edit = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DogStanceTable, self).__init__(*args, **kwargs)

    def render_delete(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            delete_url = (reverse('portal_app:delete-stance',
                                  args=[record.pk]) + '?page=' + current_page
                          + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-danger" onclick="return confirm(\'Are you sure you want '
                               'to delete this stance?\');"><span class="icon-delete text-white"></span></a>', delete_url)
        return ''

    def render_edit(self, record):
        if self.request:
            current_page = self.request.GET.get('page', '1')
            current_sort = self.request.GET.get('sort', '')
            current_search = self.request.GET.get('search', '')
            edit_url = (reverse('portal_app:edit-stance',
                                args=[record.pk]) + '?page=' + current_page
                        + '&sort=' + current_sort + '&search=' + current_search)
            return format_html('<a href="{}" class="btn btn-light shadowed-light" title="Edit"><span class="icon-edit text-dark"></span></a>', edit_url)

    # Format Time in HH:MM:SS format
    def render_stanceStartTime(self, record):
        if record.stanceStartTime:
            return record.stanceStartTime.strftime('%H:%M:%S')

        return '—'

    class Meta:
        model = DogStance
        template_name = 'django_tables2/bootstrap.html'
        fields = ('observation', 'stanceStartTime', 'dogStance', 'dogLocation', 'edit', 'delete')
        # Order by observation and then by stanceStartTime
        order_by = ('observation', 'stanceStartTime')
