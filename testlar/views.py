from django.shortcuts import render, redirect
from .models import Test, Natija, Question, Variant
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TestForm
from .get_code import generate_secret_code
from django.contrib.auth.models import User


def list(request):
    tests = Test.objects.filter(public=True)
    return render(request, "testblog/index.html", {"posts": tests})


def error404(request):
    return render(request, "404.html")


def detail(request, code):
    test = Test.objects.get(code=code)
    if request.method == 'GET':
        if request.GET.get('start') == 'True' and test.author == request.user:
            test.is_start = True
            test.save()
            messages.success(request, "Test boshlandi!")
            return redirect('/test/'+str(code) + '/')
        if request.GET.get('finish') == 'True' and test.author == request.user:
            test.is_end = True
            test.save()
            messages.success(request, "Test tugadi!")
            return redirect('/test/'+str(code) + '/')
    
    return render(request, "testblog/detail.html", {"post": test})


@login_required
def result(request, code):
    test = Test.objects.get(code=code)
    soni = Question.objects.filter(test=test).count()
    result = Natija.objects.filter(test=test).order_by('-soni')

    try:
        res = Natija.objects.get(user=request.user)
    except Natija.DoesNotExist:
        res = {}
        messages.info(request, "Siz bu testni yechmagansiz.")

    return render(request, "testblog/results.html", {"results": result, "soni": soni, "res": res})


@login_required
def delete_test(request, code):
    test = Test.objects.get(code=code)

    if test.author == request.user:
        test.delete()
        messages.success(request, "Test muvoffaqiyatli o'chirildi!")
        return redirect('/')
    else:
        messages.error(request, "Testni faqat testning egasi o'chira oladi.")
        return redirect('/error-page/')


@login_required
def add_question(request, code):
    test = Test.objects.get(code=code)

    if test.is_start:
        messages.error(request, "Test boshlanganligi sababli savol qo'shib bo'lmaydi.")
        return redirect('/error-page/')
    
    if test.author == request.user:
        queryDict = dict(request.POST)  
        if request.method == 'POST':
            savol = queryDict['savol'][0]
            if savol:
                question = Question.objects.create(test=test, question=savol)
                options = queryDict['variant']
                for i in options:
                    option = Variant.objects.create(savol=question, variant=i)
                    if options[int(queryDict['option'][0])] == i:
                        option.is_true = True
                        option.save()
                messages.success(request, "Savol muvaffaqiyatli qo'shildi!")
                return redirect('/test/'+str(code)+'/')
            else:
                messages.warning(request, "Savol matni kiritilmadi.")
    else:
        messages.error(request, "Faqat test muallifi savol qo'shishi mumkin.")
        return redirect('/error-page/')

    return render(request, "testblog/add_question.html")


@login_required
def solve_test(request, code):
    test = Test.objects.get(code=code)

    if Natija.objects.filter(user=request.user, test=test).exists():
        messages.error(request, "Siz bu testni allaqachon bajargansiz.")
        return redirect('/error-page/')
    
    questions = Question.objects.filter(test=test)
    queryDict = dict(request.POST)
    
    if request.method == 'POST':
        result = Natija.objects.create(user=request.user, test=test)
        for pk, option in queryDict.items():
            if pk != 'csrfmiddlewaretoken':
                pk = int(pk.replace("question_", ""))
                savol = Question.objects.get(id=pk)
                t_javob = Variant.objects.get(savol=savol, is_true=True)
                if str(t_javob) == option[0]:
                    result.soni += 1
                    result.save()
        messages.success(request, "Test muvaffaqiyatli yakunlandi!")
        return redirect("/test/"+code+'/score/')

    data = {
        "questions": questions,
        "test": test
    }
    return render(request, "testblog/test.html", data)


@login_required
def score(request, code):
    test = Test.objects.get(code=code)
    if Natija.objects.filter(user=request.user).exists() and Question.objects.filter(test=test).count() != 0:
        total_questions = Question.objects.filter(test=test).count()
        correct_answers = Natija.objects.get(user=request.user, test=test).soni
        score = correct_answers/total_questions*100
        return render(request, "testblog/result.html", {"total_questions": total_questions, "correct_answers": correct_answers, "score": score})
    else:
        messages.error(request, "Testni hali ishlamagansiz.")
        return redirect("/error-page/")
    return render(request, "testblog/result.html")


def enter_test(request):
    code = request.GET.get('q', None)

    if Test.objects.filter(code=code).exists():
        messages.success(request, "Testga muvaffaqiyatli kirdingiz.")
        return redirect('/test/'+str(code)+'/')
    else:
        messages.error(request, "Kiritilgan kod bo'yicha test topilmadi.")
        return redirect('/error-page/')


@login_required
def add_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            summary = form.cleaned_data['summary']
            public = form.cleaned_data['public']
            time = form.cleaned_data['time']
            code = generate_secret_code()
            
            test = Test.objects.create(name=name, summary=summary, public=public, time=time, code=code, author=request.user)
            messages.success(request, "Test muvaffaqiyatli qo'shildi!")
            return redirect('/test/'+test.code+'/') 
        else:
            messages.error(request, "Formada xatoliklar mavjud.")
    else:
        form = TestForm()

    return render(request, 'testblog/add_test.html', {'form': form})


@login_required
def profile(request):
    if Test.objects.filter(author=request.user).exists():
        tests = Test.objects.filter(author=request.user)
        messages.success(request, "Siz yaratgan testlar ro'yxati.")
    else: 
        tests = {}
        messages.info(request, "Siz hali test yaratmagansiz.")

    return render(request, "testblog/profile.html", {"user_tests": tests})
