from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from .forms import ProfileForm, AnswerForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Question, Tag, Count, Vote, Answers
from django.core.urlresolvers import reverse_lazy, reverse

# Create your views here.


def home(request):
    print(request.user.id)
    top_questions = Question.objects.all()[:50]
    return render(request, 'stack/home.html', {'top_questions': top_questions})


def user_registration(request):
    if request.POST:
        ok = True
        user_creation_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if not user_creation_form.is_valid():
            ok = False
        if not profile_form.is_valid():
            ok = False
        if ok:
            print('it should work')
            try:
                users = user_creation_form.save()
                profile = profile_form.save(commit=False)
                profile.user = users
                profile.save()
                return redirect('stack:Login')
            except:
                return render_to_response("registration/create_user.html",
                                      {'u_form': UserCreationForm, 'p_form': ProfileForm},
                                      context_instance=RequestContext(request))
    return render_to_response("registration/create_user.html",
                                  {'u_form': UserCreationForm, 'p_form': ProfileForm},
                                  context_instance=RequestContext(request))


def permission_denied(requests):
    return render_to_response("stack/permission_denied.html",
                              context_instance=RequestContext(requests))

class ListOfUsers(ListView):
    model = Profile

def user_profile(request, user_id):
    try:
        profile = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    if Question.objects.filter(pk=user_id):
        questions = Question.objects.filter(pk=user_id)
        context = {"profile": profile, 'questions': questions}
    else:
        context = {"profile": profile}
    context['questions'] = Question.objects.filter(user=profile.user)
    return render_to_response("stack/user-profile.html",
                              context, context_instance=RequestContext(request))


class ListOfQuestions(ListView):
    model = Question


def question_page(request, question_id):
    try:
        ques = Question.objects.filter(pk=question_id)
        if Answers.objects.filter(question=ques):
            answer = Answers.objects.filter(question=ques)
            context = {'question': ques, 'answer': answer}
        else:
            context = {'question': ques}
    except Question.DoesNotExist:
        return HttpResponse('Not Found!')
    return render_to_response('stack/question_detail.html',
                              context,
                              context_instance=RequestContext(request))


class AskQuestion(CreateView):
    model = Question
    fields = ['title', 'text', 'tags']
    success_url = reverse_lazy('stack:home')

    def form_valid(self, form):
        current_user = User.objects.get(pk=self.request.user.id)
        form.instance.user = current_user
        return super(AskQuestion, self).form_valid(form)


def answer_question(request, question_id):
    if request.POST:
        user_id = request.user.id
       # user_id = User.objects.get(id=user_id)
        print('got user_id')
        print(user_id)
        question = request.question
        print('Question: {}'.format(question))
        usr = request.user
        ok = True
        answer_form = AnswerForm(request.POST)
        if not answer_form.is_valid():
            ok = False
        if ok:
            print('answer form at second if')
            try:
                print('answer_form at try')
                answer = answer_form.save(commit=False)
                answer.user = usr.profile
                answer.question = question
                answer.save()
                print('answer_form made it to end of try')
                return redirect('stack:question_page', question_id)
            except:
                answer.user = usr.profile
                answer.question = question
                answer.save()
                print('answer_form hit except')
                return render_to_response('stack/answer_question.html',
                                          {'answer_form': AnswerForm},
                                          context_instance=RequestContext(request))
    return render_to_response('stack/answer_question.html',
                                          {'answer_form': AnswerForm},
                                          context_instance=RequestContext(request))

"""

def user_registration(request):
    if request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_form = UserCreationForm({
            'username': username,
            'password1': password1,
            'password2': password2
        })
        try:
            user_form.save(commit=True)
            return HttpResponseRedirect("/")
        except ValueError:
            return render_to_response("registration/create_user.html",
                                      {'form': user_form},
                                      context_instance=RequestContext(request))

    return render_to_response("registration/create_user.html",
                              {'form': UserCreationForm()},
                              context_instance=RequestContext(request))
                              """