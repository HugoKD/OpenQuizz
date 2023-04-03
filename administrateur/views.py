from django.shortcuts import render, redirect
from .models import Question, Quizz
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json as json
import os
from django.core.files.storage import FileSystemStorage

@login_required
def dashboard(request):
    if request.method == 'POST':
        checkbox = request.POST.getlist('choice')
        enonce = request.POST.get('enonce')
        if 'qcm' in checkbox:
            choix1 = request.POST.get('choix1')
            choix2 = request.POST.get('choix2')
            choix3 = request.POST.get('choix3')
            choix4 = request.POST.get('choix4')
            reponseqcm = request.POST.get('reponseqcm')
            newquestion = Question(pseudo=str(request.user.username) ,enonce=enonce, reponse1=choix1, reponse2=choix2, reponse3=choix3, reponse4=choix4, reponseVrai=reponseqcm, qcm=True)
            newquestion.save()
        else:
            reponselongue = request.POST.get('reponselongue')
            newquestion = Question(pseudo=str(request.user.username), enonce=enonce, reponse=reponselongue)
            newquestion.save()

        return redirect('/dashboard/')
    quizzs = Quizz.objects.all().filter(pseudo=str(request.user.username))
    for k in range(len(quizzs)):
        quizzs[k].numero = k
        quizzs[k].save()


    context = {
        "quizzs":quizzs,
    }
    return render(request, "administrateur/dashboard.html", context)


#reste à rendre required au moins deux du qcm et la réponse selon le mode

@login_required
def suppression(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        quizzsupp = Quizz.objects.all().filter(pseudo=str(request.user.username)).filter(numero=numero)
        quizzsupp.delete()
        return redirect("/dashboard/")

    else:
        questions = Question.objects.all().filter(pseudo=str(request.user.username))
        for i in range(len(questions)):
            questions[i].numero = i
            questions[i].save()
        quizzs = Quizz.objects.all().filter(pseudo=str(request.user.username))
        for k in range(len(quizzs)):
            quizzs[k].numero = k
            quizzs[k].save()


        context = {
            "questions": questions,
            "quizzs": quizzs,
        }
        return render(request, "administrateur/dashboard.html", context)


@login_required
def creation_de_quizz(request):
    questions = Question.objects.all().filter(pseudo=str(request.user.username))
    for i in range(len(questions)):
        questions[i].numero = i
        questions[i].save()
    context = {
        "questions": questions
    }
    return render(request, "administrateur/creationQuizz.html", context)


@login_required
def enregistrement(request):
    if request.method == 'POST':
        liste = request.POST.get('liste')
        time = request.POST.get('timer')

        classementdisplay =request.POST.get('classementdisplay')
        if classementdisplay=="true":
            classementdisplay = True
        else:
            classementdisplay = False

        stocker = request.POST.get('stocker')
        if stocker=="true":
            stocker = True
        else:
            stocker = False

        mode = request.POST.get('mode')
        name = request.POST.get('name')
        liste_questions = ""
        questions = Question.objects.all().filter(pseudo=str(request.user.username))
        for question in questions:
            if str(question.numero) in liste:
                liste_questions += str(question.id) +', '
        newQuizz = Quizz(pseudo=str(request.user.username),name=name, mode=mode, afficher=classementdisplay, timer=time, stocker=stocker, questions=liste_questions)
        newQuizz.save()
        return redirect("/dashboard/")
    else:
        quizzs = Quizz.objects.all().filter(pseudo=str(request.user.username))
        for k in range(len(quizzs)):
            quizzs[k].numero = k
            quizzs[k].save()

        context = {
            "quizzs": quizzs,
        }
        return render(request, "administrateur/dashboard.html", context)



@login_required
def banquequestions(request):
    if request.method == 'POST':
        checkbox = request.POST.getlist('choice')
        enonce = request.POST.get('enonce')
        if 'qcm' in checkbox:
            choix1 = request.POST.get('choix1')
            choix2 = request.POST.get('choix2')
            choix3 = request.POST.get('choix3')
            choix4 = request.POST.get('choix4')
            reponseqcm = request.POST.get('reponseqcm')

            newquestion = Question(pseudo=str(request.user.username), enonce=enonce, reponse1=choix1, reponse2=choix2,
                                   reponse3=choix3, reponse4=choix4, reponseVrai=reponseqcm, qcm=True)
            newquestion.save()
        else:
            reponselongue = request.POST.get('reponselongue')

            request_file = request.FILES['file'] if 'file' in request.FILES else None
            if request_file:

                fs = FileSystemStorage()
                print(request_file.name, request_file)
                file = fs.save(request_file.name, request_file)
                fileurl = fs.url(file)
                print(fileurl.split('/')[1])

            newquestion = Question(pseudo=str(request.user.username), enonce=enonce, reponse=reponselongue, image=fileurl.split('/')[2]
                                   )
            newquestion.save()



        return redirect('/banque-question/')
    questions = Question.objects.all().filter(pseudo=str(request.user.username))
    for i in range(len(questions)):
        questions[i].numero = i
        questions[i].save()

    context = {
        "questions": questions,
    }
    return render(request, 'administrateur/banquequestions.html', context)

@login_required
def suppression_question(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        questionsupp = Question.objects.all().filter(pseudo=str(request.user.username)).filter(numero=numero)
        os.remove('media/'+str(questionsupp[0].image))
        questionsupp.delete()
        return redirect("/banque-question/")

    else:
        questions = Question.objects.all().filter(pseudo=str(request.user.username))
        for i in range(len(questions)):
            questions[i].numero = i
            questions[i].save()()

        context = {
            "questions": questions,
        }
        return render(request, "administrateur/banquequestions.html", context)


@login_required
def modifierquizz(request, id):
    if request.method == 'POST':

        quizz = Quizz.objects.get(id=id)
        liste = request.POST.get('liste')
        time = request.POST.get('timer')

        classementdisplay = request.POST.get('classementdisplay')
        if classementdisplay == "true":
            classementdisplay = True
        else:
            classementdisplay = False

        stocker = request.POST.get('stocker')
        if stocker == "true":
            stocker = True
        else:
            stocker = False

        mode = request.POST.get('mode')
        name = request.POST.get('name')
        liste_questions = ""
        questions = Question.objects.all().filter(pseudo=str(request.user.username))
        for question in questions:
            if str(question.numero) in liste:
                liste_questions += str(question.id) + ', '
        quizz.questions = liste_questions
        if time != '':
            quizz.timer = time
        quizz.stocker = stocker
        quizz.afficher = classementdisplay
        quizz.mode = mode
        if name != '':
            quizz.name = name
        quizz.save()
        return redirect('/dashboard/')


    quizz = Quizz.objects.all().filter(pseudo=str(request.user.username)).filter(id=id)[0]
    questions = Question.objects.all().filter(pseudo=str(request.user.username))
    liste_id = ''
    for i in range(len(questions)):
        questions[i].numero = i
        questions[i].save()
        liste_id += str(questions[i].id)+', '
    context = {
        "questions": questions,
        "quizz":quizz,
        "liste_id":liste_id,
    }
    return render(request, "administrateur/modifierquizz.html", context)

@login_required
def modifyquestion(request, id):

    if request.method == 'POST':
        question = Question.objects.get(id=id)
        checkbox = request.POST.getlist('choice')
        if request.POST.get('enonce') != '':
            question.enonce = request.POST.get('enonce')

        if 'qcm' in checkbox:
            question.reponse = 'null'
            question.qcm = True
            if request.POST.get('choix1') != '':
                question.reponse1 = request.POST.get('choix1')
            if request.POST.get('choix2') != '':
                question.reponse2 = request.POST.get('choix2')
            if request.POST.get('choix3') != '':
                question.reponse3 = request.POST.get('choix3')
            if request.POST.get('choix1') != '':
                question.reponse4 = request.POST.get('choix4')

            if request.POST.get('reponseqcm') != '':
                question.reponseVrai = request.POST.get('reponseqcm')


            question.save()
        else:
            question.reponseVrai = 'null'
            question.reponse1 = 'null'
            question.reponse2 = 'null'
            question.reponse3 = 'null'
            question.reponse4 = 'null'

            if request.POST.get('reponselongue') != '':
                question.reponse = request.POST.get('reponselongue')
            question.save()

        return redirect('/banque-question/')



    questions = Question.objects.all().filter(pseudo=str(request.user.username))
    for i in range(len(questions)):
        questions[i].numero = i
        questions[i].save()

    question = Question.objects.get(id=id)

    context = {
        "questions": questions,
        "questionmodify":question,
    }
    return render(request, 'administrateur/modifyquestion.html', context)