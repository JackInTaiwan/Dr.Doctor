from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
from django.template import RequestContext
from doctor.models import *
import tensorflow
from .web_version import util
from .web_version import prediction_rnn



def cover(request):
    return render(request, "cover.html")

def chatroom(request):
    if "nickname" in request.POST and "text" not in request.POST :
        values = ["nickname", "gender", "height", "weight", "password"]
        for value in values :
            if request.POST.get("nickname") != None :
                break
        else :
            return HttpResponseRedirect("/reg")
        print ("use")
        nickname = request.POST.get("nickname")
        gender = request.POST.get("gender")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        password = request.POST.get("password")
        return render_to_response('chatroom.html', locals(),RequestContext(request))

    else :
        #if 'nickname' in request.POST and 'text' in request.POST:
            nickname = 'Jack'
            text = request.POST.get('text')
            text = util.convert_s_to_std_format(text)
            if nickname and text:
                m = Message.objects.create(nickname=nickname, text=text)
                m.save()
                nickname2, text2 = reply(text)
                if text == "hello doctor":
                    m2 = Message.objects.create(nickname=nickname2, text='hello '+nickname+', may I help you')
                    m2.save()            
                else:
                    m2 = Message.objects.create(nickname=nickname2, text=text2)
                    m2.save()
            messages = Message.objects.order_by('timestamp')
      
            #Message.objects.all().delete()
            if Message.objects.count() >= 10 :
                objs = Message.objects.all()[:8]
            
                for obj in objs:
                    obj.delete()
            

    #the_first_name = messages[0].nickname if len(messages) > 0 else " "
            return render_to_response('chatroom.html', locals(),RequestContext(request))

def reply(in_text):
    nickname = 'bot'
    text = prediction_rnn.prediction(in_text)
    text = mapping(text)
    return nickname, text

def mapping(chinese):
    if chinese == '急性咽炎':
        english = 'Acute pharyngitis'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '急性鼻竇炎':
        english = 'stomach flu'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '急性支氣管炎':
        english = 'Acute bronchitis'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '急性外耳炎':
        english = 'external otitis'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '過敏性鼻炎':
        english = 'Allergic rhinitis'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '急性扁桃腺炎':
        english = ' Acute Tonsillitis'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '其他非傳染性胃腸炎及大腸炎':
        english = 'Acute rhinosinusitis'       
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '急性咽喉炎':
        english = 'Acute pharyngolaryngitis'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == '急性上呼吸道感染':
        english = 'Acute upper respiratory tract infection'
        return 'Oh! I know it. Your syndrome may be ' + english + '.'
    elif chinese == None:
        english = 'Please specify your syndrom more!'
        return english

def welcome(request):
    if 'nickname' in request.POST and 'text' in request.POST:
        nickname = request.POST.get('nickname')
        text = request.POST.get('text')
        if nickname and text:
             m=Message.objects.create(nickname=nickname, text=text)
             m.save()
    messages = Message.objects.order_by('timestamp')
    the_first_name = messages[0].nickname
    return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))



### Register Methods
def reg(request) :
    return render(request, "reg.html")