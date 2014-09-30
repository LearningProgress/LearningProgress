import json

from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DeleteView, FormView, ListView, View
from reportlab.pdfgen import canvas
# from reportlab.platypus import Table  # TODO

from . import forms
from .models import PROGRESS_CHOICES, MockExam, Section, UserSectionRelation


def get_progress_info(index, info):
    """
    Returns the requested info for user's progress. Index is an integer from
    0 to 3. Info is one of the following strings: text, css_glyphicon,
    css_progress_bar.
    """
    progress_choices = dict(PROGRESS_CHOICES)
    progress_info = {
        0: {'text': progress_choices[0],
            'css_glyphicon': '',
            'css_progress_bar': ''},
        1: {'text': progress_choices[1],
            'css_glyphicon': 'eye-open',
            'css_progress_bar': 'warning'},
        2: {'text': progress_choices[2],
            'css_glyphicon': 'wrench',
            'css_progress_bar': 'info'},
        3: {'text': progress_choices[3],
            'css_glyphicon': 'ok',
            'css_progress_bar': 'success'}}
    return progress_info[index][info]


class SectionListView(ListView):
    """
    View for all sections, strutured via mptt template tag.
    """
    queryset = Section.objects.all()
    self_pattern_name = 'section_list'

    def get_context_data(self, **context):
        """
        Inserts the users learning progress value.
        """
        context = super().get_context_data(**context)

        # Evaluate section queryset
        sections = dict()
        for section in context['section_list']:
            sections[section.pk] = section

        # Total scores
        total_scores = sum(section.scores for section in sections.values() if section.is_leaf_node())
        if total_scores == 0:
            total_scores = 1

        # User scores
        section_progresses = dict()
        user_learning_progress = []
        # # Initiate list user_learning_progress
        for index in range(4):
            user_learning_progress.append(dict(
                css_glyphicon=get_progress_info(index, 'css_glyphicon'),
                css_progress_bar=get_progress_info(index, 'css_progress_bar'),
                text=get_progress_info(index, 'text'),
                value=0))
        # # Parse user's data into list and dict
        for usersectionrelation in UserSectionRelation.objects.filter(user=self.request.user, progress__gt=0):
            section = sections[usersectionrelation.section_id]  # TODO: Check whether to use section.pk.
            # section = sections[usersectionrelation.section.pk]
            if not section.is_leaf_node():
                continue
            progress_dict = user_learning_progress[usersectionrelation.progress]
            progress_dict['value'] += section.scores
            section_progresses[section.pk] = usersectionrelation.progress
        # # Calculate "Nothing done" case
        for progress_dict in user_learning_progress:
            user_learning_progress[0]['value'] += -progress_dict['value']
        user_learning_progress[0]['value'] += total_scores
        # # Calculate percentage value
        for progress_dict in user_learning_progress:
            progress_dict['value'] = round(progress_dict['value'] * 100 / total_scores)

        context['section_progresses'] = section_progresses
        context['user_learning_progress'] = user_learning_progress
        return context


class UserSectionRelationUpdateView(FormView):
    """
    View for a single relation between an user and a section.
    """
    template_name = 'progress/usersectionrelation_form.html'
    form_class = forms.UserSectionRelationUpdateForm
    success_url = reverse_lazy('section_list')
    self_pattern_name = 'usersectionrelation_update'

    def get(self, *args, **kwargs):
        """
        Handles GET requests. Special response for ajax requests.
        """
        if self.request.is_ajax():
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            context = self.get_context_data(form=form)
            context.update(csrf(self.request))
            # context['STATIC_URL'] = settings.STATIC_URL  # TODO
            html = render_to_string('progress/usersectionrelation_form_snippet.html', context)
            html = '<p><button type="button" class="close" aria-hidden="true">&times;</button></p>' + html
            response = self.render_to_json_response({'html': html})
        else:
            response = super().get(*args, **kwargs)
        return response

    def get_initial(self):
        """
        Returns the initial value for the form. Creates a relation from the user to the section if necessary.
        """
        try:
            self.section = Section.objects.get(pk=self.kwargs['pk'])
            if self.section.get_children().exists():
                raise Section.DoesNotExist
        except Section.DoesNotExist:
            raise Http404
        self.user_section_relation, __ = UserSectionRelation.objects.get_or_create(
            user=self.request.user, section=self.section)
        return {'progress': self.user_section_relation.progress, 'comment': self.user_section_relation.comment}

    def get_context_data(self, **context):
        """
        Inserts the section into the template context.
        """
        return super().get_context_data(section=self.section, **context)

    def form_valid(self, form):
        """
        Processes the valid form. Saves the input into the database.
        """
        self.user_section_relation.progress = form.cleaned_data['progress']
        self.user_section_relation.comment = form.cleaned_data['comment']
        self.user_section_relation.save()
        if self.request.is_ajax():
            response = self.render_to_json_response({})
        else:
            response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        """
        Returns a response with the form errors. Returns a special response
        for ajax requests.
        """
        if self.request.is_ajax():
            response = self.render_to_json_response({'form_errors': form.errors})
        else:
            response = super().form_invalid(form)
        return response

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a HttpResponse object with JSON data for ajax requests.
        """
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


class UserSectionRelationExportView(View):
    """
    View to export all leaf node sections with users progress data and
    comments as JSON.
    """
    def get(self, request, *args, **kwargs):
        sections = [
            section.serialize(user=self.request.user)
            for section in Section.objects.all()
            if section.is_leaf_node()]
        return HttpResponse(json.dumps(sections), content_type='application/json')


# TODO
class PrintNoteCardsView(View):
    """
    View to export all user's section comments in a printable format (PDF).
    """
    def get_queryset(self):
        return UserSectionRelation.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        # Create the PDF object, using the response object as its "file".
        pdf = canvas.Canvas(response)

        # from reportlab.pdfgen.canvas import Canvas
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        # from reportlab.lib.units import inch, cm
        from reportlab.platypus import Paragraph, Frame

        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        cards = []

        # Get all cards with their stories.
        story = []
        story.append(Paragraph("This is a Heading", styleH))
        story.append(Paragraph("This is a paragraph in<i>Normal</i>style.", styleN))
        cards.append(story)
        cards.append([Paragraph("This is another Heading1", styleH)])
        cards.append([Paragraph("This is another Heading2", styleH)])
        cards.append([Paragraph("This is another Heading3", styleH)])
        cards.append([Paragraph("This is another Heading4", styleH)])
        cards.append([Paragraph("This is another Heading5", styleH)])
        cards.append([Paragraph("This is another Heading6", styleH)])
        cards.append([Paragraph("This is another Heading7", styleH)])
        cards.append([Paragraph("This is another Heading8", styleH)])

        # Add cards to PDF object.
        if len(cards) % 2 != 0:
            cards.append('')
        while True:
            for i in range(3):
                h = height * 2/3 - height * 1/3 * i
                f1 = Frame(0, h, width/2, height * 1/3, showBoundary=1)
                f2 = Frame(width/2, h, width/2, height * 1/3, showBoundary=1)
                f1.addFromList(cards.pop(0), pdf)
                f2.addFromList(cards.pop(0), pdf)
                if len(cards) == 0:
                    break
            else:
                pdf.showPage()
                continue
            pdf.showPage()
            break

        # Close the PDF object cleanly, and we're done.
        pdf.save()
        return response

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # p.drawString(100, 100, "Hello world.")
        # t = Table([[1,2,3], [4,5,6]])
        # #import pdb; pdb.set_trace()
        # #p.append(t)
        # from reportlab.lib.pagesizes import A4, cm
        # width, height = A4
        # t.wrapOn(p, width, height)
        # t.drawOn(p, 100, 100)
        # # Close the PDF object cleanly, and we're done.
        # p.showPage()
        # p.save()


class MockExamFormView(FormView):
    """
    View to display and update user's mock exams.
    """
    template_name = 'progress/mockexam_form.html'
    form_class = forms.MockExamForm
    success_url = reverse_lazy('mockexam_form')
    self_pattern_name = 'mockexam_form'

    def get_context_data(self, **context):
        """
        Inserts the mock exams into the context.
        """
        context = super().get_context_data(**context)
        context['mockexam_list'] = MockExam.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        """
        Processes a valid input of a new mock exam.
        """
        mockexam = form.save(commit=False)
        mockexam.user = self.request.user
        mockexam.save()
        return super().form_valid(form)


class MockExamDeleteView(DeleteView):
    """
    View to delete a single mock exam.
    """
    model = MockExam
    success_url = reverse_lazy('mockexam_form')
    self_pattern_name = 'mockexam_delete'

    def dispatch(self, *args, **kwargs):
        """
        Ensures that you can only delete your own mock exams.
        """
        if not self.get_object().user == self.request.user:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)
